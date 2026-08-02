# 스카우트 추천 큐 (자동 생성)

사용 방법:
1. 매일 밤 23:05, `nightly_scout.ps1`이 이 파일 맨 위에 새 후보 5개를 `[ ]` 미체크 상태로 추가합니다.
2. 사람이 아침이나 저녁에 이 파일을 열어, 실제로 진행하고 싶은 항목만 `[ ]` → `[x]`로 바꿔 저장합니다.
3. 다음날 00:40, `nightly_executor.ps1`이 `[x]` 항목만 골라 카드로 만들고, 처리 완료되면 `[done]`으로 바꿉니다.
4. `[ ]`로 남아있는(선택 안 된) 항목은 건드리지 않고 그대로 큐에 남습니다.

---

## 2026-08-02 23:05 생성 (카테고리: GENRE)
- [ ] 익스트랙션 슈터 (Extraction Shooter / PvPvE) — connects_to: ELEM-027 — why_now: ELEM-027(추출형 런 구조) 카드는 있으나 이를 코어로 삼는 GENRE 군집 카드가 없음 - 07-27 다이제스트의 다크 판타지 추출형 ARPG 'Mistfall Hunter'(오픈베타 약 43만 명 참여, 07-29 정식출시)가 대표 사례 — obscurity: 중간
- [done] 히어로 슈터 (Hero Shooter) — connects_to: ELEM-036 — why_now: ELEM-036(픽/밴 드래프트)이 MOBA(GENRE-024) 카드로만 연결돼 있고, 같은 절차를 쓰는 경쟁 히어로 슈터 자체의 GENRE 군집 카드가 비어 있음 — obscurity: 낮음 — GENRE-026
- [done] 오토배틀러 (Auto Battler / Auto Chess) — connects_to: ELEM-022 — why_now: GENRE-019(서바이버라이크) 태그에 #auto-battler가 이미 쓰이고 있으나, 자동 전투와 지수적 스케일링(ELEM-022)이 코어인 오토배틀러 자체 장르 카드가 없어 태그-카드 간극이 있음 — obscurity: 중간 — GENRE-027
- [done] 수집형 카드 대전 PvP (Collectible Card Game PvP) — connects_to: ELEM-020 — why_now: GENRE-012(로그라이크 덱빌더)는 1인 런 기반만 다루며, 같은 덱 구축(ELEM-020) 요소를 상시 대전형(PvP)으로 쓰는 군집이 비어 있음 — obscurity: 높음 — GENRE-028
- [done] 리듬 액션 (Rhythm Action) — connects_to: ELEM-031 — why_now: ELEM-031(시각 피드백 과장/Juiciness)이 여러 카드에 걸쳐 재료로 쓰이지만, 입력 타이밍 자체가 코어이고 피드백 과장이 필수인 리듬 장르를 다루는 GENRE 카드가 아직 없음 — obscurity: 높음 — GENRE-029

## 2026-08-01 23:05 생성 (카테고리: GAME)
- [ ] Mistfall Hunter (다크 판타지 추출형 ARPG) — connects_to: ELEM-027, GENRE-009 — why_now: 오픈베타(2026-06-14~22) 약 43만 명 참여 후 07-29 정식 출시, Game Pass 무료 포함 - ELEM-027(추출형 런 구조) 카드는 이미 있지만 이를 실제로 구현한 GAME 카드가 아직 없음 (07-27 다이제스트) — obscurity: 중간
- [ ] Forsaken Realms: Vahrin's Call (다크 판타지 신작) — connects_to: GENRE-009 — why_now: 2026년 7월 마지막 주 다크 판타지/소울라이크 태그 신작 밀집 출시(07-27) 사례 중 하나 - Mistfall Hunter·Beast of Reincarnation과 함께 언급됐지만 개별 GAME 카드는 아직 없음 (07-27 다이제스트) — obscurity: 높음
- [done] NARAKA: BLADEPOINT (NVIDIA ACE 탑재 배틀로얄) — connects_to: ELEM-025, GENRE-003 — why_now: NVIDIA ACE(온디바이스 SLM 실시간 음성 NPC) 스택이 데모를 넘어 실제 출시 빌드에 탑재된 구체 사례로 inZOI와 함께 거론됨 - ELEM-025 카드는 있지만 이를 보여주는 GAME 카드가 아직 없음 (07-27 다이제스트) — obscurity: 낮음 — GAME-049
- [done] Towerful Defense: A Rogue TD (로그라이트 TD 하이브리드) — connects_to: GENRE-010, ELEM-018, GAME-027 — why_now: 로그라이트+타워 디펜스 하이브리드화가 개별 사례가 아니라 장르 차원 흐름임을 보여주는 신작(2026-07-30 itch.io 출시), Rogue Tower(GAME-027)와 유사하나 별도 GAME 카드는 없음 (07-31 다이제스트) — obscurity: 높음 — GAME-050
- [done] Yet Another Zombie Survivors (스쿼드형 서바이버라이크) — connects_to: GENRE-019, GAME-037 — why_now: 단일 캐릭터 자동전투가 기본인 서바이버라이크 장르 정의에서 벗어나 최대 3인 스쿼드 동시 조작을 도입한 변주 - 정식판 08-20 얼리액세스 종료 예정, 재확인 필요 ★ (07-31 다이제스트) — obscurity: 높음 — GAME-051

## 2026-07-31 23:05 생성 (카테고리: ELEM)
- [ ] NPC 자율성 의사결정 아키텍처 전면 재설계 (End-to-end Autonomy Decision-Making Redesign) — connects_to: ELEM-005, ARCH-005 — why_now: inZOI 개발일지(2026-07-24)가 부분 수정이 아니라 자율성 의사결정 로직 자체를 전면 재설계 중이라고 발표(8월 업데이트 예정) - 기존 ELEM-005(AI 통합)의 "실시간 반응 생성"과 달리 반응 이전의 의사결정 구조 자체를 다루는 하위 요소 (07-25 다이제스트) — obscurity: 낮음
- [done] 탐사형 포토그래피 목표 동사 (Exploration Photography as Core Verb) — connects_to: ELEM-012 — why_now: Wholesome Direct 2026에서 소개된 우주 로버 사진 촬영 신작 'ROVA' - 랜드마크 기반 탐험(ELEM-012)에 "사진으로 증거를 남긴다"는 구체적 목표 동사를 결합한 사례이나 아직 카드 부재 (07-25 다이제스트) — obscurity: 높음 — ELEM-034
- [done] 접객 서비스 루프 (Hospitality / Service Sim Loop) — connects_to: ELEM-013, GENRE-007 — why_now: Wholesome Direct 2026에서 소개된 픽셀아트 주점 시뮬 신작 'Long Live My Lady' - 코지 시뮬 군집에 "손님 접객"이라는 구체적 서비스 루프 사례가 아직 카드로 없음 (07-25 다이제스트) — obscurity: 높음 — ELEM-035
- [ ] 롱테일 유지형 신규 플레이어블 클래스 추가 (Long-tail Retention via New Playable Class Addition) — connects_to: ELEM-032, GAME-022 — why_now: 다키스트 던전 10주년 DLC 'The Fire's Edge'(2026-08-18)가 발작 시스템 확장과 별개로 신규 히어로 2종(듀얼리스트·러너웨이)을 추가해 장기 유지를 노리는 신호 - 뉴 게임 플러스(ELEM-032)와는 다른 '신규 클래스 투입형' 재플레이 유인 (07-27 다이제스트) — obscurity: 낮음
- [ ] 일상 행동 그럴듯함 미세조정 (Everyday Behavior Plausibility Fix) — connects_to: ARCH-005 — why_now: inZOI 개발일지(2026-07-24)가 자율성 전면 재설계와 별개로 방치된 음식을 냉장고에 넣는 등 소규모 행동 개선을 예고 - 상태머신(ARCH-005)에 세부 상태·조건을 더하는 저비용·고체감 개선 패턴이 아직 카드로 없음 (07-25 다이제스트) — obscurity: 낮음

## 2026-07-30 23:05 생성 (카테고리: ELEM)
- [ ] 재화 전환형 제작 마찰 완화 (Craft Material Conversion to Reduce Grind Friction) — connects_to: ELEM-019, GAME-023 — why_now: Diablo IV 3.1.1/3.1.1a 패치가 판데모니움 조각 요구량을 5→4로 낮추고 "신화 아이템 1회 제작" 제한을 철폐해, 루트 기반 마찰을 재화 전환으로 완화하는 신호 (07-27 다이제스트) — obscurity: 중간
- [done] 광기 파생 액티브 전투 메커닉 (Derangement-driven Active Combat Mechanic) — connects_to: ELEM-015, GAME-022 — why_now: 다키스트 던전 10주년 DLC 'The Fire's Edge'(2026-08-18)가 발작(derangement) 시스템을 신규 'Burn' 전투 메커닉으로 확장 투자 (07-27 다이제스트) — obscurity: 중간 — [removed 2026-07-31] ELEM-024는 ELEM-015와 근거(GAME-022 DLC 발표)가 동일해 중복 → ELEM-015 성공 사례·리스크로 통합 후 삭제
- [done] 온디바이스 SLM 실시간 음성 대화 NPC (On-device SLM Real-time Voice NPC, e.g. NVIDIA ACE) — connects_to: ELEM-005, ELEM-006, GAME-011 — why_now: NVIDIA ACE 스택(ASR+소형 언어모델+TTS+표정)이 데모를 넘어 inZOI·NARAKA: BLADEPOINT 등 실제 출시 빌드에 탑재되기 시작, 텍스트 기반 AI 통합과 구분되는 음성 전용 파이프라인 (07-27 다이제스트) — obscurity: 낮음 — ELEM-025
- [done] 추출형 런 구조 (Loot-and-Extract Run Structure) — connects_to: ELEM-004, ELEM-014, GENRE-009 — why_now: 다크 판타지 추출형 ARPG 'Mistfall Hunter' 오픈베타에 약 43만 명 참여 후 07-29 정식 출시 - 죽음=손실이 아니라 '탈출 성공 여부'로 보상이 갈리는 별도 순환 구조 (07-27 다이제스트) — obscurity: 높음 — ELEM-027
- [done] 테마 쏠림형 바이럴 소재 선택 (Thematic Convergence for Shareability, 고양이 테마 사례) — connects_to: ELEM-010, GENRE-007 — why_now: 2026년 7월 코지 신작 밀집 출시 중 고양이 테마가 SNS 공유·참여도에서 일관된 우위를 보인다는 보도 - 장르 관습이 아니라 '소재 선택'이 바이럴리티를 좌우하는 신호 (07-25 다이제스트) — obscurity: 중간 — [removed 2026-07-31] ELEM-026의 관측(고양이 테마 우위)이 ELEM-010·GENRE-007에 이미 동일 출처로 기록돼 중복 → ELEM-010 조합 궁합으로 통합 후 삭제
