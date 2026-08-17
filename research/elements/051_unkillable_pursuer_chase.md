+++
card_id = "ELEM-051"
type = "mechanic"
title = "Unkillable Pursuer Chase"
summary = "A structure in which a pursuer cannot be defeated by any player attack, so the only available verbs are flee, hide, and distract, and a director decides when pressure rises and falls"
tags = ["horror", "chase", "pursuer", "no-combat", "pacing", "director-ai", "fairness"]
updated = "2026-08-17"
confidence = "medium"
+++
## Definition
One enemy is exempt from the game's combat rules. Weapons, damage, and stagger do nothing to it, so the player can only run, hide, or briefly push it away. Because the threat never resolves, the designer — not the player's aim — decides how long each encounter lasts. Well-built versions therefore separate two jobs: an actor that hunts the player, and a director that decides when the hunt intensifies and when it backs off so the player can make progress.

## Success Cases
- Alien: Isolation splits behaviour into a "macro" director-AI and a "micro" alien-AI. The director always knows the player's location and manages a "menace gauge", periodically sending the alien toward the player and then withdrawing it once tension peaks so play can continue. [source: Game Developer, "The Perfect Organism: The AI of Alien: Isolation", Tommy Thompson, as of 2017-10-31]
- The pursuer in that game is stated plainly as unkillable: players can distract it or scare it off, but not remove it. Its behaviour tree carries over 100 nodes, and new behaviours are locked until non-lethal conditions have taught the player the consequence first. [source: Game Developer, "The Perfect Organism: The AI of Alien: Isolation", Tommy Thompson, as of 2017-10-31]
- That design keeps a fairness contract despite the director's omniscience: the alien "never cheats" and teleports only twice in the whole campaign, and then only for cutscene purposes. [source: Game Developer, "The Perfect Organism: The AI of Alien: Isolation", Tommy Thompson, as of 2017-10-31]
- [interpretation] The reusable part is the split. An unkillable pursuer without a director becomes either a constant unavoidable threat or a harmless prop, because nothing else regulates encounter length.

## Failure Cases
- GAME-060 (SOMA): Thomas Grip stated that "the 'chased by monsters'-gameplay was not even a core part of the SOMA-experience", and that in negative user reviews, "When people say they didn't like it, it is almost always because of the monster encounters – a non-core part of the experience." [source: Frictional Games, "SOMA One Year Later", as of 2016-09-23]
- GAME-033 (Little Nightmares III): reviewers repeatedly pointed to a lack of creativity in the pursuers and environments, and many reviews identified the "repetitive formula" as the problem, producing the lowest-rated entry in the series while the atmosphere itself stayed intact. [source: GAME-033 card, Success/Failure Drivers section, as of 2026-07-30]
- [interpretation] Both failures share a shape: the chase was repeated as structure without renewing what the player must read or decide, so it converted from tension into a toll.

## User Reaction Summary
- Demand to skip the chases is measurable rather than hypothetical. Frictional received repeated requests from players who wanted GAME-060's narrative but felt blocked by the creature encounters, and a community mod called "Wuss Mode" was popular enough to validate that demand. [source: Frictional Games, "What is SOMA's Safe Mode?", as of 2017-11-30]
- The studio's answer was not to disable attacks but to redesign creature conduct while keeping every puzzle and event, with the explicit goal that the mode "not feel like a cheat, but for it to be a genuine way of experiencing the game." [source: Frictional Games, "What is SOMA's Safe Mode?", as of 2017-11-30]
- [interpretation] The pattern to read from this: players who leave over chases are usually there for the story, and they are recoverable through an option rather than lost to the genre.

## Synergy
- ELEM-050 (Core Verb as Narrative Metaphor): strong fit — when fleeing is the repeated verb, reversing it at the climax is the payoff the chase has been paying into.
- ELEM-049 (Suppressed Memory and Identity Reconstruction): good fit — an unkillable pursuer reads naturally as something the protagonist cannot resolve by force because it is not external.
- ELEM-048 (Mundane Bonding / Horror Contrast): good fit — the chase gains meaning when it deforms a place the player already knows as safe.
- ELEM-004 (Loop Mechanic): shared constraint — that card requires each repetition to renew new information, dialogue, or build; repeated chases inherit the same requirement.
- ELEM-052 (Assist and Accessibility Options): mitigation pair — this is the mechanic whose failure mode ELEM-052 exists to catch.
- ARCH-005 (NPC State Machine): the pursuer actor's states; the director that schedules pressure is a separate owner. [interpretation]
- ARCH-033 (Level State Overlay): implementation fit — a chase back through an already-explored space needs that space to exist in two authored states with identical timing on every retry.
- Genre anchors: GENRE-014 (Side-scrolling Horror), where evasion and hiding are the basic verbs rather than combat; GENRE-040 (Grief-Reconstruction Psychological Narrative).

## Risks
- [interpretation] Encounter length has no natural end. Without an explicit director rule for backing off, tension becomes attrition.
- [interpretation] The failure condition must be authored, not assumed. If the pursuer cannot be damaged, the design still has to declare what contact does — damage, capture, or restart — before chase difficulty can be tuned at all.
- [interpretation] Retry must be deterministic. A chase that resolves differently on each attempt teaches nothing, and the player reads the loss as arbitrary.
- [interpretation] Repetition without renewal is the dominant failure, as both cases above show. Each chase needs a new thing to read, not only a new backdrop.
- [interpretation] The pursuer's silhouette and behaviour carry the fear. Reusing one pursuer across a long campaign requires deliberate escalation of its behaviour, or the players stop watching it.
