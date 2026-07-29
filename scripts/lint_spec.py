#!/usr/bin/env python3
"""lint_spec.py — 기획 AI가 발행한 spec 카드 검사기 (lint.py와 같은 철학)
검사 항목:
  S1 TOML frontmatter(+++) 존재/파싱
  S2 필수 키: spec_id, version, blueprint_version, refs
  S3 refs가 _index.md에 존재하는 카드인지
  S4 필수 섹션: 목표/구현 범위/제외 범위/합격 기준
  S5 합격 기준 각 줄: 금지어 없음 + (숫자 또는 관찰 키워드) 포함
"""
import sys, re, json, tomllib, pathlib

# 한국어 로케일 Windows 콘솔은 cp949 라서 아래 PASS/FAIL 기호를 인코딩하지 못하고
# 결과를 한 줄도 보여주기 전에 죽는다.
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

INDEX = pathlib.Path(__file__).resolve().parent.parent / "research" / "_index.md"

# 규칙은 여기 적지 않는다 — Game-Developer-AI 의 strategic/specs.py 가 같은 판정을
# 내야 하는데, 저장소가 달라 임포트로 공유할 수 없다. 그래서 데이터로 공유하고
# 두 사본이 같은지는 저쪽의 tests/test_spec_rules_sync.py 가 본다.
RULES_PATH = pathlib.Path(__file__).resolve().parent / "spec_rules.json"
RULES = json.loads(RULES_PATH.read_text(encoding="utf-8"))

REQUIRED_KEYS = RULES["requiredKeys"]
REQUIRED_SECTIONS = RULES["requiredSections"]
BANNED = RULES["bannedWords"]
OBSERVABLE = RULES["observableWords"]
CARD_ID_RE = re.compile(RULES["cardIdPattern"])

def known_ids():
    """_index.md 에 실재하는 카드 ID 집합."""
    return set(CARD_ID_RE.findall(INDEX.read_text(encoding="utf-8")))

def lint(path: pathlib.Path):
    errs = []
    text = path.read_text(encoding="utf-8")
    m = re.match(r"\+\+\+\n(.*?)\n\+\+\+\n(.*)", text, re.S)
    if not m:
        return ["S1: +++ frontmatter 없음"]
    try:
        meta = tomllib.loads(m.group(1))
    except tomllib.TOMLDecodeError as e:
        return [f"S1: TOML 파싱 실패 — {e}"]
    body = m.group(2)

    for k in REQUIRED_KEYS:
        if k not in meta:
            errs.append(f"S2: 필수 키 누락 — {k}")

    # specs.py::lint_spec 의 S3 와 같은 순서로 본다 — 형식이 먼저, 실재가 다음.
    # (예전에는 _index.md 원문에 대한 부분 문자열 검사라 형식이 깨진 ref 도
    #  우연히 통과할 수 있었고, 두 검사기의 판정이 갈렸다.)
    index_ids = known_ids()
    for ref in meta.get("refs", []):
        if not CARD_ID_RE.fullmatch(ref):
            errs.append(f"S3: 카드 ID 형식이 아님 — {ref}")
        elif ref not in index_ids:
            errs.append(f"S3: 존재하지 않는 카드 인용 — {ref}")

    for sec in REQUIRED_SECTIONS:
        if f"## {sec}" not in body:
            errs.append(f"S4: 필수 섹션 누락 — {sec}")

    crit = re.search(r"## 합격 기준\n(.*?)(\n## |\Z)", body, re.S)
    if crit:
        for line in [l.strip("- ").strip() for l in crit.group(1).splitlines() if l.strip().startswith("-")]:
            for b in BANNED:
                if b in line:
                    errs.append(f"S5: 측정 불가 표현 '{b}' — \"{line}\"")
            if not (re.search(r"\d", line) or any(o in line for o in OBSERVABLE)):
                errs.append(f"S5: 숫자/관찰 키워드 없음 — \"{line}\"")
    return errs

if __name__ == "__main__":
    ok = True
    for p in sorted(pathlib.Path(sys.argv[1]).glob("spec-*.md")):
        errs = lint(p)
        print(f"\n[{p.name}] {'PASS ✅' if not errs else 'FAIL ❌ (' + str(len(errs)) + '건)'}")
        for e in errs:
            print("  -", e)
        ok = ok and not errs
    sys.exit(0 if ok else 1)
