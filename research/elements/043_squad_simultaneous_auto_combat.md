+++
card_id = "ELEM-043"
type = "mechanic"
title = "스쿼드 동시 조작 자동전투 (Squad Multi-Character Simultaneous Auto-Combat)"
summary = "서바이버라이크의 단일 캐릭터 자동전투 관례를 벗어나, 한 명의 플레이어가 여러 캐릭터를 동시에 지휘하며 각 캐릭터는 스스로 공격하게 만드는 조작 구조"
tags = ["survivors-like", "bullet-heaven", "squad", "auto-combat", "control-variant", "emerging"]
updated = "2026-08-06"
confidence = "medium"
+++
## Definition
서바이버라이크(불릿 헤븐) 게임은 보통 캐릭터 한 명만 조종합니다. 캐릭터는 알아서
공격하고, 플레이어는 움직여서 피하고 업그레이드만 고르면 됩니다. 이 요소는 그
캐릭터를 한 명이 아니라 여러 명으로 늘린 방식입니다. 여러 캐릭터가 동시에 화면에
있고, 각자 알아서 공격하지만, 플레이어는 이들을 하나의 무리(스쿼드)처럼 함께
지휘합니다. GAME-037(Vampire Survivors)이 세운 "단일 캐릭터 자동전투" 표준에서
캐릭터 수라는 축만 바꾼 변주입니다.

## Success Cases
- GAME-051 (Yet Another Zombie Survivors) - 최대 3인 스쿼드까지 동료를 영입해 함께
  조작. Steam 리뷰 4,745건 중 94% 긍정, 최근 30일 152건 중에서도 94% 긍정 유지
  [source: Steam, 2026-08 확인].
- Entropy Survivors - 강력한 메카와 저격 개구리 두 캐릭터를 동시에 조작하는 불릿
  헬 로그라이크. 능력·무기 커스터마이징 결합 [source: bulletheavengames.com 장르 정리
  웹 검색 종합, 2026-08 확인].

## Failure Cases
<!-- 증거 부족: 스쿼드 동시 조작 자체가 원인으로 지목된 실패·혹평 사례는 조사 중
확인하지 못함. 아래는 이 조작 방식이 안고 있는 긴장을 보여주는 커뮤니티 신호임 -->
- [interpretation] 커뮤니티 일각에서는 "각 캐릭터가 알아서 조준·발사하니 전략적 손맛이 약하다"며
  수동 조작·발사를 요청하는 목소리가 있었다 [source: Steam 커뮤니티 토론 "Manual
  Control", Yet Another Zombie Survivors, 2026-08 확인].

## User Reaction Summary
- 선호: "조작은 단순한데 화면은 스쿼드로 꽉 찬다"는 반응 - 복잡한 컨트롤 없이
  전략적 깊이만 더했다는 평가 [source: Steam 리뷰 종합, 2026-08 확인].
- 불호: 일부 유저는 자동 조준이 아니라 직접 조준·발사를 원함. 다른 유저는 평균
  반응속도로는 다중 캐릭터를 수동 추적하기 어려워 자동이 낫다고 반박함 [source: Steam
  커뮤니티 토론, 2026-08 확인].

## Synergy
- 좋음: GENRE-019 (서바이버라이크) - 이 요소가 "단일 캐릭터 자동전투"라는 장르 정의의
  예외·변주 축을 형성함.
- 나쁨: 지수적 점수 스케일링(ELEM-022)과 결합할 때 캐릭터 수만큼 화면 이펙트가
  중첩돼, 가독성이 급격히 떨어질 위험이 있다 - 시각 피드백 과장(ELEM-031)과
  함께 쓸 때 절제가 특히 필요하다.

## Risks
- [interpretation] 캐릭터 수가 늘수록 화면 정보량이 많아져, 장르의 핵심 매력인 "단순한 조작"이
  희석될 위험이 있다.
- [interpretation] 자동전투를 유지하는 한 각 캐릭터의 개성은 스탯·룩 차이로만 드러나, 늘어난
  캐릭터 수만큼 콘텐츠 제작 비용이 커진다.
