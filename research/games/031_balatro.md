+++
card_id = "GAME-031"
type = "success"
title = "Balatro (2024, LocalThunk / Playstack)"
summary = "누구나 아는 포커 족보를 바탕으로 쓰고 그 위에 조커 조합을 얹어, 익명 1인 개발로 500만 장을 판 로그라이트"
genres = ["GENRE-013", "GENRE-012"]
elements = ["ELEM-021", "ELEM-022", "ELEM-020"]
tags = ["roguelite", "deckbuilder", "poker", "solo-dev", "indie", "rating-controversy", "broad-appeal"]
updated = "2026-07-29"
confidence = "medium"
+++
## Summary and Sales/Review Metrics
익명 1인 개발자 LocalThunk가 만들고 Playstack이 퍼블리싱해 2024년 2월 20일 출시 [source: GameSpot,
2024 기준]. 출시 첫 몇 시간 매출이 60만 달러를 넘겼고 [source: GamesRadar+, 2024 기준], 50만 장까지
10일이 걸린 뒤 100만 장을 돌파했다 [source: GameSpot, 2024 기준]. 2024년 12월 초 350만 장이었다가
The Game Awards 2024 올해의 게임 후보에 오른 뒤 노출이 늘어 전 플랫폼 누적 500만 장을 넘겼다
[source: Game Developer, 2024년 12월 기준]. 모바일판은 2025년 1월 기준 인앱 결제 매출 900만 달러
이상을 기록했다 [source: Statista, 2025-01 기준].
The Game Awards 2024에서 5개 부문 후보에 올라 Best Independent Game, Best Debut Indie Game,
Best Mobile Game 3개를 수상했다 [source: GameSpot, 2024 기준].

## Elements Used
- ELEM-021 (친숙한 규칙 차용) - 포커의 시각 언어를 그대로 쓰되, 사람을 밀어낼 수 있는 실제 포커나
  텍사스 홀덤의 규칙에는 의존하지 않는다 [source: GameSpace 분석 기사, 2026-07 확인]. LocalThunk는
  표준 트럼프 카드가 거의 모든 문화권에 퍼져 있고 사람들이 카드를 정렬하고 배치하며 전략을 생각하기
  좋아한다는 점을 활용했다고 밝혔다 [source: Rogueliker 인터뷰, 2026-07 확인].
- ELEM-022 (지수적 점수 스케일링) - 150종의 조커 카드가 각자 다른 방식으로 점수에 개입하고
  [source: PCGamesN, 2024 기준], 리트리거가 중첩되는 구조를 통해 수백만 점 단위까지 점수가 폭발한다
  [source: kokutech 디자인 분석, 2026-07 확인].
- ELEM-020 (덱 구축) - 한 판 동안만 유지되는 덱을 카드·조커 획득으로 키워간다.

## Success/Failure Drivers
- 사실: 개발의 출발점은 어릴 때 친구들과 하던 광둥식 카드 게임 Big Two였고, 이것이 발전해 Balatro가
  됐다 [source: Rogueliker 인터뷰, 2026-07 확인]. 슬롯머신 로그라이트 Luck Be a Landlord를
  스트리머 Northernlion의 방송으로 접한 것도 직접적 영감이었다 [source: 검색 결과 종합(장르 정리 기사),
  2026-07 확인].
- [interpretation] 규칙을 새로 발명하지 않고 이미 아는 것에서 시작했기 때문에 튜토리얼 부담이 거의 없다. 1인
  개발이 감당 가능한 범위에 들어온 결정적 이유로 보인다.
- 사실: 플레이어는 조커 조합이 서로 어떻게 상호작용하는지 패턴을 익히게 되고, 그 지점부터 게임이
  운이 아니라 통제된 최적화처럼 느껴지면서 장기 재플레이성이 생긴다 [source: kokutech 디자인 분석,
  2026-07 확인].
- 사실: 2024년 3월 PEGI가 등급을 3+에서 18+로 올리면서 "두드러진 도박 이미지와 도박을 가르치는
  내용을 담고 있다"고 판단했고, 그 여파로 유럽 여러 나라의 콘솔 디지털 스토어에서 한동안 내려갔다
  [source: 검색 결과 종합(GameSpot·TheGamer 등 보도), 2024 기준]. 게임에는 마이크로트랜잭션도
  페이투윈 요소도 없다 [source: 같은 보도 종합, 2024 기준].
  실패 지점: 빌린 규칙에는 그 규칙의 사회적 맥락이 함께 딸려 온다. 실제 도박 요소가 없어도 심의는
  화면에 보이는 것으로 판단했다.
- 사실: 퍼블리셔 측이 제출한 이의신청이 받아들여져 PEGI 불만처리위원회가 등급을 12+로 재분류했고,
  PEGI는 모든 게임에 대한 모의 도박 관련 정책을 재검토하겠다고 밝혔다 [source: BBC News / focusgn 보도,
  2024 기준]. LocalThunk는 실제 도박 메커닉이 있는 게임이 3+를 받는 현실을 들어 기준을 비판했다
  [source: GameSpot, 2024 기준].
<!-- 증거 부족: Steam 리뷰 건수·긍정률은 이번 조사에서 확정 수치를 확인하지 못함 -->

## Implications for Our Project
1인 개발 규모에서 "가르치지 않아도 되는 규칙"을 고르는 것은 콘텐츠 제작비를 직접 줄이는 선택이다
[interpretation]. 다만 그 규칙이 도박·사행성과 연결돼 있으면 등급 심의라는 예측 못 한 비용이 붙는다 - Balatro는
이겼지만 그 사이 유럽 콘솔 판매가 멈췄다 [interpretation]. 친숙한 규칙을 빌릴 거라면 도박 계열이 아닌 쪽
(보드게임·전통 놀이 등)이 같은 이점을 규제 비용 없이 가져갈 수 있다 [interpretation]. GENRE-013의 빈칸 참조.
