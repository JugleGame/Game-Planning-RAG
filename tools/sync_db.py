#!/usr/bin/env python3
"""Synchronize research Markdown into Postgres mirror tables.

Markdown is authoritative. This script is the only writer to cards, card_sections, card_refs,
and digests. It preserves existing DB rows for files whose frontmatter cannot be parsed.
Embedding and body_hash updates belong to embed_cards.py.

Usage:
  python tools/sync_db.py [--dsn postgresql://...] [--dry-run]
"""
import argparse
import datetime
import glob
import os
import pathlib
import re
import sys
import tomllib

import psycopg2
import psycopg2.extras

BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(BASE))
from _db import resolve_dsn
from card_schema import (CARD_ID_RE as ID_PAT, CARD_REQUIRED, DIGEST_REQUIRED,
                         split_sections)

RESEARCH = BASE / "research"

FM_PAT = re.compile(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)$", re.S)
DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})_")


def parse_date(v):
    if isinstance(v, datetime.date):
        return v
    return datetime.date.fromisoformat(str(v).strip())


def load_frontmatter(path: pathlib.Path):
    raw = path.read_text(encoding="utf-8")
    m = FM_PAT.match(raw)
    if not m:
        raise ValueError("frontmatter (+++ block) not found")
    fm = tomllib.loads(m.group(1))
    body = m.group(2).strip()
    return fm, body


def collect():
    """research/**/*.md를 훑어 (card_rows, digest_rows, errors)를 돌려준다."""
    card_rows, digest_rows, errors = [], [], []
    for path_str in glob.glob(str(RESEARCH / "**" / "*.md"), recursive=True):
        path = pathlib.Path(path_str)
        # '_'로 시작하는 파일은 카드가 아니라 운영 문서다 (_index*, _scout_queue,
        # _automation_state). audit_links.py와 같은 규칙을 쓴다.
        #
        # 전에는 _index.md 하나만 건너뛰어서, 나머지 운영 문서가 매번 '프론트매터
        # 없음'으로 errors에 쌓이고 종료코드 1을 냈다 - 실패가 아닌데 실패로 보이는
        # 상태였고, 그 탓에 진짜 실패도 같이 무시되기 쉬웠다.
        if path.name.startswith("_"):
            continue
        rel = str(path.relative_to(BASE))
        try:
            fm, body = load_frontmatter(path)
            is_digest = str(fm.get("type", "")).strip() == "digest"
            if is_digest:
                missing = [k for k in DIGEST_REQUIRED if not fm.get(k)]
                if missing:
                    raise ValueError(f"digest required fields missing: {missing}")
                m = DATE_PREFIX.match(path.name)
                if m:
                    digest_date = datetime.date.fromisoformat(m.group(1))
                elif fm.get("period_end"):
                    digest_date = parse_date(fm["period_end"])
                else:
                    raise ValueError("filename has no YYYY-MM-DD prefix and period_end is missing")
                digest_rows.append({
                    "digest_date": digest_date,
                    "period": str(fm["period"]),
                    "sources": list(fm.get("sources", [])),
                    "status": str(fm["status"]),
                    "body": body,
                    "file_path": rel,
                })
            else:
                missing = [k for k in CARD_REQUIRED if not fm.get(k)]
                if missing:
                    raise ValueError(f"card required fields missing: {missing}")
                card_id = str(fm["card_id"])
                if not re.match(r"^(ELEM|GAME|GENRE|ARCH)-\d{3}$", card_id):
                    raise ValueError(f"invalid card_id format: {card_id}")

                refs = {r for r in ID_PAT.findall(body) if r != card_id}
                refs |= {g for g in fm.get("example_games", []) if g != card_id}

                sections = split_sections(body)
                if not sections:
                    raise ValueError("no schema-recognized '## ' sections found "
                                     "(check section titles with lint_card.py)")

                card_rows.append({
                    "card_id": card_id,
                    "type": str(fm["type"]),
                    "title": str(fm["title"]),
                    "summary": str(fm["summary"]),
                    "tags": list(fm.get("tags", [])),
                    "elements": list(fm.get("elements", [])),
                    "genres": list(fm.get("genres", [])),
                    "updated": parse_date(fm["updated"]),
                    "confidence": str(fm["confidence"]),
                    "body": body,
                    "file_path": rel,
                    "refs": sorted(refs),
                    "sections": sections,
                })
        except Exception as e:
            errors.append((rel, f"{type(e).__name__}: {e}"))
    return card_rows, digest_rows, errors


CARD_UPSERT = """
INSERT INTO cards (card_id, type, title, summary, tags, elements, genres,
                    updated, confidence, body, file_path)
VALUES ($1, $2, $3, $4, $5::text[], $6::text[], $7::text[], $8::date, $9, $10, $11)
ON CONFLICT (card_id) DO UPDATE SET
  type=EXCLUDED.type, title=EXCLUDED.title, summary=EXCLUDED.summary,
  tags=EXCLUDED.tags, elements=EXCLUDED.elements, genres=EXCLUDED.genres,
  updated=EXCLUDED.updated, confidence=EXCLUDED.confidence, body=EXCLUDED.body,
  file_path=EXCLUDED.file_path
"""

# 절은 (card_id, ord)로 upsert하고 남는 꼬리만 자른다.
#
# 통째로 DELETE 후 INSERT 하지 않는 이유: 그러면 매 동기화마다 embedding과
# body_hash가 같이 날아가 embed_cards.py가 전량 재계산을 하게 된다. 본문이 안 바뀐
# 절의 좌표는 그대로 둬야 '지문 안 바뀐 건 건너뛴다'는 설계가 산다.
SECTION_UPSERT = """
INSERT INTO card_sections (card_id, ord, section_key, section_title, body)
VALUES ($1, $2, $3, $4, $5)
ON CONFLICT (card_id, ord) DO UPDATE SET
  section_key=EXCLUDED.section_key, section_title=EXCLUDED.section_title,
  body=EXCLUDED.body
"""

DIGEST_UPSERT = """
INSERT INTO digests (digest_date, period, sources, status, body)
VALUES ($1::date, $2, $3::text[], $4, $5)
ON CONFLICT (digest_date) DO UPDATE SET
  period=EXCLUDED.period, sources=EXCLUDED.sources, status=EXCLUDED.status, body=EXCLUDED.body
"""


def build_plan(card_rows, digest_rows):
    """실행 계획 [(sql, params, tag)]를 만든다 - 백엔드 중립.

    자리표시자는 Postgres 네이티브 $1,$2… 를 쓴다. psycopg2로 실행할 때만 %s로 바꾼다
    (각 $n은 문 안에서 정확히 한 번, 오름차순으로만 등장해야 한다).
    tag가 붙은 문은 실행 후 삭제 건수를 세기 위한 것이다.
    """
    # 같은 SQL을 연달아 놓는다 (카드별 인터리브가 아니라 단계별로).
    #
    # execute_pg가 '연속된 같은 문'을 execute_batch 한 번으로 묶기 때문에, 이 순서가
    # 곧 왕복 횟수다. 카드별로 섞어 놓으면 162장 × 약 12문 ≈ 2,000회 왕복이 되고
    # 원격 Neon에서는 그것만으로 수 분이 걸린다. 단계별로 모으면 8회 남짓이다.
    #
    # 단계 순서는 의미상 지켜야 한다: refs는 지운 뒤 다시 넣고, 절은 upsert한 뒤
    # 꼬리를 자른다. 단계 사이 순서만 맞으면 단계 안의 순서는 상관없다.
    plan = []
    plan += [(CARD_UPSERT, [c["card_id"], c["type"], c["title"], c["summary"],
                            c["tags"], c["elements"], c["genres"],
                            c["updated"], c["confidence"], c["body"], c["file_path"]], None)
             for c in card_rows]
    plan += [("DELETE FROM card_refs WHERE from_id = $1", [c["card_id"]], None)
             for c in card_rows]
    plan += [("INSERT INTO card_refs (from_id, to_id) VALUES ($1, $2) ON CONFLICT DO NOTHING",
              [c["card_id"], to_id], None)
             for c in card_rows for to_id in c["refs"]]
    plan += [(SECTION_UPSERT, [c["card_id"], ordn, key, title, text], None)
             for c in card_rows for ordn, key, title, text in c["sections"]]
    # 절이 줄어든 카드의 꼬리 행 제거 (늘어난 경우는 upsert가 처리한다)
    plan += [("DELETE FROM card_sections WHERE card_id = $1 AND ord >= $2",
              [c["card_id"], len(c["sections"])], None)
             for c in card_rows]

    live_card_ids = [c["card_id"] for c in card_rows]
    if live_card_ids:
        plan.append(("DELETE FROM cards WHERE card_id != ALL($1::text[]) RETURNING card_id",
                     [live_card_ids], "deleted_cards"))
    else:
        plan.append(("DELETE FROM cards RETURNING card_id", [], "deleted_cards"))

    seen = set()
    for d in digest_rows:
        if d["digest_date"] in seen:
            raise ValueError(f"digest_date conflict: {d['digest_date']} appears in multiple signal files")
        seen.add(d["digest_date"])
        plan.append((DIGEST_UPSERT, [d["digest_date"], d["period"], d["sources"],
                                     d["status"], d["body"]], None))

    live_digest_dates = [d["digest_date"] for d in digest_rows]
    if live_digest_dates:
        plan.append(("DELETE FROM digests WHERE digest_date != ALL($1::date[]) RETURNING digest_date",
                     [live_digest_dates], "deleted_digests"))
    else:
        plan.append(("DELETE FROM digests RETURNING digest_date", [], "deleted_digests"))
    return plan


def _to_pyformat(sql: str) -> str:
    """$1,$2… -> %s (psycopg2용). 파라미터는 이미 순서대로 들어 있다."""
    return re.sub(r"\$\d+", "%s", sql)


def execute_pg(dsn, plan, dry_run=False):
    """psycopg2(5432)로 계획을 한 트랜잭션에 실행한다.

    연속된 같은 SQL은 execute_batch로 묶어 한 번에 보낸다. psycopg2는 문 하나마다
    서버 응답을 기다리므로, 원격 Neon에서는 왕복 지연이 실행 시간의 전부다.
    rowcount를 봐야 하는 문(tag가 붙은 것)은 묶지 않고 따로 실행한다 -
    execute_batch의 rowcount는 마지막 배치 것이라 신뢰할 수 없다.
    """
    counts = {}
    conn = psycopg2.connect(dsn)
    try:
        cur = conn.cursor()
        i = 0
        while i < len(plan):
            sql, params, tag = plan[i]
            if tag:
                cur.execute(_to_pyformat(sql), params)
                counts[tag] = cur.rowcount
                i += 1
                continue
            j = i
            while j < len(plan) and plan[j][0] == sql and plan[j][2] is None:
                j += 1
            batch = [p for _, p, _ in plan[i:j]]
            if len(batch) == 1:
                cur.execute(_to_pyformat(sql), batch[0])
            else:
                psycopg2.extras.execute_batch(cur, _to_pyformat(sql), batch, page_size=200)
            i = j
        conn.rollback() if dry_run else conn.commit()
        cur.close()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return counts


def execute_https(plan, dry_run=False):
    """5432가 막힌 환경에서 443/HTTPS 브리지로 계획을 한 트랜잭션에 실행한다.

    HTTP 경로는 대화형 트랜잭션을 열어둘 수 없어 '실행 후 롤백'이 불가능하다.
    따라서 --dry-run은 아무것도 실행하지 않고, 삭제 예정 건수만 조회해 보고한다.
    """
    sys.path.insert(0, str(BASE / "db"))
    from neon_https import query as https_query, transaction as https_transaction

    if dry_run:
        live_cards = {c for s, p, t in plan if t == "deleted_cards" for c in (p[0] if p else [])}
        live_dates = {str(d) for s, p, t in plan if t == "deleted_digests" for d in (p[0] if p else [])}
        db_cards = {r["card_id"] for r in https_query("SELECT card_id FROM cards")}
        db_dates = {str(r["d"])[:10] for r in https_query("SELECT digest_date::text AS d FROM digests")}
        return {"deleted_cards": len(db_cards - live_cards),
                "deleted_digests": len(db_dates - live_dates)}

    # HTTPS 경로는 계획 전체를 한 요청 본문에 담는다. 카드가 늘면 본문에 카드 전문이
    # 전부 실려 수 MB가 되고, 어느 지점에서 Neon HTTP 한도에 걸린다. 조용히 잘리는
    # 것보다 여기서 크게 실패하는 편이 낫다 - 5432가 열려 있으면 그쪽이 정답이다.
    approx_mb = sum(len(sql) + sum(len(str(x)) for x in params)
                    for sql, params, _ in plan) / 1_000_000
    if approx_mb > 4:
        raise RuntimeError(
            f"plan is too large for HTTPS (about {approx_mb:.1f}MB). "
            "Use 5432 (--transport pg) or synchronize smaller batches.")

    results = https_transaction([(sql, params) for sql, params, _ in plan])
    counts = {}
    for (sql, params, tag), res in zip(plan, results):
        if tag:
            counts[tag] = res.get("rowCount") or len(res.get("rows") or [])
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", default=None)
    ap.add_argument("--dry-run", action="store_true", help="show the plan without committing to the DB")
    ap.add_argument("--transport", choices=["auto", "pg", "https"], default="auto",
                    help="auto tries 5432 first, then falls back to 443/HTTPS (default)")
    a = ap.parse_args()
    dsn = resolve_dsn(a.dsn)

    card_rows, digest_rows, errors = collect()
    if errors:
        print(f"Skipped files: {len(errors)} (existing DB rows preserved):", file=sys.stderr)
        for rel, msg in errors:
            print(f"  - {rel}: {msg}", file=sys.stderr)

    try:
        plan = build_plan(card_rows, digest_rows)
    except ValueError as e:
        print(f"Plan generation failed: {e}", file=sys.stderr)
        sys.exit(1)

    used = None
    try:
        if a.transport in ("auto", "pg"):
            try:
                counts = execute_pg(dsn, plan, dry_run=a.dry_run)
                used = "5432"
            except psycopg2.OperationalError as e:
                if a.transport == "pg":
                    raise
                first = str(e).strip().splitlines()[0][:120]
                print(f"5432 connection failed; falling back to the 443/HTTPS bridge ({first})", file=sys.stderr)
                counts = execute_https(plan, dry_run=a.dry_run)
                used = "443/HTTPS"
        else:
            counts = execute_https(plan, dry_run=a.dry_run)
            used = "443/HTTPS"
    except Exception as e:
        print(f"Synchronization failed (rolled back): {e}", file=sys.stderr)
        sys.exit(1)

    if a.dry_run:
        mode = "[DRY-RUN, rolled back] " if used == "5432" else "[DRY-RUN, not executed] "
    else:
        mode = ""
    n_sections = sum(len(c["sections"]) for c in card_rows)
    print(f"{mode}[{used}] cards upserted: {len(card_rows)} "
          f"(deleted: {counts.get('deleted_cards', 0)}) | "
          f"sections upserted: {n_sections} | "
          f"digests upserted: {len(digest_rows)} "
          f"(deleted: {counts.get('deleted_digests', 0)})")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
