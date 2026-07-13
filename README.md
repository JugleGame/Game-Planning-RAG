# AI Game Dev Pipeline

멀티 에이전트(전략 AI / 개발 AI / QA AI) 기반 2D 픽셀 게임 개발 파이프라인.
이 저장소는 세 에이전트와 인간이 공유하는 **단일 협업 백본**입니다 — 모든 산출물은 파일로 주고받고, 모든 이력은 Git에 남습니다.

## 아키텍처

```
리서치 봇 ──(카드 저장)──▶ research/pending/ ──(인간 승인)──▶ research/approved/
                                                                    │
전략 AI ◀──(INDEX.md 읽고 카드 3~5장 검색: 파일 참조 RAG)─────────────┘
   │
   └──(작업 명세서 JSON)──▶ specs/ ──(handoff.py)──▶ 개발 AI (Unity + Claude Code)
                                                        │
                              reports/ ◀──(구현 리포트)───┘
                                 │
                              QA AI ──(acceptance_criteria 채점)──▶ 통과 / 반려
```

## 디렉터리 구조

```
.
├── README.md
├── research/                  # 지식 베이스 (4계층 카드 DB)
│   ├── INDEX.md               # 자동 생성 — 직접 수정 금지
│   ├── elements/              # ① 요소: 불변의 설계 블록 (ELEM-###)
│   ├── genres/                # ② 장르: 요소 조합 레시피 (GENRE-##)
│   ├── games/                 # ③ 게임: 증거 사례 (GAME-###)
│   ├── signals/               # ④ 신호: 날짜별 시장 데이터 (SIG-YYYY-W##) — 추가만, 수정 금지
│   └── pending/               # 리서치 봇 출력 대기소 (인간 승인 전)
├── specs/                     # 전략 AI → 개발 AI 작업 명세서 (SPEC-####.json)
├── reports/                   # 개발/QA 리포트 (SPEC-####_dev.md, _qa.md)
├── qa-policies/
│   ├── base/                  # 인간 소유 기본 QA 정책
│   └── overlays/              # AI 초안 + 인간 승인 오버레이
├── templates/                 # 카드·spec 스키마 템플릿
├── tools/
│   ├── build_index.py         # front-matter → INDEX.md 재생성 (pre-commit 훅)
│   ├── collect.py             # Steam/Reddit 수집 → pending/ 카드 생성
│   └── handoff.py             # spec JSON → 개발 AI 프롬프트 변환·실행
└── UnityProject/              # 게임 본체
```

## 지식 베이스: 4계층 카드 DB

장르가 아니라 **설계 요소를 원자 단위**로 삼는다. 장르는 요소의 조합(레시피), 게임은 증거, 신호는 날짜 붙은 인기 기록이다. "트렌드 DB"는 따로 없다 — 신호가 쌓이면 그것이 트렌드이자 역사다.

| 계층 | 내용 | 갱신 규칙 |
|---|---|---|
| ① elements | 정의·성공/실패 사례·조합 궁합·리스크 | 거의 불변 |
| ② genres | 구성 요소 ID·시장 포화도·관례·**빈칸(기회)** | 분기 점검 |
| ③ games | 수치 기반 사례 분석·시사점 | 사건 시 추가 |
| ④ signals | 관측 수치만 (해석 없음) | 매주 추가, 수정 금지 |

## 카드 작성 표준

- **카드 하나 = 개념 하나, 1페이지 이내.** 넘치면 쪼갠다.
- **2단 구성**: YAML front-matter(기계용: `card_id`, `type`, `title`, `summary`, `tags`, 연결 ID, `updated`, `confidence`) + 고정 순서의 마크다운 섹션(읽기용).
- **모든 주장에 꼬리표**: 출처가 있으면 `[출처: steam:appid]`, 우리 생각이면 `[해석]`.
- `summary` 한 줄은 필수 — INDEX.md가 여기서 자동 조립된다.

## INDEX.md 규칙

INDEX는 전략 AI의 라우팅 테이블이다(카드당 한 줄: ID | 제목 | summary | 태그 | 갱신일, 최근 7일 변경분 최상단).
**절대 손으로 수정하지 않는다** — `tools/build_index.py`가 카드 front-matter에서 재생성하며, pre-commit 훅으로 자동 실행된다:

```bash
# .git/hooks/pre-commit
python tools/build_index.py && git add research/INDEX.md
```

## 에이전트 규칙

| 에이전트 | 읽기 | 쓰기 | 금지 |
|---|---|---|---|
| 리서치 봇 | 외부 API | `research/pending/` | approved 직접 쓰기 |
| 전략 AI | `research/approved 계층 폴더/`, INDEX | `specs/`, QA 오버레이 **초안** | pending 참조, QA 기본 정책 수정 |
| 개발 AI | `specs/`, UnityProject | UnityProject, `reports/*_dev.md` | spec 범위 밖 구현(out_of_scope) |
| QA AI | `reports/`, diff, qa-policies | `reports/*_qa.md` | 채점 기준 자체 작성 |

핵심 원칙: **검증자 독립성** — 명세를 쓴 AI가 채점표를 확정하지 않는다(인간 승인 게이트). **수동 먼저** — 자동화 전, 인간이 파일을 손으로 옮기며 전체 루프를 리허설한다.

## 워크플로 (1 사이클)

1. `python tools/collect.py <요소명> <appid>` → pending/에 카드 생성
2. 인간 검수 후 `git mv research/pending/... research/elements/`
3. 커밋 → INDEX 자동 갱신
4. 전략 AI 실행 → `specs/SPEC-####.json` 생성 (근거 카드 ID 인용 필수)
5. 인간이 acceptance_criteria 승인
6. `python tools/handoff.py specs/SPEC-####.json` → 개발 AI 구현 + dev 리포트
7. QA AI 채점 → 통과 시 머지, 반려 시 사유 첨부 재시도(최대 2회, 이후 인간 에스컬레이션)

## Quick Start

```bash
git clone <repo> && cd <repo>
pip install pyyaml requests anthropic --break-system-packages
export ANTHROPIC_API_KEY=...
ln -s ../../tools/pre-commit .git/hooks/pre-commit   # INDEX 자동화
python tools/build_index.py                           # 최초 인덱스 생성
```

첫 작업: `templates/`의 스키마로 **요소 카드 5장을 손으로 작성**한다. 카드 품질이 파이프라인 전체 품질의 상한선이다.
