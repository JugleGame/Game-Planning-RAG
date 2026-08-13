+++
card_id = "ARCH-031"
type = "structure"
title = "Entities ECS / DOTS for Large 3D Simulations"
summary = "A data-oriented Unity architecture that represents many similar actors as data-only entities processed in batches by systems, with GameObject authoring converted through baking"
tags = ["unity", "3d", "ecs", "dots", "entities", "data-oriented", "performance"]
updated = "2026-08-13"
confidence = "high"
+++
## Problem
Large 3D simulations can spend substantial CPU time updating many similar actors through scattered object-oriented callbacks. Unity positions DOTS as a data-oriented approach for scaling processing, with ECS, Burst, and the C# Job System providing data organization, optimized native compilation, and safe parallel execution. [source: Unity DOTS official overview, as of 2026-08-13]

## Structure
- Entity: a unique identifier and lightweight unmanaged alternative to a GameObject. It contains no code. [source: Unity Entities package manual, Entities 1.4.8, as of 2026-08-13]
- Component: data associated with an entity. [source: Unity Entities package manual, Entities 1.4.8, as of 2026-08-13]
- System: logic that selects and processes entities by their component data. [source: Unity Entities package manual, Entities 1.4.8, as of 2026-08-13]
- Baking boundary: authoring data from GameObjects is converted into ECS data before runtime processing. [source: Unity Entities package manual, Entities 1.4.8, as of 2026-08-13]
- Runtime stack: Entities supplies ECS, Burst compiles compatible code to optimized native code, and the C# Job System enables safe parallel work. [source: Unity DOTS official overview, as of 2026-08-13]

## Core Rules
- Components hold data; systems hold behavior. Entities themselves contain no code. [source: Unity Entities package manual, Entities 1.4.8, as of 2026-08-13]
- Design systems around component queries and batch work rather than per-object ownership. [interpretation]
- Treat adding or removing components as a structural change and measure it deliberately; Unity documents structural changes as a performance concern. [source: Unity Entities package manual, Entities 1.4.8, as of 2026-08-13]
- Keep a clear hybrid boundary for systems that remain GameObject-based; Unity describes ECS for Unity as compatible with GameObjects. [source: Unity DOTS official overview, as of 2026-08-13]
- Adding the Entities package or changing ProjectSettings requires human approval under the repository baseline. [source: reference/unity_project_baseline_active.md approval boundaries]

## Unity Implementation Steps
1. Profile the 3D simulation and select a repeated, data-heavy workload rather than converting the entire project by default. [interpretation]
2. Obtain approval for the package change, then pin a released Entities version compatible with the project's Unity editor version. Entities 1.4.3 is released for Unity 6.0 in the Unity manual. [source: Unity Manual, Entities package version information, Unity 6.0, as of 2026-08-13]
3. Define data-only components and authoring data for the selected workload. [source: Unity Entities package manual, Entities 1.4.8, as of 2026-08-13]
4. Bake GameObject authoring data into entities and implement systems that process matching component sets. [source: Unity Entities package manual, Entities 1.4.8, as of 2026-08-13]
5. Move compatible hot loops to jobs and Burst only after behavior is correct, then profile the result against the original workload. [interpretation]
6. Bridge only aggregate gameplay notifications back to ARCH-001 so classic GameObject systems do not become coupled to individual entities. [interpretation]

## Anti-patterns
- ECS everywhere: converting unique cameras, menus, or low-count authored objects without a measured workload adds a second mental model without demonstrated value. [interpretation]
- Behavior in components: storing service references or object logic in data components defeats the documented data-and-system split. [interpretation]
- Structural churn: repeatedly adding and removing components in a hot path without measurement ignores Unity's explicit structural-change performance concern. [source: Unity Entities package manual, Entities 1.4.8, as of 2026-08-13]
- Leaky hybrid boundary: classic MonoBehaviours reach into individual entities while ECS systems also mutate the same gameplay authority. [interpretation]
- Package drift: adopting an experimental package line without pinning compatibility makes the card's implementation assumptions unstable. [interpretation]

## Verification
- Version inspection: the project manifest pins an approved Entities release compatible with the selected Unity editor version. [interpretation]
- Data inspection: Entity Hierarchy shows the expected entities and component sets after baking. Unity provides Entities-specific editor windows for this workflow. [source: Unity Entities package manual, Entities 1.4.8, as of 2026-08-13]
- Correctness test: the ECS workload produces the same observable gameplay result as the reference implementation for a fixed input sequence. [interpretation]
- Performance test: Unity Profiler evidence compares the same scene and workload before and after migration; no performance claim is accepted without the capture. [interpretation]
- Runtime check: the relevant Unity work has zero compile errors and zero console errors during normal operation. [source: reference/unity_project_baseline_active.md self-check criteria]

## Synergy
- ARCH-001 (Event Bus): carries aggregate ECS outcomes to classic UI, save, and commentary systems without exposing individual entities.
- ELEM-011 (Emergent Systemic Interaction): good fit when many objects follow a small set of composable data rules and object-to-object reaction channels. [source: ARCH-006 card, Synergy section, as of 2026-08-13]
