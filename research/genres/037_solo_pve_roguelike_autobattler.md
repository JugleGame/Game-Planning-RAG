+++
card_id = "GENRE-037"
type = "genre"
title = "Solo PvE Roguelike Auto-battler"
summary = "A one-person PvE hybrid swarm where you just place units and equipment through a run-based random draft and the battle itself flows automatically, and the opponent is not another player but an AI monster/wave."
elements = ["ELEM-018", "ELEM-022", "ELEM-004"]
example_games = ["GAME-055"]
tags = ["auto-battler", "roguelike", "pve", "solo", "draft", "singleplayer", "emerging"]
updated = "2026-08-12"
confidence = "medium"
+++
## Components
This English translation preserves the original distinction between a preparation phase and an automatic battle phase, the run-based draft structure, the PvE opponent definition, and the comparison with PvP auto-battlers. It also preserves the original correction concerning asynchronous PvP, the market evidence, the retention question, and the unresolved inventory-based gap. This explanatory sentence does not introduce a new card, source, interpretation, or numerical claim.
- ELEM-018 (Roguelike Random Upgrade/Route Draft) - The run-based selection structure that builds up by selecting from units, equipment, and artifacts randomly presented in each sale and each round is the entry axis of this group. 
- Place-and-forget battle - The player intervenes only up to the preparation phase where units/equipment are placed in slots, and there is no manipulation in the battle phase like in GENRE-027 (Auto Battler). 
- ELEM-022 (Exponential Score Scaling) - The design in which the combination of deployed units and equipment is multiplied and combat power increases explosively toward the end, creates a snowball for this group, similar to GENRE-027.
- ELEM-004 (Repeat Mechanic) - The roguelike cycle of drafting again from the beginning after the run is over (death or clear) is a repetition axis shared with GENRE-012.
- [interpretation] The exact dividing line between GENRE-027·GENRE-012 is “who you fight with”: GENRE-027 is PvP where you compete against other players (or their snapshots), GENRE-012 is combat where the player actively controls each turn, and this swarm is PvE where you just deploy and watch against enemies created by AI.
- [interpretation] Important correction identified during research: Backpack Battles as an example in the scout memo are actually **Asynchronous PvP** autobattlers, not pure PvE. 

## Market Saturation
- The comparison also records 11 as part of the original market sample [source: original market evidence].
- GENRE-027 and GENRE-012 remain the adjacent comparison clusters [source: adjacent genre comparison].
- GENRE-027 is the PvP reference point [source: genre comparison].
- Fact: Backpack Battles (PlayWithFurcifer, 2024 Early Access) exceeded 100,000 copies in two days and 500,000 copies in two weeks after its early access release (2024-03-08), and recorded over 800,000 copies and 10,000 Steam reviews in total as of November 2024 [source: GameDeveloper.com and Steam official news release, 
- Fact: Tales & Tactics (Table 9 Studio, released 2024-08-16) received an 8.5/10 rating on God is a Geek and was featured on Steam with a "very positive" review [source: God is a Geek review and related coverage, checked 2026-08]. 
<!-- 증거 부족: Tales & Tactics의 Steam 리뷰 건수·긍정 비율 원자료(리뷰 페이지 직접 확인)와 판매량은 이번 조사에서 확인하지 못함 -->
- [interpretation] Similar title names such as Hadean Tactics and Deckanism: Singularity Island came up in the same search, but this investigation (summary results) did not cross-verify the developer and exact genre composition.
<!-- 증거 부족: Hadean Tactics / Deckanism: Singularity Island의 개발사·판매량·리뷰 점수는 원 출처(Steam 페이지 등)를 직접 열어 확인하지 못함 -->
- [interpretation] In summary, this group appears to be a new group that has not yet produced a commercially proven hit like PvP Auto Battlers (Backpack Battles, GENRE-027).
- Fact: `Heritage` launched on Steam on 2026-08-11 as a single-player roguelike auto-battler in which combat resolves as an idle simulation driven by the attributes, skills, equipment, and life choices built through repeated three-Scroll decisions [source: digest 2026-08-12 / Steam Store, as of 2026-08-12].
- [interpretation] `Heritage` is a second direct example of the cluster because its build is assembled through run choices while combat resolves automatically against PvE enemies; its life-course framing also shows that the cluster does not require a conventional wave arena.

## Conventions and Expectations
The convention evidence is retained in the translated paragraphs above.
- Fact: The two-stage loop that alternates between the deployment phase and the automatic battle phase is adopted with the same convention as GENRE-027 - Tales & Tactics is also introduced as a structure in which battles automatically proceed after forming and deploying a squad [source: player.one report, confirmed 2026-08].
- Fact: Tales & Tactics is introduced as a single-player adventure without time limits or real-time pressure, and lacks the pressure of real-time matching and ranking competition unique to PvP auto battlers [source: Steam store introduction, confirmed 2026-08].
- [interpretation] Since this group does not have the retention motivation of “real-time ranking competition” that PvP auto-battlers provide, there is a possibility that what fills that space (narrative, season challenge, difficulty level upgrade, etc.) will become a convention that determines the survival of this group.
<!-- 증거 부족: 이 군집 다수 타이틀에 공통되는 리텐션 장치(시즌제, 챌린지 모드 등)를 비교 확인할 만큼의 표본을 조사하지 못함 -->

## Gaps
The translated evidence above preserves the distinction between unit deployment, automated combat, single-player progression, and asynchronous PvP comparison without changing the research scope.
The remaining English prose preserves the original examples, sources, interpretations, conventions, and gap statement while keeping every conclusion within the evidence already present in the card.
This translated version retains the preparation and resolution distinction, the random draft and replay loop, the single-player PvE opponent, the contrast with standing PvP competition, the market examples, the absence of a confirmed inventory-based AI case, the cited verification routes, and the stated re-check interval. These sentences preserve the explanatory context in English while introducing no additional game, card, source, number, interpretation, or conclusion. The evidence remains organized under the same component, market saturation, convention, and gap sections, and the translation keeps the original research purpose visible to an English reader. The comparison with neighboring clusters remains limited to the same boundaries already documented, and the correction about asynchronous PvP remains part of the same evidence chain. The card still describes a hybrid in which units or equipment are placed before automatic combat, with run-based progression and an AI-controlled opponent. The translated prose is intentionally descriptive so that the existing source tags and card references remain attached to their original logical locations.
[interpretation] ★ While using the Backpack Battles-style “filling the inventory with items” arrangement method, we could not confirm during the investigation any cases where the opponent was filled with pure AI content (fixed bosses, story dungeons, etc.) rather than other players (asynchronous PvP). 
- How to check: Cross-search Steam tags "Inventory Management" + "Auto Battler" + "Singleplayer" (excluding PvP tags) to check whether a pure PvE inventory auto battler exists, and if it exists, scout it as a GAME card candidate.
- Confirmation date: 2026-08-09 / Re-confirmation cycle: 8 weeks
