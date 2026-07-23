#!/usr/bin/env python3
"""verify_db.py - 미러링 상태 점검: 행 수, 참조 무결성, pgvector 유사도 샘플.

사용법:
  python tools/verify_db.py [--dsn postgresql://...] [--like ELEM-001]
"""
import argparse
import pathlib
import sys

import psycopg2

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _db import resolve_dsn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", default=None)
    ap.add_argument("--like", default=None, help="이 card_id와 임베딩 코사인 유사 카드 top-5 조회")
    a = ap.parse_args()
    dsn = resolve_dsn(a.dsn)

    conn = psycopg2.connect(dsn)
    cur = conn.cursor()

    cur.execute("SELECT kind, count(*) FROM cards GROUP BY kind ORDER BY kind")
    print("cards:", dict(cur.fetchall()))

    cur.execute("SELECT count(*) FROM card_refs")
    print("card_refs:", cur.fetchone()[0])

    cur.execute("SELECT count(*) FROM digests")
    print("digests:", cur.fetchone()[0])

    cur.execute("SELECT missing_card, referenced_by FROM unresolved_refs")
    unresolved = cur.fetchall()
    print(f"unresolved_refs: {len(unresolved)}건")
    for missing, refs in unresolved:
        print(f"  - {missing} <- {refs}")

    cur.execute("SELECT count(*) FROM cards WHERE embedding IS NOT NULL")
    n_embedded = cur.fetchone()[0]
    print(f"embedding 채워진 카드: {n_embedded}")

    if a.like:
        cur.execute(
            """
            SELECT b.card_id, b.title, 1 - (a.embedding <=> b.embedding) AS cosine_sim
            FROM cards a JOIN cards b ON b.card_id != a.card_id
            WHERE a.card_id = %s AND a.embedding IS NOT NULL AND b.embedding IS NOT NULL
            ORDER BY a.embedding <=> b.embedding LIMIT 5
            """,
            (a.like,),
        )
        rows = cur.fetchall()
        if not rows:
            print(f"{a.like}: 비교 가능한 임베딩 없음 (embed_cards.py 먼저 실행)")
        else:
            print(f"\n{a.like}와 가장 유사한 카드 (pgvector 코사인 유사도):")
            for cid, title, sim in rows:
                print(f"  {sim:.4f}  {cid}  {title}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
