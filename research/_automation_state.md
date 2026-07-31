# 자동화 상태 (nightly_scout / nightly_executor 공용)

<!-- 이 파일이 2026-07-30 야간 executor 실행 시점에 존재하지 않아 이번 세션이 새로
초기화했다. 이전 세션들의 누적치를 알 수 없어 pending_new_cards는 이번 세션에
새로 만든 카드 수만 반영한 값이다 - 실제 누적치와 다를 수 있으니 사람 확인 필요. -->

- pending_new_cards = 5
- last_signal_digest = "2026-07-31"

## 사람 확인 필요
- 2026-07-30 nightly_executor: `research/_automation_state.md` 파일이 존재하지
  않아 이번 세션이 새로 생성함. pending_new_cards의 이전 누적치(오늘 낮에 추가된
  ARCH-011~014, ELEM-023, GAME-032/033, GENRE-014 등이 반영됐었는지 여부)를 알 수
  없어 3(이번 세션 신규 카드 수)으로만 초기화했다. 다이제스트 반영 임계치(10장)
  판단이 부정확할 수 있으니 필요 시 사람이 값을 보정할 것.
