+++
card_id = "ARCH-002"
type = "structure"
title = "Scene Streaming (Boot / World_Base / Chunk Additive Structure)"
summary = "A world composition approach that never builds the game as one monolithic scene, splitting it into startup, always-on and fragment scenes, then adding only the fragments needed and switching them on and off"
tags = ["scene", "streaming", "additive", "open-world", "core", "unity", "2d"]
updated = "2026-07-29"
confidence = "high" # 프로젝트 기준 구조(reference/unity_project_baseline.md) + Unity 공식 SceneManager 문서 근거
+++
## Problem

Packing an entire 2D open world into a single scene means loading the whole world into memory at startup, so loading drags and memory blows up. Swapping scenes outright instead (Single mode) destroys the player, the UI and the managers along with them, wedging a black screen into every transition. Put simply: stack every library book on your desk and the desk collapses; clear the desk each time you read and your pens disappear too. You need a way to leave the pens on the desk and swap only the books.

## Structure

- Division of labour across three scene types [source: reference/unity_project_baseline.md baseline structure]
- `Boot.unity` — the startup scene. Managers only. It opens first at game start and loads World_Base.
- `World_Base.unity` — player, camera, UI. **Always on** while the game runs. This is the "pens" in the analogy above.
- `Chunk_x_y.unity` — a world fragment. Switched on and off with Additive loading. Terrain, objects and NPCs live here.
- Additive mode is a loading method that appends a new scene without discarding the existing one, so it is used to stitch together wide spaces like an open world. [source: Unity official Scripting API — SceneManagement.LoadSceneMode.Additive]
- Loading uses the asynchronous form (LoadSceneAsync), not the synchronous one (LoadScene). Synchronous loading is a cause of frame hitches. [source: Unity official SceneManager documentation and community write-ups]

## Core Rules

- Chunk rule: world objects must go into a Chunk scene. They do not go into World_Base. [source: reference/unity_project_baseline.md]
- World_Base holds only "things that must stay alive for as long as the game runs". The test: does it need to survive when a chunk is off? Yes → World_Base, no → Chunk.
- A script inside a Chunk scene never references an object in another Chunk directly. A chunk can be switched off at any time, so the reference breaks. Chunk-to-chunk communication uses the ARCH-001 event bus.
- Changing the scene structure itself needs human approval. [source: reference/unity_project_baseline.md]
- The chunk coordinate rule is that the filename `Chunk_x_y` *is* the world coordinate. If the name and the actual position drift apart, the loader switches on the wrong fragment.

## Unity Implementation Steps

1. Create the Boot and World_Base scenes and register them in Build Settings. An unregistered scene cannot be loaded at runtime.
2. Put GameManager in the Boot scene and load World_Base asynchronously in Additive mode at startup.
3. Create Chunk scenes under the grid naming rule (`Chunk_0_0`, `Chunk_1_0`, …) and register those in Build Settings as well.
4. Handle load completion — call the active-scene assignment (SetActiveScene) **after** the asynchronous load finishes. Called right after the load call, it does nothing. [source: Unity Discussions, write-up on assigning the active scene with SceneManager]
5. Check which scene newly instantiated objects belong to. If the active scene is set wrong, chunk objects get created in World_Base and the chunk rule breaks.
6. The actual decision to load and release chunks belongs to the ARCH-003 chunk loader. This card is responsible only up to scene composition.

## Anti-patterns

- One giant scene: cramming the world into a single scene. Convenient early on, but the moment the world grows it collapses irreversibly under loading and memory. Undoing it costs far more than splitting from the start.
- Single-mode scene transitions: swapping scenes on every move. Player, UI and managers are destroyed together, state is lost, and the "continuous world" feeling of an open world disappears.
- World_Base bloat: putting world objects in World_Base because it is convenient. This violates the chunk rule and ends up equivalent to one giant scene.
- Overusing synchronous loading: switching a chunk on with LoadScene (synchronous) stalls that entire frame. To the player it looks like the game froze.
- Activating several chunks in one frame: the instant a scene activates, every object inside it wakes in that same frame, so performance collapses. [source: Unity community write-up — the bulk activation cost at scene-activation time] Spread activation out.

## Verification

- 0 compile errors, 0 console errors. [source: reference/unity_project_baseline.md self-check criteria]
- Scene-membership check: unloading one chunk during play must leave the player, camera and UI alive. If any of them vanishes, something that belongs in World_Base ended up in a chunk.
- Inverse check: unloading a chunk must definitely remove the world objects inside it. Anything left behind violates the chunk rule.
- Loading-method check: the frame must not visibly stall at the moment of a chunk transition (detects synchronous loading slipping in).
- Confirm every Chunk scene is registered in the Build Settings scene list.

## Synergy

- ARCH-003 (chunk loader): the party that actually switches this structure on and off. Structure and loader are always a pair.
- ARCH-001 (event bus): notices when a chunk goes on or off, and chunk-to-chunk communication, all route through the bus. A direct reference will always break on chunk unload.
- GENRE-006 (pixel-art 2D open world / sandbox): the genre this structure presupposes. The whole purpose of stitching a wide world together comes from here.
- Conflict warning — this is overkill for a small stage-based game with no scene-to-scene travel. If the world is a few screens across, a single scene is better.
