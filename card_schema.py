"""card_schema.py - 카드/digest 규격의 단일 정의.

scripts/lint_card.py, tools/build_index.py, tools/sync_db.py, tools/search_cards.py가
공유한다. 값을 여기서만 바꾸면 나머지가 함께 갱신된다 (전에는 여러 곳에 각각 다른
목록이 있어 lint는 통과 못 해도 index/DB 동기화는 통과하는 카드가 나올 수 있었다).

TYPE_VOCAB은 db/00_init_all.sql의 `type_vocab` CHECK 제약과 같은 값을
유지해야 한다 (SQL 쪽은 Python 상수를 직접 참조할 수 없어 수동 동기화 필요).

## 절 제목과 section_key (2026-08-12)

절 제목은 사람이 읽는 한국어 문자열이고, `section_key`는 기계가 거는 언어 중립
식별자다. 둘을 나눈 이유:

- 검색 필터가 `WHERE section_key = 'failure_cases'`로 걸린다. 이 키가 한국어면
  오케스트레이션 프롬프트(영어 예정)와 데이터 사이에 번역 매핑이 영구히 남는다.
- 절 제목을 영어로 바꾸는 날, DISPLAY만 갈아끼우면 DB·검색기·프롬프트가 그대로 산다.
  카드 168장의 `## ` 헤더 치환과 이 사전 수정이 전부다.
- 같은 뜻의 절은 종류가 달라도 같은 키를 쓴다 (ELEM '조합 궁합' == ARCH '조합 궁합'
  == synergy). 종류를 가로지르는 절 단위 검색이 이것 때문에 가능하다.
"""

CARD_REQUIRED = ["card_id", "type", "title", "summary", "tags", "updated", "confidence"]
DIGEST_REQUIRED = ["type", "period", "sources", "status"]

TYPE_VOCAB = {
    "ELEM":  {"mechanic", "narrative-device", "tone", "tech"},
    "GAME":  {"success", "failure", "mixed"},
    "GENRE": {"genre"},
    "ARCH":  {"pattern", "structure", "convention"},
}

CONFIDENCE_VOCAB = ["high", "medium", "medium-low", "low"]

# 새로 쓰는 카드가 쓸 절 제목 언어. 'ko' | 'en'.
#
# 검사·검색은 언제나 section_key로 하므로, 이 값을 바꿔도 기존 카드는 계속 통과한다.
# 실제 소비처는 lint/check_sections의 오류 메시지뿐이다 — 새 카드의 절 제목은
# templates/*.md 가 정한다. 둘이 어긋나면 오류 메시지가 있지도 않은 제목을 요구하게
# 되므로 **templates 와 항상 같은 언어**여야 한다.
#
# 2026-08-12: 카드 165장의 절 제목·근거 표시를 영어로 옮기고(migrate_card_lang.py
# --headings) templates 4개도 함께 옮겨서 'en'으로 전환했다. 본문 산문은 아직
# 한국어이며, 그 혼재 상태는 정상이다 (SECTION_KEY가 두 언어를 모두 받는다).
CARD_LANG = "en"

# section_key -> 언어별 절 제목. 이게 절 사전의 단일 소스다.
SECTION_TITLES = {
    "definition":        {"ko": "정의",                    "en": "Definition"},
    "success_cases":     {"ko": "성공 사례",                "en": "Success Cases"},
    "failure_cases":     {"ko": "실패 사례",                "en": "Failure Cases"},
    "user_reaction":     {"ko": "유저 반응 요약",            "en": "User Reaction Summary"},
    "synergy":           {"ko": "조합 궁합",                "en": "Synergy"},
    "risk":              {"ko": "리스크",                  "en": "Risks"},

    "summary_metrics":   {"ko": "한 줄 요약 + 판매·리뷰 수치", "en": "Summary and Sales/Review Metrics"},
    "elements_used":     {"ko": "사용한 요소",               "en": "Elements Used"},
    "cause_analysis":    {"ko": "성공/실패 원인",             "en": "Success/Failure Drivers"},
    "implications":      {"ko": "우리 프로젝트 시사점",        "en": "Implications for Our Project"},

    "components":        {"ko": "구성 요소",                "en": "Components"},
    "market_saturation": {"ko": "시장 포화도",               "en": "Market Saturation"},
    "conventions":       {"ko": "관례와 기대치",             "en": "Conventions and Expectations"},
    "gaps":              {"ko": "빈칸",                    "en": "Gaps"},

    "problem":           {"ko": "문제",                    "en": "Problem"},
    "structure":         {"ko": "구조",                    "en": "Structure"},
    "rules":             {"ko": "핵심 규칙",                "en": "Core Rules"},
    "unity_procedure":   {"ko": "Unity 구현 절차",          "en": "Unity Implementation Steps"},
    "antipatterns":      {"ko": "안티패턴",                 "en": "Anti-patterns"},
    "verification":      {"ko": "검증 방법",                "en": "Verification"},
}

# 카드 종류별 필수 절 (키로 적는다 - 언어에 흔들리지 않는다).
# 목록 순서는 카드 안의 관례 순서와 맞춰 둔다.
KIND_SECTIONS = {
    "ELEM":  ["definition", "success_cases", "failure_cases", "user_reaction", "synergy", "risk"],
    "GAME":  ["summary_metrics", "elements_used", "cause_analysis", "implications"],
    "GENRE": ["components", "market_saturation", "conventions", "gaps"],
    "ARCH":  ["problem", "structure", "rules", "unity_procedure", "antipatterns",
              "verification", "synergy"],
}

ALL_SECTION_KEYS = sorted(SECTION_TITLES)

# 제목 -> 키. **두 언어를 모두 받는다** - 전환 기간에 섞여 있어도 둘 다 해석된다.
SECTION_KEY = {}
for _key, _langs in SECTION_TITLES.items():
    for _title in _langs.values():
        if SECTION_KEY.setdefault(_title, _key) != _key:
            raise ValueError(f"절 제목 '{_title}'이 두 key에 매핑됨")


def section_title(key: str, lang: str = None) -> str:
    return SECTION_TITLES[key][lang or CARD_LANG]


# 하위 호환 + 템플릿·오류 메시지용: 현재 언어의 '필수 절 제목 리스트'
REQUIRED_SECTIONS = {kind: [section_title(k) for k in keys]
                     for kind, keys in KIND_SECTIONS.items()}

# 예전 이름. (제목 -> 키) 형태를 기대하던 코드용.
SECTIONS = {kind: {section_title(k): k for k in keys}
            for kind, keys in KIND_SECTIONS.items()}

import re as _re

# 사실/해석 표시자. 카드 본문을 영어로 옮기면 이것도 같이 넘어가므로 두 언어를 다 받는다.
# lint(근거 검사)와 embed_cards(좌표 계산용 정리)가 같은 정의를 써야 어긋나지 않는다.
MARKERS = {
    "source":         {"ko": "출처", "en": "source"},
    "interpretation": {"ko": "해석", "en": "interpretation"},
}
# 여는 표시만으로 판정한다 - 출처 태그는 줄바꿈을 넘나들어서 닫는 괄호를 같은
# 덩어리에서 못 볼 수 있다. lint는 '근거를 달려는 의도'가 보이면 통과시킨다.
SOURCE_OPENERS = tuple(f"[{v}" for v in MARKERS["source"].values())
INTERP_MARKS = tuple(f"[{v}]" for v in MARKERS["interpretation"].values())

SOURCE_TAG_RE = _re.compile(r"\[(?:출처|source)[^\]]*\]", _re.I)

# 카드 ID 참조. lint_card / audit_links / sync_db / migrate_card_lang 이 공유한다.
#
# 끝에 `\b`를 쓰면 안 된다. 한글 조사는 파이썬 정규식에서 단어 문자라서 "ARCH-002의",
# "ARCH-004를" 처럼 조사가 바로 붙으면 숫자와 조사 사이에 경계가 없어 매치가 통째로
# 실패한다. 이 저장소에서 그렇게 **보이지 않던 링크가 124건(카드 57장)** 있었고,
# 그만큼 card_refs 간선이 비었고 audit_links 의 간극 점검도 그 참조를 못 봤다.
# `(?!\d)` 는 ARCH-0021 을 ARCH-002 로 잘못 읽는 것만 막는다 - 조사는 통과시킨다.
CARD_ID_RE = _re.compile(r"\b(?:ELEM|GAME|GENRE|ARCH)-\d{3}(?!\d)")

_SECTION_SPLIT = _re.compile(r"^## +(.+?)[ \t]*$", _re.M)


def split_sections(body: str):
    """카드 본문을 '## ' 기준으로 절 단위로 쪼갠다.

    반환: [(ord, section_key, section_title, section_body), ...]

    사전에 없는 제목은 key를 만들 수 없으므로 건너뛴다 (lint_card.py가 이미
    '사전에 없는 절 제목'으로 잡아내므로, 여기서 조용히 추측하지 않는다).
    첫 '## ' 앞의 서두 텍스트도 버린다 - 카드 규격상 그 자리에 내용이 오면 안 된다.
    """
    out = []
    marks = list(_SECTION_SPLIT.finditer(body))
    for i, m in enumerate(marks):
        title = m.group(1).strip()
        key = SECTION_KEY.get(title)
        if key is None:
            continue
        end = marks[i + 1].start() if i + 1 < len(marks) else len(body)
        text = body[m.end():end].strip()
        if text:
            out.append((len(out), key, title, text))
    return out


# 반례·위험 신호가 사는 절. search_cards.py의 반례 조회가 이 목록을 쓴다.
#
# 예전에는 반례를 `kind='GAME' AND type IN ('failure','mixed')`로만 찾았다. 그러면
# 성공 카드 안에 적힌 실패 문단(GAME-031 Balatro의 PEGI 18+ 재분류 사건 등)에는
# 영원히 도달하지 못한다. 반례는 카드의 속성이 아니라 절의 속성이다.
COUNTER_SECTION_KEYS = [
    "failure_cases", "risk", "cause_analysis", "antipatterns",
    "market_saturation", "gaps",
]
