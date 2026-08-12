+++
card_id = "GAME-029"
type = "success"
title = "Warframe (2013, Digital Extremes)"
summary = "규제가 강제하기 전에 전체 드롭 테이블을 자발적으로 공개해 확률 투명성을 브랜드로 만든 부분유료 루트 슈터"
genres = ["GENRE-011"]
elements = ["ELEM-019"]
tags = ["looter-shooter", "free-to-play", "transparency", "drop-table", "live-service", "long-tail"]
updated = "2026-07-29"
confidence = "medium"
+++
## Summary and Sales/Review Metrics
2013년 PC로 출시된 부분유료 루트 슈터로, 2026년 7월 기준 누적 등록 플레이어 8,500만 명 이상을 기록했다
[source: Digital Extremes TennoCon 공식 보도자료(Business Wire), 2026-07-11 기준]. 같은 보도자료 기준
서비스 14년차이며 플레이 가능한 워프레임 60종 이상, 행성 18곳 이상과 오픈월드 4곳을 운영 중이다
[source: Digital Extremes 보도자료, 2026-07-11 기준].
<!-- 증거 부족: 매출 수치는 비공개 회사 추정치만 확인돼 카드에 싣지 않음 -->

## Elements Used
- ELEM-019 (무작위 전리품 드롭 & 루트 테이블) - 임무·유물·적 처치 등 대부분의 획득 경로가 확률 테이블로
  구성돼 있고, Digital Extremes는 그 테이블 전체를 공식 사이트(warframe.com/droptables)에 게시한다
  [source: WARFRAME Wiki 'Drop Tables' 문서, 2026-07 확인]. 이 페이지는 게임 내부 데이터에서 자동 생성된다
  [source: WARFRAME Wiki, 2026-07 확인].

## Success/Failure Drivers
- 사실: 2017년 7월, Digital Extremes는 모든 전리품의 드롭 확률표를 공개하면서 자신들이 이런 자료를
  올린 첫 개발사라고 밝히고 "흐름을 만들고 싶다(start a trend)"고 말했다 [source: Massively Overpowered,
  2017-07-04 기준]. 회사는 "커뮤니티와의 투명성에 새로운 기준을 세우고, 플레이어에게 보상이 배정되는
  과정을 더 보여주고 싶다"는 취지를 밝혔다 [source: PC Gamer / WARFRAME Wiki 인용 종합, 2026-07 확인].
- 사실: 공개 당시 배경으로 중국이 확률 공개를 의무화하는 법을 통과시켰고 Blizzard 등 다른 퍼블리셔가
  확률을 공개하기 시작한 흐름이 있었다 [source: 검색 결과 종합(TechRaptor·PSU 등 보도), 2026-07 확인].
- [interpretation] 규제가 자기 시장에 도착하기 전에 먼저 공개했다는 점이 핵심이다. 같은 정보를 나중에 강제로
  공개하면 "들켜서 공개한 것"이 되지만, 먼저 공개하면 브랜드 자산이 된다. GAME-025(메이플스토리 큐브)가
  정확히 반대편 사례다.
- 사실: 다만 회사는 이 자료가 게임의 복잡성 때문에 "완전하지 않으며" 정확성을 보장하지 않는다고 명시했고,
  아이템이 미리 노출되는 것을 막기 위해 모든 핫픽스마다 갱신하지는 않는다 [source: WARFRAME Wiki 'Drop
  Tables' 문서, 2026-07 확인].
  약점: "공개했다"와 "항상 최신이다"는 다르다. 공개 자체가 신뢰를 만들지만 갱신 지연은 여전히 불신의
  씨앗으로 남는다.
- 사실: 공식 데이터를 커뮤니티가 파싱하기 쉬운 형태로 재가공한 외부 도구(WFCD/warframe-drop-data,
  drops.warframestat.us)가 유지되고 있다 [source: 해당 저장소·사이트, 2026-07 확인].
- [interpretation] 확률을 공개하면 커뮤니티가 그 위에 도구를 얹어 정보 생태계를 대신 만들어준다. 개발사가 직접
  만들지 않아도 되는 유지 비용을 커뮤니티가 흡수하는 셈이다.

## Implications for Our Project
확률을 공개하는 것은 손해가 아니라 신뢰 장치다 [interpretation]. 다만 공개하기로 했다면 갱신 주기까지 함께
약속해야 한다 - Warframe도 "완전하지 않다"는 단서를 달았고, 이것이 남는 불신의 지점이다 [interpretation].
확률을 숨겼다가 제재로 이어진 GAME-025와 대조해서 볼 것.
