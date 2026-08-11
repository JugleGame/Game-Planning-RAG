#!/usr/bin/env python3
"""check_sections.py - 절 청킹이 저장소 전체에서 성립하는지 확인한다 (DB 불필요).

sync_db.py가 카드를 절로 쪼개 DB에 넣기 전에, 그 분할이 실제 카드 168장에서
빠짐없이 동작하는지 여기서 먼저 깨진다. 실패하면 DB에 '절이 하나도 없는 카드'가
조용히 들어가는 대신 여기서 멈춘다.

사용법:
  python scripts/check_sections.py
종료코드: 0=통과, 1=실패
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
        assert len(set(keys)) == len(keys), f"{kind}: 필수 절 key 중복"
        for k in keys:
            assert k in SECTION_TITLES, f"{kind}: 사전에 없는 key {k}"

    # 두 언어 제목이 같은 key로 해석돼야 한다 (전환 기간에 섞여 있어도 동작)
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
            problems.append(f"{rel}: 표준 절을 하나도 못 찾음")
            continue
        keys = [k for _, k, _, _ in secs]
        if len(keys) != len(set(keys)):
            problems.append(f"{rel}: 절 중복 {[k for k in keys if keys.count(k) > 1]}")
        missing = [section_title(k) for k in KIND_SECTIONS.get(kind, []) if k not in keys]
        if missing:
            problems.append(f"{rel}: 필수 절 누락 {missing}")
        empty = [k for _, k, _, b in secs if not b.strip()]
        if empty:
            problems.append(f"{rel}: 빈 절 {empty}")

    return total_cards, total_sections, problems


def main():
    unit_checks()
    n_cards, n_sections, problems = repo_checks()
    if problems:
        print(f"[FAIL] 카드 {n_cards}장 중 {len(problems)}건 문제")
        for p in problems:
            print("   -", p)
        sys.exit(1)
    avg = n_sections / n_cards if n_cards else 0
    print(f"[PASS] 카드 {n_cards}장 → 절 {n_sections}개 (카드당 평균 {avg:.1f})")


if __name__ == "__main__":
    main()
