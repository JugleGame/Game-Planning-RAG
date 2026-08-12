"""apply_patch.py의 사전 검증 게이트를 stdlib만으로 검사한다."""

import json
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "apply_patch.py"
CARD = '''+++
card_id = "ELEM-999"
type = "mechanic"
title = "Test"
summary = "Test"
tags = ["test"]
updated = "2026-01-01"
confidence = "low"
+++
## Definition
Original.

## Risks
Original risk.
'''


def run(patch, cards):
    patch_file = cards.parent / "patch.json"
    patch_file.write_text(json.dumps({"patches": patch}), encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(patch_file), "--cards-dir", str(cards)],
        capture_output=True,
        text=True,
    )


def main():
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        cards = root / "research" / "elements"
        cards.mkdir(parents=True)
        card = cards / "999_test.md"
        card.write_text(CARD, encoding="utf-8")

        invalid = [
            {"card_id": "ELEM-999", "section": "Definition", "action": "append", "text": "Valid."},
            {"card_id": "ELEM-999", "section": "Missing", "action": "append", "text": "Invalid."},
        ]
        result = run(invalid, cards.parent)
        assert result.returncode == 1, result.stdout + result.stderr
        assert card.read_text(encoding="utf-8") == CARD, "검증 실패 뒤 파일이 일부 변경됨"

        valid = [
            {"card_id": "ELEM-999", "section": "Definition", "action": "append", "text": "Added."}
        ]
        result = run(valid, cards.parent)
        assert result.returncode == 0, result.stdout + result.stderr
        assert "Original.\nAdded." in card.read_text(encoding="utf-8")

    print("[PASS] apply_patch 사전 검증과 적용")


if __name__ == "__main__":
    main()
