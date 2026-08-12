+++
card_id = "ARCH-003"
type = "pattern"
title = "Chunk Loader (3x3 Active Rule)"
summary = "A loading manager that keeps only the surrounding 3x3 chunks active around the tile the player stands on and switches off the ones left behind, holding a wide world at a constant cost"
tags = ["streaming", "chunk", "world", "performance", "open-world", "unity", "2d"]
updated = "2026-07-29"
confidence = "high" # 프로젝트 기준 구조(reference/unity_project_baseline.md)의 3x3 규칙 명시 + Unity 씬 활성화 비용 근거
+++
## Problem

Splitting the world into chunks (ARCH-002) is useless without something deciding "when to switch which chunk on and off". Keeping them all on defeats the point of splitting; keeping only the current tile on means the moment you step sideways you are looking at a world that has not been built yet. Put simply: walking through a dark room with a flashlight, lighting only your feet leaves you blind to the next step. You have to light one step ahead to walk naturally. The 3x3 rule is that "one step ahead".

## Structure

- Location: `Assets/Scripts/World/ChunkLoader` — activates only the 3x3 chunks around the player. [source: reference/unity_project_baseline.md baseline structure]
- State: the chunk coordinate the player currently occupies, and the set of chunk coordinates currently switched on.
- Flow: player position → compute the containing chunk coordinate → only when that coordinate changed → compute the required set (3x3 centred = nine tiles) → load (required but absent) + unload (present but not required).
- Computation: dividing the world coordinate by the chunk size and flooring yields the chunk coordinate. Chunk coordinates map 1:1 onto ARCH-002's scene filenames `Chunk_x_y`.
- Loading and unloading are both asynchronous, and completion notices are broadcast over the ARCH-001 event bus.

## Core Rules

- The active range is fixed at 3x3 including the centre, i.e. nine tiles. Widening the range is a structural change and needs human approval. [source: reference/unity_project_baseline.md]
- Do not compute every frame. Judge whether to refresh **only on the frame where the player's chunk coordinate changed**.
- Entry events must be broadcast. A player entering a chunk is an action covered by the broadcast rule. [source: reference/unity_project_baseline.md broadcast rules]
- The loader knows nothing about what is inside a chunk. Whatever it holds, the loader switches it on and off only at scene granularity. The moment the loader knows the contents, coupling appears and every new chunk means editing the loader.
- Before unloading, hand that chunk's changed state (blocks broken, enemies killed) to the save layer. Skip it and the world looks reverted the next time the player walks back in. The save format follows ARCH-004.

## Unity Implementation Steps

1. Create `Scripts/World/ChunkLoader.cs` — hold fields for chunk size, current coordinate and the active set.
2. Write the coordinate function — take a world position, return a chunk coordinate. Define chunk size as a constant in exactly one place so it cannot drift out of step with the tilemap.
3. Refresh decision — check the player coordinate periodically (not every frame, but on a fixed interval or off movement events) and call the refresh function only when the chunk coordinate changes.
4. Set difference — compare the required set against the current set to build the load list and the unload list. If both are empty, do nothing.
5. Execute loading — process chunks one at a time rather than activating several within a single frame. Simultaneous activation is a frame-drop cause.
6. Execute unloading — in order: save state → unload scene → release unused resources.
7. Broadcast entry events — announce over the event bus on entering a new chunk. The commentator (ARCH-007) listens for this broadcast.

## Anti-patterns

- Full recomputation every frame: recalculating the nine tiles and rechecking load status on every frame. The result is identical on most frames, so it is pure waste.
- Boundary oscillation (chunk thrashing): the same chunk being switched on and off repeatedly while the player stands on a chunk boundary and steps back and forth. Prevent it with a margin at the boundary (hysteresis) — that is, set the switch-on threshold and the switch-off threshold apart from each other.
- Synchronous unloading: handling unload synchronously stalls that frame. Do it asynchronously, as with loading.
- Unloading without saving state: switching a chunk off without persisting what the player did. Come back and the world has reset, giving the worst possible feeling — "what I did has vanished".
- A loader that knows gameplay: putting exceptions like "do not unload if it is the boss chunk" inside the loader. Express exceptions as data (chunk settings) and let the loader execute rules only.

## Verification

- 0 compile errors, 0 console errors. [source: reference/unity_project_baseline.md self-check criteria]
- Active-count check: at any point during play, the number of active chunk scenes must be nine or fewer. Exceeding that means an unload was missed.
- Oscillation check: travelling back and forth across a chunk boundary must not pile up repeated load/unload log lines.
- Broadcast check: entering a chunk must leave an entry-event line in `Logs/commentator.log`. [source: reference/unity_project_baseline.md logging rules]
- State-persistence check: change an object in a chunk → move far enough away to unload it → the change must survive on return.

## Synergy

- ARCH-002 (scene streaming): the structure the loader switches on and off. The two always travel together.
- ARCH-001 (event bus): the path for entry and load-completion notices.
- ARCH-004 (save system): the recipient of the state saved just before unloading.
- ELEM-011 (emergent systemic interaction): fit warning — if a rule like fire spreading has to cross chunk boundaries, the simulation stops in a switched-off chunk. Interactions that cross boundaries need a separate design.
- ELEM-012 (landmark-based exploration): good fit — a landmark visible from afar must stay visible even while its chunk is off, which suits a design that keeps landmarks alone in World_Base or as low-resolution stand-ins.
