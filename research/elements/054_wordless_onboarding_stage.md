+++
card_id = "ELEM-054"
type = "mechanic"
title = "Wordless Onboarding Stage"
summary = "A game's first side-scrolling stage is authored as the tutorial itself, arranging enemies, blocks, and gaps so the player learns the core verbs by playing, with no text panel, prompt overlay, or separate tutorial mode"
tags = ["level-design", "2d", "side-scroller", "onboarding", "tutorial", "teaching", "first-hour"]
updated = "2026-08-22"
confidence = "medium-low"
+++
## Definition
The opening stage carries a teaching job instead of delegating it to instructions. Every early object is placed so that the natural thing to try is the correct thing, and so that a wrong guess is survivable: the first enemy approaches slowly on flat ground, the first block sits where a jump will hit it, the first hazard is visible before it can be reached. The player is not told the rules; the arrangement makes the rules the easiest conclusion to draw. The success test is that a player who read nothing can state what the buttons do by the end of the stage.

## Success Cases
- World 1-1 of Super Mario Bros. was designed as a tutorial level containing what the player needs so that they "gradually and naturally understand what they're doing", with the team weighing how to teach several things at once: avoiding an enemy, defeating an enemy, how question blocks behave, and how to tell a Goomba from a helpful mushroom. [source: Eurogamer interview with Shigeru Miyamoto, as of 2015-09-08]
- Miyamoto described the working method as repeated simulation of the player rather than instruction: "We kept simulating what the player would do." [source: Eurogamer interview with Shigeru Miyamoto, as of 2015-09-08]
- The stated goal of the opening is a handover of authorship: the player should "learn what the game is all about" and then "start to play more freely", and "once the player realizes what they need to do, it becomes their game." [source: Eurogamer interview with Shigeru Miyamoto, as of 2015-09-08, reported by Game Developer, "How Miyamoto built Super Mario Bros.' legendary World 1-1"]
- [interpretation] The reusable technique is ordering by consequence, not by complexity: teach each verb first in the arrangement where getting it wrong costs the least, then combine.

## Failure Cases
<!-- No evidence: no sourced postmortem was found attributing a shipped side-scroller's failure to a wordless opening stage or to the forced-tutorial alternative; available discussion is opinion pieces and forum threads rather than primary evidence. -->

## User Reaction Summary
<!-- No evidence: no sourced player-sentiment or retention data specific to wordless opening stages was found. -->

## Synergy
- ELEM-053 (Four-beat Stage Structure): direct pair — the onboarding stage is that beat order applied to the game's base verbs. [interpretation]
- ELEM-055 (Bite-sized Rooms with Instant Respawn): compatible — cheap failure lets an opening stage teach by letting the player be wrong, instead of protecting them from being wrong. [interpretation]
- ELEM-031 (Exaggerated Visual Feedback): supporting — a verb taught only by arrangement still needs a legible response at the moment of contact, or the lesson is ambiguous. [interpretation]
- ELEM-052 (Assist and Accessibility Options): complement — a wordless opening removes reading load for some players but raises the precision floor for others; the assist card covers the second group. [interpretation]
- ARCH-024 (Tilemap Level Structure): implementation fit — teaching arrangements are iterated many times, and layer-separated tilemaps make each pass cheap. [interpretation]
- GAME-032 (LIMBO): a side-scrolling puzzle platformer whose atmosphere is carried without text; the same restraint applies to its instruction. [interpretation]
- Genre anchor: GENRE-041 (Precision 2D Side-scrolling Platformer) — this cluster names this element as a component. [interpretation]

## Risks
- [interpretation] The lesson is invisible in review. Nothing in the build reports that teaching failed, so this stage needs observed playtests with players who have never seen the game.
- [interpretation] A wordless opening cannot teach a rule the player cannot see. Off-screen consequences, resource rules, and menu systems still need an explicit surface.
- [interpretation] The technique is expensive per verb. A game with a large verb set cannot teach all of it this way inside one stage without the stage becoming a checklist.
- [interpretation] Skippable or randomized first stages break the guarantee, because the teaching order is the design.
- [interpretation] Returning players get no fast path. Without a way to move through the opening quickly, the teaching stage becomes a toll on every replay.
