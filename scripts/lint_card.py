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
from card_schema import (CARD_ID_RE as ID_PAT, CARD_REQUIRED as REQUIRED,
                         DIGEST_REQUIRED, TYPE_VOCAB,
                         KIND_SECTIONS, SECTION_KEY, SECTION_TITLES, section_title,
                         SOURCE_OPENERS, INTERP_MARKS)
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
        marked = (any(o in blk for o in SOURCE_OPENERS)
                  or any(m in blk for m in INTERP_MARKS))
        if nums and not marked:
            errs.append(f"출처/해석 없는 지표 {nums[:3]}  <- \"{blk[:40]}...\"")
    return errs

# 다이제스트(신호)의 '연결' 절은 구조상 전부 제안이다.
#
# 신호 파일은 세 절 고정이다: `## 기간 / 수집원`, `## 관측 사실만`,
# `## 연결 (제안 - 편집자 확정 필요)`. 앞의 둘은 출처가 붙은 관측이고, 마지막은
# 그 관측을 어느 카드에 반영할지 제안하는 편집 메모라 관측 수치를 되풀이한다.
#
# 그 되풀이에 출처를 요구하면 고칠 수 없는 실패가 남는다 — 신호 파일은
# **추가 전용이고 수정 금지**이기 때문이다(README 3곳에 명시). 고칠 수 없는
# 파일을 계속 실패시키면 저장소가 깨끗한 lint 상태에 영영 도달하지 못하고,
# 그러면 진짜 실패도 같이 묻힌다.
# 두 언어를 다 받는다. 신호 파일은 추가 전용이라 기존 6장은 한국어로 남지만,
# 앞으로 쓰는 다이제스트는 영어다 - 한쪽만 알면 제안 절을 못 잘라내고, 그러면
# 고칠 수 없는 파일에 고칠 수 없는 lint 실패가 쌓인다 (위 주석의 바로 그 문제).
DIGEST_PROPOSAL_HEADINGS = ("## 연결", "## Links")


def facts_only(body: str) -> str:
    """다이제스트에서 관측 부분만 남긴다 (제안 절 이후를 자른다)."""

    for heading in DIGEST_PROPOSAL_HEADINGS:
        head, sep, _ = body.partition(heading)
        if sep:
            return head
    return body


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
    """절 검사는 제목이 아니라 section_key로 한다.

    제목은 한국어/영어 둘 다 받는다 - 카드 168장을 한 번에 번역할 수 없으므로
    전환 기간에는 언어가 섞이고, 그 상태에서도 검사가 돌아야 한다.
    다만 **한 카드 안에서** 섞이는 건 반쯤 옮기다 만 것이므로 오류로 잡는다.
    """
    found_titles = [l[3:].rstrip() for l in body.splitlines() if l.startswith("## ")]
    need = KIND_SECTIONS.get(card_id.split("-")[0], [])

    errs, found_keys, langs = [], [], set()
    for t in found_titles:
        key = SECTION_KEY.get(t)
        if key is None:
            errs.append(f"사전에 없는 절 제목: ## {t}")   # 오타·변형 탐지
            continue
        found_keys.append(key)
        langs |= {lang for lang, title in SECTION_TITLES[key].items() if title == t}

    errs += [f"필수 절 누락: ## {section_title(k)}" for k in need if k not in found_keys]
    errs += [f"이 종류({card_id.split('-')[0]})에 없는 절: ## {section_title(k)}"
             for k in found_keys if k not in need]
    # 같은 절이 두 번 나오면 card_sections에서 같은 section_key가 중복된다.
    # (card_id, ord) 기본키라 저장은 되지만, 절 단위 필터가 어느 쪽을 뜻하는지
    # 모호해진다 - 카드 안에서 절은 유일해야 한다.
    errs += [f"절 중복: ## {section_title(k)}"
             for k in sorted(set(found_keys)) if found_keys.count(k) > 1]
    if len(langs) > 1:
        errs.append(f"한 카드 안에서 절 제목 언어가 섞임: {sorted(langs)} "
                    "(번역이 중단된 카드일 수 있음)")
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
        is_digest = fm is not None and str(fm.get("type", "")).strip() == "digest"
        if fm is not None:
            errs += check_frontmatter(fm)
            errs += check_numbers(facts_only(body) if is_digest else body)
        if not is_digest:
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