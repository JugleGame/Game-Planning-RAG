#!/usr/bin/env python3
"""audit_links.py - 카드 사이 '한쪽만 생긴 링크'를 기계적으로 찾아낸다.

카드를 새로 쓰면 새 카드 → 기존 카드 방향의 링크는 생기지만, 기존 카드 → 새 카드
방향은 사람이 일일이 찾아 고쳐야 한다. 이 스크립트가 그 간극만 전담한다.
lint_card.py가 '카드 한 장이 규격에 맞는가'를 본다면, 여기는 '카드 사이가 맞물리는가'를 본다.

사용법:
  python scripts/audit_links.py                      # 저장소 전체 감사 (사람이 읽는 표)
  python scripts/audit_links.py --for GAME-042       # 이 카드 때문에 고쳐야 할 곳만
  python scripts/audit_links.py --json               # prompts/5_linker.md에 넣을 기계 출력
  python scripts/audit_links.py --only backlink_missing,orphan
종료코드: 0=간극 없음, 1=간극 있음 (CI/훅에 걸 수 있게)

검사 항목:
  broken_ref            카드가 참조하는 ID가 _index.md에 없다 (오타 또는 삭제된 카드)
  missing_card          _index.md에는 있는데 카드 파일이 없다
  backlink_missing      GAME.elements가 지목한 ELEM 카드 본문에 그 GAME이 없다
  genre_example_missing GAME.genres ↔ GENRE.example_games 가 한쪽만 있다 (양방향 검사)
  genre_anchor_missing  GENRE.elements가 지목한 ELEM 카드 본문에 그 GENRE가 없다
  fm_body_drift         GAME 본문이 언급하는 ELEM이 frontmatter elements에 없다
  orphan                아무 카드도 참조하지 않는 카드 (검색으로 도달 불가)

주의: HTML 주석(<!-- ... -->) 안의 ID는 '언급'으로 치지 않는다. 카드가 "이 요소는
쓰지 않았다"고 명시적으로 배제한 기록(증거 부족 주석)을 간극으로 오인하지 않기 위함이다.
"""
import re, json, argparse, pathlib, sys, tomllib

ID_PAT = re.compile(r"\b(?:ELEM|GAME|GENRE|ARCH)-\d{3}\b")
FM_PAT = re.compile(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n(.*)$", re.S)
COMMENT_PAT = re.compile(r"<!--.*?-->", re.S)

CHECKS = ["broken_ref", "missing_card", "backlink_missing", "genre_example_missing",
          "genre_anchor_missing", "fm_body_drift", "orphan"]

# hard = 기계적으로 확실한 간극 (기본 종료코드 1의 근거)
# soft = 사람 판단이 필요한 신호. 카드가 "이 요소는 쓰지 않았다"고 비교·배제한 경우가 섞인다.
#        --strict 를 줘야 종료코드에 반영된다.
HARD = {"broken_ref", "missing_card", "backlink_missing", "genre_example_missing"}

# 간극별 기본 처방 - 5_linker 프롬프트와 사람이 같은 지침을 보게 한다
FIX = {
    "backlink_missing":      ("성공 사례", "그 게임을 사례 한 줄로 추가. 수치는 GAME 카드에서 인용하고 [출처: GAME-### 카드] 표기"),
    "genre_example_missing": (None, "frontmatter의 example_games / genres 배열에 상대 ID 추가 (본문 아님)"),
    "genre_anchor_missing":  ("조합 궁합", "'장르 앵커: GENRE-### (제목) - 이 군집이 이 요소를 구성 요소로 지목한다' 한 줄 추가"),
    "fm_body_drift":         (None, "본문이 실제 사용을 서술하면 frontmatter elements에 추가, 비교·배제 언급이면 그 문장을 주석으로 옮길 것"),
    "orphan":                ("조합 궁합", "이 카드를 참조해야 마땅한 인접 카드를 찾아 그쪽에 링크 추가 (반대 방향)"),
    "broken_ref":            (None, "오타면 ID 수정, 삭제된 카드면 문장에서 ID 제거 후 서술로 대체"),
    "missing_card":          (None, "카드를 새로 쓰거나 _index.md 예약 행을 제거"),
}


def load_cards(root):
    """research/ 아래 카드를 읽어 frontmatter/본문/참조를 정리한다. digest는 refs만 쓴다."""
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
            print(f"[경고] TOML 파싱 실패로 건너뜀: {f}", file=sys.stderr)
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
    """간극 목록을 반환한다. 각 항목은 '어느 카드를 고쳐야 하는가'(card)를 기준으로 적는다."""
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
                add("broken_ref", cid, r, f"{r} 카드가 존재하지 않음")
            elif idx_ids and r not in idx_ids:
                add("broken_ref", cid, r, f"{r}가 _index.md에 없음 (build_index.py 재실행 필요)")
    for rid in sorted(idx_ids - known):
        add("missing_card", rid, None, f"_index.md에 있으나 카드 파일 없음")

    # 2) GAME → ELEM 역링크
    for cid, c in cards.items():
        if not cid.startswith("GAME"):
            continue
        for e in c["elements"]:
            if e in cards and cid not in cards[e]["refs"]:
                add("backlink_missing", e, cid, f"{cid}가 {e}를 사용 요소로 지목하는데 {e} 본문에 {cid}가 없음")

    # 3) GAME.genres ↔ GENRE.example_games (양방향)
    for cid, c in cards.items():
        if cid.startswith("GAME"):
            for g in c["genres"]:
                if g in cards and cid not in cards[g]["examples"]:
                    add("genre_example_missing", g, cid, f"{cid}.genres에 {g}가 있는데 {g}.example_games에 {cid}가 없음")
        elif cid.startswith("GENRE"):
            for g in c["examples"]:
                if g in cards and cid not in cards[g]["genres"]:
                    add("genre_example_missing", g, cid, f"{cid}.example_games에 {g}가 있는데 {g}.genres에 {cid}가 없음")

    # 4) GENRE → ELEM 장르 앵커
    for cid, c in cards.items():
        if not cid.startswith("GENRE"):
            continue
        for e in c["elements"]:
            if e in cards and cid not in cards[e]["refs"]:
                add("genre_anchor_missing", e, cid, f"{cid}가 {e}를 구성 요소로 지목하는데 {e} 본문에 {cid}가 없음")

    # 5) 본문 ↔ frontmatter 어긋남 (주석 밖 언급만)
    for cid, c in cards.items():
        if not cid.startswith("GAME"):
            continue
        drift = sorted(r for r in c["refs"] if r.startswith("ELEM") and r not in c["elements"])
        if drift:
            add("fm_body_drift", cid, ",".join(drift), f"본문은 {', '.join(drift)}를 언급하는데 frontmatter elements={c['elements']}")

    # 6) 고아 카드
    inbound = {i: 0 for i in cards}
    for cid, c in list(cards.items()) + list(digests.items()):
        for r in c["all_refs"] | set(c["elements"]) | set(c["genres"]) | set(c["examples"]):
            if r in inbound and r != cid:
                inbound[r] += 1
    for cid, n in sorted(inbound.items()):
        if n == 0:
            add("orphan", cid, None, "이 카드를 참조하는 카드가 하나도 없음 - 검색으로 도달할 수 없다")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cards-dir", default="research")
    ap.add_argument("--index", default="research/_index.md")
    ap.add_argument("--for", dest="focus", default=None,
                    help="이 카드와 얽힌 간극만 (예: GAME-042). 새 카드를 쓴 직후에 쓴다")
    ap.add_argument("--only", default=None, help=f"검사 항목 제한, 쉼표 구분: {','.join(CHECKS)}")
    ap.add_argument("--json", action="store_true", help="기계 출력 (prompts/5_linker.md 입력용)")
    ap.add_argument("--strict", action="store_true",
                    help="soft 항목(장르 앵커·본문 어긋남·고아)도 종료코드 1에 반영")
    a = ap.parse_args()

    cards, digests = load_cards(a.cards_dir)
    findings = audit(cards, digests, index_ids(a.index))

    if a.only:
        keep = {s.strip() for s in a.only.split(",")}
        bad = keep - set(CHECKS)
        if bad:
            sys.exit(f"알 수 없는 검사 항목: {', '.join(sorted(bad))}")
        findings = [f for f in findings if f["kind"] in keep]
    if a.focus:
        fid = a.focus.upper()
        if fid not in cards:
            sys.exit(f"{fid} 카드를 찾을 수 없음")
        findings = [f for f in findings if fid in (f["card"], f["other"]) or (f["other"] or "").find(fid) >= 0]

    hard_n = sum(1 for f in findings if f["severity"] == "hard")
    fail = bool(findings) if a.strict else bool(hard_n)

    if a.json:
        print(json.dumps({"total": len(findings), "hard": hard_n, "focus": a.focus,
                          "findings": findings}, ensure_ascii=False, indent=2))
        sys.exit(1 if fail else 0)

    scope = f" (기준: {a.focus})" if a.focus else ""
    if not findings:
        print(f"[깨끗함] 카드 {len(cards)}장 사이에 한쪽만 생긴 링크 없음{scope}")
        sys.exit(0)

    print(f"[간극 {len(findings)}건 / 확실 {hard_n}건] 카드 {len(cards)}장 감사{scope}\n")
    for kind in CHECKS:
        group = [f for f in findings if f["kind"] == kind]
        if not group:
            continue
        section, how = FIX[kind]
        where = f"'## {section}' 절에 " if section else ""
        mark = "확실" if kind in HARD else "확인 필요"
        print(f"── [{mark}] {kind} ({len(group)}건) → 고칠 카드에서 {where}{how}")
        for f in group:
            print(f"   {f['card']:<10} {f['detail']}")
        print()
    if hard_n < len(findings):
        print("'확인 필요' 항목은 카드가 일부러 비교·배제한 경우일 수 있다 - 본문을 보고 판단할 것.\n")
    print("다음 단계: prompts/5_linker.md에 아래 출력을 넣어 patch.json을 만들고, 사람이 승인 후")
    print("  python scripts/apply_patch.py patch.json --cards-dir research")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
