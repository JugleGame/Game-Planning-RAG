#!/usr/bin/env python3
"""search_cards.py - 자유 텍스트 쿼리와 의미상 가장 유사한 카드를 pgvector로 검색한다.

card_context.py --similar 는 '이미 있는 카드 ID'끼리만 비교하지만, 이건 아직 카드가
아닌 임의의 문장(예: 신규 아이디어, 다이제스트 관측)을 같은 임베딩 공간에 넣어 비교한다.
--model은 embed_cards.py와 반드시 같아야 벡터 공간이 맞는다(기본값도 동일하게 유지).

2단 쿼리: Q1(전체 유사도) + Q2(GAME이면서 type이 failure/mixed인 카드만) - prompts/6_planner.md의
"반례 카드 최소 1개 필수, 없으면 '반례 조사 부족'이라 명시" 규칙을 자동으로 지원하기 위함.
반례는 별도 --no-counter로 끌 수 있다.

사용법:
  python tools/search_cards.py "AI가 실시간으로 심문하는 게임" [-k 5] [--counter-k 3] [--dsn postgresql://...]
"""
import argparse
import pathlib
import sys

import psycopg2
from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _db import resolve_dsn


def query_similar(cur, vec, k, extra_where=""):
    cur.execute(
        f"""
        SELECT card_id, title, 1 - (embedding <=> %s::vector) AS cosine_sim
        FROM cards
        WHERE embedding IS NOT NULL {extra_where}
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (vec, vec, k),
    )
    return cur.fetchall()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", help="검색할 자유 텍스트")
    ap.add_argument("--dsn", default=None)
    ap.add_argument("--model", default="jhgan/ko-sroberta-multitask")
    ap.add_argument("-k", type=int, default=5, help="전체 유사도 결과 수")
    ap.add_argument("--counter-k", type=int, default=3, help="반례(실패/혼재 GAME) 결과 수")
    ap.add_argument("--no-counter", action="store_true", help="반례 조회 생략")
    a = ap.parse_args()
    dsn = resolve_dsn(a.dsn)

    model = SentenceTransformer(a.model)
    vec = model.encode([a.query], normalize_embeddings=True)[0].tolist()

    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    rows = query_similar(cur, vec, a.k)

    if not rows:
        print("검색 가능한 임베딩 없음 (embed_cards.py 먼저 실행)")
        cur.close(); conn.close()
        return

    print(f"'{a.query}'와 가장 유사한 카드:")
    for cid, title, sim in rows:
        print(f"  {sim:.4f}  {cid}  {title}")

    if not a.no_counter:
        counter_rows = query_similar(
            cur, vec, a.counter_k,
            extra_where="AND kind = 'GAME' AND type IN ('failure', 'mixed')",
        )
        print("\n반례 후보 (GAME, 실패/혼재 사례만):")
        if counter_rows:
            for cid, title, sim in counter_rows:
                print(f"  {sim:.4f}  {cid}  {title}")
        else:
            print('  없음 - planner 프롬프트 규칙대로 "반례 조사 부족"으로 명시할 것')

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
