+++
card_id = "ARCH-034"
type = "structure"
title = "Side-scroll Camera Framing (Dead Zone + Lookahead + Confiner)"
summary = "A 2D camera rig that frames a side-scrolling stage with three separated controls — a dead zone that ignores small player motion, lookahead that biases the view toward travel direction, and a polygon confiner that stops the view from leaving authored space"
tags = ["camera", "cinemachine", "2d", "side-scroller", "level-design", "unity", "framing", "confiner"]
updated = "2026-08-22"
confidence = "medium"
+++
## Problem

A side-scrolling stage is authored as a readable picture: the player must see a hazard before reaching it, and must never see past the edge of what was built. A camera that rigidly follows the player transform fails both jobs at once. It jitters on every small hop because it reacts to motion that carries no meaning, it shows the same amount of space behind and ahead regardless of travel direction so the player runs into off-screen hazards, and it pans past the last tile into empty background. Solving these inside one follow script produces a single tangle of clamps where changing the framing of one stage breaks another, because three separate concerns — what motion to ignore, where to bias the view, and where the view may not go — are being decided by the same numbers.

## Structure

Keep the camera in the always-loaded scene and the framing data in the stage. The baseline puts the player, camera, and UI in `World_Base.unity`, which stays loaded while stage content is added and removed, and keeps world objects including tilemaps in the chunk scenes [source: reference/unity_project_baseline_active.md baseline structure; chunk rules]. The rig therefore has one persistent camera and one per-stage bounding shape that arrives and leaves with the stage.

Three responsibilities, three owners:

- Framing owner — Cinemachine's Position Composer, which moves the camera in its X-Y plane until the tracking target sits at the desired point on screen, where `Screen Position` gives that point and "Zero represents center; ±0.5 represent edges" [source: Unity Cinemachine 3.1.7 documentation, Position Composer, as of 2026-08-22].
- Motion filter — the dead zone, where "The camera will not adjust when the target is within this range of the Screen Position", the surrounding soft zone in which "the camera will adjust to put it back in the dead zone", and `Damping`, "How responsively the camera tries to maintain the desired position, in each of the three camera-space axes" [source: Unity Cinemachine 3.1.7 documentation, Position Composer, as of 2026-08-22].
- Boundary owner — the Confiner 2D extension, which confines "the camera's position so that the screen edges stay within a shape defined by a 2D polygon" for orthographic or perspective cameras [source: Unity Cinemachine 3.0.1 documentation, Cinemachine Confiner 2D, as of 2026-08-22].

Lookahead belongs to the framing owner rather than to player code: it "Adjusts the offset of the Cinemachine Camera from the Tracking target based on the motion of the target", estimating where the target will be `Lookahead Time` seconds ahead, with `Lookahead Smoothing` where "Larger values smooth out jittery predictions and increase prediction lag", and `Lookahead Ignore Y` to disregard vertical movement in that prediction [source: Unity Cinemachine 3.1.7 documentation, Position Composer, as of 2026-08-22].

## Core Rules

1. The camera lives in `World_Base` and is never duplicated per stage; stage scenes contribute only the bounding shape and any framing overrides [source: reference/unity_project_baseline_active.md baseline structure; chunk rules].
2. Vertical and horizontal framing are tuned separately. In a side-scroller the player crosses the screen horizontally all the time and vertically only on purpose, so `Lookahead Ignore Y` and a taller dead zone are the default rather than the exception. [interpretation]
3. Every playable stage has a confining shape, authored from the level's own geometry so the two cannot drift apart. The documented input is a 2D collider, with a Composite Collider 2D set to `Is Trigger` and `Geometry Type` Polygons as the recommended setup [source: Unity Cinemachine 3.0.1 documentation, Cinemachine Confiner 2D, as of 2026-08-22].
4. Any change to the shape's points or a non-uniform scale must invalidate the cached polygon through `InvalidateBoundingShapeCache()`, because Cinemachine computes and caches a second, smaller polygon and that computation is resource-intensive [source: Unity Cinemachine 3.0.1 documentation, Cinemachine Confiner 2D, as of 2026-08-22].
5. Framing values are stage data, not code constants. A stage that needs a different frame gets different values, not a new camera script. [interpretation]

## Unity Implementation Steps

1. Place one Cinemachine Camera in `World_Base` tracking the player, and set its position control to Position Composer.
2. Set `Screen Position` and `Camera Distance` for the intended frame, then widen the dead zone until ordinary jumps and small steps stop moving the view.
3. Set `Damping` per axis, starting with a slower vertical response than horizontal, because vertical motion in a side-scroller is usually a deliberate act rather than continuous travel. [interpretation]
4. Enable lookahead: set `Lookahead Time` to the horizontal bias the stage needs, raise `Lookahead Smoothing` until direction changes stop snapping, and enable `Lookahead Ignore Y` unless the stage is built around vertical traversal.
5. Author the stage boundary as a Composite Collider 2D on a dedicated object inside the stage scene, using the recommended trigger and Polygons configuration, and reference it from a Confiner 2D extension on the camera.
6. Set the confiner's `Damping`, which "Is applied around corners to avoid jumps", and `Slowing Distance`, which makes the camera "slow down gradually until the edge is reached" as it approaches a boundary [source: Unity Cinemachine 3.0.1 documentation, Cinemachine Confiner 2D, as of 2026-08-22].
7. Swap the bounding shape when the active stage changes, and invalidate the cache on any run-time edit of that shape.

## Anti-patterns

- Hard-clamping the camera transform in `LateUpdate` after Cinemachine has positioned it. The clamp fights the damping that is already running, producing a stutter at the exact moment the player is near an edge and needs the clearest picture. [interpretation]
- Baking the boundary as four numbers per stage. It survives until a stage stops being a rectangle, and then every L-shaped or vertical stage needs a special case, whereas the documented input is a polygon shape [source: Unity Cinemachine 3.0.1 documentation, Cinemachine Confiner 2D, as of 2026-08-22].
- Editing the confining shape at run time without invalidating the cache, which leaves the camera constrained to a polygon that no longer matches the level [source: Unity Cinemachine 3.0.1 documentation, Cinemachine Confiner 2D, as of 2026-08-22].
- Implementing lookahead by offsetting the follow target inside the player controller. The bias becomes movement-code responsibility, and every camera tuning pass then has to be made by someone who can break the character. [interpretation]
- Raising `Lookahead Time` to fix late hazard reads. Smoothing increases prediction lag by documented behaviour, so aggressive prediction trades one readability problem for a swimming view; the stage layout is usually the real fix [source: Unity Cinemachine 3.1.7 documentation, Position Composer, as of 2026-08-22]. [interpretation]

## Verification

- Walk the player to every boundary of every stage and confirm no frame shows space outside the authored shape, including at corners where damping is applied.
- Stand still and hop in place; the camera must not move at all while the target stays inside the dead zone.
- Reverse direction at full speed and confirm the view re-biases without snapping. A visible jump means smoothing is too low; a late frame means it is too high.
- Confirm 0 compile errors and 0 console errors during normal operation, per the baseline self-check criteria [source: reference/unity_project_baseline_active.md self-check criteria].
- Inspect that exactly one camera object exists after several stage loads and unloads; a second one means the camera was placed in stage content instead of `World_Base` [source: reference/unity_project_baseline_active.md chunk rules].

## Synergy

- ARCH-024 (Tilemap Level Structure): direct pair — the same layer separation that holds collision can supply the shape the confiner uses, so camera boundary and level geometry share one source. [interpretation]
- ARCH-033 (Level State Overlay): compatible — when an overlay changes what a space means, framing values and bounding shape are part of what the overlay may swap. [interpretation]
- ELEM-053 (Four-beat Stage Structure): the twist beat depends on the player seeing a change, which is a framing requirement before it is a level requirement. [interpretation]
- ELEM-054 (Wordless Onboarding Stage): dependency — teaching by arrangement only works if the arrangement is on screen at the moment of decision. [interpretation]
- ELEM-055 (Bite-sized Rooms with Instant Respawn): the camera must resolve to the room's frame instantly on respawn, or the retry loop pays a camera-blend tax on every death. [interpretation]
- ARCH-035 (Room Checkpoint and Deterministic Retry): dependency in the other direction — that card's retry budget includes the frame this rig has to produce, so camera settling time is part of its measurement. [interpretation]
- ELEM-012 (Landmark-based Exploration): shared requirement — a landmark the camera never frames cannot pull the player toward it. [interpretation]
- GENRE-014 (Side-scrolling Horror): tension — that cluster uses off-screen space as the raw material of horror, so a wide, generous frame removes the effect the genre depends on. [interpretation]
