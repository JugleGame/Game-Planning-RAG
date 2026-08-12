+++
card_id = "ARCH-023"
type = "structure"
title = "Game Flow Structure (Boot → Title → Play → Result Scene Transitions)"
summary = "The whole-game skeleton in which no arbitrary script calls scenes, and a single flow owner performs only the permitted transitions asynchronously"
tags = ["scene-flow", "game-loop", "loadsceneasync", "structure", "unity", "core"]
updated = "2026-08-02"
confidence = "medium"
+++
## Problem
A game moves from the start screen to play, and from play to the result screen. If any script
does this moving directly, the game's skeleton — "where can you go from where right now" —
scatters across the code and nobody can see the whole. It is like a building with several
staircases secretly cut into it. This structure gathers the staircases into one place and makes
all traffic use only them.

## Structure
- There is one flow owner. Every request to change scenes passes through this one place, and
  other scripts merely say "take me to the next step" without knowing which scene that is.
- Default path: Boot (create managers) → Title → Play (World_Base + Chunk) → Result → Title.
  During the play segment, the always-loaded scene World_Base is kept while only Chunk pieces are turned on and off [source: reference/unity_project_baseline.md section 3 baseline structure].
- Flow and state are different things. Whether we are now running, paused, or finished is held
  by GameManager (ARCH-018), and which scene to move to when that state changes is decided by
  this structure.
- Managers are created only once in Boot and are not created again on later transitions (ARCH-011).
- [interpretation] So the transition table is not a "list of scene names" but a "list of permitted
  moves". A move not on the list is blocked by the table, not by code.

## Core Rules
- Do not call the scene loading API directly outside the flow owner. If it is not gathered in
  one place, the transition table stops being the truth.
- Do transitions asynchronously. Synchronous loading freezes the screen until loading finishes.
- Do not accept input while loading. If two transition requests overlap, which scene survives is
  unpredictable.
- When you must load ahead and show later, turn scene activation off. In that case progress waits, stopped at 0.9, and completes only once activation is turned back on [source: Unity Scripting API AsyncOperation.allowSceneActivation, verified 2026-08].
- The always-loaded scene (World_Base) is not an unload target. Unloading it makes the player,
  camera, and UI disappear along with it.
- The result screen does not recalculate the score. It receives an already-finalized state and
  only displays it.

## Unity Implementation Steps
1. Register the scenes in the build target list. A scene that is not registered opens only in the editor.
2. Write the permitted transitions as a table in one place. This is the substance of this
   structure; the rest is code that executes that table.
3. Expose only one window for transition requests. Other systems know only this window and not scene names.
4. Kick off asynchronous loading and update the loading screen with the progress value. If there
   is no need to show it immediately, keep it waiting with activation turned off.
5. Unload the previous scene after the new scene is ready. Additively loaded scenes do not clean themselves up, so if you skip the unload they stay in memory [source: Unity Scripting API SceneManager.UnloadSceneAsync, verified 2026-08].
6. When a transition finishes, broadcast completion (ARCH-001). Each system hears this broadcast
   and initializes itself — if the flow owner starts calling individual systems one by one, it
   becomes a spiderweb again.
7. Leave one log line per transition (ARCH-010). Transitions are events that are hard to confirm
   by eye alone.

## Anti-patterns
- Calling scene loading from any script: the flow table and the actual behavior diverge, and
  nobody notices even when a path back appears.
- Synchronous loading: the screen halts during loading, so to the user the game looks frozen.
- Skipping Boot and running the play scene directly: it starts without managers and reference errors erupt everywhere. This is the most common trap that reproduces only in the editor [source: mortoray.com 'Loading a bootstrap scene while testing in the Unity editor', verified 2026-08].
- Recalculating state on the result screen: the premise that GameManager is the sole owner of
  state breaks, and the numbers in the two places start to disagree.
- Recreating managers on every transition: the more you move between scenes, the more copies of
  the same manager pile up.

## Verification
- Round-trip check: after going once around Title → Play → Result → Title, there must be exactly
  one manager object of each kind.
- Log check: there must be one line per transition in the format `[timestamp] [eventId] [reaction summary]` [source: reference/unity_project_baseline.md section 3 logging rules].
- Console check: 0 console errors over one round trip [source: reference/unity_project_baseline.md section 4 self-check].
- Always-loaded scene check: World_Base must stay loaded throughout the play segment.
- Duplicate request check: even if the transition button is mashed during loading, the final
  active scene must be one.

## Synergy
- ARCH-011 (Boot bootstrap & manager lifetime): the starting point of this structure. Without
  bootstrapping, the very subject that does the transitioning is created anew every time.
- ARCH-018 (Game manager): the owner of state. This card takes charge of the path by which those
  state changes lead to screen transitions.
- ARCH-002 (Scene streaming): the scene composition inside the play segment. Flow is between
  segments, streaming is within a segment.
- ARCH-010 (Logging convention): the basis for the format of transition records.
- ARCH-001 (Event Bus): the notification path for transition completion.
- ELEM-004 (Repeatable mechanics): synergy essential — in a game where repetition is the core,
  result → re-entering play is the most frequently traveled road, so transition cost and manager
  lifetime handling become that game's felt rhythm.
