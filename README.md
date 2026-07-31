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
│   └── 4_updater.md                #   신호를 기존 카드 patch 제안으로 변환
├── research/                       # ★ 지식 베이스 (5계층 카드 DB)
│   ├── _index.md                   #   라우팅 인덱스 겸 ID 등록부 — 직접 수정 금지, build_index.py가 재생성
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
│   ├── lint_card.py                #   frontmatter·필수 절·ID 참조·수치 근거 검사기
│   ├── apply_patch.py              #   4_updater의 patch.json을 카드에 섹션 단위로 적용
│   └── scan_refs.py                #   참조됐지만 카드가 없는 ID를 찾아 작업 큐 생성
├── tools/                          # 인덱스 재생성 + DB 미러링 + 의미 검색
│   ├── build_index.py              #   카드 frontmatter → research/_index.md 재생성
│   ├── _db.py                      #   DSN 해석 공통 헬퍼
│   ├── init_db.py                  #   db/00_init_all.sql 실행 (테이블 DROP 포함 — 최초 1회만)
│   ├── sync_db.py                  #   research/*.md(원본) → cards/card_refs/digests(거울)
│   ├── embed_cards.py              #   카드 본문 → pgvector 임베딩 (본문 해시로 변경분만)
│   ├── search_cards.py             #   하이브리드(벡터+트라이그램) 검색 + 반례 자동 조회
│   ├── verify_db.py                #   행 수·참조 무결성·임베딩 커버리지 점검
│   └── read_section.py             #   여러 카드에서 같은 절만 잘라 읽기 (토큰 절약)
├── db/                             # Postgres(Neon) 스키마 + 443/HTTPS 우회 경로
│   ├── 00_init_all.sql
│   ├── neon_https.py
│   └── requirements.txt
├── bridge/                         # neon_https.py가 쓰는 Node.js 브리지(@neondatabase/serverless)
├── skills/                         # 이 파이프라인을 담은 이식용 Claude Skill 패키지
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

# 4) M단계 — 카드를 만들거나 지웠으면 반드시 이 순서로 (embed는 sync 다음)
python tools/build_index.py
python tools/sync_db.py
python tools/embed_cards.py
python tools/verify_db.py        # unresolved_refs가 0이어야 완료

# 5) 매주 research/signals/YYYY-MM-DD_*.md 작성 (관측 사실만, 추가 전용)
# 6) 4_updater로 patch.json 생성 → 사람 승인 → 반영
python scripts/apply_patch.py patch.json --digest research/signals/YYYY-MM-DD_*.md

# 7) 필요 시 참조됐지만 카드가 없는 ID 점검
python scripts/scan_refs.py --cards-dir research --index research/_index.md
```

검사는 언제든 단독 실행할 수 있습니다:

```bash
python scripts/lint_card.py research/*/*.md --index research/_index.md
```

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
