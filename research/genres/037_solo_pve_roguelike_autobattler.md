+++
card_id = "GENRE-037"
type = "genre"
title = "솔로 PvE 로그라이크 오토배틀러 (Solo PvE Roguelike Auto-battler)"
summary = "런 기반 무작위 드래프트로 유닛·장비를 배치만 하고 전투 자체는 자동으로 흘러가는, 상대가 다른 플레이어가 아니라 AI 몬스터/웨이브인 1인 PvE 하이브리드 군집"
elements = ["ELEM-018", "ELEM-022", "ELEM-004"]
example_games = ["GAME-055"]
tags = ["auto-battler", "roguelike", "pve", "solo", "draft", "singleplayer", "emerging"]
updated = "2026-08-09"
confidence = "medium"
+++
## 구성 요소
- ELEM-018 (로그라이크 무작위 업그레이드/경로 드래프트) - 매 판·매 라운드마다 무작위로 제시되는 유닛·장비·유물 중에서 골라 쌓아가는 런 기반 선택 구조가 이 군집의 진입 축이다. GENRE-012(로그라이크 덱빌더)와 드래프트 문법 자체는 공유한다.
- 배치-후-방치(place-and-forget) 전투 - 유닛/장비를 슬롯에 배치하는 준비 페이즈까지만 플레이어가 개입하고, 전투 페이즈에는 GENRE-027(오토배틀러)처럼 조작이 없다. 다만 그 전투의 상대가 다른 플레이어의 팀이 아니라 AI가 짠 몬스터·웨이브라는 점이 GENRE-027과 가르는 지점이다. Tales & Tactics는 Steam 태그에 "Auto Battler"와 "PvE"를 동시에 달고 "no time limits, no pressure"의 싱글플레이 모험으로 소개된다 [출처: Steam 상점 페이지 태그 및 소개문, 2026-08 확인].
- ELEM-022 (지수적 점수 스케일링) - 배치한 유닛·장비 조합이 곱해지며 전투력이 후반으로 갈수록 폭발적으로 불어나는 설계가 GENRE-027과 마찬가지로 이 군집의 스노우볼을 만든다.
- ELEM-004 (반복 메커닉) - 런이 끝나면(사망 또는 클리어) 처음부터 다시 드래프트를 짜는 로그라이크 순환이 GENRE-012와 공유하는 반복 축이다.
- [해석] GENRE-027·GENRE-012와 가르는 정확한 경계선은 "누구와 싸우는가"다: GENRE-027은 다른 플레이어(또는 그 스냅샷)와 겨루는 PvP, GENRE-012는 플레이어가 매 턴 능동으로 조작하는 전투, 이 군집은 AI가 짠 적을 상대로 배치만 하고 지켜보는 PvE다.
- [해석] 조사 중 확인한 중요한 정정: 스카우트 메모가 예시로 든 Backpack Battles는 실제로는 순수 PvE가 아니라 **비동기 PvP** 오토배틀러다. 배치까지는 혼자 하지만 전투 상대는 다른 플레이어가 최근에 짠 가방이며, 최후 1인이 남을 때까지 겨루는 방식이다 [출처: ResetEra 게시판 제목("Asynchronous PvP inventory management auto-battler") 및 PC Gamer 소개 기사, 2026-08 확인]. 따라서 Backpack Battles는 이 카드가 아니라 GENRE-027(PvP 오토배틀러) 쪽 경계 사례로 봐야 한다.

## 시장 포화도
- 사실: Backpack Battles(PlayWithFurcifer, 2024 얼리액세스)는 얼리액세스 출시(2024-03-08) 후 이틀 만에 10만 장, 2주 만에 50만 장을 넘겼고, 2024년 11월 기준 누적 80만 장 이상·Steam 리뷰 1만 건 이상을 기록했다 [출처: GameDeveloper.com 및 Steam 공식 뉴스 발표, 2024-11 기준]. 다만 위에서 정정했듯 이 수치는 **PvP 오토배틀러**의 성과이지 이 카드가 다루는 순수 PvE 군집의 성과가 아니다.
- 사실: Tales & Tactics(Table 9 Studio, 2024-08-16 출시)는 God is a Geek에서 8.5/10 평가를 받았고 Steam에서 "매우 긍정적" 평가로 소개됐다 [출처: God is a Geek 리뷰 및 관련 보도, 2026-08 확인]. 정확한 리뷰 건수·판매량은 확인하지 못했다.
<!-- 증거 부족: Tales & Tactics의 Steam 리뷰 건수·긍정 비율 원자료(리뷰 페이지 직접 확인)와 판매량은 이번 조사에서 확인하지 못함 -->
- [해석] 같은 검색에서 Hadean Tactics, Deckanism: Singularity Island 같은 유사 타이틀명이 나왔으나, 이번 조사(요약 결과)로는 개발사·정확한 장르 구성을 교차 검증하지 못했다.
<!-- 증거 부족: Hadean Tactics / Deckanism: Singularity Island의 개발사·판매량·리뷰 점수는 원 출처(Steam 페이지 등)를 직접 열어 확인하지 못함 -->
- [해석] 종합하면, 이 군집은 PvP 오토배틀러(Backpack Battles, GENRE-027)만큼 상업적으로 검증된 대박 사례가 아직 나오지 않은 신생 군집으로 보인다.

## 관례와 기대치
- 사실: 배치 페이즈와 자동 전투 페이즈를 번갈아 반복하는 2단 루프는 GENRE-027과 동일한 관례로 채택된다 - Tales & Tactics도 스쿼드를 구성해 배치한 뒤 전투가 자동 진행되는 구조로 소개된다 [출처: player.one 보도, 2026-08 확인].
- 사실: Tales & Tactics는 시간제한이나 실시간 압박이 없는 싱글플레이 모험으로 소개되며, PvP 오토배틀러 특유의 실시간 매칭·랭킹 경쟁 압박이 빠져 있다 [출처: Steam 상점 소개문, 2026-08 확인].
- [해석] PvP 오토배틀러가 주는 "실시간 순위 경쟁"이라는 리텐션 동기가 이 군집에는 없으므로, 그 자리를 무엇으로 채우는지(서사, 시즌 챌린지, 난이도 승급 등)가 이 군집의 생존을 가르는 관례로 자리잡을 가능성이 있다.
<!-- 증거 부족: 이 군집 다수 타이틀에 공통되는 리텐션 장치(시즌제, 챌린지 모드 등)를 비교 확인할 만큼의 표본을 조사하지 못함 -->

## 빈칸
[해석] ★ Backpack Battles류의 "인벤토리에 아이템을 채워 넣는" 배치 방식을 그대로 쓰면서도, 상대를 다른 플레이어(비동기 PvP)가 아니라 순수 AI 콘텐츠(고정 보스, 스토리 던전 등)로 채운 사례는 조사 중 확인하지 못했다. Tales & Tactics·Hadean Tactics 계열은 PvE이지만 배치 단위가 "인벤토리 속 아이템"이 아니라 "전장 위의 유닛(스쿼드)"이어서, Backpack Battles의 인벤토리 테트리스식 배치 감각과는 다른 하위 갈래로 보인다. 즉 이 군집 안에서도 "유닛 배치형 PvE"(Tales & Tactics류)와 "인벤토리 아이템 배치형 PvE"(Backpack Battles의 PvE 버전에 해당하나 실사례 미확인)가 갈라져 있고, 후자가 비어 있다.
- 확인 방법: Steam 태그 "Inventory Management"+"Auto Battler"+"Singleplayer"(PvP 태그 제외) 교차 검색으로 순수 PvE 인벤토리 오토배틀러 존재 여부 확인, 존재 시 GAME 카드 후보로 스카우트
- 확인일: 2026-08-09 / 재확인 주기: 8주
