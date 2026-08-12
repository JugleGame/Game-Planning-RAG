+++
card_id = "ELEM-020"
type = "mechanic"
title = "Deck-building (Deck-building)"
summary = "A structure in which the player starts with a weak group of cards and builds a personal deck by adding and removing cards during play"
tags = ["deckbuilder", "roguelike", "randomness", "replayability", "indie", "strategy"]
updated = "2026-07-31"
confidence = "medium"
+++
## Definition
This method collects cards into a personal group and fights with that group, called a deck. The player starts with a few very weak cards and adds new cards after winning fights. But there is a trap: as the deck grows, the desired cards become harder to draw. The chance of drawing one good card differs between a ten-card deck and a forty-card deck. Therefore, **not adding unnecessary cards and removing cards already owned** can be more important than adding many good cards. The defining feature is that gaining something does not automatically make the player stronger.

## Success Cases
- GAME-030 (Slay the Spire) - Grew the deck by choosing one of the cards presented after each battle, exceeded 10,000,000 copies across PC and console [source: Alinea Analytics, as of 2026-03-20], and maintains 97% positive among more than 194,000 Steam reviews [source: Notebookcheck sales report, confirmed 2026-07].
- GAME-030 sequel - Within two weeks of its early-access release on 2026-03-05, reached 4,600,000 copies / more than $92,000,000 and a peak DAU of 2,200,000 [source: Alinea Analytics, as of 2026-03-20]. More than 50% of players exceeded 20 hours and 14% recorded more than 50 hours [source: Alinea Analytics, as of 2026-03-20].
- GAME-031 (Balatro) - A variation that builds a deck on poker rules and exceeded 5,000,000 copies across all platforms [source: Game Developer, as of 2024-12].
- GAME-034 (Wildfrost) - A positional deckbuilder that places each card on a field tile to create synergy with adjacent cards, shifting the axis of deck-building from "what to add" to "where to place it" [source: GAME-034 card].

## Failure Cases
- Fact: After GAME-030's early-access success at the end of 2017, the genre became saturated, with repeated criticism that later works have loops almost indistinguishable from the original [source: GameShub genre analysis article, confirmed 2026-07].
  Failure point: Deck-building has simple rules and a low imitation cost. Copying the element directly produces "that game again"; differentiation comes only from what is built on top of it.
<!-- 증거 부족: 실패한 개별 타이틀의 판매·리뷰 수치는 확인하지 못해 장르 수준 관찰만 기재함 -->

## User Reaction Summary
- Preference: Each run's different deck makes players repeat the same game for dozens or hundreds of hours; for the sequel, more than 50% exceeded 20 hours and 1% exceeded 100 hours [source: Alinea Analytics, as of 2026-03-20]
- Preference: In a shared-seed daily mode, everyone can compete with the same map, card rewards, and relics [source: Slay the Spire Wiki 'Daily Climb' article, confirmed 2026-07]
- Dislike: Fatigue with later works indistinguishable from the original [source: GameShub genre analysis article, confirmed 2026-07]

## Synergy
- Good: ELEM-018 (Roguelike Random Upgrade/Path Draft) - Choosing one randomly presented card supplies the input for deck-building directly; the elements are practically paired.
- Good: ELEM-004 (Repetition Mechanic) - A differently built deck makes the same run a different game.
- Conflict: ELEM-019 (Random Loot Drop & Loot Table) - [interpretation] Their accumulation logic is opposite. Loot drops assume "more makes you stronger," while adding more cards can dilute desired cards and make a deck weaker. Combining them can make players wrongly learn that everything gained is good and damage their own deck.
- Genre anchors: GENRE-012 (Roguelike Deckbuilder), GENRE-013 (Casino-rules Roguelite), GENRE-028 (Collectible Card PvP) - All three clusters identify this element as a component. GENRE-028 differs because it uses a fixed deck prepared from the whole owned collection for ongoing matches, not a run-based deck that lasts one game [source: GENRE-028 card].
- Specification: ELEM-047 (Asymmetric Starting-Deck Character Roster) - A concrete case that adds a roster axis of "different starting decks for each character" on top of this card's "single deck grows" structure. Ironclad, Silent, Defect, and Watcher in Slay the Spire each have a different starting deck [source: ELEM-047 card].

## Risks
- [interpretation] The rule that a larger deck can be weaker is counterintuitive. Without explicit teaching, beginners accept every reward card, defeat themselves, and blame randomness.
- [interpretation] Low imitation cost means the element itself does not differentiate a game. The difference between GAME-030 and GAME-031 (Balatro) comes from the rules added on top (Ascension difficulty / poker hands), not deck-building.
- [interpretation] As card types increase, combination-verification cost rises sharply. One balance-breaking combination can make an entire run meaningless, so more cards do not automatically mean more content.
