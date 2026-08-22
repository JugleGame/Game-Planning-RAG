+++
card_id = "ARCH-035"
type = "structure"
title = "Room Checkpoint and Deterministic Retry"
summary = "A retry structure for short 2D stage segments in which one room is the unit of both checkpointing and reset, and every restart returns the room to a single authored state so repeated attempts teach the player instead of varying under them"
tags = ["checkpoint", "respawn", "retry", "determinism", "2d", "side-scroller", "physics", "unity", "level-design"]
updated = "2026-08-22"
confidence = "medium"
+++
## Problem

A stage cut into short rooms with fast restarts only works if each restart is the same room. Without one owner of the reset, state leaks across attempts: a moving platform is mid-cycle, a door opened on the previous try is still open, a knocked-back enemy stands somewhere new, an accumulated velocity carries into the first frame. The player is then practising a challenge that changes while they practise, and reads the loss as arbitrary rather than as their own error. The second failure is cost: if the reset is implemented as a full scene reload with a fade, a music restart, and an intro animation, the retry stops being cheap and the room-sized design that depended on cheap failure collapses.

## Structure

The room is the unit. One component owns the room's boundaries, its spawn point, and its reset, and the player controller owns none of it.

- Room record — spawn transform, the set of resettable objects inside the room, and the room's framing data. It lives with the stage content, which the baseline places in chunk scenes rather than in `World_Base` [source: reference/unity_project_baseline_active.md baseline structure; chunk rules].
- Retry owner — a single call that restores the room record, repositions the player, and clears carried motion. It is invoked by death, by a manual restart input, and by entering the room from the previous one, so all three paths converge on one implementation. [interpretation]
- Progress record — the last room entered, persisted through the save system rather than held in the room itself, so quitting mid-stage returns the player to a room boundary and not to an arbitrary coordinate. [interpretation]
- Event surface — room entry and death are broadcast rather than read, matching the baseline rule that player actions including area entry go through `EventBus.Publish(GameEvent)` and that consumers depend on the broadcast rather than on another system's fields [source: reference/unity_project_baseline_active.md broadcast rules].

Determinism is a physics claim, and Unity states its limits directly: "2D physics in Unity can be deterministic on the same machine, but not across different machines", because "Different compilers and different processors implement floating point math differently", and even "a tiny change of processing order can result in a larger simulation change over time" [source: Unity Support, "Determinism with 2D Physics", as of 2024-02-20]. The same document names the only full guarantee: "The only accurate way to guarantee determinism in 2D Physics using Box2D is to reload the Scene. This performs a cold restart, which destroys and recreates the Box2D physics world" [source: Unity Support, "Determinism with 2D Physics", as of 2024-02-20]. A room reset is therefore a deliberate trade — the cheap in-place restore for the expensive cold restart — and the design has to say which rooms need which.

## Core Rules

1. One retry owner. Death, manual restart, and room entry all call the same reset; no system resets a subset of the room on its own. [interpretation]
2. Everything a room contains that can move, open, break, or count is registered as resettable when the room is authored, not discovered at run time by searching the scene. An unregistered object is the standard source of a drifting retry. [interpretation]
3. Reset clears carried motion explicitly — velocity, input buffers, animation state, timers — because position alone does not restore a simulation. [interpretation]
4. Fixed-step simulation only. Determinism "only applies when using a fixed-step simulation update and not a manual variable time-step" [source: Unity Support, "Determinism with 2D Physics", as of 2024-02-20].
5. Rooms whose challenge depends on exact physics reproduction use a scene reload as the reset, and pay its cost knowingly, since a cold restart of the physics world is the documented guarantee [source: Unity Support, "Determinism with 2D Physics", as of 2024-02-20].
6. Retry latency is a budgeted number owned by this structure, not an emergent result of whatever fades and loads happen to run. [interpretation]

## Unity Implementation Steps

1. Author each room as an object in the stage scene carrying its spawn point, its bounds, and the list of resettable children.
2. Implement the reset as restore-in-place: return each registered object to its recorded transform and state, zero the player's `Rigidbody2D` velocity, and clear buffered input and timers before the first simulated frame.
3. Publish room entry and death through the event bus, and let the camera, UI, and audio subscribe rather than being called from the retry path [source: reference/unity_project_baseline_active.md broadcast rules].
4. Persist only the last-entered room identifier through the save system; never persist per-object room state, so a resumed session starts a room from its authored state. [interpretation]
5. For rooms that require a cold physics restart, reload the scene instead of restoring in place, and prefer the asynchronous load path, since Unity documents that `SceneManager.LoadScene` "loads in the next frame, that is it does not load immediately" and recommends `LoadSceneAsync` to avoid frame stutter [source: Unity 6.5 Scripting API, SceneManager.LoadScene, as of 2026-08-22].
6. Keep the reload additive to the always-loaded scene, so the camera, player rig, and UI are not destroyed and recreated on every death [source: reference/unity_project_baseline_active.md chunk rules].
7. Measure the retry: record the time from death to first controllable frame and treat a regression in that number as a bug, not as polish.

## Anti-patterns

- Reloading the whole stage on every death. It is the only documented determinism guarantee, but applying it to every room converts a fifteen-second attempt into a load-screen loop and destroys the reason the stage was cut into rooms at all [source: Unity Support, "Determinism with 2D Physics", as of 2024-02-20]. [interpretation]
- Resetting the player and forgetting the room. The most common leak: the character returns to the spawn point while platforms, doors, and enemies keep the state the previous attempt left them in. [interpretation]
- Letting each object reset itself on a timer. Reset then depends on when death happened rather than on a single instant, so the room's first frame differs between attempts. [interpretation]
- Building the retry path on top of the checkpoint save. Writing a file per death makes the cheapest, most frequent action in the game the one that touches disk. [interpretation]
- Assuming a recorded run reproduces on another machine. Unity states that 2D physics is not deterministic across machines, so replay, ghost, and time-trial features cannot rest on re-simulation alone [source: Unity Support, "Determinism with 2D Physics", as of 2024-02-20].

## Verification

- Fail the same room ten times without leaving it and confirm that the first controllable frame is identical each time: same player position and velocity, same object positions, same timer values.
- Complete a room, re-enter it from the previous room, and confirm the state matches a post-death retry of the same room.
- Quit and relaunch mid-stage and confirm play resumes at a room boundary in the room's authored state, not at the exact death coordinate. [interpretation]
- Log death and room-entry events and confirm one line per occurrence with no duplicates, matching the baseline requirement that a repeated event must not create duplicate log lines [source: reference/unity_project_baseline_active.md logging rules; self-check criteria].
- Confirm 0 compile errors and 0 console errors during normal operation [source: reference/unity_project_baseline_active.md self-check criteria].
- Track per-room death and attempt counts; a room with an outlier count is a level-design finding, and a room where counts cannot be reproduced by a skilled tester is a determinism finding. [interpretation]

## Synergy

- ELEM-055 (Bite-sized Rooms with Instant Respawn): direct pair — this is the structure that mechanic requires, and the retry-latency budget is where that design either holds or fails. [interpretation]
- ELEM-014 (Punishing Death Loop): conflicting — that structure deliberately makes death take resources and restart the player away from the failure, which is the opposite contract; a project picks one per stage type. [interpretation]
- ELEM-053 (Four-beat Stage Structure): compatible — one beat per room makes each retry a retry of exactly one idea. [interpretation]
- ELEM-052 (Assist and Accessibility Options): complement — cheap deterministic retry lowers the cost of an attempt but not the precision required, which is what assist options address. [interpretation]
- ARCH-034 (Side-scroll Camera Framing): dependency — the camera must resolve to the room's frame within the retry budget instead of blending in from the death position. [interpretation]
- ARCH-033 (Level State Overlay): compatible — an overlay declares which authored state a room returns to, which is exactly what a deterministic reset needs to name. [interpretation]
- ARCH-004 (Save System (JSON Serialization)): owns the progress record only; per-attempt room state must never enter the save file. [interpretation]
- ARCH-024 (Tilemap Level Structure): the static collision layer is the part that never needs resetting, which is a reason to keep dynamic room objects out of the tilemap. [interpretation]
