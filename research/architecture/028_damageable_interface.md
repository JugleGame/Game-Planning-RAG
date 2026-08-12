+++
card_id = "ARCH-028"
type = "pattern"
title = "Hit/Damage Interface (IDamageable + Health Component)"
summary = "A combat structure that treats enemies, players, and boxes in the same way by binding them together with one promise that 'the hitting side can take damage' without knowing the identity of the hitting side."
tags = ["combat", "damage", "interface", "health", "pattern", "unity", "2d"]
updated = "2026-08-02"
confidence = "medium"
+++
## Problem
The attack can reach enemies, crates, and the player himself. At this time, the code on the hitting side is
If you start checking one by one, "Is this an enemy? Is this a box? Is this a player?", what can be hit?
Every time there is an increase, the entire attack code must be modified. A sign saying "I can get hit" is given to the person who gets hit.
This structure is to sweeten and have the person hitting only see the sign.

## Structure
- There is only one promise. The "can take damage" interface defines the window through which damage is applied,
Any target that can be hit implements this. The target can be anything: an enemy, a player, a box, or a door. [source: Medium 'IDamagable Interface in Unity' (James Lafritz), check 2026-08].
- The hitting party only checks whether the person it collided with had this promise, and if so, passes on the damage. The opponent
I don't know what it is. [source: Medium 'IDamageable Interface in Unity' (tmaurodot), check 2026-08].
- Stamina is held by the component, not the interface. A promise is a "how to receive" and how to endure...
What happens when you die is implemented differently for each subject.
- Death/hit broadcasts the result (ARCH-001). The health bar, sound effects, and commentator only listen to this broadcast and react.
The combat code does not call UI or audio directly.
- [interpretation] This card is another axis with the same shape as ARCH-006 (interaction). Interaction is "the player
If it is "intentionally approached and dealt with," then this card is "damage is delivered regardless of intention."
If you combine the two into one interface, it becomes confusing whether you have to hit or press the box to open it.

## Core Rules
- The party doing the damage does not check the specific type of the opponent. The moment a type test appears, this structure
The reason for writing disappears.
- Stamina values ​​are not directly modified from the outside. Change always goes through the damage/recovery window. Then, negative stamina,
Conditions such as additional damage after death can be prevented in one place [source: Medium 'IDamageable Interface in Unity' (tmaurodot), check 2026-08].
- Death processing must occur only once. Even if multiple feet hit the same frame, there is only one death broadcast.
- The default values ​​for damage and health are placed in the data asset rather than in the code (ARCH-012).
- Like invincibility time and team division, the decision of “whether to hit or not” is made by the side that gets hit. The person hitting knows the exception.
When you start, it goes back to the type check.
- [interpretation] Even if the sources are different, such as projectiles, floors, or falling missiles, the window must be the same. If there are multiple windows, you are treated as invincible.
Each log is split.

## Unity Implementation Steps
1. Define one promise to be harmed. At the very least, you receive the amount of damage and, if necessary, who did it.
2. Let's create a fitness component and implement this promise. The lower limit of physical strength and death judgment are placed here.
3. Attach this component to the enemy, player, and destructible object prefabs. So you can fit it just by sticking it on
It has to be.
4. The attacking side (proximity checks, projectiles, trap triggers) looks for this promise in the collision opponent and passes the damage if it is found.
5. The incident is broadcast at the time of attack or death. Health bars, sound effects, and effects are attached to that subscriber (ARCH-014, ARCH-017).
6. Dead objects are disposed of by return, not destruction. In the small grass that dies and grows frequently,
It was borrowed (ARCH-015).
7. A log is left for each hit (ARCH-010). The battle passes in an instant and cannot be verified with the eyes.

## Anti-patterns
- Check each type of target one by one: As the number of targets that can be hit increases, the attack code grows together.
- Keep stamina open as a public variable: It is impossible to track where it was cut, and invincibility and death processing are scattered all over the place.
- Duplicate death processing: This is a typical glitch where the same enemy dies twice and rewards are paid twice.
- Attack code directly calls UI/sound: Combat and expression become attached, making it impossible to change just one of them.
- Adding damage to interactive interfaces: The two axes are mixed up, resulting in “talk to and take damage” kind of thinking.
- Putting the damage amount as a constant in the script: Balance adjustments become code modifications, and the data protocol (ARCH-012) becomes ineffective.

## Verification
- Application check: All prefabs that can be hit must have a health component. The missing prefab is
The attack passes.
- Type-independent check: Newly created destructible objects must take damage without modifying the attack code.
- Lower limit test: Stamina must not fall to negative numbers.
- Redundant death check: Even if multiple shots hit at the same time, only one death broadcast must remain — check by number of log lines [source: reference/unity_project_baseline.md Section 3 log rules].
- Log check: If the battle is performed 1 times, a line with the corresponding event ID should remain.
- Console check: Console error 0 while repeating battle [source: reference/unity_project_baseline.md 4 self-check].

## Synergy
- ARCH-006 (Interaction): Partner card and borderline. Intentional contact is on that side, and damage delivery is on this side.
- ARCH-001 (Event Bus): Attack/death broadcast route. The point where combat separates from expression.
- ARCH-012 (Data/Data Asset Protocol): Storage location for damage and health.
- ARCH-015 (Object Pooling): Engages in both death handling and projectile creation.
- ARCH-010 (Rogue Protocol): The only evidence of combat verification.
- ARCH-005 (NPC State Machine): A representative consumer who changes states by receiving a broadcast of being hit.
- ELEM-014 (Punitive Death Cycle): Compatibility required — what death takes away determines the nature of the game,
The list of subscribers to the death broadcast is the blueprint for that punishment.

