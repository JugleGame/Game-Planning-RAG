+++ 
card_id = "ARCH-009"
type = "pattern"
title = "2D Physics Movement (Rigidbody2D)"
summary = "A movement approach that does not teleport the character by coordinates but asks the physics engine to 'please move it this way', so that walls and collisions work properly"
tags = ["physics", "rigidbody2d", "movement", "player", "unity", "2d"]
updated = "2026-07-29"
confidence = "high" # 프로젝트 기준 구조(reference/unity_project_baseline.md)의 Rigidbody2D 명시 + Unity 공식 Scripting API 근거
+++ 
## Problem

The easiest way to move a character is to add a value to its coordinates. But doing that moves the character without the physics engine knowing, so it passes through walls or collision handling bounces strangely. Put simply: if you pick up a chess piece by hand and move it, you can ignore the rules and put it anywhere. To keep to the rules you have to tell the referee "I am going here" and then move. The physics engine is that referee.

## Structure

- Location: `Assets/Scripts/Player/` — PlayerController (Rigidbody2D), PlayerInput. [source: reference/unity_project_baseline.md baseline structure]
- Role separation — separate the side that reads input (PlayerInput) from the side that moves with physics (PlayerController). This is because input runs every frame while physics runs on a fixed cycle.
- Physics updates are done in FixedUpdate. Movement code must match the physics cycle for consistent results. [source: Unity official Scripting API — the FixedUpdate recommendation in the Rigidbody2D.MovePosition documentation]
- Two movement methods — (1) Dynamic Rigidbody2D + setting velocity: suited to a player that needs physical reactions such as collisions and being pushed, (2) Kinematic Rigidbody2D + MovePosition: suited to targets that move as prescribed, such as patrolling NPCs or moving platforms. [source: Unity official Scripting API and the summary of Rigidbody2D movement methods]
- Do not set a Dynamic Rigidbody2D's position or rotation directly through Transform. This is because the physics simulation recomputes the position based on velocity. [source: the Unity official documentation's guidance against directly manipulating Transform]

## Core Rules

- Movement in FixedUpdate, input reading in Update. Mixing the two makes you miss input or makes movement waver with the frame rate.
- No assigning transform.position on a Dynamic body. What you need is movement, not "teleportation"; and if you really need teleportation, you must clean up the physics state along with it.
- Unify in one place the rule for multiplying movement values by frame time (delta). Setting velocity and moving position handle time differently, so mixing them makes speeds subtly differ.
- NPC patrol movement (the Patrol of ARCH-005) follows this rule too. If only NPCs change coordinates directly, collisions go out of alignment.
- For top-down 2D that needs no gravity, set the gravity scale to 0, but record that decision in a card or spec. Keep people from wasting time later on "why doesn't it fall?".

## Unity Implementation Steps

1. Attach a Rigidbody2D and a 2D collider to the player object. For top-down, confirm gravity scale 0 and rotation locked (Freeze Rotation Z).
2. `Scripts/Player/PlayerInput.cs` — in Update, only read and hold the input direction. Do not move anything here.
3. `Scripts/Player/PlayerController.cs` — in FixedUpdate, move the Rigidbody2D with the held direction and speed.
4. Decide the movement method — the player uses Dynamic + setting velocity by default. Targets that need no pushing or recoil use Kinematic + MovePosition.
5. Check collisions — place a wall collider and see that pushing against it does not go through.
6. Combat and hit events are broadcast on the event bus. [source: reference/unity_project_baseline.md broadcast rules]
7. Self-check — confirm 0 compile and console errors, then commit.

## Anti-patterns

- Assigning transform.position directly: the most common mistake. It is the main cause of passing through walls (tunneling) and abnormal collision responses, and it makes the physics engine and the code believe different positions are the truth.
- Physics movement in Update: it causes the character to move faster on high-frame-rate devices. Physics must be on the fixed cycle.
- Movement without a collider: attaching only a Rigidbody2D without a collider means collisions are not detected at all.
- Mixing the two methods: using both setting velocity and moving position on the same object. They overwrite each other's results and become unpredictable.
- Leaving very fast movers on default collision detection: a fast object skips over a wall between physics steps. Continuous collision detection must be set.
- Overusing scale to flip a character: handling left-right flipping with a negative scale can distort child colliders. Use the sprite flip option.

## Verification

- 0 compile errors, 0 console errors. [source: reference/unity_project_baseline.md self-check criteria]
- Wall penetration check: continually pushing against a wall must not pass through it.
- Frame independence check: even with different frame rate caps, the distance moved over the same amount of time must be the same.
- Method consistency check: the code must contain no assignment of transform.position on a Dynamic body (verifiable by search).
- Broadcast check: on combat-related actions, an event line must remain in `Logs/commentator.log`. [source: reference/unity_project_baseline.md logging rules]
- Input loss check: a briefly pressed input must not be ignored (whether the structure of reading in Update and consuming in FixedUpdate is kept).

## Synergy

- ARCH-005 (NPC State Machine): the actual movement of the Patrol state follows this rule.
- ARCH-002 (Scene Streaming): compatibility caution — the moment a chunk is loading, colliders may not exist yet, and in that gap the character can fall below the terrain. Restricting movement before loading completes or handling a safe position is needed.
- ARCH-001 (Event Bus): the broadcast path for combat and hit events. However, immediate physical reactions such as knockback should be handled directly in the relevant component rather than going through the bus.
- ELEM-011 (Emergent System Interaction): good compatibility — movement properly riding on the physics rules becomes the foundation for unexpected interactions. Conversely, with a coordinate-assignment approach such emergence is impossible altogether.
