+++
card_id = "ELEM-006"
type = "tech"
title = "AI 기반 심문 (AI-driven interrogation)"
summary = "미리 쓴 대사가 아니라 실시간 생성 AI가 등장인물을 움직여 플레이어의 질문에 즉석으로 답하게 하는 방식"
tags = ["AI", "dialogue", "local-llm", "divisive"]
updated = 2026-07-16
confidence = "medium-low"   # 조합 궁합 근거 없음 + AI Interrogation Simulator는 미출시로 유저 반응 근거 없음
+++
## 정의
인공지능(AI)이 게임 속 등장인물을 실시간으로 움직여서, 플레이어가 무엇을 물어보든 그때그때 다르게 대답하게 만드는 방식입니다. 미리 정해진 대사가 아니라 AI가 즉석에서 답을 만들어냅니다. 이 방식을 쓰는 게임은 여러 개가 따로 존재하는데, 이 카드는 그중 대표적으로 확인된 두 게임(Verbal Verdict, AI Interrogation Simulator)을 근거로 작성되었습니다 [출처: Steam store page].

## 성공 사례
- Verbal Verdic - 로컬(오프라인) LLM으로 작동하도록 만들어졌고, 개발사는 이를 플레이어 개인정보 보호와, 향후 서버가 닫히더라도 게임을 계속 즐길 수 있게 하는 보존 목적이라고 설명함 [출처: Beehaw (404 Media re-post/discussion)]. 한 리뷰에서는 이 게임을 생성형 AI를 가장 잘 구현한 사례 중 하나로 평가함 [출처: 404 Media]. 커뮤니티에서는 별도 설정 없이 로컬 LLM이 바로 작동한다는 점을 들어, 정식 출시 시 반드시 사야 할 게임이 될 것 같다는 반응이 있었음처: Steam Community].
- 한 업계 보고서는 Verbal Verdict를 실시간 온디바이스(로컬) LLM 대화를 상용화 단계에서 보여준 초기 사례 중 하나로 소개함 [출처: Hartmann Capital Q3 2025 report].

## 실패 사례
- Verbal Verdict - AI가 만들어내는 대사가 때때로 뒤죽박죽(gibberish)한 결과를 내놓았고, 캐릭터별 목소리도 L.A. Noire나 Ace Attorney 같은 손으로 직접 쓴 게임들만큼 차별화되지 못했다는 평가를 받음 [출처: 404 Media]. 이후 업데이트에서 캐릭터 음성을 들으려면 월 구독료를 내야 하도록 바뀌었고, 상호작용 조작(UI)에 대한 불만도 제기됨 [출처: Steam Community]. 조사 시점 기준 마지막 개발자 업데이트가 2년 넘게 이루어지지 않아, 앞서 언급된 로드맵이나 일정이 이미 바뀌었을 수 있음 [출처: Steam].
- AI Interrogation Simulator - 조사 시점 기준 아직 출시되지 않은 "출시 예정(Coming soon)" 상태로 유저 리뷰가 존재하지 않음 [출처: Steam store page]. 게임을 실행하려면 플레이어가 자신의 AI 계정(OpenAI, Anthropic, 또는 로컬 모델 중 선택)을 직접 연결해야 함 [출처: Steam (developer description)]. 이는 진입 장벽으로 작용할 수 있음 [해석].

※ Verbal Verdict는 성공·실패 근거가 모두 확인되므로 복합적(Mixed) 사례로 분류함 [해석].

## 유저 반응 요약
- 선호: 별도 설정 없이 로컬 LLM이 바로 작동한다, 정식 출시되면 반드시 사야 할 게임이다 [출처: Steam Community]
- 선호: 생성형 AI 대화를 가장 인상 깊게 구현한 사례라는 평가 [출처: 404 Media]
- 불호: AI 대사가 가끔 뒤죽박죽해진다, 캐릭터 목소리가 밋밋하다 [출처: 404 Media]
- 불호: 음성을 들으려면 월 구독료가 생겼다, 조작(UI)이 불편하다 [출처: Steam Community]

## 조합 궁합
<!-- No evidence: JSON 근거 자료에 ELEM-006과 다른 요소 간의 조합 관련 서술이 없음 -->

## 리스크
- [해석] 실시간 생성 AI 대사는 예측이 불가능해, 게임의 톤이나 의도와 다른 방향으로 흐를 위험이 있음 (Verbal Verdict의 뒤죽박죽 사례가 근거).
- [해석] 외부 AI 계정을 요구하는 구조는 진입 장벽을 높이고, 해당 서비스가 중단되면 게임 자체를 즐길 수 없게 만들 위험이 있음 (AI Interrogation Simulator 사례).
- 부가 수익화(월 구독료) 도입이 유저 불만으로 이어질 수 있음 [출처: Steam Community].
