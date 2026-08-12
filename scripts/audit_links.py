#!/usr/bin/env python3
"""Find one-sided links and other referential gaps between RAG cards.

New cards normally add outbound links, but existing cards still need explicit
backlinks. This complements ``lint_card.py``: lint validates one card's schema;
this command validates cross-card relationships.

Examples:
  python scripts/audit_links.py
  python scripts/audit_links.py --for GAME-042
  python scripts/audit_links.py --json
  python scripts/audit_links.py --only backlink_missing,orphan

Exit code: 0 = no relevant gaps; 1 = gap found (usable in CI/hooks).
HTML comments are excluded from reference detection, so deliberate comparison or
exclusion notes do not become false link findings.
"""
import re, json, argparse, pathlib, sys, tomllib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from card_schema import CARD_ID_RE as ID_PAT
FM_PAT = re.compile(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)$", re.S)
COMMENT_PAT = re.compile(r"<!--.*?-->", re.S)

CHECKS = ["broken_ref", "missing_card", "backlink_missing", "genre_example_missing",
          "genre_anchor_missing", "fm_body_drift", "orphan"]

# hard = mechanically certain gap (causes exit code 1 by default)
# soft = signal requiring judgment; a card may deliberately compare or exclude it.
HARD = {"broken_ref", "missing_card", "backlink_missing", "genre_example_missing"}

# Default remediation guidance, shared by people and prompts/5_linker.md.
FIX = {
    "backlink_missing":      ("Success Cases", "Add one line naming the game. Cite metrics from the GAME card as [source: GAME-### card]."),
    "genre_example_missing": (None, "Add the counterpart ID to the frontmatter example_games / genres array (not the body)."),
    "genre_anchor_missing":  ("Synergy", "Add: 'Genre anchor: GENRE-### (title) — this cluster names this element as a component.'"),
    "fm_body_drift":         (None, "Add it to frontmatter elements when the body describes actual use; move comparison/exclusion mentions into a comment."),
    "orphan":                ("Synergy", "Find an adjacent card that should reference this card and add the reverse-direction link there."),
    "broken_ref":            (None, "Correct an ID typo; if the target was deleted, remove the ID and replace it with prose."),
    "missing_card":          (None, "Check whether the generated index is stale, then rerun tools/build_index.py."),
}


def load_cards(root):
    """Load card frontmatter, body, and references; digests supply refs only."""
    cards, digests = {}, {}
    for f in sorted(pathlib.Path(root).rglob("*.md")):
        if f.name.startswith("_"):
            continue
        text = f.read_text(encoding="utf-8")
        m = FM_PAT.match(text)
        if not m:
            continue
        try:
            fm = tomllib.loads(m.group(1))
        except tomllib.TOMLDecodeError:
            print(f"[warning] skipped after TOML parse failure: {f}", file=sys.stderr)
            continue
        body = m.group(2)
        visible = COMMENT_PAT.sub("", body)          # 주석 밖에서만 '언급'으로 인정
        rec = {
            "path": f.as_posix(),
            "elements": list(fm.get("elements") or []),
            "genres": list(fm.get("genres") or []),
            "examples": list(fm.get("example_games") or []),
            "refs": set(ID_PAT.findall(visible)),
            "all_refs": set(ID_PAT.findall(body)),
        }
        if str(fm.get("type", "")).strip() == "digest":
            digests[f.as_posix()] = rec
        else:
            cards[str(fm.get("card_id", ""))] = rec
    return cards, digests


def index_ids(index_path):
    p = pathlib.Path(index_path)
    return set(ID_PAT.findall(p.read_text(encoding="utf-8"))) if p.exists() else set()


def audit(cards, digests, idx_ids):
    """Return gaps, each targeting the card that requires a change."""
    out = []

    def add(kind, card, other, detail):
        section, how = FIX[kind]
        out.append({"kind": kind, "severity": "hard" if kind in HARD else "soft",
                    "card": card, "other": other, "detail": detail,
                    "path": cards.get(card, {}).get("path"), "section": section, "how": how})

    known = set(cards)

    # 1) 깨진 참조 / 인덱스 불일치
    for cid, c in list(cards.items()) + [(f"(digest) {k}", v) for k, v in digests.items()]:
        linked = c["all_refs"] | set(c["elements"]) | set(c["genres"]) | set(c["examples"])
        for r in sorted(linked):
            if r == cid:
                continue
            if r not in known:
                add("broken_ref", cid, r, f"{r} card does not exist")
            elif idx_ids and r not in idx_ids:
                add("broken_ref", cid, r, f"{r} is absent from _index.md (rerun build_index.py)")
    for rid in sorted(idx_ids - known):
        add("missing_card", rid, None, "listed in _index.md but card file is missing")

    # 2) GAME → ELEM 역링크
    for cid, c in cards.items():
        if not cid.startswith("GAME"):
            continue
        for e in c["elements"]:
            if e in cards and cid not in cards[e]["refs"]:
                add("backlink_missing", e, cid, f"{cid} names {e} as an element, but {e} does not mention {cid}")

    # 3) GAME.genres ↔ GENRE.example_games (양방향)
    for cid, c in cards.items():
        if cid.startswith("GAME"):
            for g in c["genres"]:
                if g in cards and cid not in cards[g]["examples"]:
                    add("genre_example_missing", g, cid, f"{cid}.genres contains {g}, but {g}.example_games lacks {cid}")
        elif cid.startswith("GENRE"):
            for g in c["examples"]:
                if g in cards and cid not in cards[g]["genres"]:
                    add("genre_example_missing", g, cid, f"{cid}.example_games contains {g}, but {g}.genres lacks {cid}")

    # 4) GENRE → ELEM 장르 앵커
    for cid, c in cards.items():
        if not cid.startswith("GENRE"):
            continue
        for e in c["elements"]:
            if e in cards and cid not in cards[e]["refs"]:
                add("genre_anchor_missing", e, cid, f"{cid} names {e} as a component, but {e} does not mention {cid}")

    # 5) 본문 ↔ frontmatter 어긋남 (주석 밖 언급만)
    for cid, c in cards.items():
        if not cid.startswith("GAME"):
            continue
        drift = sorted(r for r in c["refs"] if r.startswith("ELEM") and r not in c["elements"])
        if drift:
            add("fm_body_drift", cid, ",".join(drift), f"body mentions {', '.join(drift)}, but frontmatter elements={c['elements']}")

    # 6) 고아 카드
    inbound = {i: 0 for i in cards}
    for cid, c in list(cards.items()) + list(digests.items()):
        for r in c["all_refs"] | set(c["elements"]) | set(c["genres"]) | set(c["examples"]):
            if r in inbound and r != cid:
                inbound[r] += 1
    for cid, n in sorted(inbound.items()):
        if n == 0:
            add("orphan", cid, None, "no card references this card; retrieval cannot reach it")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cards-dir", default="research")
    ap.add_argument("--index", default="research/_index.md")
    ap.add_argument("--for", dest="focus", default=None,
                    help="Only gaps involving this card (for example, GAME-042); use after adding a card.")
    ap.add_argument("--only", default=None, help=f"Limit checks (comma-separated): {','.join(CHECKS)}")
    ap.add_argument("--json", action="store_true", help="Machine-readable output for prompts/5_linker.md")
    ap.add_argument("--strict", action="store_true",
                    help="Include soft findings (genre anchors, body drift, orphans) in exit code 1.")
    a = ap.parse_args()

    cards, digests = load_cards(a.cards_dir)
    findings = audit(cards, digests, index_ids(a.index))

    if a.only:
        keep = {s.strip() for s in a.only.split(",")}
        bad = keep - set(CHECKS)
        if bad:
            sys.exit(f"Unknown check name: {', '.join(sorted(bad))}")
        findings = [f for f in findings if f["kind"] in keep]
    if a.focus:
        fid = a.focus.upper()
        if fid not in cards:
            sys.exit(f"Card not found: {fid}")
        findings = [f for f in findings if fid in (f["card"], f["other"]) or (f["other"] or "").find(fid) >= 0]

    hard_n = sum(1 for f in findings if f["severity"] == "hard")
    fail = bool(findings) if a.strict else bool(hard_n)

    if a.json:
        print(json.dumps({"total": len(findings), "hard": hard_n, "focus": a.focus,
                          "findings": findings}, ensure_ascii=False, indent=2))
        sys.exit(1 if fail else 0)

    scope = f" (focus: {a.focus})" if a.focus else ""
    if not findings:
        print(f"[clean] no one-sided links across {len(cards)} cards{scope}")
        sys.exit(0)

    print(f"[gaps: {len(findings)} / hard: {hard_n}] audited {len(cards)} cards{scope}\n")
    for kind in CHECKS:
        group = [f for f in findings if f["kind"] == kind]
        if not group:
            continue
        section, how = FIX[kind]
        where = f"in '## {section}', " if section else ""
        mark = "hard" if kind in HARD else "review"
        print(f"── [{mark}] {kind} ({len(group)}) → in the target card, {where}{how}")
        for f in group:
            print(f"   {f['card']:<10} {f['detail']}")
        print()
    if hard_n < len(findings):
        print("'review' findings may be deliberate comparisons or exclusions; inspect the card body before editing.\n")
    print("Next: provide this output to prompts/5_linker.md to produce patch.json, then obtain human approval before running:")
    print("  python scripts/apply_patch.py patch.json --cards-dir research")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
