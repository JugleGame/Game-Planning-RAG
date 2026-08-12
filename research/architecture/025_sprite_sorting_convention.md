+++
card_id = "ARCH-025"
type = "convention"
title = "2D Sorting Order Convention (Sorting Layer / Order in Layer / Y-Axis Sorting)"
summary = "The agreement that what is drawn in front of what in 2D is decided not by adjusting individual object coordinates but by sorting layers and axis rules shared across the whole project"
tags = ["sorting", "sprite", "render-order", "convention", "2d", "unity"]
updated = "2026-08-02"
confidence = "medium"
+++
## Problem
2D has no depth. So the engine cannot know by itself whether a character should stand in front
of or behind a tree; someone has to decide. If that decision is made by nudging the z value a
little per object as you go, nobody can later explain why only this tree has z = -0.3. This
convention is deciding in advance, with a number per sheet, "which sheet is on top" when
stacking drawings.

## Structure
- Judgment proceeds in three steps. First the Sorting Layer, then if equal the Order in Layer,
  and if still equal, distance along the sorting axis.
- The defaults are all the same. Any 2D object not otherwise specified belongs to the Default layer and has the same order-in-layer value [source: Unity manual '2D renderer sorting', verified 2026-08].
- The sorting layer list is defined once in project settings and everyone uses only that list. It
  corresponds to the layers of the screen, like background, ground, characters, decoration above
  ground, and screen effects.
- For characters and objects that overlap vertically within the same layer, do not give order by
  hand; leave it to axis sorting. Set the transparency sort mode to Custom Axis and turn on the y component of the sorting axis, and a sprite higher in y goes behind a sprite lower down [source: Unity manual 'Sort sprites' / shootingdux.co.uk 'Unity 2D Sprite Sorting – Y Sorting', verified 2026-08].
- UI is separate from this system. It follows the canvas ordering rules, so do not wedge UI in
  with sorting layers (ARCH-014).
- [interpretation] The worth of this convention lies not in "it is decided" but in "it is decided
  in only one place". Because the list is in one place in project settings, whoever creates a new
  object does not have to judge it every time.

## Core Rules
- Do not grow the sorting layer list arbitrarily. The moment you grow it, the relative order of
  existing objects can change.
- Do not adjust front-to-back with the z coordinate. z is a value used by the camera and physics,
  not a handle for drawing order.
- Leave front-to-back between characters to axis sorting, and use the order-in-layer value only
  for exceptions that axis sorting does not resolve.
- Put the sprite's pivot at the feet. What axis sorting looks at is the pivot's y, so if the
  pivot is at the chest or the center, the standing position and the drawing order disagree.
- Tilemap layers use the same list too (ARCH-024). Using a different system per layer makes it
  impossible to predict which layer a character stands in front of.

## Unity Implementation Steps
1. Define the sorting layer list in project settings in screen-layer order. The order of the list
   is the front-to-back order.
2. Assign the corresponding layer to each tilemap layer and to prefabs' sprite renderers.
3. For layers where characters and objects overlap each other, change the transparency sort mode
   to Custom Axis and turn on y on the sorting axis.
4. Unify sprite assets' pivots at the feet. Postponing this work means having to re-place the
   positions of all prefabs later.
5. Give an order-in-layer value only to objects that need an exception. Leave the reason with the
   exception.
6. Check that the camera is Orthographic. The sorting axis setting works together with the camera
   projection mode (ARCH-013).

## Anti-patterns
- Fixing front-to-back with z coordinates: it works for now but collapses the moment you touch
  physics or camera settings, and nobody can explain what the values mean.
- Assigning order values by hand per object: every time a new object is added it must be wedged in
  between existing values, and eventually renumbering work occurs periodically.
- Creating a sorting layer per object type: it becomes a classification rather than a layer, and
  the list grows without limit.
- Inconsistent pivots: even with axis sorting on, the overlap result differs per character, making
  the rule pointless.
- Bringing UI to the front with sorting layers: two truths arise alongside the canvas system.

## Verification
- List check: the sorting layer list must exactly match the decided layer names, with no other
  values.
- Overlap check: a character standing below the same object must be drawn in front of it, and
  standing above must be drawn behind it.
- z check: the z coordinates of sprite objects must all be identical. Differing values are traces
  of having fixed order with z.
- Pivot check: the y of a character sprite's pivot must be at the bottom of the sprite.
- Console check: 0 console errors during normal play after changing sorting settings [source: reference/unity_project_baseline.md section 4 self-check].

## Synergy
- ARCH-024 (Tilemap level structure): directly interlocking. That card divides the layers and this card gives the layers front-to-back order.
- ARCH-013 (2D camera follow): the orthographic camera and pixel perfect settings are preconditions of the sorting result.
- ARCH-014 (UI canvas structure): a boundary card. UI follows canvas order, not this convention.
- ARCH-026 (Sprite atlas & draw call batching): sorting order decides where batching breaks, so the atlas bundling unit follows this layer list.
- ARCH-027 (URP 2D lighting): the unit of a light's range of influence is the sorting layer. If the layer list wobbles, the whole lighting setup wobbles.
- ARCH-008 (Folder & naming convention): layer names are subject to the convention too.
- ELEM-013 (Pixel art graphic style): synergy essential — in pixel art a one pixel difference makes
  overlap noticeable, so the pivot and sorting axis rules directly determine the polish of the art.
