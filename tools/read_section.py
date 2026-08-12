#!/usr/bin/env python3
"""Read one named section from one or more cards.

Usage:
  python tools/read_section.py <card.md> "<section title>"
  python tools/read_section.py <card1> <card2> ... "<section title>"

The title must exactly match the schema; `lint_card.py` enforces it.
"""
import sys, re, pathlib

def extract(path, section):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    m = re.search(rf"^## {re.escape(section)}\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else None

def main():
    *files, section = sys.argv[1:]
    if not files:
        sys.exit("Usage: read_section.py <files...> \"<section title>\"")
    for f in files:
        got = extract(f, section)
        name = pathlib.Path(f).stem
        if got is None:
            print(f"[{name}] (section '## {section}' not found — check the title with lint)")
        else:
            print(f"[{name}] ## {section}\n{got}\n")

if __name__ == "__main__":
    main()
