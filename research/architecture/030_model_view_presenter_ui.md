+++
card_id = "ARCH-030"
type = "pattern"
title = "Model-View-Presenter for Game UI"
summary = "A three-part UI architecture that keeps game data and rules independent from Unity UI rendering by making a Presenter mediate all updates and user actions"
tags = ["unity", "ui", "mvp", "mvc", "presenter", "testing"]
updated = "2026-08-13"
confidence = "high"
+++
## Problem
HUDs, inventories, settings screens, and dialogue panels become difficult to test when the same MonoBehaviour stores game state, performs rules, reads buttons, and updates visual widgets. Unity's official MVP guidance notes that this mixed form does not scale well and adds testing and refactoring overhead as features grow. [source: Unity Learn, Build a modular codebase with MVC and MVP programming patterns, Unity 6.0, as of 2026-08-13]

## Structure
- Model: owns application data and the rules governing that data, without knowing the View. [source: Unity Learn, Build a modular codebase with MVC and MVP programming patterns, Unity 6.0, as of 2026-08-13]
- View: owns UI Toolkit or Unity UI elements, displays formatted data, and forwards user input. [source: Unity Learn, Build a modular codebase with MVC and MVP programming patterns, Unity 6.0, as of 2026-08-13]
- Presenter: sits between Model and View, handles View events, changes the Model, receives model-change events, and refreshes the View. [source: Unity Learn, Build a modular codebase with MVC and MVP programming patterns, Unity 6.0, as of 2026-08-13]
- [interpretation] ARCH-012 can hold stable configuration used by the Model, while ARCH-001 can distribute state-change notifications without making the View poll every frame.

## Core Rules
- The Model must not reference Unity UI or UI Toolkit types. [interpretation]
- The View renders and captures input but does not decide game rules. [source: Unity Learn, Build a modular codebase with MVC and MVP programming patterns, Unity 6.0, as of 2026-08-13]
- The Presenter is the only layer allowed to translate between Model data and View representation. [interpretation]
- Subscribe and unsubscribe model and view events at matched lifecycle boundaries. Unity's official sample subscribes during initialization and unsubscribes when the Presenter is destroyed. [source: Unity Learn, Build a modular codebase with MVC and MVP programming patterns, Unity 6.0, as of 2026-08-13]
- Apply the pattern where separation improves testing or maintenance; do not force it onto every small script or renderer. [source: Unity Learn, Build a modular codebase with MVC and MVP programming patterns, Unity 6.0, as of 2026-08-13]

## Unity Implementation Steps
1. Choose one UI feature boundary, such as player health, inventory, settings, or dialogue. [interpretation]
2. Extract its durable state into a Model that can be exercised without rendering a scene. [interpretation]
3. Restrict the View to widget references, display formatting, and user-input events. [interpretation]
4. Add a Presenter that receives View events, invokes Model operations, and refreshes the View after Model changes. [source: Unity Learn, Build a modular codebase with MVC and MVP programming patterns, Unity 6.0, as of 2026-08-13]
5. Bind events at initialization, release them at teardown, and add tests around the Model and Presenter boundary. [source: Unity Learn, Build a modular codebase with MVC and MVP programming patterns, Unity 6.0, as of 2026-08-13]

## Anti-patterns
- Smart View: button handlers modify inventory, health, or save data directly, so visual layout code becomes gameplay authority. [interpretation]
- Passive Presenter: the View still observes and mutates the Model directly while a Presenter exists only in name. [interpretation]
- Mega Presenter: one Presenter coordinates unrelated screens and becomes the new global manager. [interpretation]
- Universal MVP: forcing MeshRenderer behavior or tiny scripts into Model, View, and Presenter layers adds ceremony without a testing benefit; Unity explicitly warns that not every component fits the pattern. [source: Unity Learn, Build a modular codebase with MVC and MVP programming patterns, Unity 6.0, as of 2026-08-13]

## Verification
- Unit test: Model rules and Presenter reactions run without entering Play mode; Unity identifies this as a central testing benefit of MVC and MVP. [source: Unity Learn, Build a modular codebase with MVC and MVP programming patterns, Unity 6.0, as of 2026-08-13]
- Dependency inspection: Model assemblies contain no Unity UI or UI Toolkit references. [interpretation]
- Interaction test: a View event changes the Model through the Presenter, and a Model change refreshes the View exactly once. [interpretation]
- Runtime check: the relevant Unity work has zero compile errors and zero console errors during normal operation. [source: reference/unity_project_baseline_active.md self-check criteria]

## Synergy
- ARCH-001 (Event Bus): the dynamic UI can refresh from notifications instead of polling game state every frame.
- ARCH-012 (ScriptableObject Data): stable configuration belongs in data assets while the MVP Model owns runtime state. [interpretation]
- ELEM-005 (AI Integration): [interpretation] a Presenter can format variable AI output for a View while the AI-facing Model remains independent of UI widgets; ARCH-001 supplies the reaction event stream.
