# tools/build_index.py
"""Build a compact cover index and per-type detail indexes.

Keep IDs and recent changes in `_index.md`; put title, summary, and tags in per-type indexes.
This limits normal agent context while preserving a complete ID registry for validators.
At larger scale, use `tools/search_cards.py` instead of reading a full type index.
"""
import glob, os, sys, tomllib, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH = os.path.join(BASE, "research")

sys.path.insert(0, BASE)
from card_schema import CARD_REQUIRED, DIGEST_REQUIRED

order = {"element": "Elements", "genre": "Genres", "game": "Games", "signal": "Signals", "arch": "Architecture"}

# Map card-ID prefixes to categories; split on '-' because prefix lengths vary.
PREFIX_MAP = {
    "ELEM": "element",
    "GENRE": "genre",
    "GAME": "game",
    "SIGNAL": "signal",
    "ARCH": "arch",
}

def parse_date(v):
    if isinstance(v, datetime.date): return v
    return datetime.date.fromisoformat(str(v).strip())

def classify(meta):
    """Classify by card-ID prefix, falling back to type == 'digest' for signals."""
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
    # Files beginning with '_' are operational documents, not cards.
    if os.path.basename(path).startswith("_"): continue
    try:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        if not raw.startswith("+++"):
            errors.append((path, "frontmatter missing")); continue
        meta = tomllib.loads(raw.split("+++", 2)[1])

        cat = classify(meta)
        if cat is None:
            errors.append((path, f"cannot classify card_id/type (card_id={meta.get('card_id')}, type={meta.get('type')})"))
            continue

        if cat == "signal":
            for key in DIGEST_REQUIRED:
                if key not in meta: raise KeyError(f"signal required key missing: {key}")
            if "period_end" not in meta:  # Build-index-only field used for the update date.
                raise KeyError("signal required key missing: period_end")
            # Signals lack card_id/title/summary, so synthesize English routing metadata.
            # Do not copy historical source lists into indexes: they are on-demand data,
            # not normal agent context, and may remain in the original language.
            fname = os.path.splitext(os.path.basename(path))[0]
            meta["card_id"] = meta.get("card_id") or f"SIGNAL-{fname}"
            meta["title"] = meta.get("title") or f"Weekly observations ({meta.get('period_at', meta['period_end'])} to {meta['period_end']})"
            meta["summary"] = meta.get("summary") or "Append-only weekly source digest; open only when needed."
            meta["updated"] = parse_date(meta["period_end"])
        else:
            for key in CARD_REQUIRED:
                if key not in meta: raise KeyError(f"required key missing: {key}")
            meta["updated"] = parse_date(meta["updated"])

        meta["type"] = cat  # order 딕셔너리와 매칭되도록 정규화된 카테고리로 덮어씀
        cards.append(meta)
    except Exception as e:
        errors.append((path, f"{type(e).__name__}: {e}"))

today = datetime.date.today()


def write(name, lines):
    with open(os.path.join(RESEARCH, name), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return os.path.getsize(os.path.join(RESEARCH, name))


# --- Per-type detail indexes -------------------------------------------------
written = {}
for t, label in order.items():
    group = sorted([c for c in cards if c["type"] == t], key=lambda c: c["card_id"])
    lines = [f"# {label} Index (generated — do not edit)",
             f"Generated: {today} | {len(group)} entries\n"]
    for c in group:
        tags = " ".join(f"#{x}" for x in c.get("tags", []))
        lines.append(f"- {c['card_id']} | {c['title']} | {c['summary']} | {tags} | {c['updated']:%m-%d}")
    written[t] = (len(group), write(f"_index_{t}.md", lines))

# --- Cover index -------------------------------------------------------------
out = ["# RESEARCH INDEX (generated — do not edit)",
       f"Generated: {today} | {len(cards)} entries\n",
       "Open only one relevant type index for details."]
for t, label in order.items():
    n, size = written[t]
    out.append(f"- {label}: `research/_index_{t}.md` ({n} entries, {size:,}B)")
out.append("\nFor semantic lookup, use `python tools/search_cards.py \"<query>\"` instead of reading an entire index.")

recent = [c for c in cards if (today - c["updated"]).days <= 7]
if recent:
    out.append("\n## Changes in the last 7 days")
    out += [f"- {c['card_id']} | {c['title']} | {c['updated']:%m-%d}"
            for c in sorted(recent, key=lambda c: c["updated"], reverse=True)]

# Full ID registry used by lint_card.py and audit_links.py.
out.append("\n## Registered IDs (validator lookup)")
for t, label in order.items():
    ids = sorted(c["card_id"] for c in cards if c["type"] == t)
    if ids:
        out.append(f"- {label}: " + " ".join(ids))

cover = write("_index.md", out)

print(f"_index.md updated: {len(cards)} entries (cover {cover:,}B)")
for t, label in order.items():
    n, size = written[t]
    print(f"  _index_{t}.md  {n:>4} entries  {size:>8,}B")
if errors:
    print(f"\n⚠ skipped files: {len(errors)}", file=sys.stderr)
    for p, msg in errors:
        print(f"  - {os.path.relpath(p, BASE)}: {msg}", file=sys.stderr)
    sys.exit(1)
