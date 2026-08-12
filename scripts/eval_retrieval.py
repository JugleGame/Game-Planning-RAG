#!/usr/bin/env python3
"""eval_retrieval.py - 회수 품질(recall@k)을 잰다. 검색기를 바꾸기 전후로 돌린다.

이게 없으면 "모델을 바꿨더니 좋아진 것 같다"밖에 말할 수 없다. 2026-07-29 의
하이브리드 실측이 코드에 남지 않아 이번 개편(모델·청크 단위 교체)의 전후 비교가
불가능했던 것이 이 파일이 생긴 이유다.

## 골드셋은 쌍둥이다

``eval/retrieval.jsonl`` 은 Game-Develop-Orchestration 의
``Src/McpServers/evals/retrieval.jsonl`` 과 **같은 파일이어야 한다.**
두 저장소가 같은 카드 DB를 보고 같은 질의로 회수 품질을 재기 때문이다 —
한쪽만 고치면 "여기선 통과하는데 저기선 떨어지는" 상태가 되고, 그때 원인이
검색기인지 기대값인지 알 수 없게 된다. (``spec_rules.json`` 과 같은 규율이다.)

기대값은 소비 측 기준으로 적혀 있다. 이 스크립트는 그중 ``must_retrieve`` 만
본다 — 반례 관련 기대(``counterexample_*``)는 지지/반례를 나눠 뽑는 소비 측
파이프라인의 개념이고, 이 CLI 는 그 분리를 하지 않는다. 반례 품질은 저쪽
``run_evals.py retrieval`` 로 잰다.

사용법:
  python scripts/eval_retrieval.py                    # 현재 설정으로
  python scripts/eval_retrieval.py --mode vector      # 벡터 단독과 비교
  python scripts/eval_retrieval.py --window 40        # 후보 창 튜닝
  python scripts/eval_retrieval.py -k 6 --verbose     # 실패한 질의의 회수 결과

expect 표기 (``must_retrieve``):
  "GAME-002"           그 카드의 어느 절이든 맞으면 정답
  "GAME-002#risk"      그 절이어야 정답
"""
import argparse
import json
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "tools"))
sys.path.insert(0, str(BASE))
from _db import open_cursor, resolve_dsn
import search_cards


def load_cases(path: pathlib.Path):
    """jsonl 에서 질의를 읽는다. '#' 주석 줄과 빈 줄은 건너뛴다."""
    cases = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        case = json.loads(line)
        if case.get("must_retrieve"):
            cases.append(case)
    return cases


def hit(expect, rows):
    """회수 결과 안에 기대 항목이 하나라도 있으면 True."""
    got_cards = {r["card_id"] for r in rows}
    got_sections = {f"{r['card_id']}#{r['section_key']}" for r in rows}
    return any((e in got_sections) if "#" in e else (e in got_cards) for e in expect)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queries", default="eval/retrieval.jsonl")
    ap.add_argument("--dsn", default=None)
    ap.add_argument("--model", default="BAAI/bge-m3")
    ap.add_argument("-k", type=int, default=6)
    ap.add_argument("--window", type=int, default=search_cards.CANDIDATE_WINDOW)
    ap.add_argument("--mode", choices=("hybrid", "vector"), default="hybrid")
    ap.add_argument("--verbose", action="store_true", help="통과한 질의의 회수 결과도 표시")
    ap.add_argument("--transport", choices=["auto", "pg", "https"], default="auto",
                    help="auto=5432 먼저 시도 후 실패 시 443/HTTPS 폴백 (기본값)")
    a = ap.parse_args()

    cases = load_cases(BASE / a.queries)
    if not cases:
        sys.exit(f"{a.queries} 에 must_retrieve 를 가진 질의가 없다")

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(a.model)

    cur, close, used = open_cursor(resolve_dsn(a.dsn), a.transport)
    print(f"[{used}] 질의 {len(cases)}개")

    hits = 0
    for case in cases:
        query, expect = case["query"], case["must_retrieve"]
        vec = model.encode([query], normalize_embeddings=True)[0].tolist()
        rows = search_cards.query_sections(cur, vec, query, a.k, a.mode, window=a.window)
        ok = hit(expect, rows)
        hits += ok
        print(f"  [{'O' if ok else 'X'}] {case.get('id', '?')}  {query}  → 기대 {expect}")
        if not ok or a.verbose:
            for r in rows:
                print(f"        {r['card_id']}#{r['section_key']}  {r['title']}")

    close()

    n = len(cases)
    print(f"\nrecall@{a.k} ({a.mode}, window={a.window}): {hits}/{n} = {hits / n:.1%}")
    # 회귀 감지에 쓸 수 있게 종료코드로도 알린다
    sys.exit(0 if hits == n else 1)


if __name__ == "__main__":
    main()
