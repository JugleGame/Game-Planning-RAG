+++
card_id = "ARCH-016"
type = "structure"
title = "Input System (Input System package + InputActionAsset)"
summary = "Input processing structure that bundles inputs from multiple devices in advance into one action name such as 'movement' or 'interaction' rather than writing buttons for different devices such as keyboard or gamepad scattered throughout the code."
tags = ["input", "inputsystem", "inputaction", "player", "unity", "2d"]
updated = "2026-07-31"
confidence = "high"
+++
## Problem
By inserting the device and key directly into the code like `Input.GetKeyDown("space")`, the gamepad
Every time you add support or add a key reassignment function, you have to go through and modify multiple scripts.
Without separation of action (“jump”) and device-specific buttons (“spacebar” or “pad south button”)
It's my fault.

## Structure
- Unity’s Input System package provides “Action” to one `InputActionAsset` asset.
Define and map multiple device bindings (keyboard arrow keys, pad sticks, etc.) to each action.
  [source: Unity Input System Manual, Input Action Assets,
  https://docs.unity3d.com/Packages/com.unity.inputsystem@1.0/manual/ActionAssets.html].
- If you attach the `PlayerInput` component to the player object and connect this Action Asset,
When an action occurs, the specified method is called. [source: Unity Input System Manual,
  The Player Input component,
  https://docs.unity3d.com/Packages/com.unity.inputsystem@1.8/manual/PlayerInput.html].
- Input that requires combining the four directions up, down, left, and right into one vector, such as 2D movement, is "2D Vector
Composite” [source: Unity Input System Manual, Quick start guide,
  https://docs.unity3d.com/Packages/com.unity.inputsystem@1.0/manual/QuickStartGuide.html].
- This project has a processing script `PlayerInput` in `Scripts/Player/`,
`PlayerController` (moving ARCH-009 Rigidbody2D) does not poll the input directly.
It only accepts the values ​​passed by this script.

## Core Rules
- The action name (Move, Interact, etc.) does not refer to the device — "press spacebar"
Instead, the code must respond “when an interaction action occurs” to add or reassign devices.
This is possible without change.
- Separate input reading and game logic: the input script only creates and passes values,
The actual processing of movement and interaction is done in each script (PlayerController, IInteractable
Target) is in charge — ARCH-001 This is the same reason as the broadcasting rules for the event bus.
- Global inputs across scenes (pause, etc.) and player-specific inputs (movement, attack) are mutually exclusive.
Divide into different Action Maps. If you put them all in one Map, movement input is possible even when the UI is floating.
The problem of reacting together arises.

## Unity Implementation Steps
1. First check if `Packages/manifest.json` has the Input System package — if not,
Since this is a package addition, please add it to the suppression list in reference/unity_project_baseline.md (package additions require human approval).
Check with the relevant person first.
2. Create `InputActionAsset` and create Action Map (e.g. Player) and actions (Move, Interact, etc.)
Define. Move binds WASD/direction keys/pad stick together with 2D Vector Composite.
3. Attach the `PlayerInput` component to the player prefab and connect this Asset.
4. Choose a Behavior that matches the event broadcasting rules for this project — see direct reference.
Rather than increasing Unity Events, priority is given to passing only values ​​through C# events or callbacks.
5. `PlayerController`, interaction triggers, etc. Consumers only use the values ​​passed by the input script.
and does not call the `Input System` API directly.

## Anti-patterns
- Multiple scripts each polling the device directly with `Keyboard.current` etc. —
Bindings are scattered back into the code, reoccurring the problem this card was intended to solve.
- Instead of dividing the Action Map, UI input and player input are lumped into one Map, creating a menu.
Bug where the character moves even when open.
- Mixing the old `Input` Manager (Input Manager) and the new Input System in one project
The same keystroke is processed twice.

## Verification
- Play the same game by performing movement and interaction actions 1 times with each keyboard and gamepad.
Ensure responsiveness — device-independent operation is a key acceptance criterion for this architecture.
- Player movement input is not transmitted to the scene while the menu/pause UI is open.
Confirmed with Action Map conversion log.
- 0 console errors, especially 0 missing binding warnings of the "No Action Map" type.

## Synergy
- ARCH-009 (2D physical movement, Rigidbody2D): Physical movement using the vector value of the Move action as is.
The most direct consumer passed as input.
- ARCH-006 (Interact, IInteractable): Interact within the trigger range when the action is pressed.
An connection point that calls an IInteractable target.

