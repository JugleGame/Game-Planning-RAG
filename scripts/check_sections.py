#!/usr/bin/env python3
"""Verify that every card splits into schema-recognized sections without using the DB.

Run this before sync_db.py. It stops a card with no recognized sections from silently entering
the database mirror.

Usage:
  python scripts/check_sections.py
Exit status: 0=pass, 1=fail
"""
import pathlib
import re
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
from card_schema import (SECTION_TITLES, SECTION_KEY, KIND_SECTIONS, section_title,
                         split_sections)

FM_PAT = re.compile(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)$", re.S)


def unit_checks():
    """사전 자체의 무결성 + 분할 함수의 동작."""
    for kind, keys in KIND_SECTIONS.items():
        assert len(set(keys)) == len(keys), f"{kind}: duplicate required section key"
        for k in keys:
            assert k in SECTION_TITLES, f"{kind}: section key absent from schema: {k}"

    # 과거 한국어 제목과 현재 영어 제목은 같은 key로 해석돼야 한다.
    for key, langs in SECTION_TITLES.items():
        for title in langs.values():
            assert SECTION_KEY[title] == key, f"{title} -> {SECTION_KEY[title]} != {key}"
    assert SECTION_KEY["실패 사례"] == SECTION_KEY["Failure Cases"] == "failure_cases"

    body = "## 정의\n첫 절.\n\n## 리스크\n둘째 절.\n여러 줄.\n"
    got = split_sections(body)
    assert [(o, k) for o, k, _, _ in got] == [(0, "definition"), (1, "risk")], got
    assert got[1][3] == "둘째 절.\n여러 줄.", repr(got[1][3])

    # 사전에 없는 제목은 조용히 버린다 (lint_card.py가 따로 잡는다)
    assert split_sections("## 없는절\n내용\n") == []
    # 빈 절은 행을 만들지 않는다
    assert split_sections("## 정의\n\n## 리스크\n내용\n") == [(0, "risk", "리스크", "내용")]
    # 제목 뒤 공백이 있어도 잘라낸다
    assert split_sections("## 정의  \n내용\n")[0][1] == "definition"


def repo_checks():
    """실제 카드 전부가 절로 쪼개지는가."""
    problems = []
    total_cards = total_sections = 0
    for path in sorted((BASE / "research").rglob("*.md")):
        if path.name.startswith("_"):
            continue
        m = FM_PAT.match(path.read_text(encoding="utf-8"))
        if not m:
            continue
        fm_raw, body = m.group(1), m.group(2)
        cid_m = re.search(r'card_id\s*=\s*"([^"]+)"', fm_raw)
        if not cid_m:
            continue                                    # digest(신호)는 절 대상 아님
        cid = cid_m.group(1)
        kind = cid.split("-")[0]
        total_cards += 1

        secs = split_sections(body)
        total_sections += len(secs)
        rel = path.relative_to(BASE).as_posix()

        if not secs:
            problems.append(f"{rel}: no schema-recognized sections found")
            continue
        keys = [k for _, k, _, _ in secs]
        if len(keys) != len(set(keys)):
            problems.append(f"{rel}: duplicate sections {[k for k in keys if keys.count(k) > 1]}")
        missing = [section_title(k) for k in KIND_SECTIONS.get(kind, []) if k not in keys]
        if missing:
            problems.append(f"{rel}: missing required sections {missing}")
        empty = [k for _, k, _, b in secs if not b.strip()]
        if empty:
            problems.append(f"{rel}: empty sections {empty}")

    return total_cards, total_sections, problems


def main():
    unit_checks()
    n_cards, n_sections, problems = repo_checks()
    if problems:
        print(f"[FAIL] {len(problems)} problems across {n_cards} cards")
        for p in problems:
            print("   -", p)
        sys.exit(1)
    avg = n_sections / n_cards if n_cards else 0
    print(f"[PASS] {n_cards} cards → {n_sections} sections (average {avg:.1f} per card)")


if __name__ == "__main__":
    main()
