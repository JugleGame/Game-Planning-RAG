#!/usr/bin/env python3
"""read_section.py - 카드/프롬프트에서 필요한 절만 잘라 읽는다 (부분 읽기).
사용법:
  python read_section.py <파일.md> "<절 제목>"          # 예: "조합 궁합"
  python read_section.py <파일1> <파일2> ... "<절 제목>"  # 여러 카드에서 같은 절만
전제: 절 제목이 표준 사전과 글자까지 일치 (lint의 check_sections가 보장)
"""
import sys, re, pathlib

def extract(path, section):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(section)}\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else None

def main():
    *files, section = sys.argv[1:]
    if not files:
        sys.exit("사용법: read_section.py <파일...> \"<절 제목>\"")
    for f in files:
        got = extract(f, section)
        name = pathlib.Path(f).stem
        if got is None:
            print(f"[{name}] (절 '## {section}' 없음 - lint로 제목 확인 필요)")
        else:
            print(f"[{name}] ## {section}\n{got}\n")

if __name__ == "__main__":
    main()
