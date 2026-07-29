# 매일 밤 00:40~06:00 사이 실행 - 사람이 선택([x])한 항목만 카드로 제작 + 신호/기존카드 갱신
# 사용 전 확인: $RepoPath 를 본인 노트북의 실제 저장소 경로로 바꿀 것

$RepoPath = "C:\path\to\Game-Design-and-Planning_resarch"
Set-Location $RepoPath

$today = Get-Date -Format "yyyy-MM-dd"

$prompt = @"
지금은 00:40~06:00 사이의 야간 실행 세션이다 (오늘 날짜: $today). 아래 순서를 반드시 지켜라.

1. research/_scout_queue.md 를 읽어라. '[x]' 로 사람이 체크한 항목만 대상으로 삼는다.
   '[ ]' (미체크) 나 '[done]' (이미 처리됨) 항목은 절대 건드리지 마라.

2. 체크된 항목마다 다음 순서로 정식 카드를 만들어라:
   prompts/1_researcher.md (조사, JSON 산출) -> prompts/2_writer.md (템플릿 기반 집필)
   -> prompts/3_validator.md (검수, fail이면 writer 단계로 돌아가 1회 재작성).
   research/_index.md 에서 다음 카드 ID를 확인해 번호가 겹치지 않게 하라.
   세션이 감당할 수 있는 만큼(대략 1~5장) 순서대로 진행하고,
   더 진행하기 버거우면 무리하지 말고 안전하게 멈춰라 (미완료 항목은 '[x]'로 그대로 둔다).
   완성해서 저장한 항목만 큐에서 '[x]' -> '[done]' 으로 표시를 바꿔라.

3. research/_automation_state.md 를 읽어라.
   a. pending_new_cards 값에 이번 세션에서 새로 만든 카드 수를 더해 갱신하라.
   b. last_signal_digest 날짜가 오늘로부터 7일 이상 지났다면:
      research/signals/ 최근 다이제스트들과 동일한 형식으로 이번 주 시장 신호를 웹 검색으로 조사해
      새 다이제스트 파일을 research/signals/ 에 추가하고, last_signal_digest 를 $today 로 갱신하라.
   c. 갱신 후 pending_new_cards 가 10을 초과한다면:
      아직 카드에 반영되지 않은 다이제스트들을 prompts/4_updater.md 규칙대로 처리해
      관련 기존 카드에 섹션 단위 patch 를 적용하고, pending_new_cards 를 0으로 리셋하라.
      (conflict 로 분류된 항목은 카드에 반영하지 말고, research/_automation_state.md 하단에
      '## 사람 확인 필요' 목록으로 남겨라.)

4. 위 작업으로 카드 파일이 하나라도 바뀌었다면 다음을 이 순서 그대로 실행하라:
   python tools/build_index.py
   python tools/sync_db.py
   python tools/embed_cards.py
   python tools/verify_db.py
   verify_db.py 결과에 unresolved_refs 가 0이 아니면, 원인이 된 카드 파일을 스스로 고치고 재실행하라.

5. git add / commit / push 는 하지 마라. 모든 변경은 로컬 파일로만 남기고,
   커밋 여부는 사람이 아침에 diff 를 직접 확인한 뒤 결정한다.
"@

claude -p $prompt
