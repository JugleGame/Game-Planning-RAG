+++
card_id = "ARCH-015"
type = "pattern"
title = "Object Pooling (UnityEngine.Pool ObjectPool<T>)"
summary = "A structure that eliminates momentary performance burden by borrowing and returning pre-made inventory rather than creating and destroying objects that appear and disappear frequently, such as bullets and effects."
tags = ["pooling", "performance", "objectpool", "bullet", "vfx", "unity"]
updated = "2026-07-31"
confidence = "high"
+++
## Problem
Objects that are short-lived and occur frequently, such as bullets, heat effects, and enemy spawns, are used every time.
If you create and delete `Instantiate`/`Destroy`, memory allocation and
Frames bounce due to overlapping garbage collection [source: Unity Manual, Pooling and reusing objects,
https://docs.unity3d.com/6000.4/Documentation/Manual/performance-reusable-code.html].
It is cheaper to make inventory in advance, borrow it, and then return it.

## Structure
- From Unity 6000 (2021.3 and above), `ObjectPool<T>` is in the `UnityEngine.Pool` namespace.
It is built-in. Pass the delegate to be executed at each creation/rental/return/destruction time to the constructor.
It is a stack-based pool that defines behavior. [source: Unity Scripting API, Pool.ObjectPool_1,
  https://docs.unity3d.com/6000.5/Documentation/ScriptReference/Pool.ObjectPool_1.html].
- In this project, place one grass in `Core/` for each repetitive spawn object such as bullets or effects, or
At the specification stage, one of two methods is used in which the common manager holds the pool for each prefab in a dictionary.
Choose. Do not mix arbitrarily.
- Callback 4 types: createFunc (when creating a new one), actionOnGet (activating when taking out), actionOnRelease
(disabled when returning), actionOnDestroy (when actually destroyed due to exceeding the pool maximum).

## Core Rules
- Do not call `Destroy()` directly — the pull target always returns `Release()`.
If you use `Destroy`, the pool's stock count will deviate, and the next `Get()` will create a new number that is different from what you expected.
- In `actionOnGet`/`actionOnRelease`, be sure to leave traces of previous use such as location, speed, and timer.
Initialize — Unlike regular Instantiate, a reusable object holds its previous state.
This is the key difference.
- `defaultCapacity` and `maxSize` are determined based on the expected number of simultaneous occurrences of the specification.
Don’t set things arbitrarily large without any basis (waste of memory) — don’t set things small without any basis.
(The pool overflows every time and creates a new one).
- Leave `collectionCheck` (duplicate return detection) turned on during development, and use the same instance twice.
Catch `Release()` bugs early.

## Unity Implementation Steps
1. Check the specifications for the prefab and the maximum simultaneous number of pooling targets (bullets, effects, etc.).
2. By placing a reference in the target script indicating that it has been borrowed from the pool,
When finished (crash/timer expires), it causes `Release()` to be called — it returns itself.
3. Determine who owns the pool: if there are multiple launchers like bullets, a common manager pool, a specific object
If it is exclusive, the object directly holds the pool.
4. `actionOnGet` to `SetActive(true)` and state initialization, `actionOnRelease` to
Pair `SetActive(false)` — if these two callbacks are empty, pooling has no effect.
5. Spec/ARCH-011 whether to empty the pool when switching scenes or keep it as `DontDestroyOnLoad`
The decision is made according to the bootstrap rules.

## Anti-patterns
- Fake pooling, leaving `Instantiate` and `Destroy` and just calling it "pool" —
The allocation cost remains the same.
- The previous state (health, speed, subscribed events) of the object taken out of the pool is not initialized.
Creating hard-to-reproduce bugs that "occasionally appear in strange states."
- The pool grows indefinitely without a maximum limit — Memory continues to increase in situations where spawns are crowded.

## Verification
- The profiler's
Check if GC Alloc is close to 0 per frame [source: Unity Manual, Pooling and
  reusing objects].
- Even after repeatedly reusing the pool target, does the state (speed, color, etc.) from the previous round remain?
Observe through console log or inspector.
- 0 console errors, especially the "Returning an already returned item" warning caught by collectionCheck
0 gun.

## Synergy
- ARCH-001 (Event Bus): Broadcasts events such as bullet disappearance and enemy kills to determine when to return the pool.
Triggering with an event separates the firing logic and pool management logic.
- ELEM-004 (repeat mechanic): Genres with many short repetitive loops, such as roguelike battles,
The performance gain of pooling increases.
- ELEM-031 (Visual Feedback Exaggeration): Implementation premise for this element. Layering particles and effects
The rendering comes back at the frame cost without pooling.
- ELEM-022 (Exponential Score Scaling): The number of simultaneous objects on the screen increases exponentially in the second half.
In a growing design, the pool size estimate becomes a performance upper limit.

