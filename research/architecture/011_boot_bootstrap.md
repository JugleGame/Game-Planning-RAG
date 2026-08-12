+++ 
card_id = "ARCH-011"
type = "pattern"
title = "Boot Bootstrap & Manager Lifetime (DontDestroyOnLoad)"
summary = "An approach that creates the managers in exactly one place when the game starts and lets only those managers survive scene changes, so that 'who is alive until when' never becomes confusing"
tags = ["bootstrap", "lifetime", "manager", "scene", "core", "unity"]
updated = "2026-07-31"
confidence = "high" # 프로젝트 기준 구조(reference/unity_project_baseline.md)가 Boot 씬 = 매니저 전용임을 명시 + Unity 공식 매뉴얼(DontDestroyOnLoad, 스크립트 실행 순서) 근거 + 안티패턴(매니저 중복) 실사례
+++ 
## Problem

A game mixes "things that must stay alive to the end" and "things that must disappear when the scene changes". If you do not draw that boundary, one more manager appears every time you reload a scene and the same event is handled twice; or you open only a chunk scene in the editor and play, and there is no manager at all so everything quietly fails to run. Put simply: a school must have exactly one principal. If a new principal appears every time you move classrooms, orders come down twice, and in a classroom with no principal no decision can be made. The Boot scene is "the place where the principal is appointed exactly once".

## Structure

- The Boot scene holds only managers. The player, camera, and UI belong to World_Base, and world objects to Chunk scenes. [source: reference/unity_project_baseline.md baseline structure — Boot.unity "the starting scene (managers only)"]
- Manager code location: `Assets/Scripts/Core/` — GameManager, SaveSystem (JSON), EventBus. [source: reference/unity_project_baseline.md baseline structure]
- The flow is one-directional — run the Boot scene → create and initialize managers → mark them to survive across scene boundaries → load World_Base → the chunk loader turns on surrounding chunks Additively (ARCH-002, ARCH-003).
- Survival across scene boundaries is marked with Unity's DontDestroyOnLoad. A marked object is not destroyed on single scene loading and is moved to a dedicated holding scene. [source: Unity official manual — Object.DontDestroyOnLoad]
- The initialization order is set by the code itself. The order of Awake calls across different objects is not guaranteed, so an order such as "subscribers attach after the EventBus is ready" must be executed explicitly by the bootstrap. [source: Unity official manual — the Script Execution Order guidance]
- The Commentator is an EventBus subscriber. Its subscription point must be in the bootstrap order so that early events are not missed (ARCH-007).

## Core Rules

- Manager instances are created only in the Boot scene. Do not place copies of managers in World_Base or Chunk scenes. Chunks hold only world objects. [source: reference/unity_project_baseline.md chunk rules]
- There must be exactly one manager. If one already exists, the later one removes itself. Doing the opposite (deleting the one that was there first) severs the connections of the subscribers that were holding on to that manager.
- Write the initialization order in the one place, the bootstrap. The order is EventBus (the broadcast network) → SaveSystem (loading) → the remaining managers → scene load. If subscribers come up before the broadcast network exists, subscription fails silently.
- Put the responsibility for turning scenes on and off on the manager side. If individual gameplay scripts each load scenes, nobody will know which chunks are on.
- Single scene loading is used only for big swaps such as the Boot→World_Base transition. Chunks must be Additive. [source: reference/unity_project_baseline.md baseline structure — Chunks are loaded Additively]
- A manager surviving means the values it was holding survive too. Values that must be reset for a new playthrough are reverted explicitly (ARCH-004).

## Unity Implementation Steps

1. Create the `Boot.unity` scene and put it first in the build scene list. This scene holds only the bootstrap object and the managers.
2. Create an entry point in `Scripts/Core/` that acts as the bootstrap. Here, prepare things in the order EventBus → SaveSystem → the remaining managers.
3. Mark the manager objects to survive scene boundaries. Put a duplicate-prevention check at the front of each manager's initialization.
4. Include the commentator's subscription hookup in the bootstrap order. Subscription comes after the EventBus is ready and before the world load (ARCH-007).
5. After preparation is finished, load `World_Base.unity`. Hand chunk loading over to the chunk loader on the World_Base side (ARCH-003).
6. Editor convenience handling — when a developer opens World_Base or a Chunk scene directly and plays, if there is no manager, clearly announce "no bootstrap" in the console. A state that silently does not work is the most expensive.
7. Self-check — confirm 0 compile errors and 0 console errors, then commit. [source: reference/unity_project_baseline.md self-check criteria]

## Anti-patterns

- Placing one manager in each of several scenes: [interpretation] this is the most common accident in this structure. Managers multiply every time a scene is turned on Additively, so the same event is handled several times and commentator reactions are logged in duplicate.
- Attaching the survive-across-scenes marking to just any object: a surviving object stays as-is in the next scene too. Attach it to a world object and it lingers like a ghost after the chunk is turned off, with its collider still working.
- Relying on the Awake call order: the order across different objects is not guaranteed. "It works for me" means it happened to load in that order, and it breaks when the scene composition changes. [source: Unity official manual — the Script Execution Order guidance]
- Solving the initialization order only with the execution order setting: an order hidden in project settings does not show up in cards or specs, so the next person cannot find the cause. Write the order visibly in code.
- Destroying the pre-existing manager instead of the later one: whoever already referenced or subscribed to that manager is left holding a severed reference.
- Slipping a player or a test object into the Boot scene: the moment the rule that Boot is managers-only collapses, nobody knows "what is in which scene" again.

## Verification

- 0 compile errors, 0 console errors. [source: reference/unity_project_baseline.md self-check criteria]
- Uniqueness check: during play, the instance count of each manager kind must be 1 each (verifiable by name in the scene hierarchy).
- Survival check: after reloading World_Base, the managers must still exist and must not be newly created.
- Duplicate broadcast check: when one event is raised, only one line with that event ID must remain in `Logs/commentator.log`. Two lines means the manager or the subscription is duplicated. [source: reference/unity_project_baseline.md logging rules]
- Missing bootstrap detection check: when the World_Base scene is opened alone and played, a "no bootstrap" warning line must remain in the console (running silently is a fail).
- Order check: the order of the initialization log lines must appear as EventBus → SaveSystem → the rest → scene load.

## Synergy

- ARCH-001 (Event Bus): the first thing the bootstrap prepares. Subscribing before the broadcast network is ready fails.
- ARCH-002 (Scene Streaming): direct interlock — the three-tier structure of Boot → World_Base → Chunk is the same line as this card's lifetime boundary.
- ARCH-004 (Save System): at which point the loaded data is put into the managers is part of the bootstrap order.
- ARCH-007 (Commentator Pipeline): the subscription start point must be in the bootstrap so early events are not missed.
- ARCH-010 (Logging Convention): since initialization order verification is done through log lines, it follows the log format convention.
- ELEM-014 (Punishing Death Loop): compatibility core — when you die and start again, "what you lose and what you keep" is exactly the manager lifetime boundary. Put resources that should be lost in a surviving manager and the punishment disappears.
- ARCH-018 (Game Manager): the representative case that follows this rule. It is the archetype of a manager created once in Boot and surviving scene transitions.
- ARCH-023 (Game Flow Structure): scene transitions between title, play, and results happen on top of the managers the bootstrap created. Skipping Boot and running the play scene directly breaks that premise.
- ELEM-004 (Repetition Mechanic): to restart the same situation with only the variables differing, values that reset every time and values that persist across runs must be split at this boundary.
