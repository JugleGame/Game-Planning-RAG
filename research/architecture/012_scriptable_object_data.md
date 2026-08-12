+++ 
card_id = "ARCH-012"
type = "convention"
title = "Data/ Data Asset Convention (ScriptableObject Tables)"
summary = "A rule that keeps configuration values such as item stats or probability tables out of the code and in separate project data files, so numbers can be changed without touching the code"
tags = ["data", "scriptableobject", "convention", "balance", "unity", "authoring"]
updated = "2026-07-30"
confidence = "high" # reference/unity_project_baseline.md 기준 구조의 Data/ 폴더 명시 + Unity 공식 매뉴얼(ScriptableObject) 근거 + 안티패턴(런타임 변경이 에디터에만 남는 문제) 실사례
+++ 
## Problem

If you scatter numbers inside code or prefabs, every single balance adjustment requires editing and recompiling code, and accidents happen where the same item has different values in different scenes. Worse is that nobody knows where the values are. Put simply: if the amounts of cooking ingredients live only in the cook's head, the taste changes whenever the cook changes. Keep a recipe card separately and anyone can make the same dish, and to change an amount you fix just that one card. The data asset is that recipe card.

## Structure

- Location: `Assets/Data/` — the data-only folder of the baseline project structure. [source: reference/unity_project_baseline.md baseline structure — Prefabs/ , Tilemaps/ , Data/]
- Split subfolders by kind (e.g. items, NPC dialogue, drop probability tables). Folder and file names follow the naming convention (ARCH-008).
- Make the data as ScriptableObject assets. Instead of each class instance holding its own copy of the values, a ScriptableObject is a data container where many places jointly reference a single asset stored in the project. [source: Unity official manual — ScriptableObject]
- Assets do not belong to a scene. That is why World_Base and any Chunk scene can reference the same data asset. This is the only safe way to share data in the chunk streaming (ARCH-002, ARCH-003) structure.
- Data and state have different owners — configuration values (things that do not change) are held by assets in Data/, and state that changes during play (current health, belongings, progress) is held by the save system as JSON. [source: reference/unity_project_baseline.md baseline structure — Core/SaveSystem (JSON)]
- Data assets have a string ID. Save JSON cannot point at an asset directly, so it recovers it by this ID (ARCH-004).

## Core Rules

- Assets in Data/ hold only read-only configuration values. Do not write values that change during play here. Changes persist in the editor but not in a build, making it a bug that reproduces only on the developer's machine. [source: Unity official manual — ScriptableObject, and the point that a built player cannot modify asset files]
- Do not put scene object references inside a data asset. A project asset cannot save a pointer to an object inside a scene, and once the chunk is turned off that target does not even exist.
- Do not keep the same number in two places. The data asset is the single original, and prefabs and code reference it. If a number lives in two places, it will surely diverge someday.
- Data assets reference each other by ID. It is the same reason cards are linked only by ID — copied values do not get updated.
- Tables such as probabilities, drops, and rewards are not written as conditionals in code but made as table-shaped assets. The person in charge of balance must be able to adjust them without touching code.
- If a system needs to be told that data changed, broadcast it on the EventBus. A data asset does not call a system directly. [source: reference/unity_project_baseline.md broadcast rules]

## Unity Implementation Steps

1. Create per-kind folders under `Assets/Data/`. Match the names to the naming convention (ARCH-008).
2. For each data kind, put the ScriptableObject definition in the corresponding system folder inside `Scripts/` (e.g. the NPC dialogue data definition in `Scripts/NPC/`). The definition is code, the asset is in Data/.
3. Attach an editor creation menu item so people can create assets. Do not create asset files outside Data/.
4. Put a string ID field in each data asset. Match the ID to the file name so people can cross-check by eye.
5. Create one lookup list asset per kind that finds assets by ID. Do not use an approach where code scans folders — behavior differs in a build.
6. Save integration — store only IDs and changed state in JSON, and recover the assets by ID on load (ARCH-004).
7. Self-check — confirm 0 compile errors and 0 console errors, then commit. [source: reference/unity_project_baseline.md self-check criteria]

## Anti-patterns

- Using data assets as save storage: [interpretation] this is the most expensive mistake when this convention is broken. In the editor the values persist and you mistakenly think "saving works", but a built game cannot modify its own asset files, so all of the player's progress disappears. [source: Unity official manual — ScriptableObject]
- Adjusting values during play in the editor and leaving them: that change persists in the asset and the starting value of the next play quietly changes. Balance test results become contaminated.
- Linking prefab instances or scene objects into a data asset: it either does not get saved or becomes a severed reference after chunk unload.
- Keeping a number in duplicate in a code constant and a data asset: it ships with only one side fixed, and it takes time to determine which is the real one.
- Cramming every kind into one giant data asset: when several people edit at once, merge conflicts concentrate on a single file.
- Scanning folders at runtime to gather assets: it works in the editor but produces different results in a build. Do lookups with an explicit list asset.

## Verification

- 0 compile errors, 0 console errors. [source: reference/unity_project_baseline.md self-check criteria]
- Location check: there must be no data asset file outside `Assets/Data/` (verifiable by file search).
- Build persistence check: after playing in a build in a way that changes values and then restarting, the starting values must be the same as the original configuration values (if they differ, it means state is being written into data assets).
- State ownership check: progress state must be in the save JSON, and the contents of the data asset files must be identical before and after play (verified by whether the files changed).
- ID integrity check: every ID in the save JSON must resolve in the lookup list. Resolution failures are left as console errors.
- Duplicate ID check: within the same kind, there must not be two or more assets with an identical ID.

## Synergy

- ARCH-004 (Save System): the division of roles is the crux — configuration values in data assets, changing state in JSON. Blur this line and saving breaks.
- ARCH-008 (Folder and Naming Convention): that card is the basis for the rule of matching file names to IDs.
- ARCH-005 (NPC State Machine): the target for pulling values such as patrol speed and conversation conditions out of the state machine code and into data assets.
- ARCH-001 (Event Bus): the notification path for data changes. A data asset does not call a system directly.
- ELEM-019 (Random Loot Drops & Loot Tables): directly connected compatibility — a loot table is the representative table asset of this convention. Hard-coding probabilities makes adjustment costs explode.
- ELEM-017 (Gacha Rates & Pity System): rates and the pity count must be in data assets for balance adjustment and auditing (numeric verification) to be possible.
- ELEM-018 (Roguelike Random Upgrade/Path Draft): the candidate pool presented each run is managed as a table asset.
