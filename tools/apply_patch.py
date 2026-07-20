#!/usr/bin/env python3
"""apply_patch.py - U(갱신) 공정의 patch 제안을 카드에 적용 (섹션 단위, 전체 재작성 금지)
사용법: python scripts/apply_patch.py patch.json --cards-dir . [--digest digests/2026-07-14.md]
patch.json 형식: {"patches":[{"card_id","section","action"(append|replace),"text","reason"}]}
적용 전 사람이 patch.json을 눈으로 승인했다는 전제. updated 필드 자동 갱신.
"""
import sys, re, json, argparse, pathlib, datetime

def find_card(cards_dir, card_id):
    for p in pathlib.Path(cards_dir).rglob("*.md"):
        head = p.read_text(encoding="utf-8")[:300]
        if f"card_id: {card_id}" in head or f"card_id : {card_id}" in head:
            return p
    return None

def apply_one(path, section, action, text):
    src = path.read_text(encoding="utf-8")
    pat = re.compile(rf"(^## {re.escape(section)}.*?$)(.*?)(?=^## |\Z)", re.S | re.M)
    m = pat.search(src)
    if not m: return None, f"섹션 '## {section}' 없음"
    body = m.group(2).rstrip()
    new_body = (body + "\n" + text + "\n") if action == "append" else ("\n" + text + "\n")
    src = src[:m.start(2)] + new_body + src[m.end(2):]
    src = re.sub(r"^updated\s*:.*$", f"updated: {datetime.date.today().isoformat()}",
                 src, count=1, flags=re.M)
    path.write_text(src, encoding="utf-8")
    return True, "ok"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("patch_file"); ap.add_argument("--cards-dir", default=".")
    ap.add_argument("--digest", default=None)
    a = ap.parse_args()
    patches = json.loads(pathlib.Path(a.patch_file).read_text(encoding="utf-8"))["patches"]
    for p in patches:
        card = find_card(a.cards_dir, p["card_id"])
        if not card:
            print(f"[SKIP] {p['card_id']} 카드 파일을 못 찾음"); continue
        ok, msg = apply_one(card, p["section"], p["action"], p["text"])
        print(f"[{'OK' if ok else 'FAIL'}] {p['card_id']} / ## {p['section']} / {p['action']} - {msg}")
    if a.digest:  # 다이제스트 처리 상태 자동 갱신 (파이프라인 완료 표시)
        d = pathlib.Path(a.digest); s = d.read_text(encoding="utf-8")
        s = re.sub(r"^status\s*:.*$", f"status: 반영({datetime.date.today().isoformat()})",
                   s, count=1, flags=re.M)
        d.write_text(s, encoding="utf-8"); print(f"[OK] {d.name} status -> 반영")

if __name__ == "__main__": main()
