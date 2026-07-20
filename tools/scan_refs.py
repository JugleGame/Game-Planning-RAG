#!/usr/bin/env python3
"""scan_refs.py - 카드들이 참조하는 ID 중 '카드가 아직 없는 것'을 찾아 작업 큐를 만든다.
사용법: python tools/scan_refs.py --cards-dir . --index _index.md
출력: 카드 작성이 필요한 ID 목록 (cron/Actions에 걸어 주 1회 알림용)
"""
import re, argparse, pathlib
ID_PAT = re.compile(r"\b(?:ELEM|GAME|GENRE)-\d{3}\b")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cards-dir", default="research"); ap.add_argument("--index", default="research/_index.md")
    a = ap.parse_args()
    index = pathlib.Path(a.index).read_text(encoding="utf-8")
    referenced = set()
    for p in pathlib.Path(a.cards_dir).glob("*.md"):
        if p.name == "_index.md": continue
        referenced |= {m.group(0) for m in ID_PAT.finditer(p.read_text(encoding="utf-8"))}
    todo, unknown = [], []
    for rid in sorted(referenced):
        row = re.search(rf"^\|\s*{rid}\s*\|.*$", index, re.M)
        if not row: unknown.append(rid)
        elif "완성" not in row.group(0): todo.append(rid)
    if unknown: print("[오류] _index에 미등록:", ", ".join(unknown), "-> 예약 행부터 추가할 것")
    if todo:    print("[작업 필요] 카드 미작성:", ", ".join(todo))
    if not unknown and not todo: print("[깨끗함] 미해결 참조 없음")

if __name__ == "__main__": main()
