+++
card_id = "GAME-030"
type = "success"
title = "Slay the Spire (2019, Mega Crit)"
summary = "전투마다 제시된 카드 중 하나만 골라 덱을 키워가는 구조로 로그라이크 덱빌더라는 군집 자체를 만들어낸 원형작"
genres = ["GENRE-012"]
elements = ["ELEM-020", "ELEM-018"]
tags = ["roguelike", "deckbuilder", "randomness", "indie", "replayability", "broad-appeal"]
updated = "2026-07-29"
confidence = "medium"
+++
## Summary and Sales/Review Metrics
2017년 말 얼리액세스로 공개돼 2019년 1월 정식 출시된 인디 로그라이크 덱빌더 [source: GameShub 장르
분석 기사, 2026-07 확인]. PC·콘솔 합산 1,000만 장을 넘겼다 [source: Alinea Analytics, 2026-03-20 기준].
Steam 유저 리뷰 194,000건 이상 중 97% 긍정 [source: Notebookcheck 세일 보도, 2026-07 확인].
속편 Slay the Spire 2는 2026년 3월 5일 25달러 얼리액세스로 출시돼 2주 만에 460만 장 / 9,200만 달러
이상을 기록했고, 3월 14~15일 주말 최고 DAU 220만 명, 리뷰 94% 긍정을 남겼다 [source: Alinea Analytics,
2026-03-20 기준].

## Elements Used
- ELEM-020 (덱 구축) - 약한 시작 덱에서 출발해 전투가 끝날 때마다 카드를 한 장씩 더해 자기만의 덱을
  완성해 가는 구조 [source: Eneba 리뷰 기사, 2026-07 확인].
- ELEM-018 (로그라이크 무작위 업그레이드/경로 드래프트) - 매 판이 달라지는 이유는 지도 상의 도전 순서,
  무작위로 제시되는 카드 보상 중의 선택, 그리고 예측 불가능한 유물 획득이다 [source: Eneba 리뷰 기사,
  2026-07 확인].

## Success/Failure Drivers
- 사실: 각 판은 고유한 시드로 생성되며, 데일리 클라임 모드는 이 시드를 전 플레이어가 공유해 지도 배치,
  카드 보상, 유물 드롭, 이벤트 결과가 모두 동일하게 나온다 [source: Slay the Spire Wiki 'Daily Climb'
  문서, 2026-07 확인].
- [interpretation] 무작위 게임의 고질적 불만인 "쟤는 운이 좋았을 뿐"을 시드 공유로 없앤 것이 핵심이다. 같은 패를
  받고도 결과가 다르면 그 차이는 실력으로만 설명되므로, 무작위성을 유지한 채 경쟁 구도를 만들 수 있다.
- 사실: 한 판을 끝낼 때마다 다음 승천(Ascension) 난이도가 해금되고, 각 단계는 적 강화·엘리트 증가·물약
  슬롯 감소·상점 가격 상승 같은 구체적 변형을 하나씩 얹는다 [source: Eneba 리뷰 기사, 2026-07 확인].
- [interpretation] 클리어가 끝이 아니라 다음 잠금을 여는 열쇠가 되는 구조라, 콘텐츠를 새로 만들지 않고도 플레이
  시간을 늘린다. 인디 규모에서 특히 비용 효율이 높은 방식이다.
- 사실: 속편 기준으로 플레이어의 50% 이상이 20시간을 넘겼고, 14%가 50시간 이상, 1%가 100시간 이상을
  기록했다 [source: Alinea Analytics, 2026-03-20 기준].
- 사실: 속편의 2주 매출은 Hollow Knight: Silksong(8,300만 달러)과 Hades II(8,200만 달러)의 Steam 누적
  매출을 이미 넘어섰다 [source: Alinea Analytics, 2026-03-20 기준].
<!-- 증거 부족: Mega Crit이 직접 밝힌 설계 의도 진술은 이번 조사에서 확인하지 못함 -->

## Implications for Our Project
무작위성을 쓰면서도 "운 탓" 논란을 피하고 싶다면, 확률을 손보는 것보다 **같은 시드를 공유하게 만드는
쪽**이 더 싸고 확실하다 [interpretation]. 또한 승천 구조처럼 난이도 잠금을 단계적으로 여는 방식은 신규 콘텐츠
없이 플레이 시간을 늘리는 인디용 해법이다 [interpretation]. GAME-027(Rogue Tower)의 "불공평한 도박" 불만과
정확히 대비되는 지점이다.
