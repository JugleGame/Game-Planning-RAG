# 자동화 상태 (nightly_scout / nightly_executor 공용)

<!-- 이 파일이 2026-07-30 야간 executor 실행 시점에 존재하지 않아 이번 세션이 새로
초기화했다. 이전 세션들의 누적치를 알 수 없어 pending_new_cards는 이번 세션에
새로 만든 카드 수만 반영한 값이다 - 실제 누적치와 다를 수 있으니 사람 확인 필요. -->

- pending_new_cards = 6
- last_signal_digest = "2026-08-07"

<!-- 2026-08-11 nightly_executor: 큐에서 [x] 체크된 ELEM 카드 3장(ELEM-045 신격/후원자
선택형 소환 로스터 고정, ELEM-046 전투 참여형 동물 동료 자동 보조, ELEM-047 비대칭
시작덱 캐릭터 로스터)을 새로 만듦. R단계 웹 검색으로 근거를 모으고(Gods & Gore,
Beast of Reincarnation, Talespinner, 비교 사례로 Slay the Spire), lint_card.py는
세 카드 모두 초안에서 바로 PASS(재작성 없음). ELEM-045는 "고른 신에 속하지 않은
생물을 완전히 볼 수 없다"는 잠금 자체를 1차 출처로 확인하지 못해 confidence=medium,
증거 부족 주석으로 표시함. audit_links --for로 각 카드가 연 역방향 링크 간극(orphan,
'확인 필요' 등급)을 모두 닫음 - GENRE-010/ELEM-036(ELEM-045), ELEM-008(ELEM-046),
ELEM-020/GENRE-012(ELEM-047)에 조합 궁합·구성 요소 절 보강. 저장소 전체 audit_links
재확인 결과 '확실' 등급 0건, 이번 세션과 무관한 기존 '확인 필요' 6건(fm_body_drift,
GAME-013/014/026/033/038/056)은 2026-08-06·08-09·08-10 세션이 이미 검토해 남겨둔
대로 손대지 않음. pending_new_cards 3+3=6으로 임계치(10) 미만이라 다이제스트
반영(4_updater)은 건너뜀. last_signal_digest(2026-08-07)가 오늘(2026-08-11)로부터
4일 경과로 7일 미만이라 신규 다이제스트도 만들지 않음. DB 미러링은 이 세션 환경에
psycopg2 모듈이 없어 sync_db.py 자체가 즉시 실패(2026-08-06/08-09 세션과 동일 원인) -
md 카드 자체는 완결 상태이며 미러링만 보류됨. -->

<!-- 2026-08-10 nightly_executor: 큐에서 [x] 체크된 GAME 카드 3장(GAME-054 Dominocalypse,
GAME-055 Loop Hero, GAME-056 Factorio)을 새로 만듦. GAME-054는 아직 미출시라 판매·리뷰로
성공/실패를 판정할 근거가 없어 type="mixed", confidence="low"로 표기하고 근거 부족을 명시함.
audit_links --for로 각 카드가 연 역방향 링크 간극(ELEM-021/GENRE-035, ELEM-004/GENRE-037,
GENRE-036)을 모두 닫음 - '확실' 등급 잔여는 build_index 미실행으로 인한 일시적 broken_ref뿐.
GAME-056의 '확인 필요'(fm_body_drift, ELEM-039 언급)는 GENRE-030(Palworld)과의 의도된 대비
서술로 판단해 GENRE-036 카드의 기존 관례(가시적 대비 서술)를 따라 그대로 둠. pending_new_cards
0+3=3으로 임계치(10) 미만이라 다이제스트 반영(4_updater)은 건너뜀. last_signal_digest
(2026-08-07)가 오늘(2026-08-10)로부터 3일 경과로 7일 미만이라 신규 다이제스트도 만들지
않음. -->

<!-- 2026-08-09 nightly_executor: 큐에서 [x] 체크된 GENRE 카드 5장(GENRE-035 타일매칭
로그라이크 덱빌더, GENRE-036 팩토리 자동화 빌더, GENRE-037 솔로 PvE 로그라이크
오토배틀러, GENRE-038 방치형/증분형 게임, GENRE-039 턴제 전술 로그라이크)을 새로 만듦.
audit_links --for로 각 카드가 연 역방향 링크 간극(ELEM-021/GENRE-012, GENRE-030,
GENRE-027/ELEM-018/ELEM-022/ELEM-004, ELEM-022, ELEM-018/GENRE-016)을 모두 닫음 -
'확실' 등급 잔여 0건. pending_new_cards 10+5=15로 임계치(10)를 초과해 SIGNAL-2026-08-07
다이제스트(status="미반영(편집자 확인 대기)")를 prompts/4_updater.md 규칙대로 반영함 -
제안 연결 3건(GAME-023 3.2.0 PTR 코어 스탯 스케일러 하향, GENRE-010 그리스 신화 소재
로그라이트 TD 밀집, GENRE-012 도미노/요괴 소재 다변화→GENRE-035로 분리 신설됐음을 교차
참조) 모두 기존 카드와 충돌 없는 순수 추가로 판단해 conflict 없이 patch 적용, 다이제스트
status를 반영(2026-08-09)으로 갱신, pending_new_cards를 0으로 리셋함. last_signal_digest
(2026-08-07)가 오늘(2026-08-09)로부터 2일 경과로 7일 미만이라 신규 다이제스트는 만들지
않음. DB 미러링은 이 세션 환경에 psycopg2 모듈이 없어 sync_db.py 자체가 즉시 실패(2026-08-06
세션과 동일 원인) - md 카드 자체는 완결 상태이며 미러링만 보류됨. 저장소 전체 audit_links.py
정기 점검에서 이번 세션과 무관한 기존 카드 5장(GAME-013/014/026/033/038)의 '확인 필요'
(fm_body_drift) 간극이 재확인됐으나, 2026-08-06 세션이 이미 남긴 대로 오늘도 대상이 아니라
손대지 않고 남겨둠. -->

<!-- 2026-08-08 nightly_executor: `_scout_queue.md`에 '[x]' 체크된 항목이 하나도
없었음(전부 '[ ]' 미체크 또는 '[done]') - 지침에 따라 어떤 항목도 건드리지 않고
카드 생성 단계(1~2)는 완전히 건너뜀. pending_new_cards는 이번 세션 신규 카드
0장이라 10+0=10으로 변동 없음(임계치 10 초과 아님 - 도달 상태 유지, 3c 다이제스트
반영도 건너뜀). last_signal_digest(2026-08-07)가 오늘(2026-08-08)로부터 1일 경과로
7일 미만이라 신규 다이제스트도 만들지 않음. 카드 파일 변경이 없어 M단계
(build_index/sync_db/embed_cards/verify_db)는 실행하지 않음. -->

<!-- 2026-08-07 nightly_executor: `_scout_queue.md`에 '[x]' 체크된 항목이 하나도
없었음(전부 '[ ]' 미체크 또는 '[done]') - 지침에 따라 어떤 항목도 건드리지 않고
카드 생성 단계(1~2)는 완전히 건너뜀. pending_new_cards는 이번 세션 신규 카드
0장이라 10+0=10으로 변동 없음(임계치 10 초과 아님 - 도달 상태 유지). last_signal_digest
(2026-07-31)가 오늘(2026-08-07)로부터 정확히 7일 경과라 신규 다이제스트 대상으로 판단해
research/signals/2026-08-07_arpg_td_deckbuilder_signals.md를 웹 검색 기반으로 작성함
(status="미반영(편집자 확인 대기)", 연결 제안 3건: GENRE-034/GAME-023 Diablo IV 3.2.0
PTR 코어 스탯 스케일러 하향, GENRE-010 그리스 신화 소재 로그라이트 TD 밀집, GENRE-012/
ELEM-021 로그라이크 덱빌더 규칙·소재 차용 다변화). last_signal_digest를 2026-08-07로
갱신. pending_new_cards가 10을 초과하지 않아(도달만) 4_updater 반영은 이번에도 건너뜀.
카드 파일 변경이 없어 M단계(build_index/sync_db/embed_cards/verify_db)는 실행하지 않음. -->

<!-- 2026-08-06 nightly_executor: 큐에서 [x] 체크된 ELEM 카드 3장(ELEM-042 단일 타워
직접 조작형 방어, ELEM-043 스쿼드 동시 조작 자동전투, ELEM-044 그림다크 추출런 결합)을
새로 만듦. audit_links --for로 각 카드가 연 역방향 링크 간극(GAME-050/ELEM-018/GENRE-010,
GAME-051/GENRE-019, ELEM-016/ELEM-027)을 모두 닫음. pending_new_cards 7+3=10으로
임계치(10)를 넘지 않아(초과가 아니라 도달) 다이제스트 반영(4_updater)은 이번에도 건너뜀.
last_signal_digest(2026-07-31)가 오늘(2026-08-06)로부터 6일 경과로 7일 미만이라 신규
다이제스트도 만들지 않음. DB 미러링은 이 세션 환경에 psycopg2 모듈이 없어 sync_db.py
자체가 즉시 실패 - md 카드 자체는 완결 상태이며 미러링만 보류됨. 저장소 전체
audit_links.py 정기 점검에서 이번 세션과 무관한 기존 카드 5장(GAME-013/014/026/033/038)의
'확인 필요'(fm_body_drift) 간극이 확인됐으나, 오늘 세션 대상이 아니라 손대지 않고
남겨둠 - 별도 정기 점검에서 다룰 것. -->

<!-- 2026-08-05 nightly_executor: 큐에서 [x] 체크된 GAME 카드 2장(GAME-052 Rogue Defense:
Hybrid Tower TD, GAME-053 Last Epoch)을 새로 만듦. pending_new_cards 5+2=7로 임계치(10)
미만이라 다이제스트 반영(4_updater)은 건너뜀. last_signal_digest(2026-07-31)가 오늘
(2026-08-05)로부터 5일 경과로 7일 미만이라 신규 다이제스트도 만들지 않음. -->

<!-- 2026-08-04 nightly_executor: 큐에서 [x] 체크된 GENRE 카드 3장(GENRE-032 이머시브 심,
GENRE-033 CRPG, GENRE-034 핵앤슬래시 던전크롤러 ARPG)을 새로 만듦. pending_new_cards
2+3=5로 임계치(10) 미만이라 다이제스트 반영(4_updater)은 건너뜀. last_signal_digest
(2026-07-31)가 오늘(2026-08-04)로부터 4일 경과로 7일 미만이라 신규 다이제스트도 만들지
않음. DB 미러링은 이 세션 환경에 DATABASE_URL이 없어 5432/443 브리지 모두 실패 - md 카드
자체는 완결 상태이며 미러링만 보류됨. -->

<!-- 2026-08-03 nightly_executor: 큐에서 [X] 체크된 GENRE 카드 2장(GENRE-030, GENRE-031)을
새로 만듦. pending_new_cards 0+2=2로 임계치(10) 미만이라 다이제스트 반영(4_updater)은
건너뜀. last_signal_digest(2026-07-31)가 오늘(2026-08-03)로부터 7일 미만이라 신규
다이제스트도 만들지 않음. DB 미러링은 이 세션 환경에 DATABASE_URL이 없어 5432/443
브리지 모두 실패 - md 카드 자체는 완결 상태이며 미러링만 보류됨. -->


<!-- 2026-08-02 nightly_executor: 큐에서 [X] 체크된 GENRE 카드 4장(GENRE-026~029)을
새로 만들며 pending_new_cards가 8+4=12로 임계치(10)를 넘어, SIGNAL-2026-07-31
다이제스트(당시 status="미반영(편집자 확인 대기)")를 prompts/4_updater.md 규칙대로
반영함. 4건의 제안 연결 모두 기존 카드 내용과 충돌 없는 순수 추가(append)로 판단돼
conflict 없이 GENRE-010/012/013/019, GAME-023에 섹션 patch 적용, 다이제스트
status를 반영(2026-08-02)으로 갱신. 이후 pending_new_cards를 0으로 리셋함. -->

## 사람 확인 필요
- 2026-07-30 nightly_executor: `research/_automation_state.md` 파일이 존재하지
  않아 이번 세션이 새로 생성함. pending_new_cards의 이전 누적치(오늘 낮에 추가된
  ARCH-011~014, ELEM-023, GAME-032/033, GENRE-014 등이 반영됐었는지 여부)를 알 수
  없어 3(이번 세션 신규 카드 수)으로만 초기화했다. 다이제스트 반영 임계치(10장)
  판단이 부정확할 수 있으니 필요 시 사람이 값을 보정할 것.
