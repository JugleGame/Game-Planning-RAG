+++
card_id = "ARCH-022"
type = "convention"
title = "Assembly Definition Module Boundaries (Assembly Definition / asmdef)"
summary = "A project partitioning convention that places an assembly definition file in each script folder so the compiler enforces module boundaries and dependency direction"
tags = ["asmdef", "module", "dependency", "compile-time", "convention", "unity", "project-structure"]
updated = "2026-08-02"
confidence = "medium"
+++
## Problem
When all scripts sit in one lump, two things collapse at once. First, fixing a single file
recompiles the whole project, lengthening the wait between edit and check. Second, any code can
call any other code, so "who depends on whom" is left entirely to human memory and
self-restraint. It is like having no walls between rooms, so anyone walks through anywhere. The
assembly definition file (asmdef) is what puts up walls and makes traffic pass only through the
doors you cut.

## Structure
- An assembly definition file makes one folder an independent compilation unit. The Unity
  documentation explains it as serving the purpose of "helping you think clearly about the
  structure of your code and manage dependencies" [source: Unity manual Assembly definition files, verified 2026-08].
- This project's module candidates do not need to be created — they already exist. The Core /
  World / Player / Interaction / NPC / Commentator folders under `Scripts/` in the baseline
  structure are the boundary lines as they stand [source: reference/unity_project_baseline.md section 3 baseline structure].
- The dependency direction is one-way, from bottom to top. Core (EventBus, SaveSystem,
  GameManager) is the lowest, and feature modules such as Commentator, NPC, and Player sit
  above it. Feature modules reference Core, but Core does not reference feature modules.
- [interpretation] This direction is not a new rule but a transcription of the broadcast rule
  (the commentator depends only on EventBus broadcasts, direct references forbidden) into a
  form the compiler enforces [source: reference/unity_project_baseline.md section 3 core rules].

## Core Rules
- References come into being only explicitly. Code in another module that is not listed in the
  assembly definition is not visible at all.
- Circular references are forbidden. A configuration where A references B while B references A
  will not compile. What surfaces first when you erect boundaries is the circularity in the
  existing code.
- Code left in the default assembly (Assembly-CSharp) can reference code split out with asmdef,
  but split-out code cannot reference the default assembly [source: Unity manual Predefined assemblies reference, verified 2026-08]. That is why migration always proceeds "from the innermost outward".
- Editor-only code is not mixed into runtime assemblies. Keep it in a separate assembly and
  restrict the platform inclusion condition to the editor.
- [interpretation] The unit to divide boundaries by is not the folder but replaceability. A lump
  you can rip out whole while the rest still compiles is one assembly.

## Unity Implementation Steps
1. Start with the most isolated code. UI or editor tools that barely call other modules are the first candidates [source: wallstop Unity Tips 'Assembly Definitions - Best Practices', verified 2026-08].
2. Create one assembly definition file at the top of that folder. Use the folder's role as its
   name (naming follows the ARCH-008 convention).
3. Read the compile error list as it comes. The errors that blow up here are the complete list
   of dependencies that module had been quietly using. Decide here whether to add a reference or
   to change that call into an EventBus broadcast (ARCH-001).
4. When circularity surfaces, do not paper over it by adding a reference; move the common part
   down a layer (into Core) or cut it with a broadcast.
5. Do not split everything at once. Separate one module, confirm 0 console errors, then move to the next.
6. Test assemblies reference the target module, but leave the target module not referencing the tests.

## Anti-patterns
- Introducing it all at once late in the project: circular references surface in heaps, leaving
  a state that is hard to either roll back or push through. Boundaries are cheaper to erect when
  there is little code.
- Every module referencing every other: files multiply and boundaries vanish. The moment the
  reference list equals the full list, this convention becomes decoration that only costs you
  recompile time.
- Calling editor APIs from a runtime assembly: it passes in the editor and fails only in the build.
- Core referencing feature modules: if the direction flips, every fix to Core recompiles
  everything and the very reason for adopting this disappears.

## Verification
- Console error check: 0 console errors during normal play right after module separation [source: reference/unity_project_baseline.md section 4 self-check].
- Direction check: confirm that the Core assembly's reference list is empty or contains only
  Unity built-in modules. If a feature module name is in it, that is a violation.
- Circularity check: specifying two modules to reference each other must fail to compile. If it
  does not fail, the boundary was not actually divided.
- Build check: an actual build, not the editor, must succeed. Editor-only code contamination
  surfaces only at this point.

## Synergy
- ARCH-001 (Event Bus): the essential pair. Broadcasts are the channel that replaces the direct
  calls that break when you erect boundaries.
- ARCH-008 (Folder & naming convention): the basis for the boundary lines. The folder convention
  must be settled first so that where to cut assemblies is not a debate.
- ARCH-011 (Boot bootstrap & manager lifetime): Core, where managers live, is the bottom layer,
  so it must reference no feature module.
- ARCH-007 (Commentator pipeline): first in line for separation. It subscribes only to
  broadcasts, so it is already one-way.
- ELEM-005 (AI integration): synergy essential — the AI module's model, prompts, and abort
  behavior change often, so isolating it such that the game still compiles when it is ripped out
  whole lowers the cost of experimentation.
