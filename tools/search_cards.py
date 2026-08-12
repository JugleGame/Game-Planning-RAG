#!/usr/bin/env python3
"""search_cards.py - 자유 텍스트 질의에 가장 관련 있는 **절**을 하이브리드로 검색한다.

## 회수 단위가 카드에서 절로 바뀌었다 (2026-08-12)

예전에는 카드 한 장이 검색 단위였다. 두 가지가 동시에 망가져 있었다:

1. **정밀도** - "실패 사례"를 물어도 카드 전체의 평균 벡터와 비교했다. 성공 서사가
   대부분인 카드에서 실패 문단의 신호는 묻힌다.
2. **토큰** - 소비 측(기획 AI)이 카드 전문을 주입한다. 평균 2,075자 × 8장 ≈ 16,600자.
   실제로 필요한 건 보통 절 한둘(평균 340자)이다.

이제 `card_sections`에서 검색하고 절 본문을 그대로 돌려준다. 같은 회수 폭에서
주입량이 약 85% 준다.

## 왜 하이브리드인가 (2026-07-29 실측, 카드 단위 시절)

의미 임베딩 하나만 쓰면 **고유명사를 뭉갠다.** 게임 제목은 의미가 아니라 글자이기
때문이다. 실측(카드 55장, 고유명사 질의 17개):

  "Undertale 불살 루트"          → 벡터 19위 / 트라이그램 1위
  "Genshin Impact 원소 반응"     → 벡터 20위 / 트라이그램 1위
  recall@6:  벡터 단독 12/17  →  하이브리드 17/17

반대로 "죽을 때마다 무작위 업그레이드를 뽑는" 같은 의역 질의는 벡터가 잡고
트라이그램이 놓친다. 그래서 둘을 섞는다.

융합은 Reciprocal Rank Fusion — 점수가 아니라 **순위**를 더한다. 코사인 유사도
(0~1)와 트라이그램 유사도(0.03 대)는 척도가 달라 점수를 직접 섞으면 한쪽이 항상 이긴다.

주의: 위 실측의 '벡터 단독 12/17'은 임베딩 모델(ko-sroberta)의 입력 창이 128토큰이라
카드의 15.8%만 벡터에 들어가던 시절의 숫자다. 창 8192짜리 bge-m3 + 절 단위 청킹으로
바꾼 지금은 벡터 팔의 성능이 달라졌을 것이다 — **골드셋으로 다시 재야 한다.**

## 하위 호환 경고

**Game-Developer-AI 의 strategic/research_repo.py 가 이 SQL을 복제하고 있다.**
테이블(card_sections), 차원(1024), 모델(bge-m3)이 전부 바뀌었으므로 그쪽도 같이
고치지 않으면 같은 질의에 다른 근거가 나온다.

사용법:
  python tools/search_cards.py "AI가 실시간으로 심문하는 게임" [-k 5]
  python tools/search_cards.py "..." --kind ELEM,GENRE       # 종류 제한
  python tools/search_cards.py "..." --section-key gaps      # 특정 절만
  python tools/search_cards.py "..." --show-body             # 주입될 실제 본문 확인
  python tools/search_cards.py "..." --expand 3              # 인접 카드까지 넓히기
"""
import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from _db import open_cursor, resolve_dsn, vec_literal
from card_schema import ALL_SECTION_KEYS, COUNTER_SECTION_KEYS, TYPE_VOCAB

# RRF 상수. 60 은 원 논문(Cormack et al. 2009)의 값이고, 상위 순위 간의 격차를
# 완만하게 만들어 한 검색기가 1위를 독식하지 못하게 한다.
RRF_K = 60

# 각 검색기에서 몇 위까지를 후보로 볼지. 창이 없으면 두 검색기가 모두 무관하다고
# 본 행도 꼴찌 순위만큼의 표를 얻어 결과를 채운다.
#
# 카드 단위 시절의 40은 '카드 55장 중 40'이라는 실측이었다. 이제 대상이 절
# 811개이므로 그 숫자는 그대로 옮겨오면 안 된다. 60은 잠정값이고, 골드셋을 고정한
# 뒤 다시 튜닝해야 한다 (--window 로 실험 가능).
CANDIDATE_WINDOW = 60

# 트라이그램 대상. 카드 표면(제목·요약·태그)에 절 본문을 붙인다.
# 예전에는 카드 표면만 봐서 본문 안의 고유명사(개발사명, 인용 매체)가 어휘 검색에
# 걸리지 않았다.
TRIGRAM_BLOB = ("c.title || ' ' || c.summary || ' ' || array_to_string(c.tags,' ') "
                "|| ' ' || s.body")

# 신뢰도·신선도 가중치. RRF 점수에 곱한다.
#
# 폭을 일부러 좁게 잡았다(최대 10% + 6%). 순위를 뒤집는 힘이 아니라 비슷한 후보
# 사이의 타이브레이커여야 한다 - 오래됐지만 정확히 맞는 근거가 최신의 헛다리보다
# 밀리면 안 된다.
CONFIDENCE_WEIGHT = ("CASE confidence WHEN 'high' THEN 1.00 WHEN 'medium' THEN 0.97 "
                     "WHEN 'medium-low' THEN 0.94 ELSE 0.90 END")
RECENCY_WEIGHT = ("(1.0 - LEAST(GREATEST(CURRENT_DATE - updated, 0), 730)::numeric "
                  "/ 730 * 0.06)")

HYBRID_SQL = f"""
WITH scored AS (
    SELECT s.card_id, s.ord, s.section_key, s.section_title, s.body,
           c.title, c.kind, c.confidence, c.updated,
           1 - (s.embedding <=> %(vec)s::vector) AS cosine_sim,
           similarity({TRIGRAM_BLOB}, %(query)s) AS trigram_sim
    FROM card_sections s JOIN cards c ON c.card_id = s.card_id
    WHERE TRUE {{filters}}
), ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (ORDER BY cosine_sim  DESC NULLS LAST) AS vec_rank,
           ROW_NUMBER() OVER (ORDER BY trigram_sim DESC NULLS LAST) AS trg_rank
    FROM scored
), fused AS (
    SELECT *,
           ((CASE WHEN vec_rank <= %(window)s THEN 1.0 / (%(rrf_k)s + vec_rank) ELSE 0 END)
          + (CASE WHEN trg_rank <= %(window)s THEN 1.0 / (%(rrf_k)s + trg_rank) ELSE 0 END))
           * {CONFIDENCE_WEIGHT} * {RECENCY_WEIGHT} AS score
    FROM ranked
    WHERE vec_rank <= %(window)s OR trg_rank <= %(window)s
)
SELECT card_id, ord, section_key, section_title, title, body, cosine_sim, score,
       CASE WHEN vec_rank <= %(window)s AND trg_rank <= %(window)s THEN 'vec+trg'
            WHEN vec_rank <= %(window)s THEN 'vec'
            ELSE 'trg' END AS matched_by
FROM fused
ORDER BY score DESC, cosine_sim DESC NULLS LAST
LIMIT %(k)s
"""

VECTOR_SQL = """
SELECT s.card_id, s.ord, s.section_key, s.section_title, c.title, s.body,
       1 - (s.embedding <=> %(vec)s::vector) AS cosine_sim,
       1 - (s.embedding <=> %(vec)s::vector) AS score,
       'vec' AS matched_by
FROM card_sections s JOIN cards c ON c.card_id = s.card_id
WHERE s.embedding IS NOT NULL {filters}
ORDER BY s.embedding <=> %(vec)s::vector
LIMIT %(k)s
"""

# 이웃 카드(1홉). card_refs는 지금까지 audit_links.py가 무결성만 지키고 검색은
# 쓰지 않던 자산이다 - 양방향으로 관리되는 지식 그래프가 이미 있는데 안 쓰는 건 낭비다.
NEIGHBOR_SQL = """
SELECT DISTINCT c.card_id, c.title, c.kind
FROM card_refs r
JOIN cards c ON c.card_id = CASE WHEN r.from_id = ANY(%(seeds)s) THEN r.to_id ELSE r.from_id END
WHERE (r.from_id = ANY(%(seeds)s) OR r.to_id = ANY(%(seeds)s))
  AND c.card_id <> ALL(%(seeds)s)
LIMIT %(k)s
"""


def section_ref(row):
    """절 하나를 가리키는 키. 중복 제거와 --show-body 표시에 쓴다."""
    return f"{row['card_id']}#{row['ord']}"


def build_filters(kinds, section_keys, exclude_refs=None):
    """(SQL 조각, 추가 파라미터). 값은 전부 파라미터로 넘긴다 - 문자열 삽입 금지."""
    frag, params = "", {}
    if kinds:
        frag += " AND c.kind = ANY(%(kinds)s)"
        params["kinds"] = list(kinds)
    if section_keys:
        frag += " AND s.section_key = ANY(%(section_keys)s)"
        params["section_keys"] = list(section_keys)
    if exclude_refs:
        # (card_id, ord) 복합 비교는 배열로 다루기 번거로워 텍스트 키로 뺀다.
        frag += " AND (s.card_id || '#' || s.ord) <> ALL(%(exclude_refs)s)"
        params["exclude_refs"] = list(exclude_refs)
    return frag, params


def query_sections(cur, vec, query, k, mode="hybrid", kinds=None,
                   section_keys=None, exclude_refs=None, window=CANDIDATE_WINDOW):
    frag, extra = build_filters(kinds, section_keys, exclude_refs)
    sql = (VECTOR_SQL if mode == "vector" else HYBRID_SQL).format(filters=frag)
    # 좌표는 항상 pgvector 텍스트 표기로 넘긴다 - 5432와 443이 같은 값을 봐야 한다.
    cur.execute(sql, {"vec": vec_literal(vec), "query": query, "k": k,
                      "window": window, "rrf_k": RRF_K, **extra})
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, r)) for r in cur.fetchall()]


def print_rows(rows, show_body=False):
    for r in rows:
        sim = r.get("cosine_sim")
        # 코사인은 트라이그램만으로 걸린 행에서 NULL 일 수 있다 (임베딩 없는 절).
        # HTTPS 경로는 수치형을 문자열로 돌려주기도 한다(브리지의 JSON 변환).
        shown = f"{float(sim):.4f}" if sim is not None else "  -   "
        print(f"  {shown}  [{r['matched_by']:<7}] {r['card_id']}#{r['section_key']}"
              f"  {r['title']}  › {r['section_title']}")
        if show_body:
            for line in r["body"].splitlines():
                print(f"        {line}")
            print()


def check_transport(dsn, vec, query, k, mode, window):
    """두 경로가 같은 질의에 같은 행을 주는지 확인한다 (양쪽 다 열릴 때만 가능).

    자리표시자 재작성이 미묘하게 틀리면 검색 결과가 '조용히' 달라진다 - 지금처럼
    대놓고 죽는 것보다 나쁘다. 그래서 회수 결과의 신원(절 키·순서·어느 팔에
    걸렸는지)과 코사인 값을 직접 맞춰 본다.

    수치형 표기는 경로마다 다르다(psycopg2는 Decimal, 브리지는 문자열). 표기가
    아니라 값을 비교해야 하므로 float으로 맞추고 1e-9까지 본다.
    """
    def rows_via(transport):
        cur, close, used = open_cursor(dsn, transport)
        try:
            return used, query_sections(cur, vec, query, k, mode, window=window)
        finally:
            close()

    import psycopg2
    try:
        used_pg, pg_rows = rows_via("pg")
    except psycopg2.OperationalError as e:
        # auto로 폴백해서 https끼리 비교하면 '통과'가 나온다 - 그건 거짓 통과다.
        sys.exit(f"5432에 붙을 수 없어 대조할 수 없다 (막힌 망에서는 이 점검을 돌릴 수 "
                 f"없다): {str(e).strip().splitlines()[0][:120]}")
    used_https, https_rows = rows_via("https")
    print(f"[{used_pg}] {len(pg_rows)}행  vs  [{used_https}] {len(https_rows)}행")

    def key(r):
        return (r["card_id"], int(r["ord"]), r["section_key"], r["matched_by"])

    diffs = []
    if len(pg_rows) != len(https_rows):
        diffs.append(f"행 수가 다르다: {len(pg_rows)} vs {len(https_rows)}")
    for i, (p, h) in enumerate(zip(pg_rows, https_rows)):
        if key(p) != key(h):
            diffs.append(f"{i + 1}위: {key(p)} vs {key(h)}")
        elif abs(float(p["cosine_sim"] or 0) - float(h["cosine_sim"] or 0)) > 1e-9:
            diffs.append(f"{i + 1}위 {p['card_id']} 코사인: "
                         f"{p['cosine_sim']} vs {h['cosine_sim']}")
        elif p["body"] != h["body"]:
            diffs.append(f"{i + 1}위 {p['card_id']} 본문이 다르다")
    if diffs:
        print("불일치:")
        for d in diffs:
            print(f"  - {d}")
        sys.exit(1)
    print(f"일치 - 두 경로가 같은 절을 같은 순서로 돌려준다 ({len(pg_rows)}행)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", help="검색할 자유 텍스트")
    ap.add_argument("--dsn", default=None)
    ap.add_argument("--model", default="BAAI/bge-m3",
                    help="embed_cards.py와 반드시 같아야 좌표계가 맞는다")
    ap.add_argument("-k", type=int, default=5, help="전체 유사도 결과 수")
    ap.add_argument("--counter-k", type=int, default=3, help="반례 절 결과 수")
    ap.add_argument("--no-counter", action="store_true", help="반례 조회 생략")
    ap.add_argument("--kind", default=None,
                    help=f"쉼표 구분 종류 제한: {','.join(sorted(TYPE_VOCAB))}")
    ap.add_argument("--section-key", default=None,
                    help=f"쉼표 구분 절 제한: {','.join(ALL_SECTION_KEYS)}")
    ap.add_argument("--show-body", action="store_true",
                    help="절 본문까지 출력 (소비 측에 실제로 주입될 내용)")
    ap.add_argument("--expand", type=int, default=0,
                    help="상위 결과 카드의 인접 카드(card_refs 1홉)를 N개까지 덧붙임")
    ap.add_argument("--window", type=int, default=CANDIDATE_WINDOW,
                   help="각 검색기의 후보 창 (골드셋으로 재튜닝 필요)")
    ap.add_argument("--mode", choices=("hybrid", "vector"), default="hybrid",
                    help="hybrid(기본) 또는 비교용 vector 단독")
    ap.add_argument("--transport", choices=["auto", "pg", "https"], default="auto",
                    help="auto=5432 먼저 시도 후 실패 시 443/HTTPS 폴백 (기본값)")
    ap.add_argument("--check-transport", action="store_true",
                    help="5432와 443/HTTPS가 같은 결과를 주는지 대조 (양쪽 다 열려야 함)")
    a = ap.parse_args()
    dsn = resolve_dsn(a.dsn)

    kinds = [k.strip().upper() for k in a.kind.split(",")] if a.kind else None
    if kinds:
        bad = set(kinds) - set(TYPE_VOCAB)
        if bad:
            sys.exit(f"알 수 없는 종류: {', '.join(sorted(bad))}")
    keys = [s.strip() for s in a.section_key.split(",")] if a.section_key else None
    if keys:
        bad = set(keys) - set(ALL_SECTION_KEYS)
        if bad:
            sys.exit(f"알 수 없는 section_key: {', '.join(sorted(bad))}")

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(a.model)
    vec = model.encode([a.query], normalize_embeddings=True)[0].tolist()

    if a.check_transport:
        check_transport(dsn, vec, a.query, a.k, a.mode, a.window)
        return

    cur, close, used = open_cursor(dsn, a.transport)
    rows = query_sections(cur, vec, a.query, a.k, a.mode, kinds, keys, window=a.window)

    if not rows:
        print("검색 가능한 임베딩 없음 (sync_db.py → embed_cards.py 먼저 실행)")
        close()
        return

    print(f"[{used}] '{a.query}'와 가장 관련 있는 절 ({a.mode}):")
    print_rows(rows, a.show_body)

    if not a.no_counter:
        # 반례는 카드의 속성이 아니라 절의 속성이다. 예전처럼 실패/혼재 GAME 카드만
        # 보면, 성공 카드 안에 적힌 실패 문단(GAME-031 Balatro의 PEGI 18+ 사건 등)에
        # 영원히 도달하지 못한다.
        #
        # 이미 위에 나온 절은 뺀다. 질의 자체가 실패를 묻는 경우(예: "덱빌더가
        # 실패하는 지점") 상위 결과가 이미 failure_cases라 같은 절이 두 번 나오고,
        # 소비 측은 같은 근거를 두 번 주입하게 된다.
        counter = query_sections(cur, vec, a.query, a.counter_k, a.mode, kinds,
                                 COUNTER_SECTION_KEYS, window=a.window,
                                 exclude_refs=[section_ref(r) for r in rows])
        print("\n반례·위험 절 (위 결과와 중복 제외):")
        if counter:
            print_rows(counter, a.show_body)
            # Game-Developer-AI 쪽은 여기에 유사도 하한선을 걸어 미달이면 비운다.
            # 이 CLI 는 사람이 눈으로 보는 도구라 자르지 않고 점수를 그대로 보인다.
            print("  (참고: 파이프라인은 코사인 0.45 미만을 반례로 인정하지 않는다)")
        else:
            print('  없음 - planner 프롬프트 규칙대로 "반례 조사 부족"으로 명시할 것')

    if a.expand:
        seeds = sorted({r["card_id"] for r in rows})
        cur.execute(NEIGHBOR_SQL, {"seeds": seeds, "k": a.expand})
        neighbors = cur.fetchall()
        print(f"\n인접 카드 (card_refs 1홉, 씨앗 {', '.join(seeds)}):")
        if neighbors:
            for cid, title, kind in neighbors:
                print(f"  {cid}  {title}")
        else:
            print("  없음")

    close()


if __name__ == "__main__":
    main()
