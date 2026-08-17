+++
card_id = "ARCH-033"
type = "structure"
title = "Level State Overlay"
summary = "A structure that holds one authored space in several meaning-states by keeping a single base level and switching declared overlays on top of it, instead of duplicating the level per state"
tags = ["level-design", "scene", "additive", "prefab-variant", "authoring", "state", "unity", "2d"]
updated = "2026-08-17"
confidence = "medium"
+++
## Problem
A narrative level often has to exist twice: the corridor the player explored calmly, and the same corridor after the story changed what it means. [interpretation] The obvious answer — copy the level and edit the copy — doubles every later fix, and the two copies drift until a collider exists in one state and not the other. The opposite answer — mutate the level procedurally at runtime — makes retries non-deterministic, which is unacceptable when the altered state is also a timed chase. The structural question is where the difference between states lives: in a duplicated scene, in scattered runtime code, or in one declared, inspectable overlay.

## Structure
- Base layer: the space authored once, holding the geometry, collision, and props common to every state. The project baseline already places world objects, including tilemaps and lighting objects, in Chunk scenes rather than in the always-loaded base scene. [source: reference/unity_project_baseline_active.md chunk rules]
- Overlay layer: the per-state difference, added on top rather than replacing the base. Unity's `LoadSceneMode.Additive` "Adds the Scene to the current loaded Scenes", while `LoadSceneMode.Single` "Closes all current loaded Scenes and loads a Scene" — additive is the mode that lets a second authored asset coexist with the base. [source: Unity Scripting Reference, SceneManagement.LoadSceneMode, as of 2026-08-17]
- Object-level differences that are too small for their own scene use prefab variants instead. "A prefab variant inherits properties from a base prefab. Overrides in the variant take precedence over the base values", and Unity's own example is basing several enemy types on one prefab while varying speed, added objects, or sound effects. [source: Unity Manual, Prefab Variants, as of 2026-08-17]
- Declaration layer: which overlay belongs to which state is data, not a code branch. ARCH-012 owns that table as project data assets so the mapping is editable without touching scripts.
- Ownership: ARCH-023 performs the load and unload; nothing else calls scene APIs. ARCH-032 decides *when* a state change is permitted; the overlay layer only performs it. [interpretation]
- Layer separation inside the base: ARCH-024 already splits drawing, collision, and detection into separate tilemaps, which is what makes it possible for an overlay to replace collision alone without redrawing the space.

## Core Rules
- One base level per place. A second authored copy of the same place is a defect, not a state. [interpretation]
- A state is named by a stable ID stored in data; scene names and object names are never the source of truth for which state is active. [interpretation]
- Overlays add and remove; they do not edit the base level's assets. Anything the base needs to know about the overlay arrives as an event, following the baseline rule that consumers depend on the broadcast rather than reading another system's fields. [source: reference/unity_project_baseline_active.md broadcast rules]
- The same state ID must produce the same colliders, timings, and spawn positions on every entry, including a retry after failure. [interpretation]
- The base scene stays loaded across overlay swaps, matching the baseline requirement that the always-loaded scene remains while chunk scenes are added or removed. [source: reference/unity_project_baseline_active.md chunk rules]
- Every accepted state change emits one event ID that can be checked in the logs, whose line structure is `[time] [event ID] [reaction summary]`. [source: reference/unity_project_baseline_active.md logging rules]

## Unity Implementation Steps
1. Author the place once as the base level, keeping world objects and tilemaps in the chunk-scene role defined by the baseline structure. [source: reference/unity_project_baseline_active.md baseline structure]
2. Assign a stable ID to each meaning-state of that place, and record the base-to-overlay mapping in an ARCH-012 data asset.
3. Split the difference by size: whole-space differences (added corridors, replaced collision, new lighting rigs) become additive overlay scenes; single-object differences become prefab variants of the base object. [source: Unity Manual, Prefab Variants, as of 2026-08-17]
4. Route the load through ARCH-023 using additive mode so the base level is never closed by the swap. [source: Unity Scripting Reference, SceneManagement.LoadSceneMode, as of 2026-08-17]
5. Ask ARCH-032 to authorize the state change first; perform the swap only on an accepted transition, and publish the resulting event through the broadcast layer. [source: reference/unity_project_baseline_active.md broadcast rules]
6. Persist only the active state ID through ARCH-004; never serialize scene references or loaded-object handles. [interpretation]
7. Unload the previous overlay on transition, and re-apply the saved state ID before any trigger in the space is allowed to evaluate. [interpretation]

## Anti-patterns
- Duplicated place: the altered version is a full copy of the level scene, so every later geometry fix must be made twice and the copies silently diverge. [interpretation]
- Runtime mutation: scripts move, delete, and spawn geometry to build the altered state at play time, so a retry produces a different layout and a timed sequence becomes unfair. [interpretation]
- Single-mode loading for a state change: swapping states with `LoadSceneMode.Single` closes the base level as well, discarding the shared space the structure exists to preserve. [source: Unity Scripting Reference, SceneManagement.LoadSceneMode, as of 2026-08-17]
- Scene-name truth: reading the loaded scene's name to decide which state is active, which confuses presentation with declared state — the same confusion ARCH-032 names for narrative beats. [interpretation]
- Overlay-owned progress: an overlay writes save data or story flags directly, coupling level authoring to persistence and to narrative ownership. [interpretation]
- Base edits from the overlay: the overlay reaches into base objects and changes their values, so unloading it leaves the base in a state no one authored. [interpretation]

## Verification
- Determinism test: enter the same state ID repeatedly, including after a failure, and confirm identical collider placement, trigger timing, and spawn positions each time. [interpretation]
- Swap-integrity test: after loading and unloading every overlay for a place, the base level's object count and collision match a freshly loaded base. [interpretation]
- Save/reload test: restore in each state and confirm the same state ID and the same active overlay return before any trigger evaluates. [interpretation]
- Transition-log test: each accepted state change writes exactly one log line in the declared `[time] [event ID] [reaction summary]` structure, and a repeated request adds no duplicate line. [source: reference/unity_project_baseline_active.md logging rules] [source: reference/unity_project_baseline_active.md self-check criteria]
- Runtime check: zero compile errors and zero console errors during normal operation. [source: reference/unity_project_baseline_active.md self-check criteria]

## Synergy
- ARCH-002 (Scene Streaming): supplies the additive load and unload discipline this structure reuses for overlays instead of world chunks.
- ARCH-024 (Tilemap Level Structure): the drawing/collision/detection layer split is what lets an overlay replace one layer without re-authoring the space.
- ARCH-012 (ScriptableObject Data): stores the state-to-overlay mapping outside scenes and scripts.
- ARCH-023 (Game Flow Scenes): the single owner permitted to call scene load and unload.
- ARCH-032 (Narrative Beat and Flag Ledger): authorizes when a place may change state; this card only executes the change.
- ARCH-004 (Save System): persists the active state ID, not scene or object references.
- ARCH-027 (URP 2D Lighting): lighting rigs are a common whole-space difference and belong in the overlay rather than in the base.
- ELEM-051 (Unkillable Pursuer Chase): the consuming case — a chase through an altered version of an explored space is exactly what demands deterministic overlays.
