+++
card_id = "GENRE-027"
type = "genre"
title = "Auto Battler (Auto Battler / Auto Chess)"
summary = "A PvP cluster whose core is economy management and synergy combinations, where each round you buy units in a shop and only position them while the combat itself resolves automatically"
elements = ["ELEM-022"]
example_games = []
tags = ["auto-battler", "auto-chess", "pvp", "economy", "synergy", "esports"]
updated = "2026-08-02"
confidence = "medium"
+++
## Components
- A two-stage loop of shop phase + automatic combat phase - a preparation segment where you draw and position units, and a segment where, once positioning is done, combat proceeds automatically without any input, alternate repeatedly [source: composite of genre overviews (Switchblade Gaming and others), verified 2026].
- Synergy combinations - a combination bonus system where gathering units by race, class, or trait attaches extra effects such as increased damage or defensive buffs is common to most representative titles [source: composite of genre overviews, verified 2026].
- Positioning - formation design that places tanks in the front row and damage dealers/supports in the back row is treated as the core decision that determines combat outcomes [source: composite of genre overviews, verified 2026].
- ELEM-022 (exponential score scaling) - as rounds progress, synergies and upgrades multiply so that combat power swells explosively rather than linearly, and this design creates the late-game snowball of this genre.
<!-- Insufficient evidence: there is not yet an ELEM card in this repository covering economy management (interest/rolling/level-up resource allocation) itself, so only the concept is described -->
- GENRE-037 (solo PvE roguelike auto battler) - [interpretation] it is an adjacent cluster that shares the
  two-stage shop-positioning-auto-combat loop. However, this cluster is PvP where the opponent is another player (or a snapshot of one), whereas GENRE-037
  diverges in that the opponent is monsters/waves assembled by AI in single-player PvE [source: GENRE-037 card].

## Market Saturation
- Fact: Teamfight Tactics (Riot Games) has approximately 33,000,000 monthly active users as of 2026, and recorded a peak of 10,000,000 daily players last year [source: composite of industry statistics (PC Gamer-affiliated reporting), verified 2026].
- Fact: Dota Underlords (Valve) never surpassed Teamfight Tactics after updates stopped in December 2020 and was effectively wound down [source: PC Gamer 'What happened to autobattlers?', verified 2026].
- [interpretation] Only a few years after the genre emerged, there is a clear trend of convergence onto a small number of strong players (Teamfight Tactics, and Hearthstone Battlegrounds which was layered onto an existing IP) - the room for an independent new title to break in has narrowed.
- The adjacent reference point 12 remains distinct because its deck is rebuilt during each run rather than maintained as a standing competitive collection.

## Conventions and Expectations
- Fact: it is conventional for early rounds to allow room for learning, with the difficulty curve demanding increasingly sophisticated judgment about resource allocation (pushing vs. managing interest) as the game moves into its later stages [source: composite of genre overviews, verified 2026].
- Fact: Hearthstone Battlegrounds layered itself onto the existing Hearthstone setting and existing player base, using a strategy of lowering the entry barrier that "immerses people who are already interested" [source: PC Gamer-affiliated reporting, verified 2026].
- [interpretation] PvP auto battlers tend to survive better when they start out layered onto an existing popular IP (Dota, Hearthstone, the Riot champion pool) rather than as a standalone new IP - Dota Auto Chess starting as a Dota 2 custom mode is the archetype.

## Gaps
[interpretation] ★ This repository does not yet have a GAME card covering a representative auto battler (Teamfight Tactics, Hearthstone Battlegrounds, Dota Underlords, etc.) - the #auto-battler tag on GENRE-019 (survivor-like) only points to single-character automatic combat (combat without real-time input), which is a different concept from the shop-positioning-auto-combat PvP loop this card covers, so there is room for confusion.
- How to verify: scout Teamfight Tactics or Hearthstone Battlegrounds as a GAME card candidate, and re-examine the wording of the GENRE-019 tag
- Verified on: 2026-08-02 / Re-check interval: 8 weeks
