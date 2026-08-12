+++
card_id = "ARCH-024"
type = "structure"
title = "Tilemap Level Structure (Grid + Multiple Tilemaps + Composite Collider 2D)"
summary = "A level composition method that builds a 2D map not by placing sprite objects one at a time but by splitting it into several layers of tilemaps on a grid, separating drawing, collision, and detection layer by layer"
tags = ["tilemap", "grid", "collider", "level-design", "2d", "unity", "performance"]
updated = "2026-08-02"
confidence = "medium"
+++
## Problem
When building a 2D map, placing every single floor tile as an object gives you thousands of
objects in a single map. Drawing gets slow, moving one wall means finding and moving objects,
and collision detection is created per tile as well. The tilemap structure is the approach of
painting as if stamping on graph paper, and drawing floor, walls, and decoration on separate
transparent sheets that you then view stacked.

## Structure
- Place several tilemaps under one Grid. One tilemap is one layer.
- Divide layers by role: floor, decoration on the floor, walls (with collision), the layer drawn
  in front of the player, and layers that only do pass-through detection like traps. The number of layers determines both drawing order and collision handling together, so decide it before starting level work [source: roguestarrescue.com '2D Multi-Layer Tilemap Design in Unity', verified 2026-08].
- Attach a tilemap collider only to layers that need collision. Do not attach one to the floor
  or decoration layers.
- By default a tilemap collider creates one collider per tile. What merges them is the composite collider, and attaching it also adds a Rigidbody2D. Leave this Rigidbody2D as Static and turn on the composite usage option on the tilemap collider side [source: jon-jenkins.medium.com 'Adding Colliders to Tilemaps in Unity', verified 2026-08].
- [interpretation] Map data lives in the scene, so the storage unit of this structure is
  ultimately the scene. A chunk scene (ARCH-002, ARCH-003) corresponds to one tilemap bundle.

## Core Rules
- World objects go in Chunk scenes. Tilemaps are no exception and are not placed in World_Base [source: reference/unity_project_baseline.md section 3 chunk rules].
- One role per layer. Mixing walls and decoration into the same layer makes it impossible later
  to turn off only the collision or change only the drawing order.
- Merge collision layers with a composite. Without merging, the collider vertex count grows in
  proportion to the tile count.
- The drawing order of layers is not set by hand per layer but follows the sorting convention
  (ARCH-025).
- Things that are interacted with are made as objects, not tiles. Things whose state changes,
  like doors and chests, belong as prefabs holding IInteractable (ARCH-006).
- Tile assets and palettes go in the designated folders (the ARCH-008 convention).

## Unity Implementation Steps
1. Create one grid and create tilemaps per role as its children. Use the role itself as the name.
2. Create a tile palette and register the tile assets you will use. The palette is the level
   designer's toolbox.
3. Paint the floor layer first. The floor has to exist first for the other layers to have a
   positional reference.
4. Attach a tilemap collider to the wall layer, add a composite collider, then change the
   Rigidbody2D to Static and turn on the composite usage option.
5. For layers that must detect without blocking, like traps and zone entry, leave the collider
   as a trigger and broadcast the entry event (ARCH-001).
6. Make repeating wall and path shapes as Rule Tiles, defined once. Picking corner tiles by hand
   becomes exactly the point of mistakes as the map grows.
7. Keep the same layer composition in every chunk scene. If layer names differ per chunk, the
   loader and QA cannot judge what to turn on and off.

## Anti-patterns
- Placing an object per tile: it is the same as not using a tilemap. The bigger the map, the
  slower both editing and running get.
- Drawing everything on one layer: drawing order, collision, and detection get bound into one
  lump that cannot be separated later.
- Colliders on every layer: even decoration and floor enter collision computation.
- A large map without a composite: as many colliders as tiles are created, so physics cost is
  proportional to map size.
- Attempting to give tiles state: things whose state changes, like opened doors and broken
  walls, are the job of objects, not tiles.
- Putting the map in World_Base: it violates the chunk rule and streaming does not hold.

## Verification
- Composition check: the layer names under the grid must match the decided role list. It must
  also be identical across chunk scenes.
- Collision check: only the wall layer should have a collider, and that collider must be merged
  by a composite.
- Pass-through check: the player must not pass through wall layer tiles, and must pass through
  the floor and decoration layers.
- Trigger check: entering the trap layer must leave one log line with the corresponding eventId [source: reference/unity_project_baseline.md section 3 logging rules].
- Console check: 0 console errors while repeatedly entering and leaving chunks [source: reference/unity_project_baseline.md section 4 self-check].

## Synergy
- ARCH-002 (Scene streaming): the storage unit of tilemaps is the chunk scene. The two cards share the same boundary line.
- ARCH-003 (Chunk loader): what gets turned on and off is precisely this tilemap bundle.
- ARCH-025 (2D sorting order convention): the rule that decides layer front-to-back. This card divides the layers, that card gives them order.
- ARCH-006 (Interaction): the owner of state changes that cannot be expressed with tiles.
- ARCH-008 (Folder & naming convention): the basis for where tile and palette assets live and for layer names.
- ELEM-013 (Pixel art graphic style): synergy essential — in pixel art, if tile size and grid size
  are misaligned, gaps or blurring appear at the boundaries, so deciding the art style is deciding the grid setting.
