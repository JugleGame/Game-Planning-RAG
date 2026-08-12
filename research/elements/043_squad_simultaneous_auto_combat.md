+++
card_id = "ELEM-043"
type = "mechanic"
title = "Squad Simultaneous Auto-Combat"
summary = "A control structure that departs from survivor-like single-character auto-combat by having one player direct multiple characters simultaneously while each attacks independently"
tags = ["survivors-like", "bullet-heaven", "squad", "auto-combat", "control-variant", "emerging"]
updated = "2026-08-06"
confidence = "medium"
+++
## Definition
Survivor-like (bullet-heaven) games normally control only one character. The character attacks automatically, while the player moves to dodge and chooses upgrades. This element expands that one character into several. Multiple characters appear on screen and attack on their own, while the player directs them together as one squad. It is a variation that changes only the character-count axis of GAME-037 (Vampire Survivors)'s single-character auto-combat standard.

## Success Cases
- GAME-051 (Yet Another Zombie Survivors) - Recruits companions up to a squad of three and controls them together. 94% positive among 4,745 Steam reviews, and 94% among 152 reviews in the most recent 30 days [source: Steam, verified 2026-08].
- Entropy Survivors - A bullet-hell roguelike that simultaneously controls two characters, a powerful mech and a sniper frog. It combines ability and weapon customization [source: genre-summary web-search synthesis from bulletheavengames.com, verified 2026-08].

## Failure Cases
<!-- Evidence insufficient: no failure or severe-review case explicitly attributed to simultaneous squad control was found. The following is a community signal showing the tension inherent in this control method -->
- [interpretation] Some in the community requested manual control and firing, saying that strategic feel is weak when each character aims and fires automatically [source: Steam community discussion "Manual Control", Yet Another Zombie Survivors, verified 2026-08].

## User Reaction Summary
- Preference: "The controls are simple, but the screen is packed with a squad" - an evaluation that it adds strategic depth without complex controls [source: Steam review aggregation, verified 2026-08].
- Aversion: Some users want to aim and fire directly rather than use auto-aim. Others rebut that manual tracking of multiple characters is difficult at average reaction speeds, so automation is better [source: Steam community discussion, verified 2026-08].

## Synergy
- Good: GENRE-019 (survivor-like) - This forms an exception and variation axis to the genre definition of single-character auto-combat.
- Bad: When combined with exponential score scaling (ELEM-022), screen effects overlap according to character count and readability can fall sharply - restraint is especially necessary with exaggerated visual feedback (ELEM-031).

## Risks
- [interpretation] As character count rises, the amount of screen information rises, risking dilution of the genre's core appeal of simple controls.
- [interpretation] As long as auto-combat remains, each character's individuality appears only through stat and appearance differences, so content-production cost grows with the increased character count.
