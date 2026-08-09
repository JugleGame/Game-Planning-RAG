# 스카우트 추천 큐 (자동 생성)

사용 방법:
1. 매일 밤 23:05, `nightly_scout.ps1`이 이 파일 맨 위에 새 후보 5개를 `[ ]` 미체크 상태로 추가합니다.
2. 사람이 아침이나 저녁에 이 파일을 열어, 실제로 진행하고 싶은 항목만 `[ ]` → `[x]`로 바꿔 저장합니다.
3. 다음날 00:40, `nightly_executor.ps1`이 `[x]` 항목만 골라 카드로 만들고, 처리 완료되면 `[done]`으로 바꿉니다.
4. `[ ]`로 남아있는(선택 안 된) 항목은 건드리지 않고 그대로 큐에 남습니다.

---

## 2026-08-08 23:05 생성 (카테고리: GENRE)
- [done] 타일매칭 로그라이크 덱빌더 (Tile-matching Roguelike Deckbuilder Hybrid) — connects_to: GENRE-012, ELEM-021 — why_now: 08-07 다이제스트에 도미노 타일 매칭과 로그라이크 덱빌딩을 결합한 'Dominocalypse'가 Steam 출시 예정으로 확인되고, 같은 다이제스트가 일본 신화(요괴) 소재 로그라이크 덱빌더 동시 출시까지 보고함 — 친숙한 규칙 차용(ELEM-021)의 대상이 포커·카드류를 넘어 보드게임 규칙 자체로 확장되는 흐름인데 이를 담을 GENRE 카드가 없음 — obscurity: 높음 — GENRE-035
- [done] 팩토리 자동화 빌더 (Factory / Production-chain Automation Builder) — connects_to: ELEM-039, GENRE-030 — why_now: GENRE-030(크리처 노동 자동화 서바이벌)이 '포획한 생물'이라는 전제에 자동화를 묶어서만 다루고 있어, Factorio·Satisfactory류처럼 생물 포획 없이 순수 생산 사슬 설계 자체가 코어인 자동화 장르는 레지스트리에 빈칸으로 남아 있음 — obscurity: 낮음 — GENRE-036
- [done] 솔로 PvE 로그라이크 오토배틀러 (Solo PvE Roguelike Auto-battler) — connects_to: GENRE-027, GENRE-012 — why_now: GENRE-027(오토배틀러)은 PvP 경제형만, GENRE-012(로그라이크 덱빌더)는 능동 조작 런만 다루는데, Backpack Battles류처럼 런 기반 드래프트 위에서 유닛·장비를 배치만 하고 전투는 자동으로 흘러가는 1인 PvE 하이브리드는 두 카드 사이 빈칸으로 남아 있음 — obscurity: 높음 — GENRE-037
- [done] 방치형/증분형 게임 (Idle / Incremental Game) — connects_to: ELEM-022 — why_now: ELEM-022(지수적 점수 스케일링)가 방치형 게임의 핵심 동력인데도, 모바일 매출 상위권을 꾸준히 차지하는 이 장르 자체를 감싸는 GENRE 클러스터 카드가 없음 — obscurity: 낮음 — GENRE-038
- [done] 턴제 전술 로그라이크 (Turn-based Tactical Roguelike) — connects_to: ELEM-018, GENRE-016 — why_now: GENRE-016(탄막 로그라이크)이 실시간 회피·조준 조작만 다루는데, ELEM-018(로그라이크 무작위 업그레이드/경로 드래프트)을 공유하면서도 턴제 격자 전투가 코어인 Into the Breach/FTL류 갈래는 별도 GENRE 카드가 없음 — obscurity: 중간 — GENRE-039

## 2026-08-07 23:05 생성 (카테고리: ELEM)
- [ ] 제작 캡 철폐 (Repeatable High-Rarity Crafting Cap Removal) — connects_to: ELEM-028, GAME-023 — why_now: Diablo IV 3.1.1/3.1.1a 패치가 "신화 아이템 1회 제작" 제한을 완전히 철폐해 몇 번이든 재도전할 수 있게 함(07-27 다이제스트) - ELEM-028은 흩어진 재료를 합쳐 아이템을 만드는 공식만 다루고, 만든 뒤에도 반복 재시도를 허용하는 '캡 철폐' 자체는 별도 요소로 기록된 적 없음 — obscurity: 낮음
- [ ] 무작위 웨이브 구성 (Randomized Enemy Wave Composition) — connects_to: GENRE-010, GAME-052, ELEM-018 — why_now: Rogue Defense: Hybrid Tower TD(GAME-052)가 무작위 웨이브와 무기 시너지를 결합한 모바일 로그라이트 TD로 색인에 반영됨(07-31 다이제스트의 TD 하이브리드화 흐름 연장) - ELEM-018은 플레이어가 고르는 드래프트의 무작위성만 다루고, 적 웨이브 구성 자체가 매 판 달라지는 무작위성은 별도 요소로 기록된 적 없음 — obscurity: 높음
- [ ] 조건부 빌드 시너지 보너스 (Conditional Build Synergy Bonus) — connects_to: ELEM-022, GAME-052, GAME-034 — why_now: Rogue Defense: Hybrid Tower TD의 '무기 시너지'와 Wildfrost(GAME-034)의 카드 궁합이 같은 패턴을 공유하지만(07-31 다이제스트 TD 하이브리드화 흐름), 특정 조합이 맞아떨어질 때만 조건부로 발동하는 보너스 구조 자체는 ELEM-022(곱연산 지수적 스케일링)와 구분되는 독립 요소로 기록된 적 없음 — obscurity: 높음
- [ ] 보스 텔레그래프 회피 타이밍 (Boss Attack Telegraph & Dodge-Timing Window) — connects_to: ELEM-014, GAME-021, GENRE-009 — why_now: 07월 마지막 주 다크 판타지/소울라이크 신작 밀집 출시(07-27 다이제스트)로 장르 포화가 이어지는 가운데, 처벌적 죽음 순환(ELEM-014)의 핵심 재료인 '보스 공격 예고 후 회피 타이밍'이라는 구체 전투 메커닉 자체는 아직 별도 ELEM 카드로 분해된 적 없음 — obscurity: 낮음
- [ ] 협동 자원 풀 내 숨은 배신자 긴장 (Hidden-role Betrayal Tension within Shared Co-op Pool) — connects_to: ELEM-029, GENRE-018 — why_now: 공유 금고형 협동(ELEM-029)과 소셜 디덕션(GENRE-018)이 각각 카드로 있으나, 같은 협동 자원 풀 안에 숨은 배신자 역할을 얹어 신뢰를 시험하는 결합형 긴장 구조는 두 카드 어디에도 기록되지 않은 빈칸 — obscurity: 높음

## 2026-08-06 23:05 생성 (카테고리: ELEM)
- [done] 단일 타워 직접 조작형 방어 (Single-Tower Skill-Controlled Defense) — connects_to: GAME-050, ELEM-018, GENRE-010 — why_now: GAME-050(Towerful Defense)이 이미 '단일 타워를 스킬로 직접 조작'하는 방식을 쓰지만, 이를 로그라이크 드래프트(ELEM-018)와 구분되는 별도 요소로 다루는 ELEM 카드가 없음 - Brotato식 조작을 TD로 옮긴 하이브리드가 개별 게임을 넘어 요소 자체로 반복될 조짐 (07-31 다이제스트, TD 하이브리드화 흐름) — obscurity: 높음 — ELEM-042
- [ ] 족보 등급별 배수 스코어링 (Poker Hand-Rank Tiered Multiplier Scoring) — connects_to: ELEM-021, ELEM-022, GAME-031, GENRE-013 — why_now: Balatro Wiki 기준 2년 넘게 라이브 지원이 지속되며 "Balatro-like"가 하위장르 용어로 정착(07-31 다이제스트) - 그러나 '족보 등급이 곧 배수가 되는' 구체 스코어링 메커닉 자체를 다루는 ELEM 카드는 없고 ELEM-021·022는 각각 규칙 차용과 지수적 스케일링만 다룸 — obscurity: 낮음
- [done] 스쿼드 동시 조작 자동전투 (Squad Multi-Character Simultaneous Auto-Combat) — connects_to: GENRE-019, GAME-051, GAME-037 — why_now: Yet Another Zombie Survivors가 단일 캐릭터 자동전투라는 서바이버라이크 정의를 벗어나 최대 3인 스쿼드 동시 조작을 도입(07-31 다이제스트) - 이 조작 축 변주 자체를 다루는 ELEM 카드가 없어, 장르 정의의 예외가 요소로는 기록되지 않은 상태 — obscurity: 높음 — ELEM-043
- [ ] AI NPC 멀티모달 실시간 파이프라인 (ASR+SLM+TTS+표정 합성 통합 스택) — connects_to: ELEM-025, ELEM-005, GAME-049, GAME-011 — why_now: NVIDIA ACE가 온디바이스 여부와 무관하게 '음성 인식→소형 언어모델→음성 합성→표정 애니메이션'을 하나로 묶은 파이프라인으로 확산 중(07-27 다이제스트) - ELEM-025는 온디바이스 SLM 자체에 한정돼, 다중 AI 컴포넌트를 잇는 파이프라인 구조 자체는 별도로 기록된 적이 없음 — obscurity: 중간
- [done] 그림다크 추출런 결합 (Grimdark Extraction Hybrid) — connects_to: ELEM-016, ELEM-027, GENRE-009, GENRE-011 — why_now: Mistfall Hunter가 다크 판타지 톤(ELEM-016)과 추출형 런 구조(ELEM-027)를 결합해 오픈베타 43만 명 참여 후 Game Pass 무료 포함 정식 출시(07-27 다이제스트) - 두 요소의 결합 자체가 아직 독립 ELEM으로 기록되지 않은 빈칸(ELEM-041과 같은 조합형 패턴) — obscurity: 중간 — ELEM-044

## 2026-08-05 23:05 생성 (카테고리: GAME)
- [ ] Beast of Reincarnation (다크 판타지 신작) — connects_to: GENRE-009, ELEM-014 — why_now: 2026년 7월 마지막 주 다크 판타지/소울라이크 태그 신작 밀집 출시(07-31) 사례 중 하나 - Mistfall Hunter·Forsaken Realms: Vahrin's Call과 함께 언급됐지만 개별 GAME 카드는 아직 없음 (07-27 다이제스트) — obscurity: 높음
- [done] Rogue Defense: Hybrid Tower TD (로그라이트 TD 하이브리드) — connects_to: GENRE-010, ELEM-018, GAME-050 — why_now: Towerful Defense(GAME-050)와 별개로 같은 주 Google Play에서 업데이트된 사례 - 로그라이트+TD 하이브리드화가 단일 신작이 아니라 장르 차원 흐름임을 보여주는 두 번째 데이터포인트 (07-31 다이제스트) — obscurity: 높음 — GAME-052
- [ ] Disco Elysium (2019, ZA/UM) — connects_to: GENRE-033 — why_now: GENRE-033(CRPG)이 08-04 신설됐으나 GAME-041(발더스 게이트 3) 외에는 이 군집을 실증하는 GAME 카드가 없어, 대사·서사 분기 중심의 또 다른 대표 사례로 간극을 채울 필요 — obscurity: 낮음
- [ ] Dishonored (2012, Arkane Studios) — connects_to: GENRE-032, ELEM-011 — why_now: GENRE-032(이머시브 심)가 08-04 ELEM-011("화학 엔진")의 역사적 원류로 신설됐으나, 이를 실증하는 GAME 카드가 아직 없어 장르 서술이 태그만 있고 사례가 비어 있음 — obscurity: 낮음
- [done] Last Epoch (2024, Eleventh Hour Games) — connects_to: GENRE-034 — why_now: GENRE-034(핵앤슬래시 던전크롤러 ARPG, 시즌제 리그형)가 08-04 신설됐으나 GAME-023(디아블로 IV, 오픈월드형)뿐이라 좁은 던전 반복·시즌 리그가 코어인 정통 사례가 비어 있음 — obscurity: 중간 — GAME-053

## 2026-08-04 23:05 생성 (카테고리: GENRE)
- [done] 이머시브 심 (Immersive Sim) — connects_to: ELEM-011 — why_now: BOTW/TOTK(ELEM-011, 창발적 시스템 상호작용)의 계보상 원류인 이머시브 심 장르(Dishonored, Prey, System Shock류)를 다루는 GENRE 군집 카드가 없어, "화학 엔진" 서술의 역사적 뿌리가 빠져 있음 — obscurity: 높음 — GENRE-032
- [done] CRPG (선택 기반 파티 롤플레잉) — connects_to: GAME-041 — why_now: GAME-041(발더스 게이트 3)이 이미 #crpg 태그로 등록돼 있으나, 이를 묶는 GENRE 군집 카드가 없어 태그만 있고 장르 서술이 비어 있는 간극 — obscurity: 낮음 — GENRE-033
- [ ] PvP 하드코어 서바이벌 크래프팅 (Rust/ARK류) — connects_to: GENRE-020 — why_now: GENRE-020(서바이벌 크래프팅 오픈월드)은 협동(#co-op) 중심 서술만 갖고 있고, 같은 시스템을 플레이어 간 약탈·레이드로 돌리는 PvP 갈래는 서버 경제·공격 손실 같은 별도 시장 궤적을 가져 구분 서술이 필요 — obscurity: 중간
- [ ] 파티 협동 카오스 게임 (Overcooked류) — connects_to: ELEM-031 — why_now: ELEM-031(시각 피드백 과장/Juiciness)이 여러 카드의 재료로만 쓰이고, 시간 압박형 협동 자체가 코어 루프인 파티 게임 GENRE 군집이 비어 있음 — obscurity: 중간
- [done] 핵앤슬래시 던전크롤러 ARPG (시즌제 리그형, 예: Path of Exile류) — connects_to: GAME-023 — why_now: GAME-023(디아블로 IV)이 오픈월드 다크 판타지(GENRE-009)로만 연결돼 있고, 좁은 던전 반복과 시즌제 리그·빌드 메타가 코어인 핵앤슬래시 ARPG 고유 갈래를 다루는 GENRE 카드가 없음 — obscurity: 낮음 — GENRE-034

## 2026-08-03 23:05 생성 (카테고리: GENRE)
- [ ] 접객 서비스 시뮬레이션 (Hospitality / Service Sim) — connects_to: ELEM-035, GENRE-007 — why_now: ELEM-035(접객 서비스 루프)는 카드로 있지만, GENRE-007(코지 심)은 농사·꾸미기 위주 서술이라 손님 응대 루프만의 시장 궤적을 다루는 GENRE 카드가 없음 - 서브컬쳐·라이브서비스 장르가 계속 세분화되는 가운데 코지 계열의 세분화는 아직 비어 있음 — obscurity: 높음
- [ ] 사진 탐험 어드벤처 (Photo Exploration Adventure) — connects_to: ELEM-034, GENRE-008 — why_now: ELEM-034(탐사형 포토그래피 목표 동사)는 있으나, 전투 없는 저스트레스 탐험이 코어인 이 갈래를 GENRE-008(감정 서사 어드벤처)과 구분해 다루는 장르 카드가 없음 - 최근 신설 GENRE가 대전형(MOBA·배틀로얄·CCG)에 쏠려 비전투 탐험 계열이 상대적으로 비어 있음 — obscurity: 높음
- [done] 크리처 노동 자동화 서바이벌 (Creature Labor Automation Survival) — connects_to: ELEM-039, GAME-045 — why_now: GAME-045(Palworld)가 2026-07-10 정식 출시 후 폭발적 판매를 기록했지만, ELEM-039(포획형 동료 노동 시스템)를 코어로 삼아 GENRE-020(서바이벌 크래프팅 오픈월드)과 구분되는 '포획→노동 배치→자동화' 장르 궤적을 다루는 GENRE 카드가 없음 — obscurity: 중간 — GENRE-030
- [done] 무협 근접 액션 배틀로얄 (Wuxia Melee Action Battle Royale) — connects_to: GAME-049, GENRE-022 — why_now: GAME-049(NARAKA: BLADEPOINT)가 NVIDIA ACE AI 팀원 탑재로 재조명됐지만, 총격 중심인 GENRE-022(배틀로얄)와 조작 축 자체가 다른 근접 무협 액션 배틀로얄을 별도로 다루는 장르 카드가 없음 — obscurity: 중간 — GENRE-031
- [ ] AI 코멘터리 동반 게임 (AI Commentary Companion Genre) — connects_to: ELEM-041, ARCH-007 — why_now: ELEM-041 카드 자체가 "아직 어떤 게임도 완성하지 못한 빈칸"으로 명시돼 있고 ARCH-007(해설자 파이프라인)까지 구현 아키텍처가 문서화된 상태 - 이 조합을 상용 코어 판매 포인트로 삼는 장르가 실제로 형성되는지 추적할 GENRE 카드가 필요 — obscurity: 높음

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
