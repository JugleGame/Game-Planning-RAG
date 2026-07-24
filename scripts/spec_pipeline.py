#!/usr/bin/env python3
"""spec_pipeline.py - 개발 파이프라인(prompts/5,6,7: developer/planner/qa)용 실행 골격.

Unity 구현·QA 판정 자체는 사람 또는 별도 AI 세션이 수행한다(이 스크립트가 대신하지 않는다).
지금까지 이 파이프라인은 prompts/5~7 문서만 있고 이를 뒷받침하는 코드가 전혀 없었다.
이 스크립트가 메우는 구멍은 세 가지뿐이다:
  1. design/ logs/ inbox/ 폴더가 아직 없어 워크플로가 문서로만 존재하던 문제 (init)
  2. "합격 기준 통과 전 Developer에게 전달 금지"(prompts/6_planner.md §5) 규칙을
     실제로 강제할 수단이 없던 문제 (gate)
  3. devreport의 '제안', qa_report의 '스펙 결함'(prompts/6_planner.md §6)을
     사람이 매번 손으로 훑어야 했던 문제 (inbox)

사용법:
  python scripts/spec_pipeline.py init
  python scripts/spec_pipeline.py gate    # design/spec-*.md 전체가 lint_spec을 통과하는지 확인
  python scripts/spec_pipeline.py inbox   # devreport 제안 / qa_report 스펙 결함을 모아 초안 생성
"""
import argparse
import datetime
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DESIGN = ROOT / "design"
LOGS = ROOT / "logs"
INBOX = ROOT / "inbox"

PLACEHOLDER = {
    DESIGN: ("# design/\n\nblueprint.md, spec-*.md (prompts/6_planner.md 산출물).\n"
             "spec는 반드시 `python scripts/spec_pipeline.py gate` 통과 후에만 Developer에게 전달한다.\n"),
    LOGS: ("# logs/\n\nplan-{spec_id}.md / devreport-{spec_id}.md (prompts/5_developer.md),\n"
           "qa_report-{spec_id}.md (prompts/7_qa.md).\n"),
    INBOX: ('# inbox/\n\nprocessed-{date}.md (prompts/6_planner.md §6 "Inbox").\n'
            "`python scripts/spec_pipeline.py inbox`로 devreport 제안/qa_report 스펙 결함을 훑어 초안을 만든다.\n"),
}

# devreport 양식(prompts/5_developer.md §6)은 마크다운 절이 아니라 "제안:" 이 마지막 필드인
# 평문 key-value라 마지막 줄부터 파일 끝까지를 캡처한다.
PROPOSAL_PAT = re.compile(r"^제안\s*[:：]\s*(.*)", re.M | re.S)
# qa_report 양식(prompts/7_qa.md §5)은 "== 절 ==" 구분자를 쓴다.
DEFECT_PAT = re.compile(r"==\s*스펙 결함\s*==\s*\n(.*?)(?:\n==|\Z)", re.S)


def cmd_init(a):
    for d, readme in PLACEHOLDER.items():
        d.mkdir(exist_ok=True)
        marker = d / "README.md"
        if not marker.exists():
            marker.write_text(readme, encoding="utf-8")
            print(f"[생성] {marker.relative_to(ROOT)}")
        else:
            print(f"[유지] {d.relative_to(ROOT)} (이미 있음)")


def cmd_gate(a):
    if not DESIGN.exists() or not list(DESIGN.glob("spec-*.md")):
        sys.exit("[중단] design/spec-*.md 없음 - 먼저 `init` 실행 및 스펙 작성 필요")
    r = subprocess.run([sys.executable, str(ROOT / "scripts/lint_spec.py"), str(DESIGN)])
    if r.returncode == 0:
        print("[GATE PASS] 모든 스펙이 lint_spec을 통과함 - Developer에게 전달 가능")
    else:
        sys.exit("[GATE FAIL] 위 스펙은 Developer에게 전달 금지 (prompts/6_planner.md §5)")


def cmd_inbox(a):
    if not LOGS.exists():
        sys.exit("[중단] logs/ 없음 - 먼저 `init` 실행 필요")
    today = datetime.date.today().isoformat()
    out = [f"# inbox 처리 대상 ({today} 스캔)\n"]

    for p in sorted(LOGS.glob("devreport-*.md")):
        m = PROPOSAL_PAT.search(p.read_text(encoding="utf-8"))
        text = (m.group(1).strip() if m else "")
        if text:
            out.append(f"## {p.stem} 제안\n- 채택/보류/기각 + 사유:\n> {text}\n")

    for p in sorted(LOGS.glob("qa_report-*.md")):
        m = DEFECT_PAT.search(p.read_text(encoding="utf-8"))
        text = (m.group(1).strip() if m else "")
        if text:
            out.append(f"## {p.stem} 스펙 결함\n- 관련 스펙 버전 인상 여부:\n> {text}\n")

    if len(out) == 1:
        print("[깨끗함] devreport 제안 / qa_report 스펙 결함 없음")
        return

    INBOX.mkdir(exist_ok=True)
    dest = INBOX / f"processed-{today}.md"
    dest.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"[생성] {dest.relative_to(ROOT)} - 사람/Planner가 판단·기입 후 커밋할 것")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="design/logs/inbox 폴더 생성")
    sub.add_parser("gate", help="design/spec-*.md 전체 lint_spec 게이트")
    sub.add_parser("inbox", help="devreport 제안 / qa_report 스펙 결함 스캔")
    a = ap.parse_args()
    {"init": cmd_init, "gate": cmd_gate, "inbox": cmd_inbox}[a.cmd](a)


if __name__ == "__main__":
    main()
