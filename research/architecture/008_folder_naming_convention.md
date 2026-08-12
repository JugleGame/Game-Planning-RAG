+++ 
card_id = "ARCH-008"
type = "convention"
title = "Folder and Naming Convention"
summary = "An agreement that decides in advance where to put a new file and what to name it, so that humans and AI do not have to deliberate every time or place things differently from one another"
tags = ["convention", "naming", "folder", "project-structure", "unity", "workflow"]
updated = "2026-07-29"
confidence = "high" # 프로젝트 기준 구조(reference/unity_project_baseline.md)와 저장소 실제 관례에서 도출
+++ 
## Problem

Without rules for where files go and how they are named, the same kind of code scatters across three places and the names all differ. Especially in this project where AI generates code, it easily creates things in a different place with a different name each time, and then nobody knows what is where. Put simply: if you decide which drawer each thing goes in, you can find it with your eyes closed, but if you put things anywhere you have to search the whole house every time. This card is the drawer label.

## Structure

- Code folder map [source: reference/unity_project_baseline.md baseline structure]
- `Scripts/Core/` — GameManager, SaveSystem, EventBus. Things that stay alive for the whole life of the game.
- `Scripts/World/` — world composition and streaming, such as ChunkLoader.
- `Scripts/Player/` — PlayerController, PlayerInput.
- `Scripts/Interaction/` — IInteractable and interaction handling.
- `Scripts/NPC/` — the NPC state machine.
- `Scripts/Commentator/` — the AI commentator.
- Non-code folders — `Scenes/` (Boot, World_Base, Chunk_x_y), `Prefabs/`, `Tilemaps/`, `Data/`.
- Convention on the research repository side (a separate system) — card files are `research/<kind>/number_english_snake.md`, and card IDs are `<prefix>-###`. Architecture cards use `research/architecture/` and `ARCH-###`.

## Core Rules

- Decide placement by "who owns this". If only the player uses it, Player; if the whole world uses it, World; if the whole game uses it, Core.
- If you are unsure where to put it, do not put it in Core. The moment Core becomes the junk drawer, the structure collapses. When unsure, ask a human.
- Changes to the structure itself (such as adding a new top-level folder) require human approval. [source: reference/unity_project_baseline.md]
- File name = the name of the main class inside it. C# scripts use Pascal case (PlayerController.cs), and interfaces take the prefix I (IInteractable).
- Scene names must reveal their role. Chunks carry coordinates in the name as `Chunk_x_y` — the ARCH-003 loader finds scenes by name, so arbitrary changes are forbidden.
- For research card IDs, `_index.md` is the single issuing authority. Do not invent new IDs on your own.
- No temporary names: do not commit names containing Test, New, Temp, Untitled, or Copy.

## Unity Implementation Steps

1. Before creating a new file, decide the owner (by the criteria above). Once the owner is decided, the folder is decided.
2. First check whether a file with the same role already exists in an existing folder. If so, put it next to that one.
3. Match the file name to the class name. In Unity, if a MonoBehaviour's file name differs from its class name, it will not attach as a component.
4. Write the file paths exactly in the plan report. The Developer AI does not create files that are not in the plan. [source: reference/unity_project_baseline.md work order]
5. Separate data from code — values such as numbers, dialogue, and routes go to `Data/`, and code holds only rules.
6. If a folder seems necessary, get human approval before creating it.

## Anti-patterns

- Core bloat: the habit of putting everything hard to judge into Core. Eventually Core becomes half the project and you can no longer tell what is genuinely shared.
- Mixing feature folders and layer folders: dividing some things by feature (Player) and others by kind (Managers, Utils). When two criteria mix, the same file looks at home in both places and a different decision is made each time.
- Utils / Common / Misc folders: folders whose names give no information. Files that go in there never come back out.
- File name and class name mismatch: in Unity this is the cause of components silently failing to attach, and it is the mistake beginners struggle with the longest.
- Arbitrary scene renaming: breaking the `Chunk_x_y` rule means the loader cannot find it. Sometimes the name is itself data.
- Keeping the convention only in documents without checking it: a convention survives only when there is a way to check that it is followed. Write it in a checkable form.

## Verification

- 0 compile errors, 0 console errors. [source: reference/unity_project_baseline.md self-check criteria]
- Placement check: confirm that every newly committed script is in one of the six folders above. Being at the top level or in a wrong folder is a fail.
- Naming check: confirm that MonoBehaviour scripts have matching file names and class names.
- Forbidden-word check: no file name may contain Test/New/Temp/Untitled/Copy (formal tests inside a test folder are an exception).
- Scene name check: confirm that Chunk scene names follow the coordinate rule and are registered in Build Settings.
- Plan consistency check: confirm that the devreport's list of changed files matches the plan's file list. [source: reference/unity_project_baseline.md report format]

## Synergy

- ARCH-002 (Scene Streaming): the home of the scene naming rule. The two cards are joined in that the name is the loader's input.
- ARCH-010 (Logging Convention): a convention card of the same nature. What they share is that a convention is not "knowledge" but "agreement", so changing it requires human approval.
- ARCH-001 (Event Bus): the rule of keeping event type definitions only in Core comes from the same basis as this card's placement principle.
- ARCH-022 (Assembly Definition Module Boundaries): this convention's folder dividing lines become the module boundaries as they are. The folders must be decided first so that where to cut assemblies is not a debate.
- ELEM-013 (Pixel Art Style): compatibility note — a pixel art pipeline grows sprite and tilemap assets quickly, so it is better to set the conventions under `Tilemaps/` and `Prefabs/` as early as the code folders.
