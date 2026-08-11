# Game Design Research — RAG 데이터 저장소

게임 설계의 **요소·장르·사례·시장 신호·구현 아키텍처**를 5계층 카드로 쌓아, 다른 AI 에이전트가
검색해 쓸 수 있는 **RAG 지식 베이스**를 만드는 저장소입니다.

이 저장소가 하는 일은 **데이터 수집·검증·미러링 하나**입니다. 게임을 기획하거나 Unity로 구현하거나
QA로 판정하는 파이프라인은 여기 없습니다(2026-07-31 제거). 그런 작업은 이 저장소를 **읽어 가는 쪽**의
몫이고, 여기는 읽히는 쪽입니다.

- **원본은 항상 마크다운 파일**입니다. Postgres/pgvector는 검색을 위한 **거울**일 뿐, 없어도 저장소는 동작합니다.
- **사실과 해석을 문장 단위로 분리**합니다. 수치 주장에는 `[출처: 매체, 날짜 기준]`, 우리 추론에는 `[해석]`을 붙이고 `lint_card.py`가 기계로 검사합니다.
- **모든 편입은 사람이 승인**합니다. 카드를 쓴 프롬프트가 스스로 통과시키지 않습니다.

현재 규모: 카드 106장(ARCH 20 / ELEM 30 / GAME 40 / GENRE 16) + 주간 신호 4건.

## 파이프라인

```
0_scout(후보 제안) ──▶ 사람이 _index.md에 ID 예약
                                │
                  scripts/make_card.py 실행
                                │
1_researcher(웹조사 ▶ 증거 JSON) ──▶ 2_writer(카드 초안)
                                │
            3_validator(적대적 검수) ⇄ scripts/lint_card.py(기계 검사)
                     │ fail → 사유 되먹여 1회 재시도       │ pass
                     └─────────────────────────▶ draft/*.md
                                │
              사람이 검토 후 research/<계층>/ 로 이동 + 커밋
                                │
        scripts/audit_links.py --for <새 카드> (한쪽만 생긴 링크 탐지)
                                │
        5_linker(역방향 patch 제안) ──▶ 사람 승인 ──▶ apply_patch.py
                                │
        M단계: build_index → sync_db → embed_cards → verify_db

research/signals/ (주간 관측, 추가 전용) ──▶ 4_updater(섹션 patch 제안 JSON)
                                │
          사람이 patch.json 승인 ──▶ scripts/apply_patch.py (섹션 단위 반영)
```

## 디렉터리 구조

```
.
├── README.md
├── card_schema.py                  # 카드/digest 필수 필드 단일 정의 (lint_card·build_index·sync_db 공유)
├── prompts/                        # RAG 수집 파이프라인 역할별 시스템 프롬프트
│   ├── 0_scout.md                  #   조사 후보 제안 (중복·연결 근거 체크)
│   ├── 1_researcher.md             #   웹조사 → 증거 JSON (해석·평가 금지)
│   ├── 2_writer.md                 #   증거만으로 카드 초안 집필
│   ├── 3_validator.md              #   적대적 검수 (반려 사유 탐색이 목적)
│   ├── 4_updater.md                #   신호를 기존 카드 patch 제안으로 변환
│   └── 5_linker.md                 #   새 카드가 연 간극을 기존 카드 쪽 patch 제안으로 변환
├── research/                       # ★ 지식 베이스 (5계층 카드 DB)
│   ├── _index.md                   #   표지(장수·최근 변경·ID 등록부) — 직접 수정 금지, build_index.py가 재생성
│   ├── _index_<종류>.md             #   종류별 상세 색인 (element/genre/game/signal/arch) — 한 번에 하나만 연다
│   ├── _scout_queue.md             #   0_scout이 쌓는 조사 후보 큐 (사람이 [ ]→[x]로 선택)
│   ├── _automation_state.md        #   야간 자동 실행 상태 기록
│   ├── elements/                   #   ① 요소: 설계 블록 (ELEM-###)
│   ├── genres/                     #   ② 장르: 요소 조합 레시피 (GENRE-###)
│   ├── games/                      #   ③ 게임: 수치 기반 증거 사례 (GAME-###)
│   ├── signals/                    #   ④ 신호: 날짜별 시장 관측, 추가만·수정 금지 (YYYY-MM-DD_*.md)
│   └── architecture/               #   ⑤ 아키텍처: Unity 구현 패턴·규약 (ARCH-###)
├── templates/                      # 카드 스키마 템플릿 (Elem/Genre/Game/Arch)
├── reference/                      # 카드가 인용하는 근거 문서 (실행 지시서가 아님)
│   ├── unity_project_baseline.md   #   ARCH 카드 16장이 인용하는 프로젝트 기준 구조·규칙
│   └── qa_verification_policy.md   #   ARCH 카드 '검증 방법' 절이 따르는 판정 기준
├── scripts/                        # 카드 생산 도구
│   ├── make_card.py                #   R→W→V→lint 자동 루프(1회 재시도), 결과는 draft/에 저장
│   ├── lint_card.py                #   카드 한 장이 규격에 맞는가 (frontmatter·필수 절·수치 근거)
│   ├── audit_links.py              #   카드 사이가 맞물리는가 (한쪽만 생긴 링크·고아·깨진 참조)
│   ├── check_sections.py           #   카드 전부가 표준 절로 쪼개지는가 (DB 없이, sync_db 전 관문)
│   └── apply_patch.py              #   4_updater/5_linker의 patch.json을 섹션 단위로 적용
├── tools/                          # 인덱스 재생성 + DB 미러링 + 의미 검색
│   ├── build_index.py              #   카드 frontmatter → _index.md 표지 + 종류별 색인 재생성
│   ├── _db.py                      #   DSN 해석 공통 헬퍼
│   ├── init_db.py                  #   db/00_init_all.sql 실행 (테이블 DROP 포함 — 최초 1회만)
│   ├── sync_db.py                  #   research/*.md(원본) → cards/card_sections/card_refs/digests(거울)
│   ├── embed_cards.py              #   절+카드 → pgvector 임베딩 (지문 해시로 변경분만)
│   ├── search_cards.py             #   하이브리드(벡터+트라이그램) **절 단위** 검색 + 반례 자동 조회
│   ├── verify_db.py                #   행 수·참조 무결성·임베딩 커버리지 점검
│   └── read_section.py             #   여러 카드에서 같은 절만 잘라 읽기 (토큰 절약)
├── db/                             # Postgres(Neon) 스키마 + 443/HTTPS 우회 경로
│   ├── 00_init_all.sql             #   빈 DB를 새로 지을 때 (DROP 포함)
│   ├── 01_migrate_v2.sql           #   살아 있는 DB를 v1(카드 단위) → v2(절 단위)로 (DROP 없음)
│   ├── neon_https.py
│   └── requirements.txt
├── bridge/                         # neon_https.py가 쓰는 Node.js 브리지(@neondatabase/serverless)
├── skills/                         # 이식용 Claude Skill 패키지 (R→W→V→L→M→C 전 공정, 최신 버전만 유지)
└── reports/                        # 설계 결정 기록 (예: ARCH 계층 도입 평가 보고서)
```

## 5계층 카드 DB

장르가 아니라 **설계 요소를 원자 단위**로 삼습니다. 장르는 요소의 조합(레시피), 게임은 증거,
신호는 날짜 붙은 관측 기록, 아키텍처는 그 설계를 Unity로 지을 때의 구현 지식입니다.
"트렌드 DB"는 따로 없습니다 — 신호가 쌓이면 그것이 트렌드이자 역사입니다.

| 계층 | ID | 고정 절 | 갱신 규칙 |
|---|---|---|---|
| ① elements | ELEM-### | 정의 / 성공 사례 / 실패 사례 / 유저 반응 요약 / 조합 궁합 / 리스크 | 거의 불변 |
| ② genres | GENRE-### | 구성 요소 / 시장 포화도 / 관례와 기대치 / **빈칸(기회)** | 신호 반영 시 patch |
| ③ games | GAME-### | 한 줄 요약+수치 / 사용한 요소 / 성공·실패 원인 / 시사점 | 사건 시 추가 |
| ④ signals | 날짜 파일명 | 기간 / 수집원 / 관측 사실만 / 연결 제안 | 매주 추가, 수정 금지 |
| ⑤ architecture | ARCH-### | 문제 / 구조 / 핵심 규칙 / Unity 구현 절차 / 안티패턴 / 검증 방법 / 조합 궁합 | 기준 구조 변경 시 |

절 제목은 위 문자열과 **글자까지 일치**해야 합니다(`lint_card.py`가 변형 제목을 잡아냅니다).

## 카드 작성 표준

- **카드 하나 = 개념 하나, 1페이지 이내.** 넘치면 쪼갭니다.
- **2단 구성**: TOML frontmatter(`+++ ... +++` — `card_id`, `type`, `title`, `summary`, `tags`, 연결 ID, `updated`, `confidence`) + 고정 순서의 마크다운 절.
- **모든 수치 주장에 꼬리표**: `[출처: 매체, 날짜 기준]` 또는 `[해석]`. 둘 다 없는 수치는 lint에서 FAIL입니다.
- **근거가 없으면 빈칸을 빈칸이라고 씁니다**: `<!-- 증거 부족: ... -->` 주석으로 무엇이 없는지 명시합니다.
- 참조하는 ID는 `_index.md`에 먼저 등록돼 있어야 합니다(단일 ID 발급처 규칙).
- **양방향 참조**: GAME이 요소를 지목하면 그 ELEM 카드의 성공/실패 사례에도 그 게임이 있어야 합니다. GENRE의 `example_games`와 GAME의 `genres`도 마찬가지입니다.

## 워크플로 (1 사이클)

```bash
# 1) 후보 제안 → 사람이 research/_scout_queue.md에서 선택, _index.md에 ID 예약
# 2) 카드 생성 (R→W→V→lint 자동 루프, 결과는 draft/)
python scripts/make_card.py "GAME-042 <제목>" --template templates/Game.md \
       --examples research/games/031_balatro.md research/games/037_vampire_survivors.md

# 3) 사람이 draft/ 검토 후 research/<계층>/ 로 이동 + 커밋

# 4) 연결 보강 — 새 카드가 기존 카드 쪽에 만든 간극을 닫는다 (아래 절 참고)
python scripts/audit_links.py --for GAME-042
#    → 5_linker로 patch.json 생성 → 사람 승인 →
python scripts/apply_patch.py patch.json --cards-dir research

# 5) M단계 — 카드를 만들거나 지웠으면 반드시 이 순서로 (embed는 sync 다음)
python tools/build_index.py
python tools/sync_db.py
python tools/embed_cards.py
python tools/verify_db.py        # unresolved_refs가 0이어야 완료

# 6) 매주 research/signals/YYYY-MM-DD_*.md 작성 (관측 사실만, 추가 전용)
# 7) 4_updater로 patch.json 생성 → 사람 승인 → 반영
python scripts/apply_patch.py patch.json --digest research/signals/YYYY-MM-DD_*.md
```

검사는 언제든 단독 실행할 수 있습니다:

```bash
python scripts/lint_card.py research/*/*.md --index research/_index.md   # 카드 한 장의 규격
python scripts/audit_links.py                                            # 카드 사이의 맞물림
```

## 연결 보강 (audit_links.py + 5_linker)

카드를 새로 쓰면 **새 카드 → 기존 카드** 방향 링크는 생기지만, **기존 카드 → 새 카드** 방향은
저절로 생기지 않습니다. GAME 카드가 `elements = ["ELEM-021"]`이라고 선언해도 ELEM-021의
`성공 사례`에는 그 게임이 없는 식입니다. 카드가 100장을 넘으면 이 간극을 눈으로 찾을 수 없습니다.
(2026-07-31 최초 감사에서 58건이 쌓여 있었습니다.)

`scripts/audit_links.py`가 그 간극만 기계적으로 찾습니다. `lint_card.py`가 **카드 한 장이 규격에
맞는가**를 본다면, 이쪽은 **카드 사이가 맞물리는가**를 봅니다.

| 검사 | 등급 | 뜻 |
|---|---|---|
| `broken_ref` | 확실 | 참조한 ID의 카드가 없다 (오타 또는 삭제된 카드) |
| `missing_card` | 확실 | `_index.md`에 예약만 되고 카드가 없다 |
| `backlink_missing` | 확실 | GAME이 지목한 ELEM 카드에 그 게임이 없다 |
| `genre_example_missing` | 확실 | `GAME.genres` ↔ `GENRE.example_games`가 한쪽만 있다 |
| `genre_anchor_missing` | 확인 필요 | GENRE가 구성 요소로 지목한 ELEM에 그 장르 표시가 없다 |
| `fm_body_drift` | 확인 필요 | GAME 본문이 언급하는 ELEM이 frontmatter에 없다 |
| `orphan` | 확인 필요 | 아무 카드도 참조하지 않아 검색으로 도달할 수 없다 |

```bash
python scripts/audit_links.py                 # 전체 감사 (확실 항목이 있으면 종료코드 1)
python scripts/audit_links.py --for GAME-042  # 이 카드 때문에 고쳐야 할 곳만
python scripts/audit_links.py --json          # 5_linker에 넣을 기계 출력
python scripts/audit_links.py --strict        # '확인 필요'도 종료코드에 반영 (pre-commit 훅용)
```

- **'확인 필요'는 결함이 아닐 수 있습니다.** 카드가 "이 요소는 일부러 쓰지 않았다"고 배제한
  기록일 수 있습니다. 그런 문장은 `<!-- 증거 부족: ... -->` 주석 안에 두면 감사가 더는 잡지 않습니다
  (주석 안의 ID는 '언급'으로 치지 않습니다).
- 감사 결과를 [prompts/5_linker.md](prompts/5_linker.md)에 넣으면 `apply_patch.py`가 그대로 먹는
  patch.json이 나옵니다. **새 사실을 만들지 않는 것**이 이 프롬프트의 유일한 규칙입니다 — 모든
  문장은 간극 양쪽 카드에 이미 있는 내용을 `[출처: GAME-### 카드]`로 인용해 옮겨 적을 뿐입니다.
- frontmatter 배열 수정(`genre_example_missing`)은 `apply_patch.py`가 하지 못하므로 5_linker가
  `manual` 목록으로 따로 내보내고, 사람이 직접 고칩니다.

## DB 미러 계층 (선택 기능)

`research/*.md`가 항상 원본이고 DB는 **거울**입니다 — 이 계층 없이도 파이프라인 전체가 동작합니다.
카드가 많아져 매번 전체를 읽기 부담스러워질 때, 의미 기반 검색과 반례(실패·혼재 사례) 자동 조회를
위해 켭니다.

```bash
pip install -r db/requirements.txt          # psycopg2-binary, sentence-transformers
echo 'DATABASE_URL=postgresql://...neon.tech/...?sslmode=require' > .env   # .gitignore에 포함됨
python tools/init_db.py                     # 최초 1회 (테이블 DROP 포함 — 이후 실행 금지)
python tools/search_cards.py "AI가 실시간으로 심문하는 게임"
```

- DSN 해석 우선순위(`tools/_db.py`): `--dsn` > `DATABASE_URL` 환경변수 > `.env` > 로컬 기본값.
- **5432가 막힌 망**: `sync_db.py`·`embed_cards.py`·`verify_db.py`는 `--transport auto`(기본값)로 `bridge/neon_bridge.mjs`를 경유한 443/HTTPS 브리지에 자동 폴백합니다. 출력의 `[5432]` / `[443/HTTPS]` 표시로 어느 경로를 탔는지 확인하세요. HTTPS 경로에서는 `--dry-run`이 실행 없이 예정 건수만 보고합니다.
- 검색은 **하이브리드**입니다. 의미 임베딩만 쓰면 고유명사(게임 제목)를 뭉개기 때문에, 벡터 검색과 트라이그램 검색의 **순위**를 Reciprocal Rank Fusion으로 합칩니다.
- `strategy_ai` 롤은 읽기 전용(`SELECT`만) — 이 저장소를 소비하는 외부 에이전트가 쓸 계정입니다.

### 회수 단위는 카드가 아니라 절입니다 (스키마 v2, 2026-08-12)

소비 측(기획 AI)이 아는 계약이 바뀌었습니다.

| | v1 | v2 |
|---|---|---|
| 검색 대상 | `cards` (카드 1장 = 1벡터) | `card_sections` (절 1개 = 1벡터) |
| 임베딩 모델 | `jhgan/ko-sroberta-multitask` | `BAAI/bge-m3` |
| 창 / 차원 | 128토큰 / 768 | 8192토큰 / 1024 |
| 반례 정의 | `kind='GAME' AND type IN ('failure','mixed')` | `section_key IN (실패 사례·리스크·안티패턴·시장 포화도·빈칸)` |

v1의 128토큰 창은 카드 임베딩 텍스트(중앙값 811토큰)를 잘라내 **168장 전부에서 카드의
15.8%만 벡터에 들어가 있었습니다.** `## 실패 사례`·`## 리스크`·`## 안티패턴` 같은 절은
벡터 공간에 존재한 적이 없어 반례 검색이 구조적으로 불가능했습니다.

절 단위 회수는 주입 토큰도 줄입니다 — 카드 평균 2,075자 대신 절 평균 340자.
같은 회수 폭에서 약 85% 절감입니다.

`section_key`는 언어 중립 식별자(`card_schema.py`의 `SECTIONS`)입니다. 절 제목을 영어로
바꿔도 이 키와 그 위에 걸린 질의는 그대로 삽니다.

```bash
python tools/search_cards.py "덱빌딩 로그라이트의 흔한 실패" --kind GAME --show-body
python tools/search_cards.py "타워 디펜스 시장 포화" --section-key market_saturation,gaps
```

**Game-Developer-AI 의 `strategic/research_repo.py`가 이 SQL을 복제합니다.** 테이블·차원·
모델이 전부 바뀌었으므로 그쪽도 같이 고치지 않으면 같은 질의에 다른 근거가 나옵니다.

### 검색기를 건드리기 전에 재세요

```bash
python scripts/eval_retrieval.py              # recall@6, 골드셋 eval/queries.json
python scripts/eval_retrieval.py --mode vector  # 벡터 단독과 비교
```

2026-07-29 하이브리드 도입 때의 실측(질의 17개)이 코드에 남지 않고 주석 문장으로만
남아, 이번 개편의 전후 비교가 불가능했습니다. 같은 일이 없도록 골드셋을 파일로
고정했습니다 — **현재 3개뿐이니 최소 20개까지 채우세요.** 고유명사형과 의역형을
반드시 섞어야 합니다(한쪽만 있으면 한쪽 검색 팔이 망가져도 점수가 안 떨어집니다).

### 카드 언어 전환 (한국어 → 영어)

절 제목은 언어 중립 `section_key`로 다루므로 두 언어가 섞여 있어도 lint·검색이
모두 동작합니다. 전환은 카드 단위로 점진적으로 합니다.

```bash
python scripts/migrate_card_lang.py research/games/*.md --out draft/en
python scripts/migrate_card_lang.py --out draft/en --apply     # 확인 후
```

번역 결과는 **수치 집합·카드 ID 집합·출처 태그 수·[해석] 수·절 구성·frontmatter가
원본과 완전히 일치할 때만** 통과합니다. 하나라도 어긋나면 그 카드는 손대지 않고
원문 그대로 남습니다. 전부 옮긴 뒤 `card_schema.py`의 `CARD_LANG`을 `"en"`으로
바꾸면 새 카드가 영어 절 제목을 쓰기 시작합니다(템플릿도 같이 교체).

## reference/ 폴더에 대해

ARCH 카드는 "우리 프로젝트의 Unity 기준 구조"를 출처로 인용합니다. 그 원문이
`reference/unity_project_baseline.md`입니다. 구현 파이프라인을 제거한 뒤에도 카드 16장이
이 문서를 90회 넘게 인용하고 있어 **근거 문서로만** 남겼습니다. 절 번호와 제목이 카드의 인용
문자열과 맞물려 있으므로 **제목을 바꾸지 마세요** — 바꾸면 인용이 끊깁니다.

## Quick Start

```bash
git clone <repo> && cd <repo>
pip install anthropic          # scripts/make_card.py 전용 (웹 검색 포함 조사·집필·검수)
export ANTHROPIC_API_KEY=...
python tools/build_index.py    # 인덱스 생성
```

Python 3.11+ 필요 (`lint_card.py`/`build_index.py`가 표준 내장 `tomllib`로 TOML frontmatter를 읽습니다).

처음 시작한다면 `templates/`의 스키마로 **요소 카드 몇 장을 손으로 작성**하세요.
카드 품질이 파이프라인 전체 품질의 상한선입니다.
