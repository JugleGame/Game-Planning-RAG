+++
card_id = "ELEM-011"
type = "mechanic"
title = "Emergent Systemic Interaction (Emergent Systemic Interaction, \"Chemical Engine\")"
summary = "A design in which a few basic rules such as fire, water, and wind collide to produce solutions even the developers did not anticipate"
tags = ["exploration", "physics", "sandbox", "open-world", "high-cost"]
updated = "2026-08-04"
confidence = "medium"
+++
## Definition
This design makes elements such as water, fire, wind, and electricity affect one another according to defined rules. Instead of specifying every result, developers define a few basic rules such as “fire burns wood” and “wind pushes objects”; players combine them and discover solutions the developers did not anticipate.

## Success Cases
- GAME-014 (Breath of the Wild) - Made objects react through elemental reaction rules called a “chemical engine.” Metacritic 98 [source: GAME-014 card].
- GAME-015 (Tears of the Kingdom) - Expanded “elemental reactions” into “structure assembly” through Ultrahand. Sold 10,000,000 copies in three days after release [source: GAME-015 card].

## Failure Cases
<!-- Evidence gap: no open-world case clearly failed after putting this element front and center has been researched yet. Follow-up research is needed. -->
[interpretation] Interlocking systems make bugs and balance difficult to predict, creating a risk that QA costs grow exponentially as the world expands.

## User Reaction Summary
- Preference: Experimentation itself becomes content - “It encourages experimentation and improvisation instead of forcing a set path” [source: The New Yorker review, re-cited by GAME-015 card]
- Preference: Real-world physics can be used as rules to solve puzzles intuitively [source: GDC 2017 talk, re-cited by GAME-014 card]

## Synergy
- Good: ELEM-012 (Landmark-based Exploration) - Combining terrain players want to inspect with freedom to discover what can be done there multiplies exploration motivation.
- Good: ELEM-005 (AI Integration) - [interpretation] AI could explain and extend rule-based reactions in real time, potentially lowering the learning curve (no case yet).
- Genre anchors: GENRE-005 (Open World), GENRE-020 (Survival Crafting Open World), GENRE-032 (Immersive Sim) - All three clusters identify this element as a component.

## Risks
- [interpretation] Initial development costs are very high - every added object must be tested against all existing rules.
- [interpretation] Bugs can become entertainment (for example, physics-bug speedruns), but they are fatal when they instead prevent progress.
