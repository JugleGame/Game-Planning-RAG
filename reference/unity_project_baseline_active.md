# Unity Project Baseline — Active ARCH Citation Guide

This is the English citation source for new ARCH research cards. It extracts only the
RAG-relevant baseline from `unity_project_baseline.md`, which remains the Korean archival
original. It is not an instruction to implement, plan, commit, or operate Unity.

Use the citation labels in this file exactly, for example:
`[source: reference/unity_project_baseline_active.md baseline structure]`.

## Baseline structure

The baseline project has these assets and ownership boundaries:

```text
Assets/
  Scenes/
    Boot.unity          managers only
    World_Base.unity    player, camera, and UI; always loaded
    Chunk_x_y.unity     world chunks; loaded and unloaded additively
  Scripts/
    Core/               GameManager, SaveSystem (JSON), EventBus
    World/              ChunkLoader; activates the 3×3 chunks around the player
    Player/             PlayerController (Rigidbody2D), PlayerInput
    Interaction/        IInteractable and trigger-based interaction
    NPC/                Idle, Patrol, and Talk state machine
    Commentator/        EventBus subscription, reaction generation, reaction logging
  Prefabs/, Tilemaps/, Data/
```

Changing this baseline structure requires human approval.

## Chunk rules

- Put world objects, including tilemaps and lighting objects, in Chunk scenes.
- Do not put world objects in `World_Base`.
- Keep the player-centred active chunk range at 3×3, including the centre chunk.
- Keep `World_Base` loaded while Chunk scenes are added or removed.

## Broadcast rules

- Broadcast player combat, pickup, dialogue, and area-entry actions through
  `EventBus.Publish(GameEvent)`.
- Systems that consume those actions, including the commentator and UI, depend on the
  broadcast rather than directly reading another system's fields.

## Logging rules

- Each commentator reaction writes one line to `Logs/commentator.log`.
- Each line has this structure: `[time] [event ID] [reaction summary]`.
- A missing expected line is not evidence that an action succeeded.

## Self-check criteria

- The relevant Unity work has 0 compile errors and 0 console errors during normal operation.
- A repeated event must not create duplicate commentator log lines.

## Approval boundaries

- Changing the baseline structure requires human approval.
- Adding or removing packages, or changing `ProjectSettings`, requires human approval.

## Provenance

Derived from the Korean archival source `unity_project_baseline.md`, especially its baseline
structure, rule, and self-check sections. If a claim needs historical wording or a disputed
interpretation, a human reviewer may compare the archive; English-only authoring agents do not
load the archive during normal work.
