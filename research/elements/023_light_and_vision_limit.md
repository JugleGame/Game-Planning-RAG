+++
card_id = "ELEM-023"
type = "mechanic"
title = "Light Source & Vision Limit (Light Source & Vision Limit)"
summary = "A method that narrows the player's visible range with a light source and makes that light a depleting resource, putting a cost on seeing"
tags = ["horror", "light", "vision", "resource", "tension", "divisive"]
updated = "2026-07-31"
confidence = "medium"
+++
## Definition
This method shows only the narrow area illuminated by a flashlight or lantern rather than the whole screen. The light is not free: leaving it on drains the battery, while saving it leaves the player unable to see ahead. It is like moving through a dark room with one flashlight. The frightening area is not where the light reaches but where it does not, so choosing where to aim becomes the game.

## Success Cases
- Half-Life 2: Episode 1 - A battery that drains quickly in a narrow light cone and recharges slowly made conserving the battery itself create tension [source: Nomads Reviews "Horror Games 101 Part 3", confirmed 2026-07].
- An implementation that made light both a survival tool and a danger that attracts enemies was praised; choice exists when both turning it on and off have costs [source: Game Rant "Great Horror Games Featuring Immersive Flashlight Mechanics", confirmed 2026-07].
- GAME-032 (LIMBO) - Does not use light as a resource, but makes "what cannot be seen" a source of horror by leaving most of the screen dark and showing only silhouettes.
- GAME-035 (Darkwood) - The central device of a day/night loop: move and prepare during the day, then restrict vision to a circular light-source range at night. Estimated revenue about $6,100,000 [source: GAME-035 card].
- GAME-036 (Signalis) - A resource-like vision device that makes the player explore a dark facility only within the flashlight's reach. 96% positive among about 20,000 and 941 Steam reviews [source: GAME-036 card].

## Failure Cases
- Doom 3-style implementation - The method in which turning on the flashlight makes the area outside the cone darker and therefore reduces visibility was repeatedly criticized. Daylight and Slender used the same method [source: Rely On Horror, ResetEra discussion, confirmed 2026-07].
  Failure point: Light took information away instead of providing it, increasing inconvenience without giving the player anything.
- The flashlight was called "the most misused gameplay element in the genre"; when darkness serves only as a substitute for tension and atmosphere, weak implementation becomes obvious [source: Rely On Horror, confirmed 2026-07].

## User Reaction Summary
- Preference: The most frightening moment is walking with the light off to conserve the battery - the response when resource management itself becomes tension [source: Nomads Reviews analysis, confirmed 2026-07]
- Dislike: "Turning it on makes me see less" - when glare simulation feels only harmful to the player [source: ResetEra discussion, confirmed 2026-07]

## Synergy
- Good: ELEM-015 (Stress/Sanity System) - Connecting time spent in darkness to mental strength binds light and sanity into one pressure; even with two meters, the player has one concern.
- Good: ELEM-016 (Grimdark Tone) - Invisible areas draw the tone, allowing atmosphere with less art production.
- Caution: ELEM-020 (Deck-building) - If cards reward more light, darkness disappears late-game and the genre's core evaporates. It is safer for cards to reward "what is gained in darkness" instead.
- Good: ELEM-013 (Pixel Art Style) - Narrowing vision reduces the screen area that must be drawn, overlapping with the low-cost benefit of low-resolution expression. GENRE-015 identifies both elements as cluster components.
- Genre anchors: GENRE-014 (Side-scrolling Horror), GENRE-015 (Pixel 2D Survival Horror) - Both clusters identify this element as a component.

## Risks
- [interpretation] Darkness is a frame, not content: hiding things alone does not create horror; something must actually exist in the dark.
- [interpretation] If light is purely a penalty, the player chooses "always on" as the optimum. Turning it on must also have a cost, such as attracting enemies, for choice to exist.
- [interpretation] Vision restriction is the cheapest way to raise difficulty and is easy to overuse - a pattern shared by the failure cases.
