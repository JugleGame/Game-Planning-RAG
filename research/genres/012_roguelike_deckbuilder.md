+++
card_id = "GENRE-012"
type = "genre"
title = "Roguelike Deckbuilder"
summary = "A cluster that builds a deck lasting only for one run by choosing from random card rewards, then makes the player rebuild from the beginning after death"
elements = ["ELEM-020", "ELEM-018", "ELEM-004", "ELEM-047"]
example_games = ["GAME-030", "GAME-001", "GAME-031", "GAME-034"]
tags = ["roguelike", "deckbuilder", "randomness", "indie", "replayability", "saturated"]
updated = "2026-08-09"
confidence = "medium"
+++
## Components
- ELEM-020 (deckbuilding) - The cluster's identity. It starts from a weak starting deck and builds a deck valid only during the run [source: Eneba review article, verified 2026-07].
- ELEM-018 (roguelike random upgrade/path draft) - The map's challenge order, choices among random card rewards, and unpredictable relics make every run different [source: Eneba review article, verified 2026-07].
- ELEM-004 (repetition mechanic) - The deck disappearing on death and being rebuilt from the beginning is the axis of repetition.
- [interpretation] What separates this cluster from ordinary card games is that the deck is "a one-run consumable, not a permanent asset." Skill therefore lies in moment-to-moment judgment, not collection (buying powerful cards).
- GENRE-035 (tile-matching roguelike deckbuilder) - [interpretation] An adjacent cluster sharing this cluster's run structure (artifact acquisition, round-based goals, and round-based shops). This cluster invents its rules anew, while GENRE-035 borrows existing tile-placement rules such as dominoes and mahjong [source: GENRE-035 card].
- ELEM-047 (asymmetric starting-deck character roster) - A convention inherited from early Slay the Spire-like works: each playable character receives a different starting deck and card pool to create replay value. The new case Talespinner (yokai-mythology theme) follows it by giving each of 3 characters unique mechanics [source: ELEM-047 card].

## Market Saturation
- Fact: After GAME-030's late-2017 early-access success, the genre became saturated, and later works whose play loops are barely distinguishable from the original continue to appear [source: GameShub genre-analysis article, verified 2026-07].
- Fact: Even so, the scale of top works keeps growing - GAME-031 (Balatro) sold 5,000,000 copies [source: Game Developer, as of 2024-12], while GAME-030's sequel sold 4,600,000 copies / more than $92,000,000 within 2 weeks of its 2026-03-05 early-access launch [source: Alinea Analytics, as of 2026-03-20].
- Fact: The sequel's 2-week revenue at the same time exceeded the cumulative Steam revenue of Hollow Knight: Silksong ($83,000,000) and Hades II ($82,000,000) [source: Alinea Analytics, as of 2026-03-20].
- [interpretation] Saturation means something different here. If the design is genuinely different, the market absorbs several works at once; if it is the same, the work is immediately buried. Entry barriers are low, but without an answer to "why play this?" it cannot even gain exposure.
<!-- 증거 부족: 연간 신작 수 등 장르 단위 출시 규모 집계는 확인하지 못함 -->
- Fact: As of 2026-07-31, Balatro (GAME-031) had updated through version 1.0.1o-FULL "Friends of Jimbo 4" and announced a free 1.1 content update, continuing live support for more than 2 years after launch [source: Balatro Wiki, as of 2026-07-31 / digest 2026-07-31].
- Fact: The first-week August 2026 digest captured ELEM-021 (borrowing familiar rules) diversifying beyond poker and cards into new works based on dominoes (Dominocalypse) and Japanese mythology [source: digest 2026-08-07]. The investigation treats branches borrowing tile-placement rules such as dominoes and mahjong as a separate adjacent cluster (GENRE-035, tile-matching roguelike deckbuilder) - both share run structure (artifacts and round-based shops), but differ in the borrowed base rule (cards vs. tiles) [source: GENRE-035 card].

## Conventions and Expectations
- Fact: Choosing exactly one card from randomly presented rewards after each battle is standard vocabulary [source: Eneba review article, verified 2026-07].
- Fact: Each run generates a unique seed, and in a shared-seed daily mode every player receives the same map layout, card rewards, relic drops, and event results [source: Slay the Spire Wiki 'Daily Climb' page, verified 2026-07].
- Fact: A progression structure that unlocks the next difficulty after clearing (Ascension) is expected - each level adds a modifier such as stronger enemies, more elites, fewer potion slots, or higher shop prices [source: Eneba review article, verified 2026-07].
- [interpretation] Players in this cluster do not readily accept "I lost because of bad luck." Shared seeds and Ascension are both devices for maintaining the frame that "defeat is the result of a choice."

## Gaps
[interpretation] ★ No deckbuilder making a shared-seed daily the **core competitive structure rather than an auxiliary mode** was confirmed. In GAME-030 too, Daily Climb is a separate mode beside the main game. Everyone receiving the same hand is almost the only device that preserves randomness while eliminating "blame luck," yet no case was found that elevates it to the main loop and binds it to rankings and seasons.
- Verification method: check daily/seed/leaderboard keywords on store pages of top Steam-tagged "Deckbuilding"+"Roguelike" works and distinguish whether daily is the main or auxiliary mode
- Verified on: 2026-07-29 / Re-check cycle: once a quarter

[interpretation] ★ No case was confirmed that directly designs around the conflict between ELEM-019 (random loot drops) and ELEM-020 (deckbuilding). Loot drops assume "the more you obtain, the stronger you become," while deckbuilding assumes "the more you add, the more diluted you become"; no game presents this contradiction itself as a player choice (for example, deciding each time whether to add acquired loot to the deck).
- Verification method: cross-search top GENRE-011 (looter shooter) works with this cluster, then verify through store pages and guides whether acquisition and deck inclusion are separate
- Verified on: 2026-07-29 / Re-check cycle: once a quarter
