+++ 
card_id = "ARCH-013"
type = "pattern"
title = "2D Camera Follow (Cinemachine 3 + Boundary Confinement + Pixel Perfect)"
summary = "An approach that does not simply attach the camera to the character but entrusts it to a dedicated 'following part', so it follows smoothly while never showing the empty space outside the world"
tags = ["camera", "cinemachine", "pixel-perfect", "2d", "unity", "world-base"]
updated = "2026-07-30"
confidence = "high" # reference/unity_project_baseline.md 기준 구조의 World_Base 카메라 명시 + Cinemachine 3.1 공식 문서(2D graphics / Confiner 2D / Pixel Perfect 확장) 근거 + 안티패턴(카메라를 플레이어 자식으로 두기) 실사례
+++ 
## Problem

Attaching the camera as a child of the character is the fastest way to complete a "following camera", but every time the character trembles slightly from physics the whole screen trembles with it, and standing at the edge of the map exposes the empty space outside the chunks. With pixel art there is one more problem — if the camera position does not land exactly on the pixel grid, the picture shakes slightly and smears. Put simply: tie the photographer to a running person's shoulder and every photo is blurry. Standing the photographer separately and giving the rule "follow that person smoothly, but do not shoot outside the stage" is what this card is.

## Structure

- The camera is in the World_Base scene and is always on. Do not put a camera in Chunk scenes. [source: reference/unity_project_baseline.md baseline structure — World_Base.unity "player, camera, UI (always on)"]
- Three-way role split — (1) the Unity camera + CinemachineBrain (the side that actually draws the screen), (2) the CinemachineCamera (the side that decides where to look, with the player as the follow target), (3) extension modules (boundary confinement, pixel perfect).
- The baseline version is Cinemachine 3.x. Going up from 2.x to 3.x changes names and structure, so it does not just work and requires separate work. [source: Unity Cinemachine 3.1 official manual — states that Cinemachine 3 requires work when upgrading from 2.X]
- 2D uses Orthographic projection. Setting it to orthographic makes Cinemachine behave accordingly, and Orthographic Size takes the place of the field of view (FOV) in the lens settings. That is, this one value decides "how wide you see". [source: Unity Cinemachine 3.1 official manual — 2D graphics]
- Not showing the outside of the world is handled by the Confiner 2D extension. This extension post-corrects the camera's final position, pushing it inside a designated boundary region. [source: Unity Cinemachine 3.1 official manual — Confiner 2D extension]
- With pixel art, use the Pixel Perfect extension as well. This extension detects whether a Pixel Perfect Camera component is attached and, according to its settings, corrects the CinemachineCamera's Orthographic Size to a value where sprites appear exactly at pixel resolution. [source: Unity Cinemachine 3.1 official manual — Cinemachine Pixel Perfect extension]

## Core Rules

- The camera object exists only in World_Base. Putting a camera in a chunk scene makes cameras multiply every time a chunk is turned on, so you cannot tell which camera is drawing the screen. [source: reference/unity_project_baseline.md chunk rules]
- Do not make the camera a child of the player. Following is done by setting the follow target, not by a parent-child relationship. Making it a child transfers physics jitter straight to the screen (ARCH-009).
- The range visible on screen must be within the chunk activation range. Since only the 3x3 chunks around the player are on, if the camera sees farther than that, not-yet-loaded empty space is exposed. [source: reference/unity_project_baseline.md baseline structure — only the 3x3 chunks around the player are active]
- Do not assign the camera position directly in code. There must be a single owner deciding the position. Effects such as shake and zoom are also handled by Cinemachine's own means.
- If a cutscene or special viewpoint is needed, create one more CinemachineCamera and switch by priority. Do not use the approach of overwriting the existing camera's settings in code — nobody will know the state to return to.
- Camera-related events (such as entering a region) are broadcast on the EventBus. The commentator sees only these broadcasts. [source: reference/unity_project_baseline.md broadcast rules]

## Unity Implementation Steps

1. Set the World_Base scene's Unity camera projection to Orthographic and attach a CinemachineBrain.
2. Create a CinemachineCamera object in World_Base and set the follow target (Follow) to the player. The camera object and the CinemachineCamera are separate things.
3. Set the visible range with the lens's Orthographic Size. Check that this value falls within the chunk activation range.
4. Adjust the follow smoothness. Setting the value close to 0 sticks it immediately, which is the same as making it a child; too large makes the controls feel laggy.
5. Create a boundary region for the world edge, add the Confiner 2D extension to the CinemachineCamera, and designate that boundary. Adding extensions is done through the add-extension menu in the CinemachineCamera Inspector. [source: Unity Cinemachine 3.1 official manual — how extensions are added]
6. For pixel art: attach the Pixel Perfect Camera component to the camera and add the Pixel Perfect extension to the CinemachineCamera. Unify the reference resolution and the units-per-pixel value across the project as one (recording them in an ARCH-012 data asset keeps them from scattering).
7. Check chunk boundary movement — see that no unloaded area appears on screen while crossing between chunks (ARCH-003).
8. Self-check — confirm 0 compile errors and 0 console errors, then commit. [source: reference/unity_project_baseline.md self-check criteria]

## Anti-patterns

- Attaching the camera as a child of the player: [interpretation] the most common starting point and the one reverted the fastest. The fine jitter of physics movement, knockback, and collision recoil all show up as screen shake.
- Assigning the camera position from a script every frame: it overwrites and is overwritten by the position Cinemachine computed, so the screen oscillates between two values.
- Putting a camera in a chunk scene: cameras multiply the moment a chunk turns on. You cannot tell which one is drawing, and turning the chunk off blacks out the screen.
- Shipping without boundary confinement: empty space is exposed at the map edge. The assumption "the player will not go there" is always wrong.
- Leaving Orthographic Size at an arbitrary value in pixel art: sprites fall out of alignment with the pixel grid and smear and shake slightly. This value must be computed from the pixel perfect settings. [source: Unity Cinemachine 3.1 official manual — the Pixel Perfect extension corrects Orthographic Size]
- Touching camera zoom in and out from several scripts separately: whichever ran last wins, so it becomes a bug that does not reproduce.
- Building a 3.x project while reading Cinemachine 2.x documentation: names and structure differ, so following it verbatim gets stuck at compilation. [source: Unity Cinemachine 3.1 official manual — upgrading from 2.X requires work]

## Verification

- 0 compile errors, 0 console errors. [source: reference/unity_project_baseline.md self-check criteria]
- Camera uniqueness check: there must be 1 active CinemachineBrain during play. It must be the same even with several chunks turned on.
- Parent relationship check: the camera object's parent must not be the player (verified in the scene hierarchy).
- Boundary check: even pushing the player past the world boundary, the area outside the boundary must not be visible on screen.
- Unloaded exposure check: while moving back and forth across a chunk boundary, no unloaded empty area must appear on screen.
- Direct assignment check: there must be no place in the code assigning a value to the camera Transform position (verifiable by search).
- Pixel alignment check (for pixel art): while the camera moves, the pixels of a stationary sprite must not shake or change thickness.
- Scene membership check: the camera and the CinemachineCamera must belong to the World_Base scene (belonging to a Chunk scene is a fail).

## Synergy

- ARCH-009 (2D Physics Movement): direct interlock — since the camera follows a target that moves by physics, separating following from physics jitter is this card's reason for existing.
- ARCH-003 (Chunk Loader): a constraint relationship — the visible range must not exceed the 3x3 active range. To widen the camera range you must first review the chunk activation rule.
- ARCH-002 (Scene Streaming): the basis for placing the camera in the always-on World_Base is in that card.
- ARCH-001 (Event Bus): the broadcast path for view-related events such as entering a region.
- ELEM-013 (Pixel Art Style): essential compatibility — choose pixel art and the pixel perfect setting becomes a requirement, not an option. Without this decision the art quality collapses at the camera.
- ELEM-012 (Landmark-Based Exploration): compatibility caution — guiding with distant landmarks requires a sufficiently wide visible range, and that range conflicts with the chunk activation range. Adopting landmark exploration requires reviewing the chunk activation rule as well.
