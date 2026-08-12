+++
card_id = "ELEM-018"
type = "mechanic"
title = "Roguelike Random Upgrade/Path Draft (Roguelike Random Upgrade & Path Draft)"
summary = "A run-based choice structure in which the player selects from randomly presented cards or tiles each run and round"
tags = ["roguelike", "randomness", "draft", "run-based", "tower-defense", "divisive"]
updated = "2026-08-05"
confidence = "medium"
+++
## Definition
Rather than following one predetermined approach every time, the game shows several random cards or choices and lets the player choose one. Unlike gacha, where the player simply receives what comes out of the machine, this structure lets the player directly select one of the random candidates. Each run therefore produces a different combination, and no two runs are identical.

## Success Cases
- GAME-027 (Rogue Tower) - Presents several random cards each round from a pool of more than 400 cards, letting players build or upgrade towers; branching path tiles are also placed randomly [source: Rogue Tower Steam store page and strategy-site synthesis, confirmed 2026-07]. 80% of 4,356 Steam user reviews are positive [source: review aggregation site, confirmed 2026-07].
- GAME-030 (Slay the Spire) - Established the classic form of this element by letting players add exactly one card from randomly presented rewards after each battle [source: Eneba review article, confirmed 2026-07], and exceeded 10,000,000 copies across PC and console [source: Alinea Analytics, as of 2026-03-20].
- GAME-034 (Wildfrost) - A run-based structure in which the player chooses one card or relic from random post-battle options to build a team. SteamSpy estimates 500,000-1,000,000 owners [source: GAME-034 card].
- GAME-050 (Towerful Defense: A Rogue TD) - A structure in which each run randomly selects up to 4 skills, traits, and items to build a single-tower setup. 70% of 207 Steam reviews are positive [source: GAME-050 card].
- GAME-051 (Yet Another Zombie Survivors) - Carries the draft structure of choosing one weapon or ability on level-up into a survivorlike squad variation. 91% positive among more than 10,000 and 3,000 Steam reviews [source: GAME-051 card].
- GAME-052 (Rogue Defense: Hybrid Tower TD) - Randomly builds weapon and guardian-skill combinations against procedurally generated enemy waves. More than 1,000,000 cumulative Google Play downloads and a 4.2/5 rating [source: GAME-052 card].

## Failure Cases
- GAME-027 (Rogue Tower) - Some users complained that a random path in which the next tile is hidden determines most of the outcome and feels like an unfair gamble [source: Steam user-review synthesis, confirmed 2026-07].
  Failure point: Draft and path randomness becomes frustrating when it feels more decisive than skill.

## User Reaction Summary
- Preference: Replayability from a different combination every run and the short 20-30 minute run length are both mentioned positively [source: Rogue Tower review synthesis, confirmed 2026-07]
- Dislike: When random paths and drafts are decisive enough to determine victory or defeat, users object that it is "luck, not skill" [source: Steam user-review synthesis, confirmed 2026-07]

## Synergy
- Good: ELEM-004 (Repetition Mechanic) - Different draft results on repeated runs add enjoyment to repetition itself.
- Good: ELEM-020 (Deck-building) - Drafted cards enter the deck directly, so the two elements are practically used together. GAME-030 is an observed case.
- Good: ELEM-017 (Gacha Probability & Pity System) - [interpretation] Both make randomness "not completely merciless"; adding minimum-guarantee or pity rules to a draft could reduce GAME-027-like complaints of unfairness (a hypothesis without an observed case; see the GENRE-010 gap).
- Genre anchors: GENRE-010 (Tower Defense), GENRE-012 (Roguelike Deckbuilder), GENRE-019 (Survivorlike), GENRE-016 (Bullet-Hell Roguelike), GENRE-039 (Turn-based Tactical Roguelike), GENRE-037 (Solo PvE Roguelike Auto-battler) - All six clusters identify this element as a component. GENRE-039 consumes this draft through turn-based planning on a grid rather than GENRE-016's real-time control, while GENRE-037 consumes it through automatically progressing PvE combat after placement.
- Good: ELEM-042 (Direct-Control Single-Tower Defense) - As GAME-050 demonstrates, the skill and item choices presented by this draft structure become materials for a build in which the player directly controls one tower.

## Risks
- [interpretation] The stronger the random element's influence on victory or defeat, the stronger the objection that it is a "luck game"; GAME-027 actually received this complaint.
- [interpretation] If the card and tile pool exceeds 400 entries, the amount of information new users must learn can become an onboarding barrier.
- Fact: GAME-030 (Slay the Spire) validated another solution instead of adding pity - in Daily Climb, every player shares the seed, so map layout, card rewards, relic drops, and event results are identical; if results differ despite receiving the same hand, the difference can be explained only by skill [source: Slay the Spire Wiki 'Daily Climb' article, confirmed 2026-07].
  [interpretation] Shared seeds may be a more validated alternative for GAME-027-like unfairness complaints because implementation is simpler than probability-adjusting pity and it prevents "blame luck" disputes at the source.
<!-- 증거 부족: 성공 사례가 GAME-027·GAME-030 2건이라 GAME 근거 3건 이상이라는 high 기준을 못 채움 -->
