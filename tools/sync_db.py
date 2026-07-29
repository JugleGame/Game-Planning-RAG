#!/usr/bin/env python3
"""sync_db.py - research/*.md (원본) -> Postgres cards/card_refs/digests (거울) 동기화.

원칙: md 파일이 원본, DB는 거울. 이 스크립트만이 cards/card_refs/digests에 쓴다.
- ELEM-###/GAME-###/GENRE-### 카드 -> cards (+ 본문에서 스캔한 ID 언급 -> card_refs)
- signals/YYYY-MM-DD_*.md (type = "digest") -> digests (digest_date = 파일명 날짜)
- 파일에서 사라진 카드/다이제스트는 DB에서도 삭제한다 (완전 거울). 단, frontmatter
  파싱에 실패한 파일은 '성공적으로 확인된 상태'가 아니므로 기존 DB 행을 보존한다
  (알 수 없는 상태에서 데이터를 지우지 않는다).
- embedding/body_hash 컬럼은 건드리지 않는다 - 그건 embed_cards.py의 책임.

사용법:
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
from card_schema import CARD_REQUIRED, DIGEST_REQUIRED

RESEARCH = BASE / "research"

FM_PAT = re.compile(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)$", re.S)
ID_PAT = re.compile(r"\b(?:ELEM|GAME|GENRE|ARCH)-\d{3}\b")
DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})_")


def parse_date(v):
    if isinstance(v, datetime.date):
        return v
    return datetime.date.fromisoformat(str(v).strip())


def load_frontmatter(path: pathlib.Path):
    raw = path.read_text(encoding="utf-8")
    m = FM_PAT.match(raw)
    if not m:
        raise ValueError("frontmatter(+++ 블록)를 찾을 수 없음")
    fm = tomllib.loads(m.group(1))
    body = m.group(2).strip()
    return fm, body


def collect():
    """research/**/*.md를 훑어 (card_rows, digest_rows, errors)를 돌려준다."""
    card_rows, digest_rows, errors = [], [], []
    for path_str in glob.glob(str(RESEARCH / "**" / "*.md"), recursive=True):
        path = pathlib.Path(path_str)
        if path.name == "_index.md":
            continue
        rel = str(path.relative_to(BASE))
        try:
            fm, body = load_frontmatter(path)
            is_digest = str(fm.get("type", "")).strip() == "digest"
            if is_digest:
                missing = [k for k in DIGEST_REQUIRED if not fm.get(k)]
                if missing:
                    raise ValueError(f"digest 필수 필드 누락: {missing}")
                m = DATE_PREFIX.match(path.name)
                if m:
                    digest_date = datetime.date.fromisoformat(m.group(1))
                elif fm.get("period_end"):
                    digest_date = parse_date(fm["period_end"])
                else:
                    raise ValueError("파일명에 YYYY-MM-DD 접두어가 없고 period_end도 없음")
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
                    raise ValueError(f"카드 필수 필드 누락: {missing}")
                card_id = str(fm["card_id"])
                if not re.match(r"^(ELEM|GAME|GENRE|ARCH)-\d{3}$", card_id):
                    raise ValueError(f"card_id 형식 불일치: {card_id}")

                refs = {r for r in ID_PAT.findall(body) if r != card_id}
                refs |= {g for g in fm.get("example_games", []) if g != card_id}

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
    plan = []
    for c in card_rows:
        plan.append((CARD_UPSERT, [c["card_id"], c["type"], c["title"], c["summary"],
                                   c["tags"], c["elements"], c["genres"],
                                   c["updated"], c["confidence"], c["body"], c["file_path"]], None))
        plan.append(("DELETE FROM card_refs WHERE from_id = $1", [c["card_id"]], None))
        for to_id in c["refs"]:
            plan.append(("INSERT INTO card_refs (from_id, to_id) VALUES ($1, $2) "
                         "ON CONFLICT DO NOTHING", [c["card_id"], to_id], None))

    live_card_ids = [c["card_id"] for c in card_rows]
    if live_card_ids:
        plan.append(("DELETE FROM cards WHERE card_id != ALL($1::text[]) RETURNING card_id",
                     [live_card_ids], "deleted_cards"))
    else:
        plan.append(("DELETE FROM cards RETURNING card_id", [], "deleted_cards"))

    seen = set()
    for d in digest_rows:
        if d["digest_date"] in seen:
            raise ValueError(f"digest_date 충돌: {d['digest_date']} 이 둘 이상의 signal 파일에서 나옴")
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
    """psycopg2(5432)로 계획을 한 트랜잭션에 실행한다."""
    counts = {}
    conn = psycopg2.connect(dsn)
    try:
        cur = conn.cursor()
        for sql, params, tag in plan:
            cur.execute(_to_pyformat(sql), params)
            if tag:
                counts[tag] = cur.rowcount
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

    results = https_transaction([(sql, params) for sql, params, _ in plan])
    counts = {}
    for (sql, params, tag), res in zip(plan, results):
        if tag:
            counts[tag] = res.get("rowCount") or len(res.get("rows") or [])
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", default=None)
    ap.add_argument("--dry-run", action="store_true", help="DB에 커밋하지 않고 계획만 확인")
    ap.add_argument("--transport", choices=["auto", "pg", "https"], default="auto",
                    help="auto=5432 먼저 시도 후 실패 시 443/HTTPS 폴백 (기본값)")
    a = ap.parse_args()
    dsn = resolve_dsn(a.dsn)

    card_rows, digest_rows, errors = collect()
    if errors:
        print(f"스킵된 파일 {len(errors)}건 (기존 DB 행은 보존됨):", file=sys.stderr)
        for rel, msg in errors:
            print(f"  - {rel}: {msg}", file=sys.stderr)

    try:
        plan = build_plan(card_rows, digest_rows)
    except ValueError as e:
        print(f"계획 생성 실패: {e}", file=sys.stderr)
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
                print(f"5432 접속 실패 -> 443/HTTPS 브리지로 폴백합니다 ({first})", file=sys.stderr)
                counts = execute_https(plan, dry_run=a.dry_run)
                used = "443/HTTPS"
        else:
            counts = execute_https(plan, dry_run=a.dry_run)
            used = "443/HTTPS"
    except Exception as e:
        print(f"동기화 실패(롤백됨): {e}", file=sys.stderr)
        sys.exit(1)

    if a.dry_run:
        mode = "[DRY-RUN, 롤백됨] " if used == "5432" else "[DRY-RUN, 실행 안 함] "
    else:
        mode = ""
    print(f"{mode}[{used}] cards upsert {len(card_rows)}장 "
          f"(삭제 {counts.get('deleted_cards', 0)}장) | "
          f"digests upsert {len(digest_rows)}건 "
          f"(삭제 {counts.get('deleted_digests', 0)}건)")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
