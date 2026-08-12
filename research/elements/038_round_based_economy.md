+++
card_id = "ELEM-038"
type = "mechanic"
title = "라운드제 경제 시스템 (Round-based Economy / Buy System)"
summary = "라운드가 끝날 때마다 성적에 따라 돈을 받고, 다음 라운드 시작 전 그 돈으로 장비를 사는 구조"
tags = ["tactical-shooter", "economy", "esports", "round-based", "pvp"]
updated = "2026-08-01"
confidence = "high"
+++
## Definition
라운드가 끝날 때마다 이긴 정도(승패, 처치)에 따라 돈을 받고, 다음 라운드가 시작하기 전에
그 돈으로 무기와 장비를 사는 구조입니다. 지난 라운드를 못 챙기면 다음 라운드도 가난하게
시작해서 계속 밀리는 눈덩이 효과가 생깁니다.

## Success Cases
- GAME-042 (Counter-Strike 2) - 리뷰 85% 긍정(9.7M+ 리뷰), 2026-07 기준 30일 평균 동시접속 약 92만 명 [source: Steambase, 2026-07 확인]. 20년 넘게 이어진 프랜차이즈의 핵심 정체성.

## Failure Cases
<!-- 증거 부족: 이 요소만 따로 원인이 되어 실패한 carded 사례를 확인하지 못함 -->

## User Reaction Summary
- 선호: [interpretation] "돈 관리 자체가 하나의 게임"이라는 전략성이 자주 호평받는다.
- 불호: CS2 출시 초기(2023-09) subtick 판정 불일치로 "돈 계산은 맞는데 총알 판정은 안 믿긴다"는 불만이 나왔다 [source: Forbes/CSMARKET 보도, 2023-09 기준].

## Synergy
- 장르 앵커: GENRE-023 (택틱컬 라운드제 슈터) - 이 군집이 이 요소를 구성 요소로 지목한다.
- [interpretation] 나쁨: ELEM-033 (동적 난이도 조절) - 팀 실력 격차를 인위적으로 보정하면 "돈 관리 전략"이라는 정체성 자체가 무의미해진다.
- [interpretation] 좋음: ELEM-036 (영웅 픽/밴 드래프트) - 둘 다 "판마다 자원 배분 결정이 승패를 가른다"는 설계 철학을 공유해 하이브리드 장르 실험의 재료가 될 수 있다.

## Risks
- [interpretation] 신규 유저 진입장벽 - 경제 관리 실수 하나가 라운드 전체를 망칠 수 있어 학습 곡선이 매우 가파르다.
- [interpretation] 무기 가격 밸런스 패치가 프로 씬과 캐주얼 씬에 다르게 작용해 논쟁이 잦다.
