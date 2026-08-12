+++
card_id = "GENRE-028"
type = "genre"
title = "Collectible Card Game PvP"
summary = "A cluster where, instead of a run-based deck used and discarded within a single session, players build a standing competitive deck in advance out of their entire owned card collection and face off"
elements = ["ELEM-020"]
example_games = []
tags = ["ccg", "tcg", "pvp", "deckbuilder", "meta", "live-service"]
updated = "2026-08-02"
confidence = "medium"
+++
## Components
- ELEM-020 (deck building) - in this genre it is used not as a run-based deck that persists only for one session (the approach of GENRE-012), but as a fixed deck assembled in advance from the entire owned card collection before the match begins. This is the point where it diverges from GENRE-012 (roguelike deckbuilder).
- Mana (resource) curve design - distributing cards by cost so that there is never a turn without a playable card from the early game through the late game is the basic unit of deck building [source: composite of Magic: The Gathering deck building guides, verified 2026].
- Meta/format rotation - there is a deck archetype (the meta) that is most used at any given point in time, and it is periodically overturned through card pool restrictions (formats such as Standard/Wild) to keep standing competitive play fresh [source: composite of the above guides, verified 2026].
<!-- Insufficient evidence: there is not yet a card treating 'meta rotation' and 'card collection (gacha-like pack purchases)' themselves as separate ELEMs, so only the concepts are described in this section -->

## Market Saturation
- Fact: Hearthstone (Blizzard) has approximately 790,000 monthly active users and approximately 176,000 daily active users as of 2026, and is still one of the most played digital CCGs [source: composite of industry statistics, verified 2026].
- Fact: Legends of Runeterra (Riot Games) recorded a cumulative 17,000,000 active players as of 2025-12, but after the 2024-01 overhaul it shifted its center of gravity from competitive PvP toward single-player modes (Path of Champions) [source: composite of industry statistics, as of 2025-12].
- Fact: Marvel Snap recorded 32,000,000 cumulative downloads and approximately $200,000,000 plus $18,000,000 in lifetime cumulative in-app purchase revenue, but its monthly active users fell sharply from the peak right after its late-2022 launch, and it is described as a "managed decline" [source: composite of industry statistics, verified 2026].
- [interpretation] The old strong player (Hearthstone) holds on, but later entrants repeat a pattern where, after initial rapid growth, standing PvP competition alone fails to retain users and the weight shifts to single-player content.

## Conventions and Expectations
- Fact: on a 60-card deck basis, conventions for resource ratios by deck archetype are established, such as aggressive decks running 20-23 lands (resource cards), midrange 24-25, and control 26-27 [source: composite of guides from Card Kingdom/Draftsim and others, verified 2026].
- [interpretation] The demand for constant optimization - "you have to keep swapping your deck to match the meta" - is both this genre's entry barrier and, at the same time, the justification for card pack sales (monetization) - unlike GENRE-012, where the team composition resets every session, in this genre the collection itself is both an asset and the object of spending.

## Gaps
[interpretation] ★ This repository does not yet have a GAME card covering standing competitive CCGs (Hearthstone, Marvel Snap, Legends of Runeterra, etc.) - GAME-001 (Inscryption) and GENRE-012 (roguelike deckbuilder) both cover only run-based single-player deckbuilders, so cases of the "collection → standing PvP" structure itself are missing.
- How to verify: scout Hearthstone or Marvel Snap as a GAME card candidate
- Verified on: 2026-08-02 / Re-check interval: 8 weeks
