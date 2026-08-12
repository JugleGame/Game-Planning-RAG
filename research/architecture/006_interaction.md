+++ 
card_id = "ARCH-006"
type = "pattern"
title = "Interaction (IInteractable Interface + Trigger)"
summary = "A structure that bundles different behaviors such as talking, picking up, and opening into a single promise of 'can be interacted with', so the player can handle a target without knowing its identity"
tags = ["interaction", "interface", "trigger", "player", "unity", "2d"]
updated = "2026-07-29"
confidence = "high" # 프로젝트 기준 구조(reference/unity_project_baseline.md)의 IInteractable + Trigger 명시
+++ 
## Problem

For the player to talk to an NPC, pick up an item, and open a door, it looks like each needs different code. But building it that way makes the player code check "is this an NPC? an item? a door?" one by one, and the player code has to be modified every time a new kind appears. Put simply: even if door handles come in all shapes, we only need to know the promise "turn it and it opens". IInteractable is that handle promise.

## Structure

- Location: `Assets/Scripts/Interaction/` — the IInteractable interface, Trigger-based. [source: reference/unity_project_baseline.md baseline structure]
- The promise (interface): the minimum specification every interactable target keeps. It exposes only one interaction-execution function and about the guidance text to show on screen (e.g. "Talk").
- Detection: put a 2D collider set as a Trigger on the target; when the player enters range register it as a candidate, and unregister when leaving.
- Execution: when the player presses the interaction key → pick one of the current candidates → call the promised execution function. The player does not know whether the target is an NPC or a chest.
- Result broadcast: execution results (conversation, acquisition, etc.) are broadcast on the ARCH-001 event bus.

## Core Rules

- The player code does not know concrete types. The moment it branches on a type check, this structure's reason for existing disappears.
- Interaction result events (conversation, acquisition) must be broadcast. [source: reference/unity_project_baseline.md broadcast rules]
- Interaction targets belong to chunk scenes. The candidate list must be cleaned up whenever a target is destroyed or a chunk is turned off. Without cleanup, calling a vanished target blows up.
- Fix a single selection rule for when there are multiple candidates (e.g. the nearest one). Without a rule the target changes every frame and confuses the player.
- Keep the interaction-execution function short. Delegate the actual content (running the conversation, adding to inventory) to each system.

## Unity Implementation Steps

1. Create `Scripts/Interaction/IInteractable.cs` — the minimum promise holding only the execution function and the guidance text.
2. Create `Scripts/Interaction/InteractionDetector.cs` — the detector attached to the player. Register and unregister candidates in the Trigger enter/exit callbacks.
3. Implement the candidate selection rule — pick the nearest candidate and pass that target's guidance text to the UI.
4. Connect input — receive the interaction key from PlayerInput and call the selected candidate's execution function.
5. Implement targets — NPC (conversation, requesting the Talk transition of ARCH-005), item (acquisition), and door (opening) each implement the promise.
6. Connect broadcasting — on successful execution, announce the event on the event bus.
7. Handle cleanup — create a path where a target removes itself from the candidate list when it is deactivated or destroyed.

## Anti-patterns

- Type branching: the player code checking the kind of target and splitting on it. The player must be modified every time a kind is added, and it ends up a function nobody can fix.
- Discriminating by name or tag: distinguishing targets by object name or tag string. A single typo fails silently and the compiler cannot catch it.
- Cramming all logic into the interaction function: putting conversation UI manipulation, inventory handling, and even sound inside the execution function. The interface stays maintainable only if it is thin.
- Missing candidate cleanup: the problem of a destroyed target remaining a candidate. It happens especially often in this project, where chunks are turned off frequently.
- Oversized Trigger range: a state where the detection range is set wide and several targets are caught at once. The player can no longer predict what they will interact with.

## Verification

- 0 compile errors, 0 console errors. [source: reference/unity_project_baseline.md self-check criteria]
- Polymorphism check: interacting with each of the three kinds — NPC, item, door — must work without modifying the player code.
- Broadcast check: after a conversation or acquisition interaction, the corresponding event line must remain in `Logs/commentator.log`. [source: reference/unity_project_baseline.md logging rules]
- Cleanup check: after destroying a target within interaction range or unloading the chunk, pressing the interaction key must produce no errors.
- Selection rule check: when standing between two targets, selection must always follow the same rule (the nearer one).
- UI check: the guidance text must appear on entering range and disappear on leaving.

## Synergy

- ARCH-005 (NPC State Machine): the relationship where a conversation interaction requests the Talk state transition.
- ARCH-001 (Event Bus): the broadcast path for interaction results.
- ARCH-002 (Scene Streaming): since targets belong to chunks, the candidate cleanup rule comes from here.
- ARCH-028 (Hit / Damage Interface): a paired card and a boundary line. Contact the player deliberately handles belongs to this card; damage delivered regardless of intent is handled by that card. Do not merge the two promises into one.
- ELEM-011 (Emergent System Interaction): compatibility caution — if you go with a design where objects react to each other, this structure of "the player presses" alone is not enough, and a separate object-to-object interaction channel is needed.
- ELEM-012 (Landmark-Based Exploration): good compatibility — to make exploration work without markers, this structure of "guidance appears when you get close" serves as the reward for discovery.
