+++
card_id = "ARCH-029"
type = "pattern"
title = "Component-based Composition for 3D GameObjects"
summary = "A Unity-native architecture that builds a 3D actor from small, replaceable capabilities attached to a GameObject instead of concentrating every behavior in one inheritance tree or manager"
tags = ["unity", "3d", "gameobject", "component", "composition", "modularity"]
updated = "2026-08-13"
confidence = "high"
+++
## Problem
A 3D actor often needs movement, collision, rendering, health, interaction, audio, and animation. If one script owns all of them, changing one capability can disturb unrelated behavior and prefab variants become branches inside the same class. [interpretation] The architecture needs a boundary that lets an actor gain or replace one capability without rewriting the rest.

## Structure
- A GameObject is the scene container, and attached Components define its behavior. Unity identifies Transform, Mesh Filter, Mesh Renderer, Camera, Rigidbody, and Collider as fundamental building blocks for 3D games. [source: Unity Manual, Key concepts, Unity 6.0, as of 2026-08-13]
- A script that derives from MonoBehaviour becomes another Component attached to a GameObject; a Component always belongs to a GameObject. [source: Unity Scripting API, Component, Unity 6.0, as of 2026-08-13]
- [interpretation] A prefab is the composition root for one actor: visual, physics, input, interaction, health, and presentation components meet there, while each component owns one capability.
- [interpretation] Cross-object notifications leave the actor through ARCH-001 rather than turning local component references into a scene-wide dependency graph.

## Core Rules
- Prefer composition of focused components over a deep gameplay inheritance hierarchy. [interpretation]
- Keep same-object collaboration explicit through serialized component references, interfaces, or a validated component lookup; fail visibly when a required capability is absent. [interpretation]
- Keep physics authority in the Rigidbody-facing component and rendering authority in presentation components. [interpretation]
- Do not make a local component search the entire scene to discover routine dependencies. [interpretation]
- Preserve the repository baseline ownership boundaries when placing new scripts; changing the baseline structure requires human approval. [source: reference/unity_project_baseline_active.md baseline structure]

## Unity Implementation Steps
1. List the capabilities of one 3D actor, such as locomotion, damage reception, interaction, animation, and audio feedback. [interpretation]
2. Assign one owner component to each capability and define the smallest messages or interfaces needed between them. [interpretation]
3. Assemble the components on a prefab with the required Transform, renderer, collider, and physics components for that actor. [source: Unity Manual, Key concepts, Unity 6.0, as of 2026-08-13]
4. Wire stable local dependencies in the Inspector and route scene-wide notifications through ARCH-001. [interpretation]
5. Create prefab variants by replacing or configuring components rather than adding actor-type branches to a central script. [interpretation]

## Anti-patterns
- God component: one MonoBehaviour handles input, physics, health, animation, UI, and saving, so every change expands its reasons to break. [interpretation]
- Hidden scene lookup: a component silently finds global objects at runtime, making prefab behavior depend on whichever scene happens to be loaded. [interpretation]
- Component-shaped inheritance: nominally separate components all inherit mutable gameplay state from a common base, recreating the coupling that composition was meant to remove. [interpretation]
- Event bus for immediate local control: sending knockback or other same-actor physics control through ARCH-001 obscures ordering; that bus is for notification rather than immediate control. [source: ARCH-001 card, Synergy section, as of 2026-08-13]

## Verification
- Prefab inspection: each required capability appears once, and removing an optional presentation component does not disable unrelated gameplay logic. [interpretation]
- Dependency inspection: required references are assigned before Play mode and no routine dependency relies on a scene-wide search. [interpretation]
- Behavior test: swap one implementation behind ARCH-006 or ARCH-028 and confirm the caller still uses the same promise. [interpretation]
- Runtime check: the relevant Unity work has zero compile errors and zero console errors during normal operation. [source: reference/unity_project_baseline_active.md self-check criteria]

## Synergy
- ARCH-001 (Event Bus): carries notifications between composed actors and global systems while immediate same-object control stays local.
- ARCH-006 (Interaction): supplies a focused interaction capability that can be attached beside other actor components.
- ARCH-028 (Hit/Damage Interface): supplies a separate damage capability instead of merging deliberate interaction and damage into one promise.
- ELEM-011 (Emergent Systemic Interaction): good fit when object capabilities react through explicit object-to-object channels; player-triggered interaction alone is insufficient. [source: ARCH-006 card, Synergy section, as of 2026-08-13]
