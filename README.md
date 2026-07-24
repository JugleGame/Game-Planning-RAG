# Game Design Research Pipeline

게임 설계 요소·장르·사례·시장 신호를 **4계층 카드**로 쌓아가는 리서치 지식 베이스.
Claude(조사/집필/검수)와 인간(승인/편입)이 함께 채우며, 모든 산출물은 파일로 남고 모든 이력은 Git에 남습니다.

## 아키텍처

```
0_scout(후보 제안, 인간 승인) ──▶ _index.md에 ID 예약
                                        │
                          scripts/make_card.py 실행
                                        │
1_researcher(웹조사 ▶ 증거 JSON) ──▶ 2_writer(카드 초안)
                                        │
                    3_validator(적대적 검수) ⇄ scripts/lint_card.py(기계 검사)
                              │ fail → 사유 되먹여 1회 재시도        │ pass
                              └──────────────────────────▶ draft/*.md
                                        │
                          인간 검토 후 research/{elements,genres,games}/ 로 이동 + 커밋
                                        │
                          tools/build_index.py ──▶ research/_index.md 재생성

research/signals/ (주간 신호, 추가 전용) ──▶ 4_updater(섹션 patch 제안, JSON)
                                        │
                    인간이 patch.json 승인 ──▶ scripts/apply_patch.py (카드에 섹션 단위 반영)
```

## 디렉터리 구조

```
.
├── README.md
├── skills/                          # 위 파이프라인을 담은 이식용 Claude Skill 패키지(zip, 버전별)
├── prompts/                        # 파이프라인 각 역할의 시스템 프롬프트 (EN/KR 병기)
│   ├── 0_scout.md                  #   조사 후보 제안 (중복·연결 근거 체크)
│   ├── 1_researcher.md             #   웹조사 → 증거 JSON (해석·평가 금지)
│   ├── 2_writer.md                 #   증거만으로 카드 초안 집필
│   ├── 3_validator.md              #   적대적 검수 (반려 사유 탐색이 목적)
│   ├── 4_updater.md                #   신호를 기존 카드 patch 제안으로 변환
│   ├── 5_developer.md              #   (개발 파이프라인) Unity MCP로 스펙대로 구현
│   ├── 6_planner.md                #   (개발 파이프라인) 아이디어→블루프린트→스펙 분해
│   └── 7_qa.md                     #   (개발 파이프라인) 스펙 기준 독립 판정 (PASS/FAIL/BLOCKED)
├── research/                       # 지식 베이스 (4계층 카드 DB)
│   ├── _index.md                   # 라우팅 인덱스 겸 ID 등록부 - 직접 수정 금지, build_index.py가 재생성
│   ├── elements/                   # ① 요소: 불변에 가까운 설계 블록 (ELEM-###)
│   ├── genres/                     # ② 장르: 요소 조합 레시피 (GENRE-###)
│   ├── games/                      # ③ 게임: 수치 기반 증거 사례 (GAME-###)
│   ├── signals/                    # ④ 신호: 날짜별 시장 관측, 추가만·수정 금지 (YYYY-MM-DD_*.md)
│   └── pending/                    # (예약) 인간 승인 전 대기소
├── templates/                      # 카드 스키마 템플릿 (TOML frontmatter + 고정 섹션)
│   ├── Elem.md
│   ├── Genre.md
│   └── Game.md
├── card_schema.py                  # 카드/digest 필수 필드 정의 (lint_card/build_index/sync_db 공유, 단일 소스)
├── scripts/
│   ├── make_card.py                # R→W→V→lint 자동 루프(1회 재시도) 오케스트레이터, 결과는 draft/에 저장
│   ├── apply_patch.py              # 4_updater의 patch.json을 카드에 섹션 단위로 적용
│   ├── lint_card.py                # TOML frontmatter/ID 참조/수치 근거 대조 검사기 (research 카드용)
│   ├── lint_spec.py                # design/spec-*.md 검사기 (개발 파이프라인용, 아래 참고)
│   ├── spec_pipeline.py            # 개발 파이프라인(prompts 5~7) 실행 골격: init/gate/inbox
│   └── scan_refs.py                # 참조되었지만 아직 카드가 없는 ID를 찾아 작업 큐 생성
├── design/ · logs/ · inbox/        # 개발 파이프라인 산출물 (spec_pipeline.py init으로 생성, 아래 참고)
├── db/                              # Postgres(Neon) 스키마 + 443 HTTPS 우회 경로 (선택 기능, 아래 참고)
│   ├── 00_init_all.sql
│   ├── neon_https.py
│   └── requirements.txt
├── bridge/                          # db/neon_https.py가 쓰는 Node.js 브리지(@neondatabase/serverless)
│   └── neon_bridge.mjs
└── tools/                           # research/*.md ↔ DB 미러링 + 의미 검색 (선택 기능, 아래 참고)
    ├── _db.py                      # DSN 해석 공통 헬퍼
    ├── build_index.py              # 카드 frontmatter → research/_index.md 재생성 (pre-commit 훅 후보)
    ├── init_db.py                  # 00_init_all.sql 실행
    ├── sync_db.py                  # research/*.md(원본) → cards/card_refs/digests(거울) 동기화
    ├── embed_cards.py              # 카드 본문 → pgvector 임베딩 저장 (본문 해시로 변경분만 재계산)
    ├── search_cards.py             # 자유 텍스트 의미 검색 + 반례(실패/혼재 GAME) 자동 조회
    ├── verify_db.py                # 미러링 상태 점검 (행 수, 참조 무결성, 유사도 샘플)
    └── read_section.py             # 여러 카드에서 같은 절만 잘라 읽기 (토큰 절약)
```

## 지식 베이스: 4계층 카드 DB

장르가 아니라 **설계 요소를 원자 단위**로 삼는다. 장르는 요소의 조합(레시피), 게임은 증거, 신호는 날짜 붙은 관측 기록이다. "트렌드 DB"는 따로 없다 - 신호가 쌓이면 그것이 트렌드이자 역사다.

| 계층 | ID 형식 | 내용 | 갱신 규칙 |
|---|---|---|---|
| ① elements | ELEM-### | 정의·성공/실패 사례·유저 반응·조합 궁합·리스크 | 거의 불변 |
| ② genres | GENRE-### | 구성 요소·시장 포화도·관례와 기대치·**빈칸(기회)** | 신호 반영 시 patch |
| ③ games | GAME-### | 한 줄 요약+수치·사용한 요소·성공/실패 원인·시사점 | 사건 시 추가 |
| ④ signals | 날짜 파일명 | 관측 사실만(해석 없음), 카드 연결 제안 | 매주 추가, 수정 금지 |

## 카드 작성 표준

- **카드 하나 = 개념 하나, 1페이지 이내.** 넘치면 쪼갠다.
- **2단 구성**: TOML frontmatter(`+++ ... +++`, 기계용: `card_id`, `type`, `title`, `summary`, `tags`, 연결 ID, `updated`, `confidence`) + 고정 순서의 마크다운 섹션(읽기용).
- **모든 수치 주장에 꼬리표**: 출처가 있으면 `[출처: 출처명, 날짜 기준]`, 우리 생각이면 `[해석]`. (`scripts/lint_card.py`가 기계적으로 검사)
- `summary` 한 줄은 필수 - `_index.md`가 여기서 자동 조립된다.
- 카드가 참조하는 ID(`ELEM-###`/`GAME-###`/`GENRE-###`)는 `_index.md`에 먼저 예약되어 있어야 한다(단일 ID 발급처 규칙).

## _index.md 규칙

`research/_index.md`는 Claude(리서치 역할)의 라우팅 테이블이자 ID 예약 대장이다(카드당 한 줄: ID | 제목 | summary | 태그 | 갱신일, 최근 7일 변경분 최상단).
**절대 손으로 수정하지 않는다** - `tools/build_index.py`가 카드 frontmatter에서 재생성한다:

```bash
python tools/build_index.py
```

## 파이프라인 역할 (prompts/)

| 역할 | 입력 | 출력 | 금지 |
|---|---|---|---|
| 0_scout | 카테고리, `_index.md`, 최근 신호 2건 | 후보 5개(JSON) | 기존 카드와 중복, 근거 없는 후보 |
| 1_researcher | 조사 대상 | 증거 JSON(수치·출처·gaps) | 해석·평가·URL 조작 |
| 2_writer | 증거 JSON, 템플릿, 예시 카드 2장 | 카드 초안(Markdown) | 증거에 없는 수치·고유명사·인용 |
| 3_validator | 카드, 증거 JSON | pass/fail + issues(JSON) | 관대한 판정 - 흠 하나면 fail |
| 4_updater | 신호(digest), 대상 카드 | patch/conflict 제안(JSON) | 카드 전체 재작성, 억지 patch |

핵심 원칙: **검증자 독립성** - 카드를 쓴 프롬프트가 스스로 통과시키지 않는다(`3_validator`가 별도 적대적 검수 + `lint_card.py` 기계 검사 이중 게이트). 모든 편입은 인간 승인을 거친다.

## 워크플로 (1 사이클)

1. (선택) `0_scout` 프롬프트로 다음 조사 후보 제안 → 인간이 `_index.md`에 ID 예약 행 추가·커밋
2. `python scripts/make_card.py "GAME-013 The Stanley Parable" --template templates/Game.md`
   → R(웹조사)→W(집필)→V(검수)→lint 자동 루프(최대 2회, 실패 시 사유 되먹임) → `draft/GAME-013.md` 생성
3. 인간이 draft 검토 후 `research/games/`(등 해당 계층)로 이동 + 커밋
4. `python tools/build_index.py` → `_index.md` 갱신
5. 매주 웹 조사로 `research/signals/YYYY-MM-DD_*.md` 작성 (관측 사실만, 추가 전용)
6. `4_updater` 프롬프트로 신호 → 기존 카드 patch 제안(JSON) 생성, 인간이 눈으로 승인
7. `python scripts/apply_patch.py patch.json --digest research/signals/YYYY-MM-DD_*.md`
   → 카드에 섹션 단위 반영 + 다이제스트 `status` 자동 갱신
8. 필요 시 `python scripts/scan_refs.py` → 참조됐지만 아직 카드가 없는 ID 점검(작업 큐)

## 개발 파이프라인 (prompts/5~7, Unity 구현)

리서치 파이프라인(0~4)과는 별도의 흐름. 전략 AI(Planner)가 카드 근거로 스펙을 쓰고,
Developer AI가 Unity MCP로 구현하고, QA AI가 물건만 보고 독립 판정한다. 세 프롬프트 모두
"판정 기준 소유자는 사람/Planner, 판정자는 QA" 원칙으로 서로의 역할을 침범하지 않는다.

```bash
python scripts/spec_pipeline.py init    # design/ logs/ inbox/ 최초 1회 생성
python scripts/spec_pipeline.py gate    # design/spec-*.md가 lint_spec을 통과해야 Developer에게 전달 가능
python scripts/spec_pipeline.py inbox   # devreport의 '제안' / qa_report의 '스펙 결함'을 모아 inbox/processed-*.md 초안 생성
```

- `6_planner`가 `design/blueprint.md`·`design/spec-XXX.md`(1 spec = 1 메커닉)를 쓰고, 합격 기준은 숫자·관찰 가능한 사실만 허용한다(`scripts/lint_spec.py`가 기계 검사).
- `5_developer`는 스펙을 바꾸지 않고 그대로 구현, `logs/plan-{spec_id}.md`(계획, 사람 승인 후 착수)와 `logs/devreport-{spec_id}.md`(자체 점검+제안)를 남긴다.
- `7_qa`는 devreport를 읽지 않고 콘솔/자동테스트/씬 구조/로그 4가지 수단으로만 `logs/qa_report-{spec_id}.md`를 판정한다(PASS/FAIL/BLOCKED). 같은 항목 2회 연속 FAIL이나 BLOCKED 30%↑는 사람에게 에스컬레이션.
- Unity 구현·콘솔 확인 자체는 사람 또는 Unity MCP가 붙은 별도 세션이 수행한다 - `spec_pipeline.py`는 그 앞뒤(폴더 골격, lint 게이트, inbox 취합)만 자동화한다.

## DB 미러 계층 (선택 기능)

`research/*.md`가 항상 원본이고 DB는 **거울**이다 - 이 계층 없이도 파이프라인 전체가 동작한다.
카드가 많아져 매번 전체를 읽기 부담스러워질 때, 의미 기반 검색과 반례(실패/혼재 사례) 자동 조회를 위해 켠다.

```bash
pip install -r db/requirements.txt          # psycopg2-binary, sentence-transformers
echo 'DATABASE_URL=postgresql://...neon.tech/...?sslmode=require' > .env   # .gitignore에 이미 포함됨
python tools/init_db.py                     # db/00_init_all.sql 실행 (cards/card_refs/digests + pgvector 컬럼)
python tools/sync_db.py                     # research/*.md → DB 미러링 (원본이 사라진 행은 DB에서도 삭제)
python tools/embed_cards.py                 # 카드 임베딩 계산/저장 (본문 해시로 변경분만, API 키 불필요·로컬 모델)
python tools/search_cards.py "AI가 실시간으로 심문하는 게임"   # 유사 카드 + 반례(GAME, 실패/혼재) 함께 조회
python tools/verify_db.py                   # 행 수·참조 무결성·임베딩 커버리지 점검
```

- DSN 해석 우선순위(`tools/_db.py`): `--dsn` 인자 > `DATABASE_URL` 환경변수 > `.env` > 로컬 기본값.
- 5432 포트가 막힌 네트워크에서는 `db/neon_https.py`(Node.js 브리지 `bridge/neon_bridge.mjs` 경유, 443/HTTPS)로 단순 조회만 우회할 수 있다. **단, `tools/*.py` 스크립트들은 전부 `psycopg2` 직결만 쓰고 이 우회 경로로 자동 폴백하지 않는다** - 5432가 막혀 있으면 `db/neon_https.py`를 별도로 직접 호출해야 한다.
- `strategy_ai` 롤은 읽기 전용(`SELECT`만) - 전략 AI(Planner)가 `search_cards.py`류 조회를 이 계정으로 실행하는 걸 전제한 설계.

## Quick Start

```bash
git clone <repo> && cd <repo>
pip install anthropic --break-system-packages   # scripts/make_card.py 전용 (웹 검색 포함 조사·집필·검수)
export ANTHROPIC_API_KEY=...
python tools/build_index.py                      # 최초 인덱스 생성
```

Python 3.11+ 필요 (`lint_card.py`/`build_index.py`가 표준 내장 `tomllib`로 TOML frontmatter를 읽음).

첫 작업: `templates/`의 스키마로 **요소 카드 몇 장을 손으로 작성**한다. 카드 품질이 파이프라인 전체 품질의 상한선이다.
