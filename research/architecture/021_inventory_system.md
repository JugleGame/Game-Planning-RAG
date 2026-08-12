+++
card_id = "ARCH-021"
type = "pattern"
title = "Inventory System (Inventory / Item Database, ScriptableObject Based)"
summary = "A structure that separates an item's 'definition' (name, icon, stats) from its 'held state' (count, durability), so that a single data asset lets multiple characters and slots share the same item information"
tags = ["inventory", "item", "scriptableobject", "rpg", "unity", "pattern"]
updated = "2026-07-31"
confidence = "high"
+++
## Problem
If each item's name, icon, description, and stats are hardcoded into a class, then once there
are just over 100 items you must recompile the code to change a single number. Moreover, if the
state "I am holding 3 potions" and the definition "what a potion is" are mixed together in the
same place, the definition gets stored redundantly whenever multiple characters hold the same
potion.

## Structure
- Baseline form: item definitions are made as ScriptableObject assets (ItemData) stored in the
  project, and the actual inventory slots hold only an ID/count pair referencing that asset
  [source: gamedevbeginner.com, generalistprogrammer.com tutorials combined, verified 2026].
  It is a concrete case of applying the principle of ARCH-012 (Data/ data asset convention) to
  items.
- Layer separation: (1) item definition asset (2) inventory slot data (which definition is held
  and how many) (3) UI display - separating the three layers means the data structure does not
  wobble even if you tear up the UI [source: pavcreations.com equipment system architecture
  analysis].

## Core Rules
- A ScriptableObject asset holds only the "definition", not the "state" (current count,
  durability) - the asset is shared data saved in the editor, so writing state directly into
  the asset at runtime produces a bug where all characters share that state.
- An inventory slot only references the item definition (by ID or SO reference), and mutable
  data such as quantity and durability lives in a separate runtime class.
- When integrating with saving (ARCH-004 save system), serialize only "item ID + quantity" to
  JSON, not the asset itself - ScriptableObjects are not direct serialization targets.

## Unity Implementation Steps
1. Define name, icon, description, stackability, and type on `ItemData : ScriptableObject`.
2. Create a `.asset` file per item in `Data/Items/` (following the ARCH-008 folder convention).
3. Manage the inventory as a `List<InventorySlot>`, where each slot holds only an `ItemData`
   reference and the current quantity.
4. The UI iterates the inventory list and displays the icon and name of the `ItemData` each
   slot references - the UI does not hardcode item attributes itself.
5. On save, serialize slots as a `{itemId, count}` array; on load, look the `ItemData` asset up
   again by ID and reconnect it.

## Anti-patterns
- Making a separate class for every single item: every increase in item count requires a new
  class, hurting extensibility.
- Overwriting quantity directly onto ScriptableObject asset fields at runtime: the asset is
  shared project-wide, so one character's usage changes the value for all other characters.
- Putting per-item-type `if/switch` branches into the inventory UI code: every new item
  requires fixing the UI code, losing the benefit of data-driven design.

## Verification
- State isolation check: even if character A uses an item, the quantity of the same item for
  character B must not change.
- Save/load check: after saving the inventory and restarting, quantities and types must be
  restored exactly.
- Console cleanliness: warnings should appear only when attempting to load a nonexistent ID,
  and must be 0 during normal play.

## Synergy
- ARCH-012 (Data/ data asset convention): this pattern is a concrete application case of that
  convention.
- ARCH-004 (Save system, JSON serialization): the direct consumer that saves and restores
  inventory state.
- ELEM-019 (Random loot drops): dropped items go through this structure when entering the inventory.
