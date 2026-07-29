#!/usr/bin/env python3
"""search_cards.py - 자유 텍스트 쿼리와 가장 관련 있는 카드를 하이브리드로 검색한다.

card_context.py --similar 는 '이미 있는 카드 ID'끼리만 비교하지만, 이건 아직 카드가
아닌 임의의 문장(예: 신규 아이디어, 다이제스트 관측)을 같은 임베딩 공간에 넣어 비교한다.
--model은 embed_cards.py와 반드시 같아야 벡터 공간이 맞는다(기본값도 동일하게 유지).

## 왜 하이브리드인가 (2026-07-29)

의미 임베딩 하나만 쓰면 **고유명사를 뭉갠다.** 게임 제목은 의미가 아니라 글자이기
때문이다. 실측(카드 55장, 고유명사 질의 17개, 지지 근거 풀):

  "Undertale 불살 루트"          → 벡터 19위 / 트라이그램 1위
  "Genshin Impact 원소 반응"     → 벡터 20위 / 트라이그램 1위
  "Breath of the Wild 사당 보상" → 벡터 14위 / 트라이그램 1위

  recall@6:  벡터 단독 12/17  →  하이브리드 17/17

반대로 "죽을 때마다 무작위 업그레이드를 뽑는" 같은 의역 질의는 벡터가 잡고
트라이그램이 놓친다. 그래서 둘을 섞는다.

융합은 Reciprocal Rank Fusion — 점수가 아니라 **순위**를 더한다. 코사인 유사도
(0~1)와 트라이그램 유사도(여기서는 0.03 대)는 척도가 달라서 점수를 직접 섞으면
한쪽이 항상 이긴다.

**Game-Developer-AI 의 strategic/research_repo.py 가 같은 방식으로 검색한다.**
한쪽만 고치면 같은 질의에 다른 근거가 나온다 — 그쪽 파일의 _HYBRID_SQL 참고.

사용법:
  python tools/search_cards.py "AI가 실시간으로 심문하는 게임" [-k 5] [--counter-k 3]
  python tools/search_cards.py "..." --mode vector   # 비교용: 예전 벡터 단독
"""
import argparse
import pathlib
import sys

import psycopg2
from sentence_transformers import SentenceTransformer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _db import resolve_dsn

# RRF 상수. 60 은 원 논문(Cormack et al. 2009)의 값이고, 상위 순위 간의 격차를
# 완만하게 만들어 한 검색기가 1위를 독식하지 못하게 한다.
RRF_K = 60

# 각 검색기에서 몇 위까지를 후보로 볼지. 창이 없으면 두 검색기가 모두 무관하다고
# 본 카드도 꼴찌 순위만큼의 표를 얻어 결과를 채운다.
#
# 20 이 아니라 40 인 이유는 실측이다. 카드 55장 전체를 후보로 두면 "Undertale
# 불살 루트" 같은 질의의 정답이 벡터 쪽 20위 밖으로 밀려 어휘 표 하나만 남고,
# 양쪽에서 어중간한 카드가 표 두 장으로 이긴다 — recall@6 이 15/17 로 떨어졌다.
# 창을 40 으로 넓히면 17/17.
CANDIDATE_WINDOW = 40

TRIGRAM_BLOB = "title || ' ' || summary || ' ' || array_to_string(tags,' ')"

HYBRID_SQL = f"""
WITH scored AS (
    SELECT card_id, title,
           1 - (embedding <=> %(vec)s::vector) AS cosine_sim,
           similarity({TRIGRAM_BLOB}, %(query)s) AS trigram_sim
    FROM cards
    WHERE TRUE {{extra_where}}
), ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY cosine_sim DESC NULLS LAST) AS vec_rank,
           ROW_NUMBER() OVER (ORDER BY trigram_sim DESC NULLS LAST) AS trg_rank
    FROM scored
)
SELECT card_id, title, cosine_sim,
       CASE WHEN vec_rank <= %(window)s AND trg_rank <= %(window)s THEN 'vec+trg'
            WHEN vec_rank <= %(window)s THEN 'vec'
            ELSE 'trg' END AS matched_by
FROM ranked
WHERE vec_rank <= %(window)s OR trg_rank <= %(window)s
ORDER BY (CASE WHEN vec_rank <= %(window)s THEN 1.0 / (%(rrf_k)s + vec_rank) ELSE 0 END)
       + (CASE WHEN trg_rank <= %(window)s THEN 1.0 / (%(rrf_k)s + trg_rank) ELSE 0 END) DESC,
         cosine_sim DESC NULLS LAST
LIMIT %(k)s
"""

VECTOR_SQL = """
SELECT card_id, title, 1 - (embedding <=> %(vec)s::vector) AS cosine_sim, 'vec' AS matched_by
FROM cards
WHERE embedding IS NOT NULL {extra_where}
ORDER BY embedding <=> %(vec)s::vector
LIMIT %(k)s
"""


def query_cards(cur, vec, query, k, mode="hybrid", extra_where=""):
    """(card_id, title, cosine_sim, matched_by) 목록. mode 는 hybrid | vector."""
    sql = (VECTOR_SQL if mode == "vector" else HYBRID_SQL).format(extra_where=extra_where)
    cur.execute(
        sql,
        {"vec": vec, "query": query, "k": k, "window": CANDIDATE_WINDOW, "rrf_k": RRF_K},
    )
    return cur.fetchall()


def _print_rows(rows):
    for cid, title, sim in ((r[0], r[1], r[2]) for r in rows):
        # 코사인은 트라이그램만으로 걸린 카드에서 NULL 일 수 있다 (임베딩 없는 카드).
        shown = f"{sim:.4f}" if sim is not None else "  -   "
        print(f"  {shown}  {cid}  {title}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", help="검색할 자유 텍스트")
    ap.add_argument("--dsn", default=None)
    ap.add_argument("--model", default="jhgan/ko-sroberta-multitask")
    ap.add_argument("-k", type=int, default=5, help="전체 유사도 결과 수")
    ap.add_argument("--counter-k", type=int, default=3, help="반례(실패/혼재 GAME) 결과 수")
    ap.add_argument("--no-counter", action="store_true", help="반례 조회 생략")
    ap.add_argument(
        "--mode",
        choices=("hybrid", "vector"),
        default="hybrid",
        help="hybrid(기본) 또는 비교용 vector 단독",
    )
    a = ap.parse_args()
    dsn = resolve_dsn(a.dsn)

    model = SentenceTransformer(a.model)
    vec = model.encode([a.query], normalize_embeddings=True)[0].tolist()

    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    rows = query_cards(cur, vec, a.query, a.k, a.mode)

    if not rows:
        print("검색 가능한 임베딩 없음 (embed_cards.py 먼저 실행)")
        cur.close(); conn.close()
        return

    print(f"'{a.query}'와 가장 관련 있는 카드 ({a.mode}):")
    _print_rows(rows)

    if not a.no_counter:
        counter_rows = query_cards(
            cur, vec, a.query, a.counter_k, a.mode,
            extra_where="AND kind = 'GAME' AND type IN ('failure', 'mixed')",
        )
        print("\n반례 후보 (GAME, 실패/혼재 사례만):")
        if counter_rows:
            _print_rows(counter_rows)
            # Game-Developer-AI 쪽은 여기에 유사도 하한선을 걸어 미달이면 비운다.
            # 이 CLI 는 사람이 눈으로 보는 도구라 자르지 않고 점수를 그대로 보인다.
            print("  (참고: 파이프라인은 코사인 0.45 미만을 반례로 인정하지 않는다)")
        else:
            print('  없음 - planner 프롬프트 규칙대로 "반례 조사 부족"으로 명시할 것')

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
