#!/usr/bin/env python3
"""Hybrid-search the most relevant RAG-card sections for a free-text query.

Retrieval is section-based (``card_sections``), not card-based: it preserves
signals such as failure cases and returns only the body that the consumer needs,
reducing injected context substantially. Retrieval blends dense vectors with
trigram search by Reciprocal Rank Fusion: vectors cover paraphrases and
trigrams preserve proper nouns.

The earlier card-level vector-only benchmark is historical. Re-measure current
section-level bge-m3 retrieval with the gold set before tuning this system.
The consumer repository duplicates this SQL, so schema/model/query changes
require a coordinated consumer update.

Examples:
  python tools/search_cards.py "an AI that interrogates the player in real time" -k 5
  python tools/search_cards.py "..." --kind ELEM,GENRE
  python tools/search_cards.py "..." --section-key gaps
  python tools/search_cards.py "..." --show-body
  python tools/search_cards.py "..." --expand 3
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
        sys.exit(f"Cannot compare transports because 5432 is unavailable "
                 f"(this check cannot run on a blocked network): {str(e).strip().splitlines()[0][:120]}")
    used_https, https_rows = rows_via("https")
    print(f"[{used_pg}] {len(pg_rows)} rows  vs  [{used_https}] {len(https_rows)} rows")

    def key(r):
        return (r["card_id"], int(r["ord"]), r["section_key"], r["matched_by"])

    diffs = []
    if len(pg_rows) != len(https_rows):
        diffs.append(f"row count differs: {len(pg_rows)} vs {len(https_rows)}")
    for i, (p, h) in enumerate(zip(pg_rows, https_rows)):
        if key(p) != key(h):
            diffs.append(f"rank {i + 1}: {key(p)} vs {key(h)}")
        elif abs(float(p["cosine_sim"] or 0) - float(h["cosine_sim"] or 0)) > 1e-9:
            diffs.append(f"rank {i + 1} {p['card_id']} cosine: "
                         f"{p['cosine_sim']} vs {h['cosine_sim']}")
        elif p["body"] != h["body"]:
            diffs.append(f"rank {i + 1} {p['card_id']} body differs")
    if diffs:
        print("Mismatch:")
        for d in diffs:
            print(f"  - {d}")
        sys.exit(1)
    print(f"Match — both transports returned the same sections in the same order ({len(pg_rows)} rows)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query", help="free-text query")
    ap.add_argument("--dsn", default=None)
    ap.add_argument("--model", default="BAAI/bge-m3",
                    help="must match embed_cards.py to use the same embedding space")
    ap.add_argument("-k", type=int, default=5, help="number of primary results")
    ap.add_argument("--counter-k", type=int, default=3, help="number of counterexample-section results")
    ap.add_argument("--no-counter", action="store_true", help="skip counterexample retrieval")
    ap.add_argument("--kind", default=None,
                    help=f"comma-separated type filter: {','.join(sorted(TYPE_VOCAB))}")
    ap.add_argument("--section-key", default=None,
                    help=f"comma-separated section filter: {','.join(ALL_SECTION_KEYS)}")
    ap.add_argument("--show-body", action="store_true",
                    help="include section bodies (the text delivered to consumers)")
    ap.add_argument("--expand", type=int, default=0,
                    help="include up to N one-hop card_refs neighbors of top results")
    ap.add_argument("--window", type=int, default=CANDIDATE_WINDOW,
                   help="candidate window per retriever; retune against the gold set")
    ap.add_argument("--mode", choices=("hybrid", "vector"), default="hybrid",
                    help="hybrid (default) or vector-only comparison")
    ap.add_argument("--transport", choices=["auto", "pg", "https"], default="auto",
                    help="auto tries 5432 first, then falls back to 443/HTTPS (default)")
    ap.add_argument("--check-transport", action="store_true",
                    help="compare 5432 and 443/HTTPS results; both transports must be reachable")
    a = ap.parse_args()
    dsn = resolve_dsn(a.dsn)

    kinds = [k.strip().upper() for k in a.kind.split(",")] if a.kind else None
    if kinds:
        bad = set(kinds) - set(TYPE_VOCAB)
        if bad:
            sys.exit(f"Unknown type: {', '.join(sorted(bad))}")
    keys = [s.strip() for s in a.section_key.split(",")] if a.section_key else None
    if keys:
        bad = set(keys) - set(ALL_SECTION_KEYS)
        if bad:
            sys.exit(f"Unknown section_key: {', '.join(sorted(bad))}")

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(a.model)
    vec = model.encode([a.query], normalize_embeddings=True)[0].tolist()

    if a.check_transport:
        check_transport(dsn, vec, a.query, a.k, a.mode, a.window)
        return

    cur, close, used = open_cursor(dsn, a.transport)
    rows = query_sections(cur, vec, a.query, a.k, a.mode, kinds, keys, window=a.window)

    if not rows:
        print("No searchable embeddings; run sync_db.py then embed_cards.py")
        close()
        return

    print(f"[{used}] Sections most relevant to '{a.query}' ({a.mode}):")
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
        print("\nCounterexample/risk sections (excluding duplicates above):")
        if counter:
            print_rows(counter, a.show_body)
            # Game-Developer-AI 쪽은 여기에 유사도 하한선을 걸어 미달이면 비운다.
            # 이 CLI 는 사람이 눈으로 보는 도구라 자르지 않고 점수를 그대로 보인다.
            print("  (Note: the pipeline does not accept cosine similarity below 0.45 as a counterexample.)")
        else:
            print('  None — report "insufficient counterexample research" in the planner output.')

    if a.expand:
        seeds = sorted({r["card_id"] for r in rows})
        cur.execute(NEIGHBOR_SQL, {"seeds": seeds, "k": a.expand})
        neighbors = cur.fetchall()
        print(f"\nNeighbor cards (one-hop card_refs; seeds: {', '.join(seeds)}):")
        if neighbors:
            for cid, title, kind in neighbors:
                print(f"  {cid}  {title}")
        else:
            print("  None")

    close()


if __name__ == "__main__":
    main()
