#!/usr/bin/env python3
"""Measure retrieval recall@k before and after a retrieval-system change.

``eval/retrieval.jsonl`` must remain identical to the consumer repository's
``Src/McpServers/evals/retrieval.jsonl``. Both repositories query the same card
database, so divergent fixtures make a retrieval regression indistinguishable
from an expectation change.

This command evaluates only ``must_retrieve``. Consumer-side evaluation owns
``counterexample_*`` expectations because it distinguishes supporting and
counterexample evidence.

Examples:
  python scripts/eval_retrieval.py
  python scripts/eval_retrieval.py --mode vector
  python scripts/eval_retrieval.py --window 40
  python scripts/eval_retrieval.py -k 6 --verbose

``must_retrieve`` accepts ``GAME-002`` for any section of a card or
``GAME-002#risk`` for one required section.
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
    """Read non-empty, non-comment JSONL cases that define must_retrieve."""
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
    """Return true when retrieval includes any expected card or section."""
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
    ap.add_argument("--verbose", action="store_true", help="Also print retrieved rows for passing queries.")
    ap.add_argument("--transport", choices=["auto", "pg", "https"], default="auto",
                    help="auto: try 5432 first, then fall back to 443/HTTPS (default)")
    a = ap.parse_args()

    cases = load_cases(BASE / a.queries)
    if not cases:
        sys.exit(f"No query with must_retrieve in {a.queries}")

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(a.model)

    cur, close, used = open_cursor(resolve_dsn(a.dsn), a.transport)
    print(f"[{used}] {len(cases)} queries")

    hits = 0
    for case in cases:
        query, expect = case["query"], case["must_retrieve"]
        vec = model.encode([query], normalize_embeddings=True)[0].tolist()
        rows = search_cards.query_sections(cur, vec, query, a.k, a.mode, window=a.window)
        ok = hit(expect, rows)
        hits += ok
        print(f"  [{'O' if ok else 'X'}] {case.get('id', '?')}  {query}  → expected {expect}")
        if not ok or a.verbose:
            for r in rows:
                print(f"        {r['card_id']}#{r['section_key']}  {r['title']}")

    close()

    n = len(cases)
    print(f"\nrecall@{a.k} ({a.mode}, window={a.window}): {hits}/{n} = {hits / n:.1%}")
    # Also expose regressions through the exit code.
    sys.exit(0 if hits == n else 1)


if __name__ == "__main__":
    main()
