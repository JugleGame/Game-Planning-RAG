#!/usr/bin/env python3
"""Preflight and apply a human-approved section-patch JSON file.

Usage:
  python scripts/apply_patch.py patch.json --cards-dir research
  python scripts/apply_patch.py patch.json --cards-dir research --digest research/signals/<file>.md

Validate every target, action, and section before writing. If any patch is invalid, write nothing.
"""

import argparse
import datetime
import json
import pathlib
import re
import sys
import tomllib

FM_TOML = re.compile(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n", re.S)


def card_id_of(text):
    match = FM_TOML.match(text)
    if not match:
        return None
    try:
        return str(tomllib.loads(match.group(1)).get("card_id", "")) or None
    except tomllib.TOMLDecodeError:
        return None


def card_paths(cards_dir):
    paths = {}
    for path in pathlib.Path(cards_dir).rglob("*.md"):
        card_id = card_id_of(path.read_text(encoding="utf-8"))
        if card_id:
            if card_id in paths:
                raise ValueError(f"duplicate card_id: {card_id}")
            paths[card_id] = path
    return paths


def bump_field(source, field, value):
    updated, count = re.subn(
        rf'(?m)^({re.escape(field)}\s*=\s*)".*?"',
        rf'\g<1>"{value}"',
        source,
        count=1,
    )
    if not count:
        raise ValueError(f"frontmatter field missing: {field}")
    return updated


def render_patch(source, patch):
    missing = [key for key in ("card_id", "section", "action", "text") if key not in patch]
    if missing:
        raise ValueError(f"required keys missing: {', '.join(missing)}")
    if patch["action"] not in {"append", "replace"}:
        raise ValueError(f"unsupported action: {patch['action']}")
    if not isinstance(patch["text"], str) or not patch["text"].strip():
        raise ValueError("text is empty")

    pattern = re.compile(
        rf"(^## {re.escape(str(patch['section']))}.*?$)(.*?)(?=^## |\Z)",
        re.S | re.M,
    )
    match = pattern.search(source)
    if not match:
        raise ValueError(f"section not found: ## {patch['section']}")

    old_body = match.group(2).rstrip()
    tail = "\n\n" if match.end(2) < len(source) else "\n"
    if patch["action"] == "append":
        new_body = old_body + "\n" + patch["text"].strip() + tail
    else:
        new_body = "\n" + patch["text"].strip() + tail

    rendered = source[:match.start(2)] + new_body + source[match.end(2):]
    return bump_field(rendered, "updated", datetime.date.today().isoformat())


def load_patches(path):
    payload = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    patches = payload.get("patches") if isinstance(payload, dict) else None
    if not isinstance(patches, list):
        raise ValueError("top-level patches array is required")
    return patches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("patch_file")
    parser.add_argument("--cards-dir", default="research")
    parser.add_argument("--digest")
    args = parser.parse_args()

    try:
        patches = load_patches(args.patch_file)
        paths = card_paths(args.cards_dir)
        rendered = {}

        for index, patch in enumerate(patches, start=1):
            if not isinstance(patch, dict):
                raise ValueError(f"patch #{index}: expected an object")
            card_id = patch.get("card_id")
            path = paths.get(card_id)
            if path is None:
                raise ValueError(f"patch #{index}: card not found: {card_id}")
            source = rendered.get(path, path.read_text(encoding="utf-8"))
            try:
                rendered[path] = render_patch(source, patch)
            except ValueError as error:
                raise ValueError(f"patch #{index} ({card_id}): {error}") from error

        digest_path = pathlib.Path(args.digest) if args.digest else None
        digest_source = None
        if digest_path:
            digest_source = bump_field(
                digest_path.read_text(encoding="utf-8"),
                "status",
                f"반영({datetime.date.today().isoformat()})",
            )
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"[FAIL] preflight failed — no changes written: {error}", file=sys.stderr)
        return 1

    for path, source in rendered.items():
        path.write_text(source, encoding="utf-8")
        print(f"[OK] {path.as_posix()}")
    if digest_path and digest_source is not None:
        digest_path.write_text(digest_source, encoding="utf-8")
        print(f"[OK] updated status in {digest_path.as_posix()}")
    if not rendered and not digest_path:
        print("[OK] no patches to apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
