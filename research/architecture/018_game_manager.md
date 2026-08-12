+++
card_id = "ARCH-018"
type = "structure"
title = "Game Manager (Global Game State: Playing / Paused / GameOver)"
summary = "A structure where the question of whether the game is currently running, halted, or over is not judged by many scripts on their own, but held in exactly one place (GameManager) that answers when asked"
tags = ["gamemanager", "singleton", "game-state", "core", "unity", "2d"]
updated = "2026-07-31"
confidence = "medium"
+++
## Problem
Once several scripts start answering questions like "are we paused right now?" or "is the game
over?" with their own `Time.timeScale` or their own variables, state inconsistencies arise
where one side thinks things are stopped while another keeps moving. The baseline structure of
`reference/unity_project_baseline.md` explicitly lists GameManager in `Core/` alongside
EventBus and SaveSystem [source: reference/unity_project_baseline.md, section 3 folder map],
but this project so far has only EventBus (ARCH-001) and SaveSystem (ARCH-004) cards, with no
card covering GameManager itself.

## Structure
- A single global singleton placed in `Core/` holds the one and only value "current game
  state". The state list starts with at minimum the three of Playing / Paused / GameOver
  [source: Unity GameManager pattern overview article, uhiyama-lab.com, verified 2026-07].
- Other systems do not change this state directly; they request GameManager to "change it", or
  subscribe to state-change events through the ARCH-001 event bus.
- Per the ARCH-011 Boot bootstrap rule it is created exactly once in the Boot scene and
  survives scene transitions with `DontDestroyOnLoad`.

## Core Rules
- Narrow the entry point for changing state down to GameManager's public methods (e.g.
  `Pause()`, `Resume()`, `EndGame()`) — if many scripts each touch `Time.timeScale = 0`
  directly, you cannot trace "who stopped it and who released it again".
- The moment the state changes, broadcast it on the ARCH-001 event bus. Systems that must react
  to state, such as UI, input (ARCH-016), and audio (ARCH-017), do not reference GameManager
  directly but subscribe only to this broadcast — the broadcast rule applies equally to game
  state changes, not just player actions.
- GameManager is responsible only for "what the state is right now". Do not pile concrete game
  rule logic such as score calculation or win/lose determination into it — if it bloats, you
  return to the problem of many scripts each imitating the state again.

## Unity Implementation Steps
1. Create `Scripts/Core/GameManager.cs` and define the state as an enum (Playing, Paused,
   GameOver, etc., only as many as the spec requires).
2. Create the instance in the Boot scene and apply `DontDestroyOnLoad` per the ARCH-011 rule.
   If an instance already exists, block duplicate creation (singleton guard).
3. Change the state value only inside the state-change methods, and immediately after it
   changes broadcast a `GameStateChanged`-style event on the event bus.
4. Keep pause handling (`Time.timeScale`) only inside GameManager, and make the UI's "pause
   button" reach it only by calling GameManager's `Pause()`.
5. If a flow that crosses scenes is needed (Boot → World_Base → GameOver screen, etc.), align
   with the ARCH-002 scene streaming rules and decide in the spec first which scene transitions
   GameManager will trigger.

## Anti-patterns
- Several scripts each holding a local flag such as `bool isPaused` — if even one misses an
  update, the whole game looks as if it only half stopped.
- Piling UI updates, sound playback, and score calculation all into GameManager, turning it
  into one giant "do-everything manager" — responsibility concentrates in one class, so every
  edit requires reading the whole thing again.
- Switching to any state instantly with no state transition rules (accepting a Pause request
  as-is during GameOver, etc.) — depending on the state combination, other systems end up
  observing wrong values.

## Verification
- Check via logs (the ARCH-010 logging convention) that a broadcast goes out on the event bus
  every time a state-change method is called — there should be one log line per state
  transition.
- Observe whether gameplay input such as player movement and combat actually stops while in the
  paused state (whether Time.timeScale is reflected).
- Check that even after a scene transition the GameManager instance is not duplicated and only
  one exists (whether the singleton guard works).
- 0 console errors.

## Synergy
- ARCH-001 (Event Bus): the only channel for delivering state changes to other systems.
- ARCH-011 (Boot Bootstrap & Manager Lifetime): GameManager itself is the representative case
  of following this rule.
- ELEM-005 (AI Integration): when the AI commentator's reaction must be gated by game state
  (GameOver, etc.), GameManager's state broadcast becomes the basis for that judgment.
