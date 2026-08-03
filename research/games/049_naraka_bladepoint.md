+++
card_id = "GAME-049"
type = "success"
title = "NARAKA: BLADEPOINT (2021, 24 Entertainment / NetEase Games)"
summary = "온디바이스 NVIDIA ACE AI 팀원(Viper)을 실제 출시 빌드에 탑재한 무협 배틀로얄"
genres = ["GENRE-022", "GENRE-031"]
elements = ["ELEM-025"]
tags = ["battle-royale", "ai-native", "voice-npc", "wuxia", "live-service", "cross-play"]
updated = "2026-08-01"
confidence = "medium"
+++
## 한 줄 요약 + 판매·리뷰 수치
- 사실: 24 Entertainment가 개발하고 NetEase Games가 서비스하는, 최대 60인이 겨루는 무협 액션 배틀로얄이다 [출처: Wikipedia/Steam 페이지, 2026-07 확인].
- 사실: Steam 유저 리뷰 약 30만 1,739건 중 73% 긍정("대체로 긍정적") [출처: Steambase 집계, 2026-07-31 기준].
- 사실: 일일 활성 이용자 100만 명 이상으로 보도되나, Steam 동시 접속자는 약 4만 1,111명 수준이다 [출처: 업계 보도 종합/steam-stats.com, 2026 확인].
<!-- 증거 부족: 일일 100만 명 수치가 모바일·PC·콘솔 중 어느 범위를 합산한 것인지 원출처를 확인하지 못함 -->

## 사용한 요소
- ELEM-025 (온디바이스 SLM 실시간 음성 대화 NPC) - NARAKA: BLADEPOINT 모바일 PC 버전에 2026-03-27 NVIDIA ACE 기반 온디바이스 AI 팀원 'Viper'가 추가됐다. ACE 음성 인식이 플레이어의 음성 지시를 알아듣고, 소형 언어모델이 판단해 적 태그 지정·전황 보고 같은 행동을 스스로 실행한다 [출처: NVIDIA GeForce News/wccftech, 2026 확인].

## 성공/실패 원인
- 사실: Viper는 파티에 합류해 함께 싸우고, 필요한 아이템을 찾고, 장비를 교체하고, 스킬 선택을 제안하는 등 전투·파밍을 능동적으로 수행한다고 보도됐다 [출처: NVIDIA GeForce News, 2026 확인].
- 사실: 이 기능은 GAME-011(inZOI)과 함께 "NVIDIA ACE가 데모를 넘어 실제 출시 빌드에 탑재된" 대표 사례로 거론된다 [출처: NVIDIA GeForce News/PCGamer, 2026-07 확인].
- [해석] inZOI가 텍스트·내면 시뮬레이션 자체가 코어인 것과 달리, NARAKA는 이미 검증된 PvP 배틀로얄 위에 AI 팀원을 보조 기능으로 얹었다 - GENRE-003(AI 네이티브 게임)처럼 "AI를 빼면 게임이 성립하지 않는" 구조와는 채택 경로가 다르다.
<!-- 증거 부족: Viper 기능 자체에 대한 유저 반응(리뷰·커뮤니티) 집계는 확인하지 못했다. 위 73% 긍정 수치는 게임 전체 리뷰이며 이 기능 도입 전후를 구분하지 못한다 -->

## 우리 프로젝트 시사점
[해석] 온디바이스 SLM 음성 NPC(ELEM-025)를 게임의 정체성 자체로 새로 설계하지 않고, 이미 성립된 게임에 보조 기능(파티원 AI)으로 얹는 채택 경로가 실제로 존재함을 보여준다. 코어 루프를 새로 짜는 리스크 없이 AI 기능을 검증하고 싶다면, 이런 "보조 역할 삽입" 방식이 진입 장벽이 더 낮을 수 있다.
