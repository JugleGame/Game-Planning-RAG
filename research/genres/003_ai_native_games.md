+++
card_id = "GENRE-003"
type = "genre"
title = "AI 네이티브 게임 (AI-native Games)"
summary = "실시간 AI 생성이 게임의 코어 메커닉인 형성 초기 군집"
elements = ["ELEM-005"]
example_games = ["GAME-010", "GAME-011"]
tags = ["ai-native", "emerging", "fragile", "high-cost"]
updated = "2026-08-01"
confidence = "medium"            # 군집 자체가 형성 초기 - 신호 변동 큼, 주간 추적 필수
+++
## Components
- ELEM-005 (AI 통합) - 군집의 정의 그 자체. AI를 빼면 게임이 성립하지 않는 작품들.

## Market Saturation
극초기. 유의미 사례가 GAME-010 (Suck Up! - 바이럴 후 Mixed 60%), GAME-011
(inZOI - 100만 장 후 동접 98% 감소) 수준이며, 둘 다 mixed - **순수 성공작이
아직 없음** [source: 각 GAME 카드]. 플랫폼 차원의 인프라화는 진행 중(NVIDIA ACE
등 온디바이스 모델 보급) [source: NVIDIA 발표, 2025-03]. 경쟁 밀도는 낮고
진입 기회는 크지만, 품질 하한선을 못 지킨 작품부터 도태되는 중. Steam 상
AI 콘텐츠 공개 게임은 약 7,300~9,400건(2026-03 기준)까지 급증했으나, 이 중
inZOI류의 "플레이어 대상 실시간 AI 생성"을 코어 메커닉으로 쓰는 진짜
AI-네이티브 게임은 극소수로 보도됨 [source: 다이제스트 2026-07-20 /
Tom's Hardware·SteamDB 집계, 2026-03 기준] - 태그 확산과 실제 코어 메커닉
채택 사이의 격차가 유지되고 있음을 시사 [interpretation].
NVIDIA ACE(음성 인식+소형 언어모델 Nemotron+신경망 TTS+Audio2Face 결합)가 inZOI·NARAKA: BLADEPOINT 등에서 데모 단계를 넘어 실제 출시 빌드로 탑재되기 시작했고, Krafton·Creative Assembly 등 복수 스튜디오가 채택 중 [source: NVIDIA GeForce News/PCGamer, 2026-07 확인 / 다이제스트 2026-07-27]. [interpretation] "플랫폼 차원의 인프라화 진행 중"이라는 기존 서술이 데모→실제 출시로 한 단계 더 구체화되는 신호.
AI 공개(disclosure) 표시 신작 비율이 2024-01 공개 의무화 시행 초기 10.9%에서 2025년 동시점 19.9%, 2026년 상반기 약 30%로 상승 - 표시 신작 출시 빈도도 의무화 이전 월 약 13건에서 월 약 530건 수준으로 늘어남 [source: Steam AI 공개 데이터 분석(Substack "Three years of AI on Steam" 재인용 보도), 2026년 상반기 기준 / 다이제스트 2026-07-14(재조사 2026-07-27)]. [interpretation] 태그 채택 자체는 계속 가속하고 있어, 실제 코어 메커닉 채택과의 격차가 좁혀지는지 다음 다이제스트에서 계속 추적 필요.
## Conventions and Expectations
- 아직 관례가 형성 중 - 유저 기대의 최소선만 확인됨: 지연 없는 반응, 기억 유지(이전 대화·행동을 잊지 않기), AI 티 안 나는 말투 [source: GAME-010 리뷰 불만 / GAME-011 보도]
- 대본 기반 걸작과의 비교가 기본값 - "AI인데 이 정도"는 면죄부가 안 됨 [interpretation]
- 생성 AI에 대한 반감 여론이 상수로 존재 - 사용 사실 자체가 논란이 될 수 있음 [source: GAME-011 커뮤니티 논란]
- 안정성·기본기(핵심 시뮬레이션 완성도)가 새로운 기대치로 편입되는 신호 확인 -
  inZOI가 신규 기능 확장보다 안정화를 우선하는 'Fundamentals First' 기조로
  전환하자 커뮤니티 반응이 "비어있다"는 비판에서 방향성 지지로 바뀜
  [source: 다이제스트 2026-07-20 / inZOI 공식 로드맵 공지, 2026-07-04 기준]

## Gaps
[interpretation] ★ 현존 사례의 AI 역할은 두 가지뿐: "설득 대상"(GAME-010 - 플레이어가
AI에게 말을 검) 또는 "자율 시뮬레이션"(GAME-011 - AI들끼리 살아감). 세 번째
역할인 "관찰자/해설자"(AI가 플레이어의 플레이를 보고 말을 걺)는 게임 형태로
미점유 - 우리 프로젝트의 조준점. ELEM-002+003+005 조합의 실행 무대가 이 군집.
이 결합 자체를 종합한 카드가 ELEM-041(AI 관찰자/해설자 결합)이다.
- 확인 방법: Steam 'Artificial Intelligence' 태그 신작 전수 확인 + AI 게임 쇼케이스 보도
- 확인일: 2026-07-15 / 재확인 주기: 격주 (형성기 군집이라 가장 빠르게 변함)