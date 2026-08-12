+++
card_id = "ARCH-004"
type = "pattern"
title = "Save System (JSON Serialization)"
summary = "A structure that turns game state into a human-readable JSON document, writes it safely to the per-platform save path, and restores it"
tags = ["save", "persistence", "json", "core", "unity", "data"]
updated = "2026-07-29"
confidence = "high" # 프로젝트 기준 구조(reference/unity_project_baseline.md)의 SaveSystem(JSON) 명시 + Unity 공식 API 근거
+++
## Problem

Close the game and reopen it, and everything the player did is gone. In a game played over long sessions, like an open world, that is fatal. On top of that, in a structure where chunks are switched off constantly (ARCH-003), state has to be left somewhere not only "on quit" but also "when a chunk unloads". Put simply: it is like forgetting the moment you leave the room because you never wrote it in a notebook. The save system is that notebook, and JSON is the handwriting you use in it.

## Structure

- Location: `Assets/Scripts/Core/SaveSystem` — the save format is JSON. [source: reference/unity_project_baseline.md baseline structure]
- Layers: game state object (a plain data class) → serialize → string → file. Reverse the order to restore.
- The save location sits under `Application.persistentDataPath`. That path resolves to the correct location per platform on its own, so never write a path by hand. [source: common recommendation across Unity save-system write-ups]
- Two save granularities — global state (player position, inventory, progression) and chunk state (per-chunk changes). Chunk state is stored separately keyed by chunk coordinate so only what is needed gets read.
- The serializer is either Unity's built-in JsonUtility or an external library — pick one. The built-in one has no dependencies but cannot serialize some types such as Dictionary directly, so it needs wrapper classes. [source: write-ups on Unity JsonUtility] Adding an external library is subject to human approval. [source: reference/unity_project_baseline.md prohibited list]

## Core Rules

- Keep save data classes separate from gameplay classes. Do not try to save a MonoBehaviour as-is. "Data for saving" lives in its own plain class.
- Put a version number in every save file. Without one, changing the structure later means blowing up while reading an old save with no way to know how to fix it.
- Write atomically: write to a temporary file first → on success, swap it into place. If the game dies mid-write, the existing save survives. [source: Unity save best-practice write-ups — the write-temp-then-swap approach]
- No hardcoded paths. Always compose them relative to `Application.persistentDataPath`.
- Saving and loading themselves may be called directly without going through the event bus (ARCH-001). Collecting "what happened", though, is cleaner done by subscribing to the bus, which keeps gameplay code uncluttered.

## Unity Implementation Steps

1. Create `Scripts/Core/SaveData.cs` — a plain data class holding a version field, global state fields and a list of chunk states. Mark it serializable.
2. Create `Scripts/Core/SaveSystem.cs` — expose only two public functions, Save(data) and Load().
3. Decide the path — create a save folder under persistentDataPath and settle a per-slot filename rule.
4. Implement atomic writing — write temp file → back up the existing file → swap. Roll back if any step fails.
5. Implement loading — if the file is absent, return new-game defaults (do not throw an exception and stall the game). If the version differs, run it through a conversion function.
6. Wire up chunks — the ARCH-003 loader hands over a chunk's changed state just before unloading it, and restores it right after loading.
7. Self-check — save, restart the game, confirm the state was restored.

## Anti-patterns

- Saving progression in PlayerPrefs: PlayerPrefs is for settings (volume, resolution). Putting progression there leaves it unstructured and hard to port or back up.
- Overwriting during a save: writing straight to the real file with no temp file. Quit mid-write and the save is corrupted, taking all of the player's progress with it. The damage from this mistake cannot be undone.
- Versionless saves: adding even a single field later leaves no way to read old saves.
- Saving GameObject references: trying to persist references to scene objects. References differ on every run, so always convert them to values such as an ID or a coordinate.
- Saving every frame: it looks safe, but file writes are expensive. Fix the save points (area transition, quit, fixed interval) and write only then.
- Hardcoding absolute paths: the classic reason something works on the development PC and cannot find the file on any other platform.

## Verification

- 0 compile errors, 0 console errors. [source: reference/unity_project_baseline.md self-check criteria]
- Round-trip check: change state → save → quit the game → relaunch → load, and confirm the values match.
- Missing-file check: launching with the save file deleted must start a new game without errors.
- Corrupt-file check: launching after deliberately damaging the save file must not kill the game — it recovers or falls through to a new game.
- Atomicity check: no temporary file may remain right after a save.
- Chunk round-trip check: run the same scenario as ARCH-003's state-persistence check, verified against the save file as well.

## Synergy

- ARCH-003 (chunk loader): the relationship that hands state over on chunk unload. If the two cards' rules disagree, the world reverts.
- ARCH-001 (event bus): gathering what happened via subscriptions keeps save logic from bleeding into gameplay code.
- ELEM-014 (punishing death loop): fit warning — a design that gives death weight is directly tied to the save-point rule. Where the game saves *is* the difficulty, so save timing is a design decision, not a technical one.
- Conflict warning — real-time autosave and a punishing death design can cancel each other out. Using both means drawing a clear line between what is saved and when.
