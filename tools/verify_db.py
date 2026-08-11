#!/usr/bin/env python3
"""verify_db.py - 미러링 상태 점검: 행 수, 참조 무결성, pgvector 유사도 샘플.

사용법:
  python tools/verify_db.py [--dsn postgresql://...] [--like ELEM-001]
"""
import argparse
import pathlib
import re
import sys

import psycopg2

BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _db import resolve_dsn


class Runner:
    """5432가 되면 psycopg2로, 안 되면 443/HTTPS 브리지로 같은 SQL을 돌린다.

    두 경로 모두 '컬럼 순서대로의 튜플 리스트'를 돌려주도록 맞춘다
    (psycopg2는 원래 튜플, HTTPS는 dict라서 cols 순서로 변환).
    자리표시자는 $1,$2… 로 쓰고 psycopg2일 때만 %s로 바꾼다.
    """

    def __init__(self, dsn, transport="auto"):
        self.conn = None
        self.https = None
        if transport in ("auto", "pg"):
            try:
                self.conn = psycopg2.connect(dsn)
                self.used = "5432"
                return
            except psycopg2.OperationalError as e:
                if transport == "pg":
                    raise
                print(f"5432 접속 실패 -> 443/HTTPS 브리지로 폴백합니다 "
                      f"({str(e).strip().splitlines()[0][:100]})", file=sys.stderr)
        sys.path.insert(0, str(BASE / "db"))
        import neon_https
        self.https = neon_https
        self.used = "443/HTTPS"

    def q(self, sql, cols, params=None):
        if self.conn:
            cur = self.conn.cursor()
            cur.execute(re.sub(r"\$\d+", "%s", sql), params or None)
            rows = cur.fetchall()
            cur.close()
            return rows
        return [tuple(r[c] for c in cols) for r in self.https.query(sql, params or [])]

    def close(self):
        if self.conn:
            self.conn.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dsn", default=None)
    ap.add_argument("--like", default=None, help="이 card_id와 임베딩 코사인 유사 카드 top-5 조회")
    ap.add_argument("--transport", choices=["auto", "pg", "https"], default="auto",
                    help="auto=5432 먼저 시도 후 실패 시 443/HTTPS 폴백 (기본값)")
    a = ap.parse_args()
    r = Runner(resolve_dsn(a.dsn), a.transport)
    print(f"[{r.used}]")

    print("cards:", dict(r.q("SELECT kind, count(*) AS n FROM cards GROUP BY kind ORDER BY kind",
                             ["kind", "n"])))
    print("card_refs:", r.q("SELECT count(*) AS n FROM card_refs", ["n"])[0][0])
    print("digests:", r.q("SELECT count(*) AS n FROM digests", ["n"])[0][0])
    print("sections:", dict(r.q("SELECT section_key, count(*) AS n FROM card_sections "
                                "GROUP BY section_key ORDER BY section_key",
                                ["section_key", "n"])))

    unresolved = r.q("SELECT missing_card, referenced_by FROM unresolved_refs",
                     ["missing_card", "referenced_by"])
    print(f"unresolved_refs: {len(unresolved)}건")
    for missing, refs in unresolved:
        print(f"  - {missing} <- {refs}")

    n_embedded = r.q("SELECT count(*) AS n FROM cards WHERE embedding IS NOT NULL", ["n"])[0][0]
    n_sec_emb = r.q("SELECT count(*) AS n FROM card_sections WHERE embedding IS NOT NULL",
                    ["n"])[0][0]
    n_sec = r.q("SELECT count(*) AS n FROM card_sections", ["n"])[0][0]
    print(f"embedding 채워진 카드: {n_embedded}")
    print(f"embedding 채워진 절: {n_sec_emb} / {n_sec}")
    if n_sec_emb < n_sec:
        print("  ! 좌표 없는 절이 있다 - tools/embed_cards.py 실행 필요", file=sys.stderr)

    if a.like:
        rows = r.q(
            """
            SELECT b.card_id, b.title, 1 - (a.embedding <=> b.embedding) AS cosine_sim
            FROM cards a JOIN cards b ON b.card_id != a.card_id
            WHERE a.card_id = $1 AND a.embedding IS NOT NULL AND b.embedding IS NOT NULL
            ORDER BY a.embedding <=> b.embedding LIMIT 5
            """,
            ["card_id", "title", "cosine_sim"], [a.like],
        )
        if not rows:
            print(f"{a.like}: 비교 가능한 임베딩 없음 (embed_cards.py 먼저 실행)")
        else:
            print(f"\n{a.like}와 가장 유사한 카드 (pgvector 코사인 유사도):")
            for cid, title, sim in rows:
                print(f"  {float(sim):.4f}  {cid}  {title}")

    r.close()


if __name__ == "__main__":
    main()
