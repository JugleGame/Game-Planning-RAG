+++
card_id = "ARCH-027"
type = "structure"
title = "URP 2D Lighting (2D Renderer + Light 2D + Shadow Caster 2D)"
summary = "2D A rendering structure that assembles the brightness and atmosphere of the screen into the range of influence for each lighting object and alignment layer, rather than drawing it into a sprite."
tags = ["lighting", "urp", "light2d", "rendering", "2d", "unity", "atmosphere"]
updated = "2026-08-02"
confidence = "medium"
+++
## Problem
To create a night, cave, or torch-like atmosphere in 2D, draw a dark version of each sprite separately or use a black
A method of covering a translucent plate is used. In the former, the drawing work is doubled, and in the latter, the entire screen is the same.
It's getting dark so I can't express "it's only bright here." This structure leaves the picture as is and sets the lighting separately.
It's like the actors on stage remain the same, but when the lighting changes, the scene changes.

## Structure
- The premise is to set the render pipeline to URP and use the 2D renderer. Without this setting, the parts below
It doesn't work.
- Lighting is divided into types. Global, which illuminates the entire screen evenly, allows you to directly draw the desired shape
Freeform, sprite type that uses the sprite shape as is, and spot type with direction and angle.
There is [source: Unity manual 'Introduction to 2D lighting in URP', check 2026-08].
- Global illumination illuminates the target sprite evenly without attenuation, blend styles and alignment layers
Only one can be used per combination. [source: Check Unity manual 'Introduction to 2D lighting in URP', 2026-08].
- **The range of influence of lighting is specified in units of sorting layers.** So this structure follows the sorting convention (ARCH-025)
It's on top, and if the layer list isn't organized, your lighting setup will quickly become confusing.
- If a shadow is needed, define the shape by attaching Shadow Caster 2D to the object that will cast the shadow.
Adjust the shadow intensity from none to maximum. [source: Check Unity manual 'Light 2D component reference for URP', 2026-08].
- If you attach a normal map to a sprite, the lighting reads the irregularity information to create three-dimensional shading. [source: Unity manual 'Introduction to 2D lighting in URP', check 2026-08].
- [interpretation] In this structure, the art asset only needs to have "one bright state". Darkness is not an asset
The scene is set.

## Core Rules
- Lighting design begins after the sorting layer list is confirmed. As layers increase, all lights are affected.
The scope needs to be revisited.
- The basic brightness is set to one global illumination. With only local lighting and no global illumination, the rest of the screen is completely
It remains black.
- Draw the outline of the free-form light so that it does not cross itself. If intersecting or overlapping attenuation areas occur,
[source: Unity manual 'Light 2D component reference for URP', check 2026-08].
- Lighting objects belong to the world, so put them in the chunk scene. Do not place in World_Base [source: reference/unity_project_baseline.md 3 clause chunk rule].
- The UI is not subject to this lighting. When the UI becomes dark, it becomes unreadable (ARCH-014).
- Gameplay judgment is not replaced by brightness. If rules such as vision or stealth are needed, those decisions are made separately.
It has to be logic, and lighting just shows the result.

## Unity Implementation Steps
1. Set the project to URP and specify the renderer as 2D renderer. Existing materials are colored pink.
If you see it, it is a sign that conversion is needed at this stage.
2. Set one global light and set the default brightness. If there are multiple states, such as day and night, only the values ​​are changed and compared.
3. Specify for each light the alignment layer that the light will affect. Here, only the background and the characters are revealed.
It's different.
4. Local light sources, such as torches and windows, are created as freehand or sprite types and placed in the corresponding chunk scene.
5. Attach Shadow Caster 2D to walls and pillars that require shadows and match the shape to the silhouette.
6. Create a normal map only for sprites that require a three-dimensional effect. If you attach it to all, both asset workload and memory increase.
7. Changes in lighting status (day → night, power outage) are reflected through broadcasting rather than calling the lighting object directly (ARCH-001).

## Anti-patterns
- Drawing separate light and dark versions of each sprite: the assets are doubled and medium brightness cannot be expressed.
- Representing night with a translucent black plate: It is not possible to create a local light source, and it is easy for the UI to become dark as well.
- Improvise different influence layers for each light: no one will be able to keep track of which light hits where.
- Starting without global lighting: Areas outside the lighting become completely black, making level work impossible.
- Keep a lighting object in the scene at all times: Even if the chunk changes, it remains and lights up the wrong place.
- Overuse of light sources without checking performance: 2D Lighting is not free, and problems first appear in low-end devices.

## Verification
- Configuration check: The render pipeline must be URP and the renderer must be the 2D renderer. looks pink
There must be no object.
- Range check: The target alignment layer list for each light must match the documented intent.
- Brightness check: When global lighting is turned off, only the area around the local light source should be bright and the rest should be dark. If there is no change
The lighting is not actually applied.
- Shadow check: A shadow appears behind an object with a shadow caster, and if the intensity is set to none,
It must disappear.
- Performance check: Record the frame number in the chunk with the most light sources and check that it does not exceed the standard.
- Console inspection: Console error 0 while repeating chunk entry/exit [source: reference/unity_project_baseline.md 4 section self-check].

## Synergy
- ARCH-025 (2D sort order convention): Prerequisite. The unit of influence of lighting is the alignment layer.
- ARCH-024 (tile map level structure): The object receiving the light. The division of layers becomes the division of objects that will soon be revealed.
- ARCH-002 (Scene Streaming) / ARCH-003 (Chunk Loader): Lifetime bounds for lighting objects.
- ARCH-013 (2D camera tracking): Determines the final screen along with the camera settings.
- ARCH-014 (UI Canvas Structure): Border excluded from lighting.
- ELEM-013 (Dot Graphic Art Style): Be careful about compatibility — pixel art has smooth falloff and normal map shading.
Since the boundaries of the dots can be blurred, it is safer to set an upper limit on the lighting intensity in terms of the art style.

