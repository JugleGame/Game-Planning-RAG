#!/usr/bin/env python3
"""migrate_card_lang.py - 카드를 한국어에서 영어로 옮긴다 (검증 게이트 포함).

## 왜 스크립트인가

번역 자체는 LLM이 한다. 이 스크립트가 하는 일은 **번역이 카드의 사실 자산을
훼손하지 않았음을 기계적으로 증명하는 것**이다. 카드의 가치는 문장이 아니라
[출처]가 붙은 수치와 카드 사이의 ID 링크에 있고, 그 둘은 번역에서 가장 잘 깨진다.

번역 결과가 아래를 하나라도 어기면 그 카드는 **쓰지 않는다**:

  1. 수치 집합 동일     lint_card.py의 METRIC 정규식이 잡는 모든 숫자가 그대로 있는가
                        (500만 장, 60만 달러, 3+/18+ 등급 …)
  2. 카드 ID 집합 동일  ELEM-021 같은 참조가 하나도 늘거나 줄지 않았는가
  3. 출처 태그 수 동일  [출처: ...] 개수가 같은가 - 근거가 슬쩍 사라지지 않았는가
  4. 해석 표시 수 동일  [해석] 개수가 같은가 - 사실과 해석의 경계가 유지됐는가
  5. 절 구성 동일       section_key 목록이 순서까지 같은가
  6. frontmatter 동일   card_id/type/tags/updated/confidence/링크 배열이 그대로인가
                        (title/summary만 번역 대상)

## 안전 장치

- 원본을 덮어쓰지 않는다. 결과는 --out 디렉터리에 쓰고, 사람이 확인한 뒤
  `--apply`로 옮긴다.
- 실패한 카드는 보고서에 사유와 함께 남고 출력되지 않는다.
- 카드 한 장씩 독립이므로 중간에 멈춰도 안전하다. 섞여 있는 상태는 정상이다
  (lint_card.py가 두 언어 절 제목을 모두 받는다).

## 사용법

  export ANTHROPIC_API_KEY=...
  python scripts/migrate_card_lang.py research/games/031_balatro.md --out draft/en
  python scripts/migrate_card_lang.py research/games/*.md --out draft/en
  python scripts/migrate_card_lang.py --out draft/en --apply      # 검증 통과분 반영

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
from card_schema import (SECTION_KEY, SECTION_TITLES, SOURCE_TAG_RE, MARKERS,
                         split_sections)

FM_PAT = re.compile(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)$", re.S)
ID_PAT = re.compile(r"\b(?:ELEM|GAME|GENRE|ARCH)-\d{3}\b")
# lint_card.py의 METRIC과 같은 정의여야 한다 - 다르면 lint가 통과시킨 수치를
# 여기서 놓치거나 그 반대가 된다.
METRIC = re.compile(r"\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?%|\d+(?:만|천억|억|천)\b|\d{4,}|\d{2,}(?:점|장|건|fps)")
INTERP_ANY = re.compile(r"\[(?:해석|interpretation)\]", re.I)

# 번역돼야 하는 frontmatter 필드. 나머지는 글자 그대로 보존한다.
TRANSLATE_FIELDS = ("title", "summary")

PROMPT = """You are migrating a Korean game-design research card to English.

This card is retrieval data for a RAG system. Its value is in cited figures and
cross-card links, not in prose. Translate faithfully; do not improve, summarize,
condense, or add anything.

Hard rules — a violation makes the output unusable:

1. Every number must survive byte-identically in the same order. Korean numeral
   units are figures too: "500만 장" -> "5 million units" is WRONG because it
   loses the token "500만". Write "500만" figures as the same digits with the
   unit spelled out only if the digits stay: prefer "5,000,000 units" ONLY when
   the source wrote digits. When the source wrote a Korean unit like 만/억,
   render the same magnitude in plain digits with commas (500만 -> 5,000,000).
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
    return {
        "numbers": sorted(METRIC.findall(ID_PAT.sub("", body))),
        "ids": sorted(ID_PAT.findall(body)),
        "sources": len(SOURCE_TAG_RE.findall(body)),
        "interps": len(INTERP_ANY.findall(body)),
        "sections": [k for _, k, _, _ in split_sections(body)],
        "fm": fm_fields,
    }


def diff(before, after):
    """어긋난 항목만 사람이 읽을 수 있게."""
    out = []
    if before["numbers"] != after["numbers"]:
        lost = [n for n in before["numbers"] if n not in after["numbers"]]
        added = [n for n in after["numbers"] if n not in before["numbers"]]
        out.append(f"수치 불일치 - 사라짐 {lost[:5]} / 새로 생김 {added[:5]}")
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

    problems = diff(before, after)
    if problems:
        return None, problems

    dest = outdir / path.relative_to(BASE / "research")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(translated, encoding="utf-8")
    return dest, []


def verify_against_head(paths):
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

        problems = diff(before, after)
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
    print("전부 옮겼다면 card_schema.py의 CARD_LANG을 'en'으로 바꿀 것 "
          "(새로 쓰는 카드가 영어 절 제목을 쓰게 된다)")
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cards", nargs="*", help="번역할 카드 경로 (생략하고 --apply만도 가능)")
    ap.add_argument("--out", default="draft/en", help="검증 통과분을 쌓을 디렉터리")
    ap.add_argument("--model", default="claude-opus-5")
    ap.add_argument("--apply", action="store_true", help="--out의 내용을 research/에 반영")
    ap.add_argument("--verify", action="store_true",
                    help="번역기를 부르지 않고, 이미 바뀐 카드를 git HEAD 판본과 대조만 한다")
    a = ap.parse_args()

    if a.verify:
        if not a.cards:
            sys.exit("검사할 카드 경로를 지정할 것 (예: --verify research/games/*.md)")
        sys.exit(1 if verify_against_head(a.cards) else 0)

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
