+++
card_id = "ELEM-004"
type = "mechanic"
title = "Loop Mechanic"
summary = "A structure in which the same situation is repeated, but the variables change each time and the results change."
tags = ["retention", "high-cost", "puzzle", "roguelike", "divisive"]   # rougelike 오타 수정, divisive 추가(근거 =GAME-005 Mixed 평가)
updated = "2026-07-31"
confidence = "high"              # 기준 충족: 출처 있는 수치 + GAME 근거 3건
+++
## Definition
It is a structure that repeats the same time or situation multiple times. However, it repeats the same every time
Rather, something about what the player “knows, has, or does” has changed.
The results change. The same day as yesterday begins again, but what I learned yesterday
It's like remembering something so you can act differently today.

## Success Cases
- GAME-008 (Outer Wilds) - The solar system resets every 22 minutes, but only “knowledge” remains. With a design where the only growth factor is player knowledge, 96% positive out of 100,000+ Steam reviews, 2020 BAFTA Best Game Award [source: Steam store/Steambase, 2026-07 confirmed].
- GAME-009 (Hades) - Every time you die and return to the starting point, new dialogue and new relationships are unlocked, making “death = narrative progress”. The developer failed to show the branching narrative in the previous work because players did not play it repeatedly, and deliberately chose a roguelike structure based on repetition. [source: Wikipedia - Hades development article]. Cumulative 1,000,000 copies (based on 2020-09, early access 700,000+ + official 300,000) [source: Supergiant announced/GameSpot, 2020-09]. Of 140,000+ Steam reviews, 98% positive [source: Steam, confirmed 2026-07].
- GAME-028 (Destiny 2) - A/B case that occurred within the same game. 2018 9 Weapon Percs from the Forsaken expansion
When the random roll comes back, even if the weapon you already have appears again, it makes you check "What kind of roll is this?"
The reason has come back and the number of players has roughly doubled [source: PC Games Insider, as of 2018].
- GAME-040 (Hades II) - The same "death = narrative progression" structure was repeated in the sequel, surpassing the previous work. A total of about 5,200,000 copies on Steam, 96% positive [source: GAME-040 cards out of 121,483 reviews].
- GAME-026 (Bloons TD 6) - A case that was established with only a repeating loop of “enemies getting stronger each round + tower upgrades” without random drafts or gacha. 97% positive [source: GAME-026 card among Steam reviews 390,000 + 1,317].
- GAME-055 (Loop Hero) - A structure in which the character automatically walks a pre-set loop path, and the player only decides to place tiles (enemy spawns and resource terrain) on the path to balance risk and reward. 500,000 copies in the first week of release, 1,000,000 copies in month 2021 year 100, Steam reviews "very positive" (90% range) [source: GAME-055 cards].

## Failure Cases
- GAME-005 (Twelve Minutes) - The 12 minute loop's twisted concept was a hot topic, but the unskippable re-performance of the same lines and actions accumulated, leading to an evaluation of "repetitive labor." Steam Overall "Mixed", 68% positive [source: Steam store, confirmed 2026-07].
Point of failure: There was no new information or new reward in the repeat section, and there was no way to skip the repeat.
- GAME-028 (Destiny 2) - Opposite half of the same game. In the first year of release, weapon perc was a static roll.
Weapons with the same name had the same performance no matter who got them, and once you have collected several types of weapons you want, you can get them repeatedly.
The reason is gone [source: GameRant 'Destiny 2 Weapons Won't Have Random Perk Rolls', based on 2017].
Point of Failure: There was no “update” as the result (Perc) was the same every time.

## User Reaction Summary
- Preference: "The story progresses with each death", "Just one more game" - Immersion when repetition feels like accumulation rather than loss [source: GAME-009 Steam review keywords / Wikipedia evaluation item]
- Preference: Praise for the structure itself of “knowledge is the only way to progress,” creating a no-spoiler recommendation culture [source: GAME-008 Top reviews on Steam, check 2026-07]
- Dislike: "You have to listen to the same lines over and over again", "If you get stuck, re-do the entire loop" [source: GAME-005 Metacritic user review / Engadget review, 2021-08]
- Dislike (minority): Loops without direction are read as “purposeless” by some users. [source: GAME-008 Metacritic critical review]

## Synergy
- Good: ELEM-001 (teaser-based release) - Repetition acts as a “shuttle to check out the next piece of cake.” An empirical example of loop + teaser combination is GAME-008 [source: GAME-008 game structure]
- Good: ELEM-003 (Z4's wall collapse) - If the character remembers and mentions the repetitive act of saving/resetting, the meta device becomes repeatable. [Empirical case GAME-002 [source: GAME-002 game structure]
- Good[interpretation]: ELEM-005 (AI integration) - If the AI ​​mentions the player's past loop in real time, the "Every repetition is new" condition can be met without a script. However, there are no released empirical cases - GENRE-001 Same point as the blank hypothesis.
- Caution: A skip method is required when combined with a narrative with high dialogue density - Without it, there are empirical cases where repetition turns into fatigue: GAME-005 [source: GAME-005 Review Complaint Keyword]
- Good: ELEM-019 (Random Loot Drops & Loot Tables) / ELEM-020 (Deck Building) / ELEM-022 (Exponential Score
Scaling) - [interpretation] All three are specific devices that "update the result every time it is repeated." The repetition mechanic uses these elements
If used alone, it is easy to repeat without update, such as GAME-005·GAME-028 (fixed roll period).
- Genre Anchor: GENRE-002 (Loop Narrative), GENRE-010 (Tower Defense), GENRE-011 (Root Shooter), GENRE-012
(Roguelike Deckbuilder), GENRE-037 (Solo PvE Roguelike Autobattler) - All five clusters make up this element.
Point out the element. This is the element shared by most genres in this repository.

## Risks
- [interpretation] repetition itself is not content - at least one of "new information, new dialogue, new build" must be updated in each loop. This is the difference between GAME-009 (with renewal) and GAME-005 (without renewal). GAME-028 is in the same game
The change from fixed roll (no update) to random roll (with update) confirms this proposition once more.
- [interpretation] High implementation cost - Requires a design that tracks and stores the state of the past loop (what the player knew and did). High-cost basis for tags.
- [interpretation] barrier to entry - If “Why do we repeat the same thing?” is not understood within the first 1 time, they will leave. Even GAME-008 has a few complaints about lack of direction.


