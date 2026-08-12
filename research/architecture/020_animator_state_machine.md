+++
card_id = "ARCH-020"
type = "pattern"
title = "Animation State Machine (Animator Controller / Animation State Machine)"
summary = "A structure where a character's animation clips are not played directly from code, but delegated to a graph laid out in advance from States and Transitions, so that changing only a parameter automatically leads into the appropriate motion"
tags = ["animation", "animator", "state-machine", "unity", "pattern", "player"]
updated = "2026-07-31"
confidence = "high"
+++
## Problem
When a character moves between several motions such as Idle, Walk, Attack, and Hit, directly
specifying "play this animation now" from code every time scatters the state transition
conditions all over the scripts, and makes it hard to see at a glance which state can go to
which. It is a problem similar to ARCH-005 (NPC state machine), but this one is specialized to
"playing the animation visible on screen" rather than "behavior logic".

## Structure
- Baseline form: Unity's Animator Controller is a graph made of States (one animation clip
  each) and Transitions (conditions for moving between states) [source: Unity official manual,
  Animation state machine, docs.unity3d.com, as of Unity 6].
- Parameters (Bool/Trigger/Float/Int) are the sole contact point between the script and the
  graph - code changes only parameter values, and the graph decides which animation actually
  plays [source: Unity official manual, Animation Parameters, as of Unity 6].
- A Transition with no conditions fires on Exit Time (playback progress) alone; with
  conditions, it fires only when all conditions are met [source: Unity official manual, State
  Machine Transitions].

## Core Rules
- Scripts do not handle state names directly, only manipulate Parameters - hardcoding state
  names in code means the scripts must be fixed every time the animator graph structure
  changes.
- Design on the premise that a Trigger parameter auto-resets once consumed - confusing it with
  Bool produces "I pressed it but it got eaten" bugs.
- If transition conditions overlap (several conditions met at once), unexpected transitions can
  occur depending on graph order, so design with mutually exclusive conditions.

## Unity Implementation Steps
1. Fix the character's state list (Idle/Walk/Attack/Hit/Die, etc.) in the spec first.
2. Create a State per state in the Animator Controller and connect an animation clip to each State.
3. Connect Transitions between states in the graph, and put Parameter conditions on each Transition.
4. In scripts, update only the parameters with `Animator.SetBool`/`SetTrigger`/`SetFloat`.
5. Do not force the behavior states of ARCH-005 (NPC state machine) and the animation states
   into 1:1 correspondence - even when the behavior is "Patrol" the animation can move between
   "Walk"/"Idle", so design the two layers separately.

## Anti-patterns
- Calling state names directly from scripts with `Animator.Play("StateName")`: it ignores the
  graph's transition conditions and forces a transition, which can conflict with other Transitions.
- Putting too many conditional branches into one State so the graph grows huge: splitting into
  Sub-State Machines is the standard practice.
- Leaving a Bool parameter unreset: it jumps to an unintended state on the next transition.

## Verification
- State transition check: perform each state combination (Idle→Walk, Walk→Attack, etc.) once
  and confirm the intended animation plays.
- Console cleanliness: warnings raised when calling `SetTrigger` etc. with a nonexistent
  parameter must be 0 during normal play.
- Regression check: after modifying the animator graph, re-confirm that previously working
  transitions still work (by the nature of graphs, one edit can affect other transitions).

## Synergy
- ARCH-005 (NPC state machine): acts as the bridge connecting behavior logic and animation
  playback as two separated layers.
- ELEM-031 (Exaggerated visual feedback): layering particles and screen shake at the moment of
  an animation transition doubles the responsiveness.
