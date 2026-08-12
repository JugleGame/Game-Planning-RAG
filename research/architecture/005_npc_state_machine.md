+++ 
card_id = "ARCH-005"
type = "pattern"
title = "NPC State Machine (Idle / Patrol / Talk)"
summary = "A structure that splits NPC behavior into multiple 'states' with only one active at a time, building behavior by switching between states according to conditions"
tags = ["npc", "fsm", "state-machine", "ai-behavior", "unity", "2d"]
updated = "2026-07-29"
confidence = "high" # 프로젝트 기준 구조(reference/unity_project_baseline.md)의 상태머신 명시 + 널리 검증된 표준 패턴
+++ 
## Problem

If you build NPC behavior with if statements, the branches tangle every time a condition is added until nobody can touch the code. Even a simple rule like "stand still, talk when the player comes near, otherwise patrol" becomes impossible to trace — what runs in which situation — after only a few extensions. Put simply: a traffic light turns on exactly one of red, yellow, or green. That is why anyone can tell what state it is in. Build the NPC the same way.

## Structure

- Location: `Assets/Scripts/NPC/` — the state machine (Idle / Patrol / Talk). [source: reference/unity_project_baseline.md baseline structure]
- Three components: (1) the states (each state knows its own behavior), (2) the context that holds exactly one current state (the NPC itself), (3) the transition rules (when to move to which state).
- Three points per state: on entering (Enter), while staying (Update), on leaving (Exit). Forgetting cleanup on exit is the usual cause of bugs.
- Three base states — Idle (waiting in place), Patrol (going back and forth along a fixed route), Talk (conversing with the player). Example transitions: Idle → (time elapsed) → Patrol, Patrol/Idle → (interaction occurs) → Talk, Talk → (conversation ends) → Idle.
- Implementation forms include separating a class per state and using an enum + switch. With about three states you may start with the latter, and move to the former as they grow. [interpretation] This project is likely to grow in state count, so separating classes from the start is safer.

## Core Rules

- Only one state is active at a time. There is no "patrolling while idling" state. If you need it, make a new state.
- Gather transition conditions in one place. If states jump to other states as they please, the flow becomes unreadable.
- Entering conversation (Talk) is broadcast. The player's conversation is a behavior subject to the broadcast rules. [source: reference/unity_project_baseline.md broadcast rules]
- NPCs belong to chunk scenes. Since they can be unloaded at any time, the state machine must not directly reference objects outside the scene. [source: reference/unity_project_baseline.md chunk rules]
- Name states only with words that mean a behavior. Names like TempState or State2 are forbidden — the name is the documentation.

## Unity Implementation Steps

1. Create `Scripts/NPC/INpcState.cs` — define only the three promises Enter / Update / Exit.
2. Create IdleState, PatrolState, and TalkState each under `Scripts/NPC/States/`.
3. Create `Scripts/NPC/NpcController.cs` — hold the current state, call the current state's Update every frame, and provide a state-swap function (previous state Exit → new state Enter).
4. Place the transition rules — gather the condition checks in NpcController and call the swap function only when a condition is met.
5. Keep the Patrol route as data — do not hard-code patrol points in code; specify them in the Inspector or put them in `Data/`. Make it so code does not have to change when the design changes.
6. Talk integration — receive a conversation request from ARCH-006 interaction, transition to Talk, and broadcast the conversation event on the event bus.
7. Patrol that needs physics movement follows the rules of ARCH-009 (no direct coordinate assignment).

## Anti-patterns

- Giant if blob: continually appending conditionals inside Update. Avoiding exactly this is the reason to use a state machine.
- Overusing state flags: keeping several booleans such as isIdle, isTalking, isPatrolling. The moment two become true at once, nobody can find the cause. Express state as a single value.
- Missing Exit cleanup: leaving a state without cleaning up coroutines, subscriptions, and animations, so the previous behavior lingers like a ghost in the next state.
- Swapping state directly inside a state: state A's Update switches straight to B, and B returns to A again — a cycle. If transitions repeat within the same frame, the game freezes. Limit transitions to once per frame.
- Putting dialogue text in the state machine: a state is "what it does" and dialogue is data. Putting dialogue in state code requires a code change for every design change.

## Verification

- 0 compile errors, 0 console errors. [source: reference/unity_project_baseline.md self-check criteria]
- Single-state check: at any moment the NPC's current state value must be exactly one.
- Transition check: when the player approaches and starts a conversation it must go to Talk, and return to Idle when it ends. If it does not return, Exit handling is missing.
- Broadcast check: when a conversation starts, a conversation event line must remain in `Logs/commentator.log`. [source: reference/unity_project_baseline.md logging rules]
- Chunk safety check: unloading the chunk the NPC is in must not produce console errors.
- Patrol check: in the Patrol state it must pass the designated route points in order.

## Synergy

- ARCH-006 (Interaction): the entrance into the Talk state. Interaction requests and the state machine performs.
- ARCH-001 (Event Bus): the broadcast path for conversation events.
- ARCH-009 (2D Physics Movement): Patrol's actual movement method follows this card's rules.
- ELEM-005 (AI Integration): compatibility caution — if you go with a design where AI generates dialogue in real time, the Talk state gains a "waiting for response" period. You must design the transition for the case where the player leaves while waiting.
- ELEM-008 (Companion / Playable Companion Character): good compatibility — a companion can reuse the same state machine structure (adding a Follow state).
