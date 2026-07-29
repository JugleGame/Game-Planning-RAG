# Unity 2D 아키텍처 지식의 RAG 데이터화 — 평가·계획·파일럿 보고서

작성: 2026-07-29 | 대상: Game-Design-and-Planning_resarch 저장소 | 결론 먼저: **실현 가능, 그것도 아주 쉽게. 이유는 이 저장소가 이미 RAG 파이프라인을 갖고 있기 때문.** 새로 짓는 게 아니라 방 하나(ARCH 카드 층)를 늘리는 공사다. 파일럿까지 오늘 완료했고, DB 미러링만 사용자 PC에서 마무리하면 된다.

---

## 0. 미리 알아둘 개념 (아주 쉽게)

**RAG가 뭐냐면:** 시험 볼 때 머릿속 기억만으로 답을 쓰는 게 아니라, 옆에 정리 노트를 두고 필요한 쪽을 펴서 보고 답을 쓰는 것. AI(Developer AI)는 Unity 일반 지식은 알지만 **"우리 프로젝트는 어떻게 짓기로 했는지"**는 모른다. 그 정리 노트를 만들어 주는 게 이번 일이다.

**이 저장소가 이미 가진 것:** 게임 디자인 지식을 카드(ELEM/GAME/GENRE) 70장으로 정리해 두고, 색인(_index.md) → DB 거울(Postgres) → 임베딩(뜻으로 검색) → 검색기(search_cards.py)까지 이어지는 관이 이미 깔려 있다. 즉 "노트 정리법 + 노트 찾는 법"이 완성되어 있고, 지금까지는 **디자인 노트만** 있었을 뿐이다.

---

## STEP 1 — 초안: 계획과 대안

### 1-1. 처음 세운 계획 (초안 그대로 기록)

1. 아키텍처 카드 종류 `ARCH-###`를 새로 만든다 (예: 이벤트 버스, 청크 스트리밍, 세이브 시스템, 상태머신...).
2. `templates/Arch.md` 템플릿을 만든다 — 기존 카드처럼 TOML frontmatter + 고정 절 구조.
3. `research/architecture/` 폴더에 카드를 쌓는다.
4. 기존 M단계(build_index → sync_db → embed_cards → verify_db)에 태워 DB·임베딩까지 반영한다.
5. Developer AI가 스펙의 '참조 카드' 목록으로 ARCH 카드를 받아 읽게 한다.

핵심 발상: **"관은 이미 있으니 물(콘텐츠)만 새 종류를 흘리자."**

### 1-2. 대안 검토 (RAG 말고 다른 길들)

| 대안 | 뭐냐면 | 실현성 | 판정 |
|---|---|---|---|
| A. 프롬프트 정적 주입 | 아키텍처 지도를 프롬프트에 통째로 박아두기. **이미 하고 있음** — prompts/5_developer.md 3절에 폴더 지도+핵심 규칙 3개가 들어 있다 | 높음(완료됨) | 유지하되 요약본만. 카드가 늘수록 프롬프트에 다 못 넣는다 |
| B. RAG 카드 확장 | ARCH 카드 층 추가 (본 계획) | 높음 | **채택.** 파이프라인 재사용, 검증(lint)·출처 규율까지 공짜로 얻음 |
| C. 예제 코드 스캐폴드 | EventBus.cs 등 "정답 코드"를 템플릿 저장소로 두고 복사하게 함 | 중간 | RAG의 보완재로 추천. 카드=왜/규칙, 스캐폴드=정확한 코드. 단독으론 "왜"가 없어 응용이 깨짐 |
| D. 규칙을 검사기로 | 아키텍처 규칙을 lint처럼 코드로 강제 (예: World_Base에 월드 오브젝트 넣으면 FAIL). 이 저장소의 spec_pipeline gate와 같은 사상 | 중간 | 2단계 과제로 추천. 지식(카드)과 강제(검사기)는 역할이 다르다 — 지식은 좋은 걸 만들게 하고, 검사기는 나쁜 걸 막는다 |
| E. 외부 문서 MCP | Context7류로 Unity 공식 문서를 실시간 주입 | 중간 | 일반 Unity API 지식엔 유용하나 "우리 프로젝트 구조"는 못 준다. 보조로만 |
| F. 파인튜닝 | 모델 자체를 우리 지식으로 재학습 | 낮음 | 기각. 비용 크고, 구조가 바뀔 때마다 재학습 필요. 노트는 고쳐 쓰면 되지만 머리는 다시 가르쳐야 한다 |

### 1-3. 유사 사례 (실제로 있었던 일)

- **Unity 자신이 같은 결론에 도달했다.** Unity의 1세대 AI 비서 Muse는 2024년 정리됐고, 2026년 5월 공개 베타로 나온 후속 **Unity AI**의 핵심 차별점이 바로 "에디터 안에서 **네 프로젝트의 씬 계층·패키지·타깃 플랫폼을 알고** 답한다"는 것이다. 일반 지식만으론 부족하고 프로젝트 맥락을 줘야 한다는 것 — 우리가 ARCH 카드로 하려는 일과 같은 방향이다.
- **AI 코딩 도구 전반의 흐름.** GitHub Copilot 계열도 사내 문서·위키를 검색해 끌어오는 RAG 방식으로 진화 중이고, 2026년 업계 분석에서는 RAG가 실패할 때 문제의 대부분이 '생성'이 아니라 **'검색(retrieval)'** 단계에서 난다고 본다 → 카드를 잘게, 제목·태그를 검색 친화적으로 쓰는 게 중요하다는 근거.
- **정적 주입 사례.** Cursor의 rules 파일, Claude Code의 CLAUDE.md — 이 저장소의 CLAUDE.md '읽기 지도'가 정확히 이 패턴이다. 소량 핵심 규칙엔 최강이지만, 지식이 수십 장으로 늘면 한계.
- **카드 내용의 출처 사례.** ARCH-001에 담은 ScriptableObject 이벤트 채널 방식은 Unite 2017 Ryan Hipple 강연과 Unity 공식 e-book "Level up your code with design patterns"에 정리된, 상용 프로젝트(Schell Games 등)에서 검증된 방식이다.

---

## STEP 2 — 초안에 대한 비판적 검토 (실제 데이터와 대조)

초안을 저장소 실물과 대조하니 **"템플릿과 카드만 추가하면 된다"는 가정이 틀렸다.** 발견한 문제들:

1. **하드코딩이 7곳.** `ELEM|GAME|GENRE` 접두어가 정규식·상수로 박힌 곳이 card_schema.py(TYPE_VOCAB), lint_card.py(ID_PAT + REQUIRED_SECTIONS), build_index.py(PREFIX_MAP + order), sync_db.py(ID_PAT + card_id 검사 2곳), scan_refs.py(ID_PAT), db/00_init_all.sql(card_id CHECK + type_vocab CHECK), spec_rules.json(cardIdPattern)까지 총 7개 파일. 하나라도 빼먹으면 "lint는 통과하는데 색인에서 빠지는" 유령 카드가 생긴다.
2. **spec_rules.json은 혼자 못 고친다.** 이 파일은 Game-Developer-AI 저장소와 **쌍둥이 동기화** 대상이고 test_spec_rules_sync.py가 한쪽만 고치면 잡는다. 반드시 두 저장소를 같이 고치고 version을 2로 올려야 한다. (흥미롭게도 그 파일의 _readme에 "층 B(UNITY-### 등) 카드를 추가하려면 여기 한 줄"이라고 **이미 이 확장을 예견한 메모**가 있다 — 설계 의도와 정확히 합치하는 확장이라는 뜻.)
3. **살아 있는 DB에는 옛 CHECK 제약이 남는다.** 00_init_all.sql을 고쳐도 이미 만들어진 테이블엔 적용되지 않고, init_db.py는 테이블을 DROP하므로 미러링 목적 재실행 금지(CLAUDE.md 규칙). → ALTER TABLE이 별도로 필요하다 (STEP 3에 SQL 제공).
4. **전달 경로에 대한 착각.** "임베딩 검색에 넣으면 Developer AI가 알아서 이해한다"는 초안의 기대는 틀렸다. 실제 주입 경로는 검색이 아니라 **스펙의 '참조 카드' 목록**이다(5_developer.md 2절: 스펙+참조 카드 없으면 작업 거부). 즉 6_planner(전략 AI)가 스펙에 ARCH-001 같은 ID를 적어줘야 지식이 흐른다. 검색(search_cards.py)은 전략 AI가 카드를 고를 때 쓰는 도구다.
5. **진실의 원천이 둘이 되는 위험.** 아키텍처 지도가 5_developer.md(프롬프트)와 ARCH 카드 양쪽에 있으면 언젠가 어긋난다. 역할 정리 필요: **카드 = 원본(상세), 프롬프트 = 요약 + "상세는 ARCH 카드 참조"**. (md가 원본, DB는 거울 — 과 같은 원칙의 반복.)
6. **lint의 숫자 검사와 코드 블록이 충돌한다.** check_numbers()의 blocks()는 ``` 코드 펜스를 모른다. 카드에 코드 스니펫을 넣고 그 안에 4자리 이상 숫자(예: 포트 번호)가 있으면 [출처] 없는 지표로 오탐한다. → 당분간 ARCH 카드엔 코드 대신 절차 서술을 쓰고, 코드는 대안 C(스캐폴드 저장소)에 두는 게 맞다. 이는 우연히도 "카드=왜, 코드=스캐폴드" 역할 분리를 강제해 주는 좋은 제약이다.
7. **검색 오염 가능성.** search_cards.py는 종류 구분 없이 섞어 반환하므로, 디자인 질문에 아키텍처 카드가 끼어들 수 있다 [해석]. 카드 수가 늘면 kind 필터 옵션 추가 검토 (cards 테이블에 kind 생성 컬럼이 이미 있어 쿼리 한 줄이면 됨).
8. **환경 함정(작은 것).** 저장소 스크립트는 tomllib(Python 3.11+) 전제. 3.10 환경에선 `pip install tomli` 후 shim이 필요하다 — 이번 파일럿 검증도 그 방식으로 수행했다.

---

## STEP 3 — 최종안: 수정된 계획 + 오늘 실제로 한 일

### 3-1. 확정 설계

- 카드 종류: `ARCH-###`, type 허용값 `pattern | structure | convention`
- 위치: `research/architecture/` (파일명은 기존 관례대로 `001_event_bus.md` — 접두어 없이 번호_이름)
- 필수 절 7개: **문제 / 구조 / 핵심 규칙 / Unity 구현 절차 / 안티패턴 / 검증 방법 / 조합 궁합**
  - 설계 의도: '문제'는 왜 필요한지, '검증 방법'은 QA AI가 관찰 가능한 판정 기준을 갖게(합격 기준 문화와 동일), '조합 궁합'은 ELEM 카드와의 다리(예: EventBus ↔ ELEM-005 AI 통합).
- 역할 분담: **ARCH 카드 = 왜+규칙+절차(원본) / 5_developer.md = 요약 지도 / 스캐폴드 코드(2단계) = 정확한 구현 / spec gate(2단계) = 강제**

### 3-2. 오늘 완료한 것 (파일럿 결과)

| 작업 | 파일 | 결과 |
|---|---|---|
| TYPE_VOCAB에 ARCH 추가 | card_schema.py | 완료 |
| ID_PAT·필수 절 추가 | scripts/lint_card.py | 완료 |
| PREFIX_MAP·⑤ 아키텍처 절 추가 | tools/build_index.py | 완료 |
| ID_PAT·card_id 검사 확장 | tools/sync_db.py, scripts/scan_refs.py | 완료 |
| SQL 스키마 정의 갱신 | db/00_init_all.sql (CHECK 2곳) | 완료 (살아있는 DB엔 아래 ALTER 필요) |
| ARCH 템플릿 | templates/Arch.md | 완료 |
| 예시 카드 1장 | research/architecture/001_event_bus.md (ARCH-001 이벤트 버스) | **lint PASS** |
| 색인 재생성 | research/_index.md | 완료 — 71장, "⑤ 아키텍처" 절 생성 확인 |
| 기존 카드 회귀 검사 | ELEM-001/005, GAME-031, GENRE-013 | 전부 PASS (수정으로 인한 부작용 없음) |
| DB 미러링 (M단계 나머지) | sync_db → embed → verify | **실패 — 이 작업 환경의 네트워크에서 Neon 호스트 접근 불가(5432, 443 모두).** 카드 완료 / 미러링 실패로 보고함 |

### 3-3. 사용자가 해야 할 일 (순서대로, 사용자 PC에서)

1. **DB 제약 갱신** — psql 또는 Neon 콘솔에서 1회:
```sql
ALTER TABLE cards DROP CONSTRAINT cards_card_id_check;
ALTER TABLE cards ADD CONSTRAINT cards_card_id_check
  CHECK (card_id ~ '^(ELEM|GAME|GENRE|ARCH)-[0-9]{3}$');
ALTER TABLE cards DROP CONSTRAINT type_vocab;
ALTER TABLE cards ADD CONSTRAINT type_vocab CHECK (
  (split_part(card_id,'-',1)='ELEM'  AND type IN ('mechanic','narrative-device','tone','tech')) OR
  (split_part(card_id,'-',1)='GAME'  AND type IN ('success','failure','mixed')) OR
  (split_part(card_id,'-',1)='GENRE' AND type = 'genre') OR
  (split_part(card_id,'-',1)='ARCH'  AND type IN ('pattern','structure','convention')));
```
   (제약 이름이 다르면 `\d cards`로 확인. init_db.py 재실행은 DROP이므로 금지.)
2. **M단계 마무리**: `python tools/sync_db.py` → `python tools/embed_cards.py` → `python tools/verify_db.py` (unresolved_refs 0 확인).
3. **spec_rules.json 두 저장소 동시 수정**: cardIdPattern을 `(?:ELEM|GENRE|GAME|ARCH)-\\d{3}`로, version을 2로 — 이 저장소와 Game-Developer-AI 양쪽 모두. 그래야 전략 AI가 스펙 '참조 카드'에 ARCH ID를 적어도 lint_spec이 통과한다.
4. **프롬프트 한 줄 연결** (진실의 원천 정리): 6_planner.md에 "구현 구조가 관련되면 ARCH 카드를 참조 카드에 포함"을, 5_developer.md 3절 끝에 "이 지도의 상세·근거는 ARCH 카드가 원본"을 추가.

### 3-4. 다음 카드 백로그 (기준 구조에서 도출, 우선순위순)

ARCH-002 씬 스트리밍(Boot/World_Base/Chunk Additive 구조), ARCH-003 청크 로더(3x3 활성 규칙), ARCH-004 세이브 시스템(JSON), ARCH-005 NPC 상태머신(Idle/Patrol/Talk), ARCH-006 상호작용(IInteractable + Trigger), ARCH-007 Commentator 파이프라인(구독→생성→로그), ARCH-008 폴더·네이밍 규약(convention), ARCH-009 2D 물리 이동(Rigidbody2D), ARCH-010 로그 규약(QA 판정용).

2단계(카드 10장 이후): 스캐폴드 저장소(대안 C) + 아키텍처 검사기(대안 D, spec gate에 편입).

### 3-5. 최종 판정

실현성 **높음** — 단, "카드만 쓰면 끝"이 아니라 ①코드 7곳 확장(완료) ②DB 제약(SQL 제공) ③쌍둥이 규칙 파일(사용자 작업) ④프롬프트 연결(한 줄)의 4개 고리를 다 이어야 지식이 실제로 Developer AI까지 흐른다. 오늘 기준 ①과 파일럿 카드·색인까지 검증 완료.

---

Sources: [Unity AI is not Muse 2.0 (iCartic)](https://businessofgames.icartic.com/p/unity-ai-is-not-muse-20) · [Unity rolls out Unity AI in Unity 6.2 (CG Channel)](https://www.cgchannel.com/2025/08/unity-rolls-out-unity-ai-in-unity-6-2/) · [Unity AI Open Beta Guide 2026](https://www.buildfastwithai.com/blogs/unity-ai-open-beta-guide-2026) · [What is RAG? (GitHub)](https://github.com/resources/articles/software-development-with-retrieval-augmentation-generation-rag) · [RAG in 2026 (Command Code)](https://commandcode.ai/guides/rag-in-2026)
