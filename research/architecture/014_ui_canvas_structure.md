+++ 
card_id = "ARCH-014"
type = "structure"
title = "UI Canvas Structure (World_Base Static/Dynamic Separation)"
summary = "Instead of leaving the screen UI in one lump, it is divided into 'things that rarely change' and 'things that change frequently', so that the entire screen is not redrawn when one bar of health bar changes."
tags = ["ui", "canvas", "performance", "world-base", "unity", "structure"]
updated = "2026-07-30"
confidence = "high" # reference/unity_project_baseline.md 기준 구조의 World_Base UI 명시 + Unity 공식 UI 최적화 지침(정적/동적 캔버스 분리, 리빌드 비용) 근거 + 안티패턴(단일 거대 캔버스) 실사례
+++ 
## Problem

The UI is clearly visible, but its costs are quietly hidden. Even if just one drawn element in the canvas changes, the entire canvas is redrawn (rebuild), and at this time, CPU usage suddenly jumps. If an element that changes every frame, such as a health bar, is on a canvas such as a menu or minimap, even the elements that have not changed are continuously recalculated. To put it simply: If you want to replace just one piece of paper on the bulletin board, you are essentially removing the entire bulletin board and rebuilding it. So, papers that change frequently are posted separately on a small bulletin board.

## Structure

- The UI root is in the World_Base scene and is always on. No UI is included in the chunk scene. [source: reference/unity_project_baseline.md Baseline Structure — World_Base.unity "Player, Camera, UI (Always On)"]
- Divide the canvas according to its properties — ① Static canvas: Things that rarely change (menu frame, background panel, fixed icons) ② Dynamic canvas: Things that change frequently (health/resource gauges, interaction guide text, commentator reaction display). Elements that change together at the same time are gathered on the same dynamic canvas. [source: Unity Official UI Optimization Guidelines — Separate static and dynamic elements into separate canvases]
- The reason for the division is to cut off the spread of rebuild. Canvases are re-grouped when any of the drawn elements they belong to change. So it is usually better to split a non-trivial canvas into at least two pieces. [source: Unity Official UI Optimization Guidelines — Canvas Rebuild and Split Recommendation]
- However, it should not be split infinitely. Every time you divide the canvas, a separate drawing call is made, which actually increases the number. It's a matter of finding a balance between rebuild costs and draw calls. [source: Unity Official UI Optimization Guidelines — Canvas Splitting Increases Draw Calls Tradeoff]
- The UI listens to the broadcast without requesting data. Changes in physical strength, acquisition of items, and starting conversations are updated by subscribing to EventBus broadcasts. The UI does not directly reference players or managers. [source: reference/unity_project_baseline.md broadcast rules]
- Displays floating above the world (interaction guides, NPC speech bubbles) are also placed in the World_Base UI, not in chunks. Only the location of the target is followed and the UI itself is not turned off along with the chunk.

## Core Rules

- UI objects are placed only in the World_Base scene. If you put UI in a chunk scene, part of the screen disappears when the chunk is turned off. [source: reference/unity_project_baseline.md chunk rule]
- Do not place elements that change every frame and elements that rarely change on the same canvas. [interpretation] This one rule prevents most UI performance issues at this scale.
- Canvas division is done only based on properties. Avoid over-splitting, such as creating one canvas for each element — this increases draw calls and the benefit is lost. [source: Unity Official UI Optimization Guidelines — Tradeoffs between Splitting and Draw Calls]
- The UI is updated only through EventBus subscription. It does not use a method of looking into the gameplay system every frame (polling). [source: reference/unity_project_baseline.md broadcast rules]
- When displaying a commentator's reaction on the screen, the UI does not directly refer to the commentator but subscribes to the broadcast made by the commentator. Log recording is the responsibility of the commentator and display is the responsibility of the UI (ARCH-007).
- Interaction guidance text is owned by the UI, not the object of interaction. The subject only announces that "interaction has become possible" and does not create the text itself (ARCH-006).
- Display elements that do not receive clicks are excluded from light detection. If a large image covering the screen remains as a detection target, the input decision will scan through it each time.

## Unity Implementation Steps

1. Create a UI root object in the World_Base scene and place canvases underneath it. Don't spread them out in one scene.
2. Create a static canvas. Contains elements whose values ​​do not change while open, such as menu frames and background panels.
3. Create dynamic canvases by property. Example: one gauge, one interaction/dialogue guide. Gather together things that change together at the same moment.
4. Unify the screen response method (scale-based resolution) of each canvas into one. If each canvas is different, the UI will be misaligned when the resolution changes.
5. Create a UI update script and subscribe to EventBus. Be sure to include unsubscription when the object is turned off — if you omit it, subscriptions will pile up and the same update will be executed multiple times (ARCH-001).
6. Text that changes frequently is updated only when the value actually changes. Re-entering the same value can be treated as a change on the canvas.
7. Turns off ray detection for display-only elements. Layout auto-placement is not used for elements that change frequently.
8. If it is a pixel art project, the UI scale standard is set along with the camera pixel settings (ARCH-013).
9. Self-check — Check 0 compilation errors and 0 console errors and commit. [source: reference/unity_project_baseline.md self-check standard]

## Anti-patterns

- Containing all UI in one canvas: When the gauge changes every frame, even the menu and minimap are continuously re-packaged. This is a typical cause of UI items popping up unexpectedly in the profiler. [source: Unity Official UI Optimization Guidelines — Elements that change every frame cause the entire canvas to be rebuilt]
- Conversely, having one canvas for each element: Rebuilds are reduced, but draw calls are increased, raising the total cost again. Division is based on nature. [source: Unity Official UI Optimization Guidelines — Tradeoff that splitting increases draw calls]
- The UI directly references the player/manager: This is a violation of broadcasting rules, and the update stops quietly when the reference is lost due to chunk loading or the manager is replaced. [source: reference/unity_project_baseline.md broadcast rules]
- Re-assigning the value every frame: If the value has not changed but is updated, unnecessary rebuilding is done.
- Inserting UI into the Chunk scene: When the player moves and the chunk is turned off, the UI disappears. It is difficult to find the cause because the reproduction condition is “only in certain locations.”
- Only subscribe and do not cancel: If you repeatedly turn UI objects on and off, subscriptions accumulate and the same response is displayed multiple times.
- Leaving an image that covers the entire screen as a target for ray detection: the input judgment has to pass through it every time, making it less responsive.
- Using auto-layout batches for frequently updated lists: recalculating batches overlaps with rebuilds, which doubles the cost.

## Verification

- 0 compilation errors, 0 console errors. [source: reference/unity_project_baseline.md self-check standard]
- Scene affiliation check: All canvases must belong to the World_Base scene. There must be no canvas in the Chunk scene.
- Separation check: Elements updated every frame and static elements must not be together on the same canvas (can be checked in hierarchical structure).
- Reference check: There should be no direct references to the player/manager in the UI script. The renewal path must be an EventBus subscription only (can be checked by searching).
- Subscription cumulative check: When a UI object is turned on and off multiple times and an event is generated, update occurs only once and there should be no duplicate lines in `Logs/commentator.log`. [source: reference/unity_project_baseline.md log rule]
- Rebuild check: When looking at UI rebuild items in the profiler, the static canvas should not be rebuilt on a frame where nothing has changed.
- Resolution check: When changing the window size, there should be no discrepancy in position or size between canvases.
- Instruction text ownership check: The interaction target script must not directly hold the UI element (ARCH-006 boundary check).

## Synergy

- ARCH-006 (Interaction): Direct engagement — The target only reports that “it has become possible” and the UI displays the text. When this boundary is blurred, UI references are embedded in each prefab.
- ARCH-001 (Event Bus): Unique update path. Subscription cancellation rules also follow the card's rules.
- ARCH-007 (Commentator Pipeline): Responsible for displaying responses. Divide the responsibilities of log recording (commentator) and screen display (UI).
- ARCH-002 (Scene Streaming): Placement rationale that the UI belongs to an always-on World_Base.
- ARCH-013 (2D camera tracking): In pixel art, the UI scale and camera pixel settings must be determined together.
- ELEM-015 (Stress/Insanity System): Directly related to compatibility — A gauge that shows numbers in real time is a representative dynamic canvas element. If you place this gauge on a static canvas, performance issues will immediately appear.
- ELEM-003 (4's Wall Collapse): Good compatibility — The UI is a surface on the player's side, not the game world, so it becomes a natural stage for production that speaks directly to the player off-screen.
- ELEM-012 (Landmark-Based Exploration): Compatibility Note — Choosing this element comes with the decision not to place arrow/icon markers in the UI. When you add a marker, the effect of the element disappears.

