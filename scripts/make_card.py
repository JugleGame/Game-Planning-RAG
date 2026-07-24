#!/usr/bin/env python3
"""make_card.py - 카드 자동 생성 파이프라인 (반자동: 결과는 draft/, 커밋은 사람이)
사용법:
  export ANTHROPIC_API_KEY=...      # 키는 코드에 넣지 말 것
  python scripts/make_card.py "GAME-013 The Stanley Parable" --template templates/game.md
흐름: R(조사+웹검색) -> W(집필) -> V(AI검수) -> lint(기계검사) -> 실패 시 사유 되먹여 1회 재시도
SDK/모델 최신 사양: https://docs.claude.com/en/api/overview
"""
import sys, os, json, re, argparse, pathlib, subprocess, datetime
import anthropic  # pip install anthropic --break-system-packages

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODEL = "claude-sonnet-4-6"   # 모델 문자열은 docs.claude.com에서 최신 확인
client = anthropic.Anthropic()  # ANTHROPIC_API_KEY 환경변수 사용

def prompt(name): return (ROOT / "prompts" / name).read_text(encoding="utf-8")

def ask(system, user, use_search=False):
    kwargs = dict(model=MODEL, max_tokens=4000, system=system,
                  messages=[{"role": "user", "content": user}])
    if use_search:
        kwargs["tools"] = [{"type": "web_search_20250305", "name": "web_search"}]
    resp = client.messages.create(**kwargs)
    return "\n".join(b.text for b in resp.content if b.type == "text")

def extract_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    return json.loads(m.group(0)) if m else None

def run_lint(card_path, evidence_path):
    r = subprocess.run([sys.executable, ROOT/"scripts/lint_card.py", str(card_path),
                        "--index", str(ROOT/"research/_index.md"), "--evidence", str(evidence_path)],
                       capture_output=True, text=True)
    return r.returncode == 0, r.stdout

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("subject")                       # 예: "GAME-013 The Stanley Parable"
    ap.add_argument("--template", required=True)     # 카드 템플릿 경로
    ap.add_argument("--examples", nargs=2,           # 스타일 앵커 카드 2장
                    default=[ROOT/"research/games/009_hades.md", ROOT/"research/games/005_twelve_minutes.md"])
    a = ap.parse_args()
    today = datetime.date.today().isoformat()
    cid = a.subject.split()[0]

    # 0) ID가 _index에 예약되어 있는지 확인 (단일 발급처 규칙)
    if cid not in (ROOT/"research/_index.md").read_text(encoding="utf-8"):
        sys.exit(f"[중단] {cid} 가 _index.md에 없습니다. 예약 행을 먼저 커밋하세요.")

    # 1) R: 조사 (웹 검색 사용, 산출물은 증거 JSON)
    print("[R] 조사 중...")
    ev = extract_json(ask(prompt("1_researcher.md").replace("{SUBJECT}", a.subject),
                          f"조사 대상: {a.subject}. 오늘 날짜: {today}", use_search=True))
    if not ev: sys.exit("[중단] R이 유효한 JSON을 내지 못함")
    ev_path = ROOT/"evidence"/f"{cid}.json"
    ev_path.parent.mkdir(exist_ok=True)
    ev_path.write_text(json.dumps(ev, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"    증거 {len(ev.get('facts',[]))}건, gaps {len(ev.get('gaps',[]))}건 -> {ev_path.name}")

    # 2) W -> 3) V -> 4) lint (실패 시 사유를 되먹여 1회 재시도)
    w_sys = (prompt("2_writer.md")
             .replace("{EVIDENCE_JSON}", json.dumps(ev, ensure_ascii=False))
             .replace("{TEMPLATE}", pathlib.Path(a.template).read_text(encoding="utf-8"))
             .replace("{EXAMPLE_CARDS}", "\n\n---\n\n".join(
                 pathlib.Path(p).read_text(encoding="utf-8") for p in a.examples)))
    feedback = ""
    for attempt in (1, 2):
        print(f"[W] 집필 (시도 {attempt})...")
        card = ask(w_sys, f"카드를 작성하라. 오늘: {today}." +
                   (f"\n\n이전 시도 반려 사유(반드시 해소할 것):\n{feedback}" if feedback else ""))
        draft = ROOT/"draft"/f"{cid}.md"; draft.parent.mkdir(exist_ok=True)
        draft.write_text(card.strip() + "\n", encoding="utf-8")

        print("[V] AI 검수...")
        v = extract_json(ask(prompt("3_validator.md")
                             .replace("{CARD}", card)
                             .replace("{EVIDENCE_JSON}", json.dumps(ev, ensure_ascii=False)),
                             "검수하라.")) or {"verdict": "fail", "issues": [{"detail": "V 출력 파싱 실패"}]}
        ok_lint, lint_out = run_lint(draft, ev_path)
        print(f"    V: {v['verdict']} / lint: {'PASS' if ok_lint else 'FAIL'}")

        if v["verdict"] == "pass" and ok_lint:
            print(f"[완료] {draft} 생성. 사람이 검토 후 카드 폴더로 이동+커밋하세요.")
            return
        feedback = json.dumps(v.get("issues", []), ensure_ascii=False) + "\n" + lint_out

    print(f"[에스컬레이션] 2회 반려. draft/{cid}.md 와 반려 사유를 사람이 직접 확인:")
    print(feedback)

if __name__ == "__main__":
    main()
