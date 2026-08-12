이 저장소는 **RAG 데이터(리서치 카드) 수집·검증·미러링만** 담당한다. 스펙 작성·Unity 구현·QA
판정 파이프라인은 2026-07-31에 제거했다 — 그런 작업 요청을 받으면 이 저장소가 아니라고 알린다.

## 읽기 지도 (무엇을 할 때 무엇만 읽는가)
| 상황 | 읽을 파일 (이것만) |
|---|---|
| 조사 주제 발굴 | prompts/0_scout.md |
| 카드 조사 | prompts/1_researcher.md |
| 카드 집필 | prompts/2_writer.md + templates/해당종류 1개 |
| 카드 검수 | prompts/3_validator.md |
| 다이제스트 반영 | prompts/4_updater.md |
| 카드를 새로 넣은 직후 (필수) | `python scripts/audit_links.py --for <ID>` → 간극 있으면 prompts/5_linker.md. 기존 카드를 눈으로 훑지 말 것 — 이 출력이 대상 목록이다 |
| 저장소 전체 연결 점검 | `python scripts/audit_links.py` — '확실' 등급은 반드시 닫고, '확인 필요'는 해당 카드 본문을 보고 판단 |
| ARCH 카드의 인용 출처 확인 | reference/unity_project_baseline.md (또는 reference/qa_verification_policy.md) — 근거 문서일 뿐 실행 지시서가 아니다. 해당 절만 확인 |
| 기존 카드 확인 | research/_index.md(표지, 4KB) → 필요한 **한 종류만** research/_index_<종류>.md → 카드 본문 최대 2장 |
| 카드 형식 오류 | templates/해당종류 1개 (전체 templates 열람 금지). 규칙 자체는 card_schema.py가 단일 소스 |
| 여러 카드의 특정 절만 필요 (궁합, 빈칸 등) | tools/read_section.py <카드들> "<절 제목>" — 전체 열람 금지 |
| 반례(실패·혼재 사례)·유사 카드 탐색 | `python tools/search_cards.py "<질문>"` — 절 단위로 회수한다. `--show-body`면 본문까지 나오므로 카드 파일을 따로 열 필요가 없다. `--kind`/`--section-key`로 좁힐 것. DB 미러가 낡았으면 먼저 M단계부터 |
| 절 분할이 깨졌는지 확인 (DB 없이) | `python scripts/check_sections.py` — 카드 전부가 표준 절로 쪼개지는지. sync_db 전에 여기서 먼저 깨진다 |
| 카드 생성·삭제·ID 변경·다이제스트 반영 후 (M단계) | `python tools/build_index.py` → `tools/sync_db.py` → `tools/embed_cards.py` → `tools/verify_db.py` **이 순서로**. embed는 cards/card_sections를 읽으므로 반드시 sync 다음 |
| DB 스키마가 v1(카드 단위)인 경우 | `psql "$DATABASE_URL" -f db/01_migrate_v2.sql` 1회. `verify_db.py`가 `card_sections` 없음으로 죽으면 이것 |
| 검색기·모델·청크 단위를 건드릴 때 (필수) | 고치기 **전에** `python scripts/eval_retrieval.py`로 기준선을 찍고, 고친 뒤 다시 잰다. 골드셋은 eval/retrieval.jsonl |
| 카드 언어 | **2026-08-12에 카드 165장 + templates의 절 제목·근거 표시·본문 산문 영어 전환 완료.** 새 카드도 영어로 작성하며 한국어로 되돌리지 않는다 |
| 번역 무결성 재검사 | `migrate_card_lang.py --verify <카드들>` — git HEAD 판본과 대조한다. 산문이 아직 한국어인 중간 상태를 볼 때만 `--allow-korean-prose` |
| 번역 게이트 자체를 고칠 때 | `python scripts/test_migrate_gate.py` 로 먼저·나중 둘 다 돌린다. 수치는 글자가 아니라 **값**으로 대조한다(500만 == 5,000,000) |
| 임베딩이 느릴 때 | `embed_cards.py`는 `--device auto`가 기본이라 GPU가 보이면 알아서 쓴다. 안 쓰면 torch가 CPU 빌드다 — db/requirements.txt의 CUDA 설치 주석 참조. VRAM 6GB 미만은 fp16 + 배치 8로 자동 조정 |
| 5432가 막힌 망 | 읽기(`search_cards.py`·`eval_retrieval.py`)와 쓰기(`sync_db.py`·`embed_cards.py`·`verify_db.py`) 모두 `--transport auto`(기본값)로 443/HTTPS 브리지에 자동 폴백. 출력의 `[5432]`/`[443/HTTPS]`로 경로 확인. 쓰기 계열의 HTTPS에선 `--dry-run`이 실행 없이 예정 건수만 보고 |
| 두 접속 경로가 같은 결과를 주는지 확인 | `python tools/search_cards.py "<질의>" --check-transport` — 5432와 443이 **둘 다 열린 곳에서만** 의미가 있다. 한쪽만 열렸으면 거짓 통과 대신 멈춘다. 검색 SQL의 자리표시자(`%(이름)s` → `$N`)를 건드렸다면 반드시 돌릴 것 |
| 미러링 결과 확인 | `verify_db.py`의 `unresolved_refs`가 0이 아니면 없는 ID를 참조하는 카드가 있다는 뜻 → md 원본을 고치고 재실행 |
| 절 제목은 표준 사전의 문자열 그대로 | 변형 제목 발견 시 lint로 잡아 수정 (임의 추측 금지). 사전은 card_schema.py의 `SECTIONS` — 제목(한국어)과 `section_key`(언어 중립)를 짝으로 들고 있다. 절 제목을 바꾸려면 이 사전만 고친다 |

## 읽기 규율 (토큰 예산)
1. 위 지도에 없는 파일은 열지 않는다. 단계당 프롬프트 1개만 읽는다.
2. 카드 확인은 _index.md 표지부터. 상세는 필요한 종류 파일 **하나만** 연다.
   본문 열람은 작업당 최대 2장 — 그 전에 search_cards.py로 절만 뽑아 쓸 수 있는지 볼 것.
3. research/ 하위 폴더를 통째로 여는 것 금지 (ls는 허용, cat 전체 금지).
4. db/, bridge/, tools/*.py 소스는 DB 미러 계층 자체를 고치는 작업이 아니면 열지 않는다 (사용은 CLI 실행만으로 충분).
5. md가 원본, DB는 거울이다. 거울에 손으로 INSERT/UPDATE 금지 — 쓰기는 sync_db.py만 한다. `tools/init_db.py`는 테이블을 DROP하므로 미러링 목적으로 실행 금지.
6. 카드를 새로 넣었으면 `audit_links.py --for <ID>`까지가 한 세트다. 새 카드에서 나가는 링크만
   만들고 끝내면 기존 카드 쪽이 그 카드를 모르는 상태로 남는다 — 역방향은 저절로 생기지 않는다.
7. 카드 파일을 건드렸으면 M단계까지 끝나야 작업 완료다. DB 접속 실패는 카드 작업의 실패가 아니므로, "카드 완료 / 미러링 실패(사유)"로 보고하고 넘어간다 — 조용히 넘기지 않는다.
