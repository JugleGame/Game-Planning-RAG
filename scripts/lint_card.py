#!/usr/bin/env python3
"""lint.py v3 - 카드 형식/근거 검사기 (TOML frontmatter 방식)

프론트매터를 +++ ... +++ 구분선 안의 TOML로 읽는다.
tomllib는 Python 3.11+ 표준 내장(읽기 전용)이라 별도 설치 불필요.

사용법:
  python scripts/lint.py <카드.md> [<카드2.md> ...] [--index _index.md] [--evidence evidence.json]
종료코드: 0=통과, 1=오류
"""
import sys, re, argparse, pathlib, datetime
import tomllib   # Python 3.11+ 표준 내장. 3.10 이하면: pip install tomli 후 'import tomli as tomllib'

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from card_schema import CARD_REQUIRED as REQUIRED, DIGEST_REQUIRED, TYPE_VOCAB

REQUIRED_SECTIONS = {
    "ELEM":  ["정의", "성공 사례", "실패 사례", "유저 반응 요약", "조합 궁합", "리스크"],
    "GAME":  ["한 줄 요약 + 판매·리뷰 수치", "사용한 요소", "성공/실패 원인", "우리 프로젝트 시사점"],
    "GENRE": ["구성 요소", "시장 포화도", "관례와 기대치", "빈칸"],
}

ID_PAT = re.compile(r"\b(?:ELEM|GAME|GENRE)-\d{3}\b")
METRIC = re.compile(r"\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?%|\d+(?:만|천억|억|천)\b|\d{4,}|\d{2,}(?:점|장|건|fps)")
DATEISH = re.compile(r"^(?:19|20)\d{2}")

FM_PAT = re.compile(r"^(?:\+\+\+|---)\s*\n(.*?)\n(?:\+\+\+|---)\s*\n(.*)$", re.S)

def load_card(path):
    text = pathlib.Path(path).read_text(encoding="utf-8")
    m = FM_PAT.match(text)
    if not m:
        return None, text, ["frontmatter(+++ 블록)를 찾을 수 없음"]
    try:
        fm = tomllib.loads(m.group(1))
    except tomllib.TOMLDecodeError as e:
        return None, m.group(2), [
            f"TOML 파싱 실패: {e}",
            "  힌트: 문자열 값엔 큰따옴표, 날짜도 \"2026-07-15\"처럼 따옴표로 감쌀 것",
        ]
    return fm, m.group(2), []

def present(fm, field):
    v = (fm or {}).get(field)
    if v is None:
        return False
    if isinstance(v, str):
        return bool(v.strip())
    if isinstance(v, (list, dict)):
        return len(v) > 0
    return True

def check_frontmatter(fm):
    if str((fm or {}).get("type", "")).strip() == "digest":
        return [f"다이제스트 필수 필드 누락 또는 빈 값: {f}" for f in DIGEST_REQUIRED
                if not present(fm, f)]
    errs = [f"필수 필드 누락 또는 빈 값: {f}" for f in REQUIRED if not present(fm, f)]
    if fm and "tags" in fm and not isinstance(fm["tags"], list):
        errs.append("tags는 TOML 배열이어야 함 (예: tags = [\"a\", \"b\"])")
    cid = str((fm or {}).get("card_id", ""))
    typ = str((fm or {}).get("type", "")).strip()
    vocab = TYPE_VOCAB.get(cid.split("-")[0])
    if vocab and typ and typ not in vocab:
        errs.append(f"type '{typ}'은 {cid.split('-')[0]} 허용값 {sorted(vocab)}에 없음")
    upd = (fm or {}).get("updated")
    if upd is not None and not isinstance(upd, datetime.date):
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(upd)):
            errs.append(f"updated 형식 오류: '{upd}' (YYYY-MM-DD)")
    return errs

def blocks(body):
    cur, out = [], []
    for line in body.splitlines():
        if line.startswith("#") or line.startswith("- ") or not line.strip():
            if cur:
                out.append(" ".join(cur)); cur = []
            if line.startswith("- "):
                cur = [line]
        else:
            cur.append(line)
    if cur:
        out.append(" ".join(cur))
    return out

def check_numbers(body):
    errs = []
    for blk in blocks(body):
        if "<!--" in blk:
            continue
        clean = ID_PAT.sub("", blk)
        nums = [n for n in METRIC.findall(clean) if not DATEISH.match(n)]
        if nums and "[출처" not in blk and "[해석]" not in blk:
            errs.append(f"출처/해석 없는 지표 {nums[:3]}  <- \"{blk[:40]}...\"")
    return errs

def check_refs(fm, body, index_ids):
    self_id = str((fm or {}).get("card_id", ""))
    found = {m.group(0) for m in ID_PAT.finditer(body)}
    return [f"미등록 ID 참조: {r} (_index.md에 없음)"
            for r in sorted(found) if r != self_id and r not in index_ids]

def check_grounding(body, evidence_path):
    ev = pathlib.Path(evidence_path).read_text(encoding="utf-8")
    errs = []
    for n in {m for m in METRIC.findall(ID_PAT.sub("", body)) if not DATEISH.match(m)}:
        if n.replace(",", "") not in ev.replace(",", ""):
            errs.append(f"근거 대조 실패: '{n}' 이 evidence.json에 없음")
    return errs

def load_index_ids(index_path):
    if not pathlib.Path(index_path).exists():
        return set()
    text = pathlib.Path(index_path).read_text(encoding="utf-8")
    return {m.group(0) for m in ID_PAT.finditer(text)}

def check_sections(card_id, body):
    found = [l[3:].rstrip() for l in body.splitlines() if l.startswith("## ")]
    need = REQUIRED_SECTIONS.get(card_id.split("-")[0], [])
    errs  = [f"필수 절 누락: ## {s}" for s in need if s not in found]
    errs += [f"사전에 없는 절 제목: ## {f}" for f in found if f not in need]  # 오타·변형 탐지
    # 뒤 공백 탐지 (정확 일치를 깨뜨리는 주범)
    errs += [f"절 제목 뒤 공백: '## {l[3:]}'" for l in body.splitlines()
             if l.startswith("## ") and l != l.rstrip()]
    return errs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cards", nargs="+")
    ap.add_argument("--index", default="_index.md")
    ap.add_argument("--evidence", default=None)
    a = ap.parse_args()
    index_ids = load_index_ids(a.index)
    fail = False
    for card in a.cards:
        fm, body, errs = load_card(card)
        if fm is not None:
            errs += check_frontmatter(fm) + check_numbers(body)
        if str(fm.get("type", "")).strip() != "digest":
            errs += check_sections(fm.get("card_id", ""), body)
            if index_ids:
                errs += check_refs(fm, body, index_ids)
            if a.evidence:
                errs += check_grounding(body, a.evidence)
        tag = "FAIL" if errs else "PASS"
        print(f"[{tag}] {pathlib.Path(card).name}")
        for e in errs:
            print("   -", e)
        fail |= bool(errs)
    sys.exit(1 if fail else 0)

if __name__ == "__main__":
    main()