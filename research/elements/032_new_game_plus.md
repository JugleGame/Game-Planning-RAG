+++
card_id = "ELEM-032"
type = "mechanic"
title = "New Game+"
summary = "A post-game replay device that lets users voluntarily carry progress (equipment and stats) forward and challenge the game again from the beginning after clearing it once"
tags = ["replayability", "post-game", "difficulty", "narrative", "broad-appeal"]
updated = "2026-07-31"
confidence = "high"
+++
## Definition
After finishing a game once, this gives the player the option to start again from the beginning while keeping the equipment and stats they collected. It is like opening a book already read, but looking for hidden meanings while knowing the plot.

## Success Cases
- Dark Souls (2011, FromSoftware) - In NG+, the story and events remain the same, but enemy difficulty rises while character stats and equipment are retained, providing the challenge of facing it with genuine skill [source: Dark Souls Wiki, 2026 confirmation]. GAME-021 (Dark Souls III) in the same series is a completed example of this death-and-combat formula.
- NieR: Automata (2017, PlatinumGames / Square Enix) - NG+ is designed as a required structure for seeing the true ending rather than an optional element. From the second playthrough, the controllable character changes to 9S, and the same events are reinterpreted through a completely different minigame genre, bullet-hell hacking [source: dualshockers.com, 2026 confirmation].
- Persona 5 Royal (2019/2020, Atlus) - Certain character events and dialogue open only in NG+, incorporating replay into content consumption [source: g2a.com news, 2026 confirmation].

## Failure Cases
- <!-- Evidence insufficient: no specific failure case in which introducing NG+ produced the opposite effect was found in the investigation -->
- [interpretation] A method that only raises difficulty while leaving the story and events exactly the same as the first playthrough, in the Dark Souls style, is easily criticized by the community as a retread with only bigger numbers because it offers no narrative discovery.

## User Reaction Summary
- Preference: "The effort from the first playthrough is not wasted" - a positive reaction to carrying progress forward [source: NG+ design column, redharegames.wordpress.com, as of 2025]
- Aversion: "Why clear it again if the story is the same?" - skepticism toward NG+ without narrative variation

## Synergy
- Good: ELEM-009 (philosophical narrative roguelike/roguelike) - The philosophical themes of death and repetition naturally fit NG+'s structure of experiencing something again while already knowing it.
- Good: ELEM-014 (punitive death cycle) - As the GAME-021 (Dark Souls III) line demonstrates, NG+ works in games where death carries weight as a reward that does not invalidate first-playthrough accumulation.
- Bad: ELEM-004 (repetition mechanic) - Using both the in-game real-time loop and NG+ can layer the concept of repetition and confuse players about which repetition is meaningful. Games whose core is already a loop, such as GAME-009 (Hades) and GAME-040 (Hades II), achieve the same goal through escalating structures such as ascension instead of NG+.
- Implementation bridge: ARCH-004 (save system) - NG+ requires the clear state and carryover targets to remain in save data. Which fields carry over and which reset is the design of this element.

## Risks
- [interpretation] NG+ that only raises difficulty without adding content may have low perceived value relative to development cost.
- [interpretation] If the true ending is hidden behind NG+, as in NieR: Automata, some players may feel forced into replay and the design intent, narrative necessity, must be communicated clearly.
