#!/usr/bin/env python3
"""migrate_card_lang.py - 카드를 한국어에서 영어로 옮긴다 (검증 게이트 포함).

## 왜 스크립트인가

번역 자체는 LLM이 한다. 이 스크립트가 하는 일은 **번역이 카드의 사실 자산을
훼손하지 않았음을 기계적으로 증명하는 것**이다. 카드의 가치는 문장이 아니라
[출처]가 붙은 수치와 카드 사이의 ID 링크에 있고, 그 둘은 번역에서 가장 잘 깨진다.

번역 결과가 아래를 하나라도 어기면 그 카드는 **쓰지 않는다**:

  1. 수치 유실 없음     원문의 지표가 번역본에 같은 **값**으로 남아 있는가
  2. 수치 환각 없음     원문에 없던 큰 수가 번역본에 생기지 않았는가
  3. 카드 ID 집합 동일  ELEM-021 같은 참조가 하나도 늘거나 줄지 않았는가
  4. 출처 태그 수 동일  [출처: ...] 개수가 같은가 - 근거가 슬쩍 사라지지 않았는가
  5. 해석 표시 수 동일  [해석] 개수가 같은가 - 사실과 해석의 경계가 유지됐는가
  6. 절 구성 동일       section_key 목록이 순서까지 같은가
  7. frontmatter 동일   card_id/type/tags/updated/confidence/링크 배열이 그대로인가
                        (title/summary만 번역 대상)
  8. 실제로 영어가 됐음 절 제목·근거 표시·본문이 번역됐는가 (1~7은 '아무것도 잃지
                        않았음'만 증명한다 - 원문을 그대로 돌려줘도 전부 통과한다)

수치는 **글자가 아니라 값**으로 본다. "500만" -> "5,000,000" 은 올바른 번역인데
토큰 대조로는 불일치라서, 예전 게이트는 한국어 단위 수치를 가진 카드 113장을
무조건 떨어뜨렸다. `test_migrate_gate.py` 가 이 불변식들을 못박아 둔다.

## 두 단계로 나눈다

절 제목(21종)과 `[출처]`/`[해석]` 표시는 고정 문자열이다. 이건 `--headings` 로
결정론적으로 끝내고, LLM 에는 산문만 맡긴다 - 실패할 수 있는 일을 굳이 실패할 수
있게 만들 이유가 없다.

## 안전 장치

- 원본을 덮어쓰지 않는다. 결과는 --out 디렉터리에 쓰고, 사람이 확인한 뒤
  `--apply`로 옮긴다.
- 실패한 카드는 보고서에 사유와 함께 남고 출력되지 않는다.
- 카드 한 장씩 독립이므로 중간에 멈춰도 안전하다. 섞여 있는 상태는 정상이다
  (lint_card.py가 두 언어 절 제목을 모두 받는다).

## 사용법

  # 1단계 - 기계 표면 (번역기 불필요, 2026-08-12 완료)
  # signals/ 는 제외한다. 신호 파일은 **추가 전용·수정 금지**다 (README 3곳에 명시).
  python scripts/migrate_card_lang.py --headings \
      research/architecture/*.md research/elements/*.md \
      research/games/*.md research/genres/*.md templates/*.md

  # 2단계 - 산문
  export ANTHROPIC_API_KEY=...
  python scripts/migrate_card_lang.py research/games/031_balatro.md --out draft/en
  python scripts/migrate_card_lang.py research/games/*.md --out draft/en
  python scripts/migrate_card_lang.py --out draft/en --apply      # 검증 통과분 반영

  # 남이 직접 번역한 카드를 검사만
  python scripts/migrate_card_lang.py --verify research/games/*.md

마지막에 반드시:
  python scripts/lint_card.py research/*/*.md --index research/_index.md
  python scripts/check_sections.py
  python tools/build_index.py && python tools/sync_db.py && python tools/embed_cards.py
"""
import argparse
import pathlib
import re
import shutil
import sys

BASE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE))
from card_schema import (CARD_ID_RE as ID_PAT, SECTION_KEY, SECTION_TITLES,
                         SOURCE_TAG_RE, MARKERS, split_sections)

FM_PAT = re.compile(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)$", re.S)
INTERP_ANY = re.compile(r"\[(?:해석|interpretation)\]", re.I)
HANGUL = re.compile(r"[가-힣]")

# 수치는 **글자**가 아니라 **값**으로 비교한다.
#
# 예전에는 lint_card.py의 METRIC 정규식이 잡은 토큰 문자열을 그대로 대조했다.
# 그러면 "500만" -> "5,000,000" 이 서로 다른 토큰이라 번역이 올바를수록 게이트가
# 떨어뜨린다. 실제로 카드 171장 중 113장이 한국어 단위 수치를 갖고 있어 무조건
# 실패했다. 우리가 지키려는 불변식은 "같은 글자"가 아니라 "같은 양"이다.
MULT = {"천": 1_000, "만": 10_000, "억": 100_000_000, "천억": 100_000_000_000}
NUM_RE = re.compile(r"(\d[\d,]*(?:\.\d+)?)\s*(천억|억|만|천)?(%?)")


def values(text):
    """텍스트의 모든 수를 (값, 퍼센트여부) 집합으로 정규화한다.

    500만 == 5,000,000 == 5000000. 콤마와 한국어 단위를 한 토큰으로 먹으므로
    "1,000만"(=1천만)도 1000이 아니라 10,000,000으로 읽는다.
    """
    out = set()
    for digits, unit, pct in NUM_RE.findall(text):
        v = float(digits.replace(",", ""))
        if unit:
            v *= MULT[unit]
        out.add((v, bool(pct)))
    return out


def significant(vals, floor):
    """번역에서 사라지거나 새로 생기면 안 되는 수만 남긴다.

    floor 미만의 정수는 버린다. "1인 개발" -> "solo development", "5개 부문" ->
    "5 categories" 처럼 세는 수는 번역에서 자연히 사라지거나 남으므로 대조 대상이
    아니다. 퍼센트와 소수는 크기와 무관하게 지표이므로 항상 남긴다 (3.5%, 1.5배).
    """
    return {(v, p) for v, p in vals if p or v >= floor or v != int(v)}


# 원문에 있던 지표는 번역본 어딘가에 반드시 다시 나타나야 한다 (유실 검사).
LOSS_FLOOR = 10
# 번역본에 새로 생긴 큰 수는 원문에 없으면 환각이다 (날조 검사). 날짜·개수와
# 섞이지 않도록 유실 검사보다 문턱을 높게 잡는다.
INVENT_FLOOR = 1000

# 번역돼야 하는 frontmatter 필드. 나머지는 글자 그대로 보존한다.
TRANSLATE_FIELDS = ("title", "summary")

PROMPT = """You are migrating a Korean game-design research card to English.

This card is retrieval data for a RAG system. Its value is in cited figures and
cross-card links, not in prose. Translate faithfully; do not improve, summarize,
condense, or add anything.

Hard rules — a violation makes the output unusable:

1. Every figure must survive with the same VALUE, written in plain digits.
   Expand Korean magnitude units into digits with thousands separators:
     500만 장   -> 5,000,000 units
     60만 달러  -> $600,000
     1,000만    -> 10,000,000
     3.5억      -> 350,000,000
   NEVER use the words "million" / "billion" / "k" for a figure — write the
   digits. "5 million units" is REJECTED; "5,000,000 units" is accepted.
   Percentages and decimals keep their exact value (12.5% stays 12.5%).
2. Never add, drop, or renumber a card ID (ELEM-021, GAME-031, GENRE-013, ARCH-015).
3. Keep every `[출처: ...]` tag, one for one, translated to `[source: ...]`.
   Publication names, dates and the phrase structure stay. "2024 기준" ->
   "as of 2024", "2026-07 확인" -> "verified 2026-07".
4. Keep every `[해석]` marker, one for one, as `[interpretation]`. This marks the
   boundary between fact and inference and must not move.
5. Keep HTML comments (<!-- ... -->) as comments, translated.
6. Keep the section order exactly. Use these section headings verbatim:
{heading_map}
7. Keep markdown structure: bullets stay bullets, line breaks inside a paragraph
   may be re-wrapped but paragraph boundaries stay.

Game titles, studio names, and platform names keep their official English form.

Return ONLY the finished card: the `+++` frontmatter block then the body.
In frontmatter translate ONLY `title` and `summary`; copy every other line
character for character.

--- CARD ---
{card}
"""


def load(path):
    raw = path.read_text(encoding="utf-8")
    m = FM_PAT.match(raw)
    if not m:
        raise ValueError("frontmatter(+++ 블록) 없음")
    return m.group(1), m.group(2)


def fingerprint(fm_raw, body):
    """번역 전후로 같아야 하는 것들."""
    fm_fields = {}
    for line in fm_raw.splitlines():
        k, _, v = line.partition("=")
        k = k.strip()
        if k and k not in TRANSLATE_FIELDS:
            fm_fields[k] = v.strip()
    clean = ID_PAT.sub("", body)
    sections = split_sections(body)
    return {
        "values": values(clean),
        "ids": sorted(ID_PAT.findall(body)),
        "sources": len(SOURCE_TAG_RE.findall(body)),
        "interps": len(INTERP_ANY.findall(body)),
        "sections": [k for _, k, _, _ in sections],
        "titles": [t for _, _, t, _ in sections],
        "ko_markers": len(re.findall(r"\[출처|\[해석\]", body)),
        "hangul": len(HANGUL.findall(body)),
        "chars": max(len(body), 1),
        "fm": fm_fields,
    }


def show(vals, n=5):
    return sorted(f"{v:,.10g}{'%' if p else ''}" for v, p in vals)[:n]


def diff(before, after, expect_en=False):
    """어긋난 항목만 사람이 읽을 수 있게.

    수치는 방향을 나눠 본다. 원문의 지표는 번역본에 **남아 있어야** 하고(유실),
    번역본의 큰 수는 원문에 **있어야** 한다(날조). 양쪽을 같은 집합으로 맞추라고
    요구하면 "5개 부문 -> 5 categories" 같은 무해한 차이까지 실패로 잡힌다.
    """
    out = []
    lost = significant(before["values"], LOSS_FLOOR) - after["values"]
    if lost:
        out.append(f"원문 수치가 번역본에서 사라짐: {show(lost)}")
    invented = significant(after["values"], INVENT_FLOOR) - before["values"]
    if invented:
        out.append(f"원문에 없는 수치가 번역본에 생김: {show(invented)}")
    if before["ids"] != after["ids"]:
        out.append(f"카드 ID 불일치 - 전 {before['ids']} / 후 {after['ids']}")
    if before["sources"] != after["sources"]:
        out.append(f"출처 태그 수 {before['sources']} -> {after['sources']}")
    if before["interps"] != after["interps"]:
        out.append(f"[해석] 표시 수 {before['interps']} -> {after['interps']}")
    if before["sections"] != after["sections"]:
        out.append(f"절 구성 {before['sections']} -> {after['sections']}")
    for k, v in before["fm"].items():
        if after["fm"].get(k) != v:
            out.append(f"frontmatter '{k}' 변경: {v!r} -> {after['fm'].get(k)!r}")
    for k in after["fm"]:
        if k not in before["fm"]:
            out.append(f"frontmatter에 없던 키 추가: '{k}'")
    if expect_en:
        out += english_gaps(after)
    return out


def english_gaps(after):
    """번역이 실제로 일어났는지 본다.

    위의 불변식 검사는 '무엇도 잃지 않았음'만 증명한다. 모델이 원문을 그대로
    돌려줘도 전부 통과한다 - 그래서 '영어가 됐는가'를 따로 물어야 한다.
    """
    out = []
    wrong = [t for t, k in zip(after["titles"], after["sections"])
             if t != SECTION_TITLES[k]["en"]]
    if wrong:
        out.append(f"절 제목이 아직 영어가 아님: {wrong[:3]}")
    if after["ko_markers"]:
        out.append(f"[출처/해석] 표시가 {after['ko_markers']}개 한국어로 남음 "
                   "([source: ...] / [interpretation])")
    ratio = after["hangul"] / after["chars"]
    if ratio > 0.02:
        out.append(f"본문이 아직 한국어 (한글 비중 {ratio:.0%}) - 번역되지 않았다")
    return out


def heading_map_for(body):
    """이 카드에 실제로 있는 절만, ko -> en 매핑으로."""
    lines = []
    for _, key, title, _ in split_sections(body):
        lines.append(f"   ## {title}  ->  ## {SECTION_TITLES[key]['en']}")
    return "\n".join(lines)


def translate(card_text, body, model):
    import anthropic
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=model,
        max_tokens=8000,
        messages=[{"role": "user",
                   "content": PROMPT.format(card=card_text,
                                            heading_map=heading_map_for(body))}],
    )
    text = "".join(b.text for b in msg.content if b.type == "text").strip()
    # 모델이 코드펜스로 감싸는 경우 벗긴다
    if text.startswith("```"):
        text = re.sub(r"^```[a-z]*\n|\n```$", "", text)
    return text.strip() + "\n"


def process(path, outdir, model):
    fm_raw, body = load(path)
    before = fingerprint(fm_raw, body)
    if not before["sections"]:
        return None, ["표준 절을 찾지 못함 - check_sections.py 먼저"]

    translated = translate(path.read_text(encoding="utf-8"), body, model)
    m = FM_PAT.match(translated)
    if not m:
        return None, ["번역 결과에 frontmatter가 없음"]
    after = fingerprint(m.group(1), m.group(2))

    problems = diff(before, after, expect_en=True)
    if problems:
        return None, problems

    dest = outdir / path.relative_to(BASE / "research")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(translated, encoding="utf-8")
    return dest, []


def convert_headings(paths):
    """절 제목과 [출처]/[해석] 표시만 영어로 바꾼다 - 번역기 없이, 제자리에서.

    카드에서 기계가 읽는 표면(절 제목 21종, 근거 표시 2종)은 고정된 문자열
    치환이다. 이것을 LLM에 맡기면 실패할 수 있는 일을 굳이 실패할 수 있게 만드는
    것이다. 여기서 결정론적으로 끝내면 LLM 은 산문만 책임지면 된다.

    원문 대비 불변식(수치·ID·절 구성·frontmatter)을 그 자리에서 재검사한다.
    되돌리려면 git 이 있다.
    """
    ko2en = {t["ko"]: t["en"] for t in SECTION_TITLES.values()}
    head_re = re.compile(r"^## +(" + "|".join(map(re.escape, ko2en)) + r")[ \t]*$", re.M)

    changed, failed, skipped = [], [], []
    for p in paths:
        path = pathlib.Path(p).resolve()
        raw = path.read_text(encoding="utf-8")
        m = FM_PAT.match(raw)
        if not m:
            failed.append((path.name, ["frontmatter 없음"]))
            continue
        fm_raw, body = m.group(1), m.group(2)
        # 다이제스트(신호 파일)는 **추가 전용·수정 금지**다 (README 3곳에 명시).
        # 호출자의 glob에 맡기지 않고 여기서 막는다 - research/*/*.md 한 번이면
        # 걸려든다.
        if re.search(r'^type\s*=\s*"digest"', fm_raw, re.M):
            skipped.append(path.name)
            continue
        before = fingerprint(fm_raw, body)

        # 본문만 건드린다. frontmatter 는 title/summary 외에는 글자 그대로 보존해야
        # 하는데, 주석에 '[해석]' 같은 표시가 섞여 있는 카드가 실제로 있다.
        new_body = head_re.sub(lambda x: "## " + ko2en[x.group(1)], body)
        new_body = new_body.replace("[출처", "[source").replace("[해석]", "[interpretation]")
        if new_body == body:
            continue

        problems = diff(before, fingerprint(fm_raw, new_body))
        if problems:
            failed.append((path.name, problems))
            print(f"[FAIL] {path.name}")
            for pr in problems:
                print("   -", pr)
            continue
        path.write_text(f"+++\n{fm_raw}\n+++\n{new_body}", encoding="utf-8")
        changed.append(path.name)

    print(f"절 제목·근거 표시 영어화: {len(changed)}장 변경 / {len(failed)}장 실패"
          + (f" / 다이제스트 {len(skipped)}장 건너뜀(추가 전용)" if skipped else ""))
    if changed:
        print("다음: python scripts/check_sections.py && "
              "python scripts/lint_card.py research/*/*.md --index research/_index.md")
    return failed


def verify_against_head(paths, expect_en=True):
    """이미 번역된 카드를 git HEAD 판본과 대조한다 (번역기 없이 검사만).

    ``--out`` 흐름은 이 스크립트가 번역까지 하지만, 사람이나 에이전트가 직접
    번역해 파일을 갈아끼운 경우에도 **같은 게이트를 통과해야 한다.** 그때 원본은
    git 이 갖고 있으므로 HEAD 판본과 비교하면 된다 - 별도 사본을 만들 필요가 없다.

    번역기를 부르지 않으므로 ANTHROPIC_API_KEY 가 필요 없다.
    """
    import subprocess

    ok, failed = [], []
    for p in paths:
        path = pathlib.Path(p).resolve()
        rel = path.relative_to(BASE).as_posix()
        try:
            raw = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=BASE,
                                 capture_output=True, check=True).stdout.decode("utf-8")
        except subprocess.CalledProcessError:
            failed.append((rel, ["HEAD 에 없는 파일 - 새 카드는 이 검사 대상이 아니다"]))
            continue

        m = FM_PAT.match(raw)
        if not m:
            failed.append((rel, ["HEAD 판본에 frontmatter 가 없음"]))
            continue
        before = fingerprint(m.group(1), m.group(2))

        m2 = FM_PAT.match(path.read_text(encoding="utf-8"))
        if not m2:
            failed.append((rel, ["현재 파일에 frontmatter 가 없음"]))
            continue
        after = fingerprint(m2.group(1), m2.group(2))

        problems = diff(before, after, expect_en=expect_en)
        if problems:
            failed.append((rel, problems))
            print(f"[FAIL] {rel}")
            for pr in problems:
                print("   -", pr)
        else:
            ok.append(rel)
            print(f"[PASS] {rel}")

    print(f"\n통과 {len(ok)}장 / 실패 {len(failed)}장")
    return failed


def apply(outdir):
    """검증을 통과해 outdir에 쌓인 것을 research/ 원위치로 옮긴다."""
    n = 0
    for src in sorted(outdir.rglob("*.md")):
        dest = BASE / "research" / src.relative_to(outdir)
        shutil.copyfile(src, dest)
        n += 1
    print(f"{n}장 반영 완료 -> research/")
    print("다음: python scripts/lint_card.py research/*/*.md --index research/_index.md")
    print("      python scripts/check_sections.py")
    print("      python tools/build_index.py && python tools/sync_db.py && python tools/embed_cards.py")
    print("반영 후 전체 --verify와 M단계까지 완료할 것")
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cards", nargs="*", help="번역할 카드 경로 (생략하고 --apply만도 가능)")
    ap.add_argument("--out", default="draft/en", help="검증 통과분을 쌓을 디렉터리")
    ap.add_argument("--model", default="claude-opus-5")
    ap.add_argument("--apply", action="store_true", help="--out의 내용을 research/에 반영")
    ap.add_argument("--verify", action="store_true",
                    help="번역기를 부르지 않고, 이미 바뀐 카드를 git HEAD 판본과 대조만 한다")
    ap.add_argument("--headings", action="store_true",
                    help="번역기 없이 절 제목과 [출처]/[해석] 표시만 제자리에서 영어로 바꾼다")
    ap.add_argument("--allow-korean-prose", action="store_true",
                    help="--verify 에서 '아직 영어가 아님' 검사를 끈다 (제목만 바꾼 중간 상태 점검용)")
    a = ap.parse_args()

    if a.headings:
        if not a.cards:
            sys.exit("바꿀 카드 경로를 지정할 것 (예: --headings research/*/*.md)")
        sys.exit(1 if convert_headings(a.cards) else 0)

    if a.verify:
        if not a.cards:
            sys.exit("검사할 카드 경로를 지정할 것 (예: --verify research/games/*.md)")
        sys.exit(1 if verify_against_head(a.cards, not a.allow_korean_prose) else 0)

    outdir = BASE / a.out
    if a.apply and not a.cards:
        if not outdir.exists():
            sys.exit(f"{outdir} 가 없음 - 먼저 번역할 것")
        apply(outdir)
        return
    if not a.cards:
        sys.exit("번역할 카드를 지정하거나 --apply 를 쓸 것")

    outdir.mkdir(parents=True, exist_ok=True)
    ok, failed = [], []
    for p in a.cards:
        path = pathlib.Path(p).resolve()
        try:
            dest, problems = process(path, outdir, a.model)
        except Exception as e:
            dest, problems = None, [f"{type(e).__name__}: {e}"]
        if dest:
            ok.append(path.name)
            print(f"[PASS] {path.name}")
        else:
            failed.append((path.name, problems))
            print(f"[FAIL] {path.name}")
            for pr in problems:
                print("   -", pr)

    print(f"\n통과 {len(ok)}장 / 실패 {len(failed)}장 -> {outdir}")
    if ok:
        print(f"내용을 확인한 뒤: python scripts/migrate_card_lang.py --out {a.out} --apply")
    if failed:
        print("실패한 카드는 손대지 않았다. 원문 그대로 남아 있다.")
        sys.exit(1)


if __name__ == "__main__":
    main()
