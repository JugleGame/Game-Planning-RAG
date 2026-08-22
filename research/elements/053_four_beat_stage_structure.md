+++
card_id = "ELEM-053"
type = "mechanic"
title = "Four-beat Stage Structure (Introduce / Develop / Twist / Conclude)"
summary = "A side-scrolling stage is authored as one mechanic taken through four ordered beats — safe introduction, complication, a change-up that breaks the expected use, and a conclusion that lets the player show what was learned — after which the mechanic is dropped"
tags = ["level-design", "2d", "side-scroller", "stage-structure", "pacing", "teaching", "kishotenketsu"]
updated = "2026-08-22"
confidence = "medium-low"
+++
## Definition
A stage is built around a single idea rather than a length of terrain. The idea appears first in a place where failing costs nothing, is then repeated under a harder arrangement, is next used in a way the player did not expect, and finally is asked for once more as a closing test. When the stage ends the idea is retired instead of being carried forward as filler. The four beats give an author a stopping rule: when the change-up and the conclusion are spent, the stage is finished, and a fifth room of the same idea is repetition, not content.

## Success Cases
- Koichi Hayashida, director of Super Mario 3D Land and Super Mario Galaxy 2, described the structure this way: "Something that's talked a lot about in Japanese manga, for example, is a phrase, kishoutenketsu, where you introduce a concept, and then in the next panel you develop the idea a little bit more; in the third panel there's something of a change-up, and then in the fourth panel you have your conclusion." [source: Game Developer, "The secret to Mario level design", Christian Nutt, as of 2012-04-13]
- The same interview states the player-facing order plainly: "First, you have to learn how to use that gameplay mechanic, and then the stage will offer you a slightly more complicated scenario in which you have to use it." [source: Game Developer, "The secret to Mario level design", Christian Nutt, as of 2012-04-13]
- The structure entered Nintendo through Shigeru Miyamoto, who drew comics as a child and would ask what the closing beat of a level was going to be. [source: Game Developer, "The secret to Mario level design", Christian Nutt, as of 2012-04-13]
- [interpretation] The transferable part is not the Japanese term but the retirement rule. Each idea gets one stage, and the twist beat is what stops the stage from being four rooms of the same jump.

## Failure Cases
<!-- No evidence: no sourced case was found of a shipped side-scroller whose stages failed specifically because they followed or abandoned this four-beat order. -->

## User Reaction Summary
<!-- No evidence: no player-sentiment data tied to this structure specifically was found; players react to individual stages, not to the authoring order behind them. -->

## Synergy
- ELEM-054 (Wordless Onboarding Stage): direct pair — the onboarding stage is the first beat applied to the game's base verbs instead of to one stage-local idea. [interpretation]
- ELEM-055 (Bite-sized Rooms with Instant Respawn): compatible — one beat per room gives the four beats a physical container, and cheap failure keeps the twist beat from becoming a wall. [interpretation]
- ARCH-024 (Tilemap Level Structure): implementation fit — separating drawing, collision, and detection layers lets a beat be rearranged without redrawing the stage. [interpretation]
- ARCH-033 (Level State Overlay): fit for the twist beat, where the same authored space has to read differently after the change-up rather than being rebuilt as a second stage. [interpretation]
- ELEM-012 (Landmark-based Exploration): shared idea at a different scale — both place the thing to be understood in view before asking for it. [interpretation]
- GENRE-014 (Side-scrolling Horror), GENRE-017 (Metroidvania): both consume authored 2D stages and can host the beat order, though a metroidvania's non-linear reopening breaks the assumption that beats are met in order. [interpretation]
- Genre anchor: GENRE-041 (Precision 2D Side-scrolling Platformer) — this cluster names this element as a component. [interpretation]

## Risks
- [interpretation] The rule needs one idea per stage. A stage with three mechanics has twelve beats and no legible shape.
- [interpretation] The twist beat is the one most often skipped under schedule pressure, and skipping it turns the stage into a difficulty ramp with nothing to remember.
- [interpretation] Retirement costs content. Dropping the idea after one stage means each stage needs a new one, which is an authoring-throughput problem, not a design problem.
- [interpretation] The order assumes a linear route. In a stage the player can enter from either side, the introduction beat is not guaranteed to come first.
- [interpretation] The structure teaches nothing on its own if the introduction beat is not actually safe — a first encounter that can kill converts the whole stage into trial and error.
