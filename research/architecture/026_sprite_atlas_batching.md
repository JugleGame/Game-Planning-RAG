+++
card_id = "ARCH-026"
type = "convention"
title = "Sprite Atlas & Draw Call Batching (Sprite Atlas)"
summary = "An asset bundling convention that packs scattered sprites into one large texture to reduce the number of drawing requests sent to the GPU"
tags = ["sprite-atlas", "draw-call", "batching", "performance", "2d", "unity", "asset"]
updated = "2026-08-02"
confidence = "medium"
+++
## Problem
A 2D game draws hundreds of sprites on screen. But if the image files are all different, the CPU
has to separately tell the GPU "use this image this time" for each draw. That number of times you
speak up is the draw call, and the flashier the screen gets, the sooner this hits its limit. It
is like bundling stickers scattered as loose pieces into one large sticker sheet so you only have
to take it out once.

## Structure
- An atlas is an asset that packs multiple sprites into a single texture. Sprites in the same atlas can be processed together in one drawing request [source: Unity manual 'Sprite atlases', verified 2026-08].
- The bundling unit is "things that appear on screen together". Putting sprites that do not appear
  in the same scene together into one atlas loads unused textures into memory too. Conversely, if
  things that do appear together are scattered across several atlases, the point of bundling
  disappears.
- This project's bundle candidates are already divided. Sorting layers (ARCH-025) and tilemap
  layers (ARCH-024) are precisely the boundaries of "what gets drawn together", so it is natural
  to divide atlases along those lines.
- If resolution must differ by device performance, keep variants of the same atlas and pick the appropriate one at runtime [source: game-developers.org 'What Is Sprite Atlas in Unity', verified 2026-08].
- [interpretation] Before it is a performance tool, an atlas is an asset bundling convention. If it
  is not settled which atlas a new sprite goes into, each person who adds one makes a different
  judgment and the bundling slowly collapses.

## Core Rules
- Do not mix assets from several scenes into one atlas. The bundling criterion is not file type
  but the moment they appear together.
- Bundling that crosses drawing order has no effect. Even if you put sprites from different
  sorting layers into one atlas, if another layer comes between them the request is split again.
- The location of atlas assets and source sprites follows the folder convention (ARCH-008).
- Do not leave sprites that are not in any atlas. Allow an exception and the exception becomes the
  default.
- [interpretation] Make optimization judgments after measuring. Whether to split or merge atlases is
  decided by looking at the profiler's batching figures, not by gut feel.

## Unity Implementation Steps
1. Decide the bundle list first. Name them by screen and sorting layer unit.
2. Create a sprite atlas asset per bundle, and register the folder rather than individual sprites.
   Registering the folder means new assets are bundled automatically, so a person does not have to
   add them each time.
3. Match compression, filter, and padding settings to the bundle's character. Pixel art needs the
   filter off and compression low to preserve the original.
4. After running, check draw call and batching figures in the profiler. Without comparing values
   before and after adoption you cannot know whether the bundling actually had an effect.
5. If per-device resolution branching is needed, create variant atlases and pick at runtime.
6. Keep UI sprites in a separate bundle. The game screen and the UI are drawn at different moments (ARCH-014).

## Anti-patterns
- The whole project in one atlas: the texture becomes huge and loading and memory worsen together.
- An atlas per sprite: the result is the same as not bundling at all.
- Bundling that ignores sorting order: batching breaks in the middle and the figures do not improve.
- Touching things without measuring: settings change without knowing which side improved, and you
  cannot even roll back.
- Keeping default compression on pixel art: colors smear and edges blur. You gain performance and
  lose the artwork.

## Verification
- Registration check: there must be no sprite in the project that belongs to no atlas.
- Figure check: compare draw call and batching figures before and after adoption in the same scene
  and record the improvement.
- Image quality check: zoom into pixel art sprites and confirm the edges have not blurred.
- Console check: 0 console errors during normal play after applying atlases [source: reference/unity_project_baseline.md section 4 self-check].

## Synergy
- ARCH-025 (2D sorting order convention): directly interlocking. What decides where batching breaks is sorting order.
- ARCH-024 (Tilemap level structure): tile assets batch best when bundled per layer.
- ARCH-015 (Object pooling): a different layer with the same purpose. Pooling reduces creation cost, atlases reduce drawing cost.
- ARCH-008 (Folder & naming convention): for folder registration to hold, asset locations must be a convention first.
- ARCH-014 (UI canvas structure): the boundary of the UI asset bundle.
- ELEM-013 (Pixel art graphic style): synergy essential — for pixel art, compression and filter
  settings are exactly the question of whether the artwork is damaged, so the art owner must help
  decide atlas settings.
