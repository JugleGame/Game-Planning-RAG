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
ID_PAT = re.compile(r"\b(?:ELEM|GAME|GENRE)-\d{3}\b")
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
                if not re.match(r"^(ELEM|GAME|GENRE)-\d{3}$", card_id):
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


def sync(conn, card_rows, digest_rows, dry_run=False):
    cur = conn.cursor()

    live_card_ids = [c["card_id"] for c in card_rows]
    for c in card_rows:
        cur.execute(
            """
            INSERT INTO cards (card_id, type, title, summary, tags, elements, genres,
                                updated, confidence, body, file_path)
            VALUES (%(card_id)s, %(type)s, %(title)s, %(summary)s, %(tags)s, %(elements)s,
                    %(genres)s, %(updated)s, %(confidence)s, %(body)s, %(file_path)s)
            ON CONFLICT (card_id) DO UPDATE SET
              type=EXCLUDED.type, title=EXCLUDED.title, summary=EXCLUDED.summary,
              tags=EXCLUDED.tags, elements=EXCLUDED.elements, genres=EXCLUDED.genres,
              updated=EXCLUDED.updated, confidence=EXCLUDED.confidence, body=EXCLUDED.body,
              file_path=EXCLUDED.file_path
            """,
            c,
        )
        cur.execute("DELETE FROM card_refs WHERE from_id = %s", (c["card_id"],))
        if c["refs"]:
            psycopg2.extras.execute_values(
                cur,
                "INSERT INTO card_refs (from_id, to_id) VALUES %s ON CONFLICT DO NOTHING",
                [(c["card_id"], to_id) for to_id in c["refs"]],
            )

    deleted_cards = 0
    if live_card_ids:
        cur.execute("DELETE FROM cards WHERE card_id != ALL(%s) RETURNING card_id", (live_card_ids,))
    else:
        cur.execute("DELETE FROM cards RETURNING card_id")
    deleted_cards = cur.rowcount

    live_digest_dates = [d["digest_date"] for d in digest_rows]
    seen = set()
    for d in digest_rows:
        if d["digest_date"] in seen:
            raise ValueError(f"digest_date 충돌: {d['digest_date']} 이 둘 이상의 signal 파일에서 나옴")
        seen.add(d["digest_date"])
        cur.execute(
            """
            INSERT INTO digests (digest_date, period, sources, status, body)
            VALUES (%(digest_date)s, %(period)s, %(sources)s, %(status)s, %(body)s)
            ON CONFLICT (digest_date) DO UPDATE SET
              period=EXCLUDED.period, sources=EXCLUDED.sources, status=EXCLUDED.status, body=EXCLUDED.body
            """,
            d,
        )

    if live_digest_dates:
        cur.execute("DELETE FROM digests WHERE digest_date != ALL(%s) RETURNING digest_date", (live_digest_dates,))
    else:
        cur.execute("DELETE FROM digests RETURNING digest_date")
    deleted_digests = cur.rowcount

    if dry_run:
        conn.rollback()
    else:
        conn.commit()
    cur.close()
    return deleted_cards, deleted_digests


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", default=None)
    ap.add_argument("--dry-run", action="store_true", help="DB에 커밋하지 않고 계획만 확인")
    a = ap.parse_args()
    dsn = resolve_dsn(a.dsn)

    card_rows, digest_rows, errors = collect()
    if errors:
        print(f"스킵된 파일 {len(errors)}건 (기존 DB 행은 보존됨):", file=sys.stderr)
        for rel, msg in errors:
            print(f"  - {rel}: {msg}", file=sys.stderr)

    conn = psycopg2.connect(dsn)
    try:
        deleted_cards, deleted_digests = sync(conn, card_rows, digest_rows, dry_run=a.dry_run)
    except Exception as e:
        conn.rollback()
        print(f"동기화 실패, 롤백함: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()

    mode = "[DRY-RUN, 롤백됨] " if a.dry_run else ""
    print(f"{mode}cards upsert {len(card_rows)}장 (삭제 {deleted_cards}장) | "
          f"digests upsert {len(digest_rows)}건 (삭제 {deleted_digests}건)")
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
