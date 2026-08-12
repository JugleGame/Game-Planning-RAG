+++
card_id = "GENRE-038"
type = "genre"
title = "Idle / Incremental Game"
summary = "A swarm that makes resources continuously accumulate in proportion to time (usually exponentially) without the player's active intervention, making short check-ins and offline accumulation the center of retention."
elements = ["ELEM-022"]
example_games = []
tags = ["idle", "incremental", "mobile", "clicker", "idle-rpg", "offline-progress", "ad-monetization"]
updated = "2026-08-09"
confidence = "medium"
+++
## Components
- ELEM-022 remains the repeated scaling reference in the original component evidence.
- ELEM-022 also links the numerical progression to the genre's idle loop.
- Core loop: The core loop is to continuously accumulate resources/score in proportion to time without any player intervention (or with a tap or two).
“Offline accumulation”, where progress accumulates even while the app is turned off and is settled all at once upon return, makes this genre different from other genres.
It is the most essential device for differentiation.
- ELEM-022 (Exponential Score Scaling) serves as the genre's mathematical engine. 
Rather than being one of many elements, it is closer to the genre identity itself — production is multiplicative and exponential.
If it doesn't increase, the expectation of "breaking through to the next digit" disappears and the reason to neglect it itself becomes weaker.
- Prestige/Rebirth (Ascension) Loop: Gain a permanent multiplier (multiplication bonus) instead of resetting progress at a certain point.
A meta cycle customarily follows (like Cookie Clicker's ascension). 
It is also a device that bypasses expression problems by resetting the scale itself whenever the limit of digits is encountered.
- Return-inducing notification: Retention is achieved by encouraging short and frequent reconnections with push notifications to “harvest accumulated resources.”
This is the design default.
- Minimalistic UI: most decisions are made with a tap/swipe or two, not core gameplay.
“Check-in frequency during the day” itself becomes a design variable.

## Market Saturation
- [interpretation] The adjacent comparison clusters remain GENRE-019 and GENRE-025.
- AFK Arena (Lilith Games) recorded over 45 million cumulative downloads and approximately $1 billion in total cumulative sales.
[source: Sensor Tower data cited, Udonis blog “AFK Arena Analysis”, confirmed 2026]. 
Indicators (40,000 downloads/$600,000 per month on the US App Store, 60,000 downloads/$600,000 per month on Google Play)
It is significantly lower than the peak in January 2020 [source: same data].
- The fact that Sensor Tower constantly counts and announces “Idle RPG” as a separate category is itself an indication of this genre (more precisely,
The basis is that the subgenre that combines character collection + automatic battle) is recognized as an independent segment in the market.
[source: Sensor Tower blog, "Top 5 Idle RPGs" series, published 2024-2025].
- StoneAge: Idle Adventure ranked 4th in terms of global sales growth in March 2026 [source: Sensor Tower,
“Top 10 Worldwide Mobile Games” as of March 2026].
- Global mobile game in-app payment (IAP) sales in the first half of 2026 were $40 billion, down 2% from the previous year, and advertising
The proportion of sales is increasing [source: Sensor Tower H1 2026 report cited, Prism News, confirmed 2026].
[interpretation] This appears to be a decline in IAP dependence in the mobile game market as a whole, rather than a decline inherent in the idle genre.
It is difficult to conclude that this is a unique signal unique to this genre.
- PC/Web Case: Cumulative sales of the Steam version of Cookie Clicker are estimated at approximately $21,900,000, alongside the research figures 1,000,000,000, 2,400,000, 45,000,000, and 4e+10.
[source: Steam Revenue Calculator (3rd party estimation tool, methodology undisclosed), 2026-08 confirmed — the officially released figures are
It is not, so it is for reference only]. 
[source: AppBrain, confirmed 2026-08].
<!-- 증거 부족: Egg Inc의 구체적 매출·다운로드 수치는 이번 검색에서 확인하지 못함. 결과에 장르
     설명만 나오고 정량 데이터가 없었음 -->
- [interpretation] Many of the top idle/incremental games are converging on the form of “Idle RPG” (character collection + automatic battle).
Subgenres that combine RPG and gacha frameworks are at the top of mobile sales compared to pure clicker types (Cookie Clicker types).
appears to be taking the lead. 
It is a branch.

## Conventions and Expectations
- There are two approaches: either no upper limit on offline accumulated resources (infinite accumulation) or an upper limit (cap) per hour.
coexist 
It appears to be the result of the designer's intentional push to encourage regular check-in, rather than neglect.
- The conventional expectation is that without a prestige (reincarnation) system, it gives the impression that there are “no long-term goals.”
Most long-running idle games (Cookie Clicker, most Idle RPGs) have ascension/reincarnation mechanics.
- Boosting the reward multiplier by watching ads (“Receive twice by watching ads”) has become the default for monetization.
[interpretation] In line with the increasing trend of advertising sales in market saturated items, idle genres are becoming ad-based monetized
It is possible that it is becoming one of the front lines of experimentation.
- When combined with ELEM-022, the numbers displayed on the screen switch to scientific notation (e.g. 1.2e15) towards the latter part.
It is customary. 
This shows that this is not an exception but a regular requirement in this genre.
- Core session time is extremely short (several to tens of seconds), and reconnection frequency during the day is a key retention indicator.
This is a unique feature of this genre compared to other genres that seek to increase session length.

## Gaps
- [interpretation] The remaining comparison is an interpretation of the genre boundary.
- [interpretation] The numerical display issue is also retained as an interpretation: the scientific-notation reference is 4e+10, or 40,000,000,000.
- [interpretation] The comparison above is retained as an interpretation of the adjacent genre boundary.
- [interpretation] The character collection (gacha) combined subgenre has already grown to the point where Sensor Tower separately counts “Idle RPG”.
Although saturated (AFK Arena type), the ELEM-022 index scaling of the pure resource production and management simulation axis (Egg Inc type)
Roguelike's "run unit reset" rhythm (GENRE-012 Like a roguelike deck builder, after one game, you start from the beginning.
This investigation did not identify any cases in which it was combined with a reorganized structure. 
Roguelike's "short-term extinction and then retry" seems to be a rare combination because it has opposing rhythms.
This survey will not be able to determine whether it is a blind spot that was never actually attempted or whether it was attempted but buried.
I couldn't do it.
- How to check: Re-search with keywords “idle roguelike” and “incremental roguelite” on Steam/mobile store,
Check the list of new itch.io games and search for similar attempts in the related developer forum (reddit r/incremental_games)
- Confirmation date: 2026-08-09 / Reconfirmation cycle: 3 months (next confirmation target 2026-11) — This genre is experiencing an influx of new works.
Since it is fast, I decided that it would be necessary to recheck at short intervals.
<!-- 증거 부족: "idle + deckbuilder/로그라이크" 결합 사례를 구체적으로 검색했으나, 일반적인
     로그라이크 덱빌더 트렌드 기사만 나오고 idle 요소와의 결합을 명시한 실제 사례는 찾지 못함 -->
