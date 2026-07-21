# tools/build_index.py
import glob, os, sys, tomllib, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH = os.path.join(BASE, "research")

order = {"element": "① 요소", "genre": "② 장르", "game": "③ 게임", "signal": "④ 신호"}

# card_id 접두어 → 카테고리. 접두어 길이가 제각각이므로 '-' 기준 분리로 매칭
PREFIX_MAP = {
    "ELEM": "element",
    "GENRE": "genre",
    "GAME": "game",
    "SIGNAL": "signal",
}

# 카테고리별로 스키마가 다름: 카드(element/genre/game)와 signal(digest)은 필수 키가 다름
CARD_REQUIRED = ("card_id", "title", "summary", "updated")
DIGEST_REQUIRED = ("period_end", "status")

def parse_date(v):
    if isinstance(v, datetime.date): return v
    return datetime.date.fromisoformat(str(v).strip())

def classify(meta):
    """card_id 접두어 우선, 없으면 type == 'digest'로 signal 폴백 감지"""
    cid = meta.get("card_id")
    if cid:
        prefix = str(cid).split("-")[0].upper()
        cat = PREFIX_MAP.get(prefix)
        if cat:
            return cat
    if meta.get("type") == "digest":
        return "signal"
    return None

cards, errors = [], []
for path in glob.glob(os.path.join(RESEARCH, "**", "*.md"), recursive=True):
    if path.endswith("_index.md"): continue
    try:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        if not raw.startswith("+++"):
            errors.append((path, "frontmatter 없음")); continue
        meta = tomllib.loads(raw.split("+++", 2)[1])

        cat = classify(meta)
        if cat is None:
            errors.append((path, f"card_id/type으로 카테고리 판별 불가 (card_id={meta.get('card_id')}, type={meta.get('type')})"))
            continue

        if cat == "signal":
            for key in DIGEST_REQUIRED:
                if key not in meta: raise KeyError(f"signal 필수 키 누락: {key}")
            # signal은 card_id/title/summary가 없으므로 인덱스 표시용으로 합성
            fname = os.path.splitext(os.path.basename(path))[0]  # 예: 2026-07-14_steam_trend
            meta["card_id"] = meta.get("card_id") or f"SIGNAL-{fname}"
            meta["title"] = meta.get("title") or f"주간 관측 ({meta['period_at']} ~ {meta['period_end']})"
            src = ", ".join(meta.get("source", []))
            meta["summary"] = meta.get("summary") or f"[{meta['status']}] {src}"
            meta["updated"] = parse_date(meta["period_end"])
        else:
            for key in CARD_REQUIRED:
                if key not in meta: raise KeyError(f"필수 키 누락: {key}")
            meta["updated"] = parse_date(meta["updated"])

        meta["type"] = cat  # order 딕셔너리와 매칭되도록 정규화된 카테고리로 덮어씀
        cards.append(meta)
    except Exception as e:
        errors.append((path, f"{type(e).__name__}: {e}"))

today = datetime.date.today()
out = ["# RESEARCH INDEX (자동 생성 - 직접 수정 금지)",
       f"생성: {today} | 카드 {len(cards)}장\n"]

recent = [c for c in cards if (today - c["updated"]).days <= 7]
if recent:
    out.append("## 최근 7일 변경")
    out += [f"- {c['card_id']} | {c['title']} | {c['summary']} | {c['updated']:%m-%d}"
            for c in sorted(recent, key=lambda c: c["updated"], reverse=True)]

for t, label in order.items():
    out.append(f"\n## {label}")
    for c in sorted([c for c in cards if c["type"] == t], key=lambda c: c["card_id"]):
        tags = " ".join(f"#{x}" for x in c.get("tags", []))
        out.append(f"- {c['card_id']} | {c['title']} | {c['summary']} | {tags} | {c['updated']:%m-%d}")

with open(os.path.join(RESEARCH, "_index.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(out) + "\n")

print(f"_index.md 갱신 완료: {len(cards)}장")
if errors:
    print(f"\n⚠ 스킵된 파일 {len(errors)}건:", file=sys.stderr)
    for p, msg in errors:
        print(f"  - {os.path.relpath(p, BASE)}: {msg}", file=sys.stderr)
    sys.exit(1)