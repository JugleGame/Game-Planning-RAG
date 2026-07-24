#!/usr/bin/env python3
"""lint_spec.py — 기획 AI가 발행한 spec 카드 검사기 (lint.py와 같은 철학)
검사 항목:
  S1 TOML frontmatter(+++) 존재/파싱
  S2 필수 키: spec_id, version, blueprint_version, refs
  S3 refs가 _index.md에 존재하는 카드인지
  S4 필수 섹션: 목표/구현 범위/제외 범위/합격 기준
  S5 합격 기준 각 줄: 금지어 없음 + (숫자 또는 관찰 키워드) 포함
"""
import sys, re, tomllib, pathlib

INDEX = pathlib.Path(__file__).resolve().parent.parent / "research" / "_index.md"
REQUIRED_KEYS = ["spec_id", "version", "blueprint_version", "refs"]
REQUIRED_SECTIONS = ["목표", "구현 범위", "제외 범위", "합격 기준"]
BANNED = ["재미", "좋은", "좋아", "멋진", "자연스러", "적절", "재치"]
OBSERVABLE = ["로그", "콘솔", "테스트", "씬", "파일", "커밋", "초", "개", "프레임", "%"]

def known_ids():
    return set(re.findall(r"(ELEM|GENRE|GAME)-\d{3}", INDEX.read_text(encoding="utf-8")))

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

    ids = {f"{t}-{n}" for t, n in re.findall(r"(ELEM|GENRE|GAME)-(\d{3})", " ".join(meta.get("refs", [])))}
    # known_ids()는 (접두어) 튜플만 주므로 원문에서 직접 대조
    index_text = INDEX.read_text(encoding="utf-8")
    for ref in meta.get("refs", []):
        if ref not in index_text:
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
