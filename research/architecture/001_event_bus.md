+++
card_id = "ARCH-001"
type = "pattern"
title = "Event Bus (EventBus / Pub-Sub)"
summary = "A loose coupling structure where systems never call each other directly: senders broadcast events to a central station (EventBus), and only the parties that want to listen subscribe and react"
tags = ["decoupling", "core", "commentator", "2d-open-world", "unity", "pub-sub"]
updated = "2026-07-31"
confidence = "high" # 프로젝트 기준 구조(reference/unity_project_baseline.md)의 방송 규칙과 동일 + Unity 공식 아키텍처 자료 근거
+++
## Problem

When game systems reference each other directly (PlayerController calling Commentator directly, NPC calling UI directly), fixing one breaks everything wired to it. This project's AI Commentator in particular needs to know about nearly every event — combat, pickups, dialogue, area entry — so building it on direct references turns the commentator into a monster with a straw stuck into every system. Put simply: if classmates pass news to each other by whispering, the chain breaks the moment one of them is absent; if you announce it over the classroom speaker, only those who want to listen need to. EventBus is that speaker.

## Structure

- Location: `Assets/Scripts/Core/EventBus.cs` [source: reference/unity_project_baseline.md baseline structure]
- Flow: sender (Player, NPC, World) → `EventBus.Publish(GameEvent)` → subscribers (Commentator, UI, SaveSystem) each react on their own
- `GameEvent` is a serializable data bundle holding the event ID, the originating actor, coordinates and a payload, defined in `Scripts/Core/`.
- The sender does not know who listens, and the subscriber does not depend on who sent it. Both know only the EventBus.
- Implementation options are a static bus built on C# `event`/`Action`, or a ScriptableObject event-channel approach. [source: Unity official e-book "Level up your code with design patterns" and the Unite 2017 Ryan Hipple talk "Game Architecture with Scriptable Objects" — the approach Schell Games applied in an actual commercial project] [interpretation] This project splits scenes Additively and often, so a static bus or an SO channel — neither of which is tied to scene lifetime — is the safe choice.

## Core Rules

- Broadcast rule: player actions (combat, pickup, dialogue, area entry) must be broadcast via `EventBus.Publish(GameEvent)`. Direct references are forbidden. [source: reference/unity_project_baseline.md]
- The commentator system depends on these broadcasts only. If the Commentator reads another system's fields directly, that is a rule violation. [source: reference/unity_project_baseline.md]
- Subscribers subscribe in `OnEnable` and must unsubscribe in `OnDisable`. Skip the unsubscribe and you will blow up calling into a destroyed object.
- Event type definitions live only in `Scripts/Core/`. Scripts inside a Chunk scene do not invent their own event types.

## Unity Implementation Steps

1. Create `Scripts/Core/GameEvent.cs` — define the event ID (enum), actor and payload fields.
2. Create `Scripts/Core/EventBus.cs` — expose only three public functions: `Publish(GameEvent)`, `Subscribe(Action<GameEvent>)`, `Unsubscribe(...)`.
3. Wire the send points — add a one-line `Publish` call in PlayerController (combat/pickup), Interaction (dialogue) and ChunkLoader (area entry) when the corresponding event occurs.
4. Wire the subscribe points — the Commentator subscribes in `OnEnable`, and after generating a reaction writes one line to `Logs/commentator.log` in the form `[time] [event ID] [reaction summary]`. [source: reference/unity_project_baseline.md logging rules]
5. Self-check — confirm 0 compile errors and 0 console errors, then commit.

## Anti-patterns

- Direct-reference wiring: binding systems together with `FindObjectOfType` or by dragging public fields. The moment a Chunk scene is unloaded Additively the reference breaks and you get a NullReference. [interpretation] In a project like this one that toggles scenes on and off, this is the failure that fires most often.
- Universal events: abusing events for everything. Broadcasting position every frame fills the bus with noise and makes debugging impossible. Events are for "occurrences" (died, obtained, entered) only.
- Missing unsubscribe: a memory leak where subscriptions survive scene unload and ghost subscribers pile up. Unity's own material also names missing event unsubscription as a classic mistake. [source: the Observer pattern chapter of the Unity official e-book "Level up your code with design patterns"]
- Publish-inside-publish chains: publishing B while handling A, where B calls A again — a cycle. Prevent it with a publish-depth limit or queued processing.

## Verification

- 0 compile errors, 0 console errors. [source: reference/unity_project_baseline.md self-check criteria]
- QA judges from the log whether `Logs/commentator.log` carries one line per event in the form `[time] [event ID] [reaction summary]`. [source: reference/unity_project_baseline.md logging rules]
- Looseness test: removing the Commentator object from the scene must leave the main game running without errors. If it does not, a direct reference is hiding somewhere.
- Missing-broadcast test: performing each of the four action types — combat, pickup, dialogue, area entry — once must leave four lines in the log.

## Synergy

- ELEM-005 (AI integration): an AI commentator needs an event stream to produce live reactions. EventBus is that supply line, so it is effectively a precondition.
- Good fit — save system: if SaveSystem collects "what happened" by subscribing to events, save logic never bleeds into gameplay code.
- ARCH-018 (game manager): global game state changes (Playing/Paused/GameOver) are broadcast over this bus. It is the only channel that keeps UI, input and audio from referencing GameManager directly.
- ARCH-014 (UI canvas structure): the dynamic canvas is refreshed only through bus subscriptions — redrawing when an event arrives instead of polling every frame is the premise of the static/dynamic split.
- Conflict warning — physics reactions that need immediacy (hit knockback and the like) should be handled directly inside the component rather than routed through the bus. The bus is for "notification", not "control".
