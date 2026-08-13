+++
card_id = "ARCH-032"
type = "structure"
title = "Narrative Beat and Flag Ledger"
summary = "A single source of truth for chapters, completed story beats, recovered memories, one-time anomalies, and reveal-dependent interaction rules"
tags = ["narrative", "state", "flags", "chapters", "save", "verification", "unity"]
updated = "2026-08-13"
confidence = "medium"
+++
## Problem
A linear emotional mystery still contains many hidden branches: a clue may already be collected, a nightmare may have played, a companion may know a fact, or the final interaction may not yet be authorized. [interpretation] If each scene and trigger stores its own booleans, save/load, retries, and chapter transitions can replay reveals or skip required bonding beats.

## Structure
- Definition layer: each chapter and beat has a stable ID, prerequisites, completion effect, and whether it can repeat. [interpretation]
- Runtime ledger: the current chapter, current beat, recovered-memory IDs, relationship milestones, and one-time event IDs form the mutable story snapshot. [interpretation]
- ARCH-012 owns stable beat definitions as data assets; ARCH-004 owns the mutable ledger in JSON. The existing cards require configuration and changing state to remain separate. [source: ARCH-012 card, Synergy section, as of 2026-08-13]
- ARCH-001 publishes dialogue, pickup, area-entry, and other player events; the narrative owner evaluates them instead of reading arbitrary component fields. [source: reference/unity_project_baseline_active.md broadcast rules]
- ARCH-023 changes large flow segments or scenes only after the ledger accepts the requested transition. [interpretation]

## Core Rules
- Only the narrative progression owner can mark a beat complete. [interpretation]
- Store stable IDs, not scene object references, in save data. [interpretation]
- A reveal flag may change an interaction's allowed outcome, but it must not silently rewrite already completed evidence. [interpretation]
- Repeated input for a one-time beat must be idempotent: no duplicated dialogue, reward, log, or transition. [interpretation]
- Every accepted beat transition emits an event ID that can be checked against ARCH-010 logs. [source: reference/unity_project_baseline_active.md logging rules]

## Unity Implementation Steps
1. Assign stable IDs to chapters, bonding activities, anomalies, nightmares, memories, and reveal gates. [interpretation]
2. Define prerequisites and completion effects outside scene scripts, following ARCH-012's configuration/runtime-state split. [interpretation]
3. Subscribe the progression owner to ARCH-001 events for dialogue, interaction, area entry, and recovered evidence. [source: reference/unity_project_baseline_active.md broadcast rules]
4. On a valid request, update the ledger once, publish the accepted beat event, and ask ARCH-023 for any required scene transition. [interpretation]
5. Serialize the ledger through ARCH-004 and restore it before scene triggers are allowed to evaluate. [interpretation]
6. Route reveal-dependent verbs through the ledger so the same input can mean flee before ELEM-049 resolves and confront afterward. [interpretation]

## Anti-patterns
- Boolean sprawl: every door and dialogue script invents private story flags, making prerequisite order impossible to inspect. [interpretation]
- Scene-name truth: assuming the active scene proves a beat is complete confuses presentation with narrative state. [interpretation]
- Trigger-owned saving: a collider writes save data directly, coupling level layout to story persistence. [interpretation]
- Retroactive clue mutation: after the reveal, old evidence assets change instead of the player's interpretation changing. [interpretation]
- Duplicate completion: repeated area-entry or dialogue events replay a one-time nightmare or final choice.

## Verification
- Fresh-run order test: each chapter accepts only its declared prerequisites and logs one transition event per completed beat. [interpretation]
- Save/reload matrix: restore before and after each nightmare, memory recovery, and reveal gate; the same current beat and completed-ID set must return. [interpretation]
- Duplicate-event test: publish the same completion event repeatedly; completed IDs, rewards, and transition logs remain single. This follows the baseline rule that repeated events must not duplicate commentator log lines. [source: reference/unity_project_baseline_active.md self-check criteria]
- Reveal-gate test: the final interaction rejects confrontation before the reveal flag and accepts it afterward, with distinct observable event IDs. [interpretation]
- Runtime check: zero compile errors and zero console errors during normal operation. [source: reference/unity_project_baseline_active.md self-check criteria]

## Synergy
- ELEM-049 (Suppressed Memory and Identity Reconstruction): each fragment and the final identity deduction receives a stable, saveable ID.
- ELEM-050 (Core Verb as Narrative Metaphor): reveal gates authorize the climactic reinterpretation of a familiar input.
- ELEM-048 (Mundane Bonding / Horror Contrast): the ledger enforces pacing between safe, anomaly, and nightmare beats.
- ARCH-001 (Event Bus): supplies observable player and world events without direct field reads.
- ARCH-004 (Save System): persists mutable progress; beat definitions do not belong in the save document.
- ARCH-012 (ScriptableObject Data): stores stable beat definitions, prerequisites, and presentation references.
- ARCH-023 (Game Flow Scenes): executes large scene transitions after narrative progression approves them.
