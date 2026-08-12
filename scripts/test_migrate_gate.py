#!/usr/bin/env python3
"""번역 검증 게이트 자체를 검사한다.  python scripts/test_migrate_gate.py

게이트가 틀리면 두 방향으로 조용히 망가진다: 올바른 번역을 떨어뜨리거나(작업이
멈춘다), 사실이 훼손된 번역을 통과시킨다(카드가 거짓말을 한다). 후자가 훨씬
비싸므로 통과/실패 양쪽을 다 못박아 둔다.
"""
import pathlib
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "scripts"))
sys.path.insert(0, str(BASE))
from migrate_card_lang import diff, fingerprint, significant, values, LOSS_FLOOR
from card_schema import CARD_ID_RE

FM_KO = 'card_id = "GAME-999"\ntype = "success"\ntitle = "테스트"\nsummary = "요약"\ntags = ["t"]\nupdated = "2026-08-12"\nconfidence = "medium"'
FM_EN = FM_KO.replace('"테스트"', '"Test"').replace('"요약"', '"Summary"')


def card(fm, body):
    return fingerprint(fm, body)


def check(name, problems, want_pass):
    got_pass = not problems
    mark = "OK " if got_pass == want_pass else "FAIL"
    print(f"[{mark}] {name}" + ("" if got_pass == want_pass else f"  <- {problems}"))
    return got_pass == want_pass


def main():
    ok = []

    # --- 정규화: 값이 같으면 표기가 달라도 같다 (113장을 막던 결함) ---
    assert values("500만")  == values("5,000,000") == values("5000000")
    assert values("1,000만") == values("10,000,000"), "콤마+단위를 한 토큰으로 먹어야 한다"
    assert values("3.5억") == values("350,000,000")
    assert values("60만 달러") == values("$600,000")
    print("[OK ] 수치 정규화: 500만 == 5,000,000, 1,000만 == 10,000,000")

    # 세는 수는 대조 대상이 아니다 ("1인 개발" -> "solo development")
    assert significant(values("1인"), LOSS_FLOOR) == set()
    assert significant(values("5개 부문"), LOSS_FLOOR) == set()
    # 지표는 크기와 무관하게 남는다
    assert significant(values("3.5%"), LOSS_FLOOR), "퍼센트는 작아도 지표다"
    assert significant(values("90점"), LOSS_FLOOR), "두 자리 이상은 지표다"
    print("[OK ] 세는 수는 무시, 퍼센트·소수·두자리는 지표로 유지")

    # --- 카드 ID: 한글 조사가 붙어도 잡아야 한다 ---
    # 끝에 `\b`를 쓰면 조사(의/를/…)가 단어 문자라서 매치가 통째로 실패한다.
    # 이 저장소에서 그렇게 안 보이던 참조가 124건 있었다 (card_refs 간선 누락).
    assert CARD_ID_RE.findall("ARCH-002의 씬 파일명") == ["ARCH-002"]
    assert CARD_ID_RE.findall("저장 규격은 ARCH-004를 따른다") == ["ARCH-004"]
    assert CARD_ID_RE.findall("ELEM-021(친숙한 규칙)과 GAME-031") == ["ELEM-021", "GAME-031"]
    assert CARD_ID_RE.findall("ARCH-002's scene filename") == ["ARCH-002"]
    # 네 자리로 늘어난 ID를 세 자리로 잘라 읽으면 안 된다
    assert CARD_ID_RE.findall("ARCH-0021") == []
    print("[OK ] 카드 ID: 조사가 붙어도 잡고(ARCH-002의), ARCH-0021 은 오독하지 않음")

    KO = ("## 한 줄 요약 + 판매·리뷰 수치\n500만 장을 팔았고 매출 60만 달러, "
          "환불률 3.5% [출처: GameSpot, 2024 기준]\n1인 개발이다. [해석] 좋다.\n"
          "## 사용한 요소\nELEM-021 을 썼다 [출처: PCGamesN, 2024 기준]\n")
    EN = ("## Summary and Sales/Review Metrics\nSold 5,000,000 units with $600,000 "
          "in revenue and a 3.5% refund rate [source: GameSpot, as of 2024]\n"
          "Solo development. [interpretation] Good.\n"
          "## Elements Used\nUsed ELEM-021 [source: PCGamesN, as of 2024]\n")

    # --- 통과해야 하는 것 ---
    ok.append(check("올바른 번역은 통과한다",
                    diff(card(FM_KO, KO), card(FM_EN, EN), expect_en=True), True))

    # --- 떨어져야 하는 것 ---
    cases = [
        ("수치 유실 (500만 장이 사라짐)", EN.replace("5,000,000 units", "many units")),
        ("수치 환각 (없던 7,200,000)",   EN.replace("$600,000", "$7,200,000")),
        ("퍼센트 변조 (3.5% -> 3.9%)",   EN.replace("3.5%", "3.9%")),
        ("출처 태그 유실",               EN.replace(" [source: PCGamesN, as of 2024]", "")),
        ("[해석] 표시 유실",             EN.replace("[interpretation] ", "")),
        ("카드 ID 유실 (ELEM-021)",      EN.replace("ELEM-021", "that element")),
        ("절 하나가 통째로 사라짐",       EN.split("## Elements Used")[0]),
    ]
    for name, broken in cases:
        ok.append(check(name, diff(card(FM_KO, KO), card(FM_EN, broken),
                                   expect_en=True), False))

    # 번역기가 원문을 그대로 돌려준 경우 - 불변식은 전부 통과하므로 여기서만 잡힌다
    ok.append(check("번역 안 된 원문 그대로 반환(pass-through)",
                    diff(card(FM_KO, KO), card(FM_KO, KO), expect_en=True), False))
    # 같은 입력이라도 불변식만 볼 때는 통과해야 한다 (--headings 중간 상태)
    ok.append(check("불변식만 볼 때 한국어 원문은 통과 (--headings 중간 상태)",
                    diff(card(FM_KO, KO), card(FM_KO, KO), expect_en=False), True))
    # frontmatter 는 title/summary 외에 손대면 안 된다
    ok.append(check("frontmatter confidence 변조",
                    diff(card(FM_KO, KO),
                         card(FM_EN.replace('"medium"', '"high"'), EN),
                         expect_en=True), False))

    print(f"\n{sum(ok)}/{len(ok)} 통과")
    sys.exit(0 if all(ok) else 1)


if __name__ == "__main__":
    main()
