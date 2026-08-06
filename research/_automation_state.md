# 자동화 상태 (nightly_scout / nightly_executor 공용)

<!-- 이 파일이 2026-07-30 야간 executor 실행 시점에 존재하지 않아 이번 세션이 새로
초기화했다. 이전 세션들의 누적치를 알 수 없어 pending_new_cards는 이번 세션에
새로 만든 카드 수만 반영한 값이다 - 실제 누적치와 다를 수 있으니 사람 확인 필요. -->

- pending_new_cards = 10
- last_signal_digest = "2026-07-31"

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
