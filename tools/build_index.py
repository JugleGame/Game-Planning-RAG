# tools/build_index.py
"""색인 생성. 표지(_index.md) + 종류별 상세 색인(_index_<종류>.md)으로 나눠 쓴다.

## 왜 나눴나 (2026-08-12)

단일 _index.md는 카드 168장에서 이미 50,029자였다. 카드당 title+summary+전체 태그를
한 줄에 담기 때문이다. 목표 규모인 1,000장에서는 선형 외삽으로 약 30만 자가 된다 —
읽을 수 없는 색인이다. 토큰 예산을 지키려고 만든 장치가 토큰 예산을 파괴한다.

새 구조:
  _index.md            표지. 장수, 최근 변경, 종류별 파일 안내, **전체 ID 목록**
  _index_element.md    ① 요소 상세 (card_id | title | summary | tags | 갱신일)
  _index_genre.md      ② 장르 상세
  _index_game.md       ③ 게임 상세
  _index_signal.md     ④ 신호 상세
  _index_arch.md       ⑤ 아키텍처 상세

표지에 ID 전체 목록을 남기는 이유: lint_card.py와 audit_links.py가 _index.md를
정규식으로 훑어 '등록된 ID 집합'을 얻는다. ID만이면 1,000장에서도 10KB 이하라
그 용도에는 충분하고, 두 스크립트를 고치지 않아도 된다.

주의: 종류별 파일도 결국 커진다(GAME 400장 ≈ 120KB). 그 규모에서 올바른 접근은
색인 통독이 아니라 tools/search_cards.py 검색이다.
"""
import glob, os, sys, tomllib, datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESEARCH = os.path.join(BASE, "research")

sys.path.insert(0, BASE)
from card_schema import CARD_REQUIRED, DIGEST_REQUIRED

order = {"element": "① 요소", "genre": "② 장르", "game": "③ 게임", "signal": "④ 신호", "arch": "⑤ 아키텍처"}

# card_id 접두어 → 카테고리. 접두어 길이가 제각각이므로 '-' 기준 분리로 매칭
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
    """card_id 접두어 우선, 없으면 type == 'digest'로 signal 폴백 감지"""
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
    # '_' 시작 파일은 카드가 아니라 운영 문서(_index*, _scout_queue, _automation_state).
    # 전에는 _index만 걸렀던 탓에 나머지가 매번 '프론트매터 없음'으로 잡혀 종료코드 1이
    # 났다 - 실패가 아닌데 실패로 보이면 진짜 실패도 같이 무시된다.
    if os.path.basename(path).startswith("_"): continue
    try:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        if not raw.startswith("+++"):
            errors.append((path, "frontmatter 없음")); continue
        meta = tomllib.loads(raw.split("+++", 2)[1])

        cat = classify(meta)
        if cat is None:
            errors.append((path, f"card_id/type으로 카테고리 판별 불가 (card_id={meta.get('card_id')}, type={meta.get('type')})"))
            continue

        if cat == "signal":
            for key in DIGEST_REQUIRED:
                if key not in meta: raise KeyError(f"signal 필수 키 누락: {key}")
            if "period_end" not in meta:  # 갱신일 계산에 쓰이지만 다른 스크립트는 요구하지 않는 build_index 전용 필드
                raise KeyError("signal 필수 키 누락: period_end")
            # signal은 card_id/title/summary가 없으므로 인덱스 표시용으로 합성
            fname = os.path.splitext(os.path.basename(path))[0]  # 예: 2026-07-14_steam_trend
            meta["card_id"] = meta.get("card_id") or f"SIGNAL-{fname}"
            meta["title"] = meta.get("title") or f"주간 관측 ({meta.get('period_at', meta['period_end'])} ~ {meta['period_end']})"
            src = ", ".join(meta.get("sources", []))
            meta["summary"] = meta.get("summary") or f"[{meta['status']}] {src}"
            meta["updated"] = parse_date(meta["period_end"])
        else:
            for key in CARD_REQUIRED:
                if key not in meta: raise KeyError(f"필수 키 누락: {key}")
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


# --- 종류별 상세 색인 -------------------------------------------------------
written = {}
for t, label in order.items():
    group = sorted([c for c in cards if c["type"] == t], key=lambda c: c["card_id"])
    lines = [f"# {label} 색인 (자동 생성 - 직접 수정 금지)",
             f"생성: {today} | {len(group)}장\n"]
    for c in group:
        tags = " ".join(f"#{x}" for x in c.get("tags", []))
        lines.append(f"- {c['card_id']} | {c['title']} | {c['summary']} | {tags} | {c['updated']:%m-%d}")
    written[t] = (len(group), write(f"_index_{t}.md", lines))

# --- 표지 -------------------------------------------------------------------
out = ["# RESEARCH INDEX (자동 생성 - 직접 수정 금지)",
       f"생성: {today} | 카드 {len(cards)}장\n",
       "상세는 종류별 파일을 볼 것. 한 번에 한 종류만 연다."]
for t, label in order.items():
    n, size = written[t]
    out.append(f"- {label}: `research/_index_{t}.md` ({n}장, {size:,}B)")
out.append("\n특정 카드를 찾는 게 아니라 '무엇이 있나'를 훑는 중이라면 색인 통독보다")
out.append("`python tools/search_cards.py \"<질문>\"` 이 싸고 정확하다.")

recent = [c for c in cards if (today - c["updated"]).days <= 7]
if recent:
    out.append("\n## 최근 7일 변경")
    out += [f"- {c['card_id']} | {c['title']} | {c['updated']:%m-%d}"
            for c in sorted(recent, key=lambda c: c["updated"], reverse=True)]

# 등록 ID 전체 목록. lint_card.py / audit_links.py가 여기서 '아는 ID 집합'을 얻는다.
out.append("\n## 등록 ID (기계 조회용)")
for t, label in order.items():
    ids = sorted(c["card_id"] for c in cards if c["type"] == t)
    if ids:
        out.append(f"- {label}: " + " ".join(ids))

cover = write("_index.md", out)

print(f"_index.md 갱신 완료: {len(cards)}장 (표지 {cover:,}B)")
for t, label in order.items():
    n, size = written[t]
    print(f"  _index_{t}.md  {n:>4}장  {size:>8,}B")
if errors:
    print(f"\n⚠ 스킵된 파일 {len(errors)}건:", file=sys.stderr)
    for p, msg in errors:
        print(f"  - {os.path.relpath(p, BASE)}: {msg}", file=sys.stderr)
    sys.exit(1)
