+++
card_id = "ARCH-017"
type = "structure"
title = "Audio Manager (AudioSource Pool + BGM/SFX Separation)"
summary = "A structure that does not create a new AudioSource every time a sound plays, but instead manages a dedicated BGM channel and an SFX pool separately in advance, so that overlapping sound effects are not cut off"
tags = ["audio", "sfx", "bgm", "pooling", "singleton", "unity"]
updated = "2026-07-31"
confidence = "medium"
+++
## Problem
Sound effects must be played overlapping several times within a short span (rapid-fire
attack sounds, etc.). If a single object holds only one `AudioSource` and calls `Play()`
again each time, the previous sound is cut off; conversely, creating and destroying a new
`AudioSource` for every sound reproduces exactly the same creation/destruction cost problem
that ARCH-015 deals with. Background music (BGM) and sound effects (SFX) differ in their very
playback style (BGM is one at a time, looping, faded / SFX is many at once, one-shot)
[source: GitHub perezromeojohn/unity-audiomanager, object pooling based audio manager,
https://github.com/perezromeojohn/unity-audiomanager].

## Structure
- A single global manager placed in this project's `Core/` is the sole entry point for audio
  playback — individual scripts do not call `Play()` on their own `AudioSource` directly.
- Hold 1–2 `AudioSource`s for BGM (2 if crossfading is needed) separately from a pool of
  `AudioSource`s for SFX (reusing the ARCH-015 object pooling structure) — because one must
  satisfy "only ever one playing" while the other must satisfy the different requirement of
  "many can play simultaneously" [source: Medium, Gaetano Tonzuso, Unity: How to make an
  AudioManager, https://medium.com/@gaetano.tonzuso/unity-how-to-make-an-audiomanager-07d059f4e894].
- Global settings such as volume and mute are exposed as `AudioMixer` exposed parameters, so
  that BGM and SFX can each be adjusted separately.

## Core Rules
- Playback requests must go through the manager — request a clip by name/ID as in
  `AudioManager.PlaySfx(clipId)`, and hide which `AudioSource` actually plays it inside the
  manager's implementation.
- BGM often must not be cut off even when the scene changes, so per the ARCH-011 Boot
  bootstrap rule it is placed as a `DontDestroyOnLoad` manager.
- An SFX pool `AudioSource` must be returned to the pool automatically once playback ends
  (after the clip length has elapsed) — automate this with a coroutine or timer so that
  manual returns are never forgotten.

## Unity Implementation Steps
1. Create `Core/AudioManager` and, per the ARCH-011 bootstrap rule, instantiate it in the Boot
   scene and keep it alive with `DontDestroyOnLoad`.
2. Place a BGM playback `AudioSource` (loop=true) and an SFX `AudioSource` pool (the ObjectPool
   structure of ARCH-015) under the manager.
3. Do not hardcode clips as direct references in code; follow the ScriptableObject data
   convention of ARCH-012 and hold them as a "sound ID → AudioClip" table — swapping sounds
   then becomes possible without code changes.
4. Expose only a small number of public methods such as `PlaySfx(id)`, `PlayBgm(id)`, and
   `StopBgm()` to the outside. Consumers subscribe to the event bus (ARCH-001) and wire up
   "this sound for this event" playback.
5. Verify that an SFX `AudioSource` is returned to the pool once playback ends, and that the
   previous clip stops when BGM switches.

## Anti-patterns
- Attaching an `AudioSource` to every script that needs to make a sound and playing directly —
  global volume control, muting, and simultaneous-playback limits all become impossible.
- Creating a new SFX `AudioSource` each time with `AddComponent`/`Destroy` — the shorter and
  more frequent the sound effect, the more this cost accumulates.
- Taking the BGM playback `AudioSource` from the same pool as SFX — this leads to an accident
  where the background music cuts off the moment it is returned to the pool.

## Verification
- Check that when the same sound effect is played repeatedly at short intervals the sounds are
  heard overlapping and are not cut off — simultaneous SFX playback is the core pass criterion
  of this structure.
- Observe whether BGM is not cut off on scene transition (or fades across as defined in the
  spec).
- 0 console errors, in particular 0 warnings about the pool being empty and continuously
  creating new `AudioSource`s (a signal of insufficient pool size).

## Synergy
- ARCH-015 (Object Pooling): the base structure for the SFX `AudioSource` pool. Reuse it as is
  rather than designing a new one separately.
- ARCH-001 (Event Bus): the connection point for hanging sounds on game events such as combat,
  pickups, and dialogue. Ties playback logic and game logic together without direct references.
