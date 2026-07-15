# build_index.py  (pip install pyyaml)
import glob, yaml, datetime

cards = []
for path in glob.glob("research/**/*.md", recursive=True):
    if path.endswith("INDEX.md"): continue
    raw = open(path, encoding="utf-8").read()
    if not raw.startswith("---"): continue
    meta = yaml.safe_load(raw.split("---")[1])
    cards.append(meta)

order = {"element": "① 요소", "genre": "② 장르", "game": "③ 게임", "signal": "④ 신호"}
out = [f"# RESEARCH INDEX (자동 생성 - 직접 수정 금지)",
       f"생성: {datetime.date.today()} | 카드 {len(cards)}장\n"]

recent = [c for c in cards if (datetime.date.today() - c["updated"]).days <= 7]
if recent:
    out.append("## 최근 7일 변경")
    out += [f"- {c['card_id']} | {c['title']} | {c['summary']} | {c['updated']:%m-%d}" for c in recent]

for t, label in order.items():
    out.append(f"\n## {label}")
    for c in sorted([c for c in cards if c["type"] == t], key=lambda c: c["card_id"]):
        tags = " ".join(f"#{x}" for x in c.get("tags", []))
        out.append(f"- {c['card_id']} | {c['title']} | {c['summary']} | {tags} | {c['updated']:%m-%d}")

open("research/INDEX.md", "w", encoding="utf-8").write("\n".join(out))
print(f"INDEX.md 갱신 완료: {len(cards)}장")