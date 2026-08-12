+++ 
card_id = "ARCH-007"
type = "pattern"
title = "Commentator Pipeline (Subscribe → Generate Reaction → Log)"
summary = "A three-stage processing flow in which the AI commentator listens to game event broadcasts, produces a reaction, and always leaves a one-line log"
tags = ["commentator", "ai", "pipeline", "logging", "core", "unity"]
updated = "2026-08-01"
confidence = "high" # 프로젝트 기준 구조(reference/unity_project_baseline.md)의 방송·로그 규칙 명시 + ELEM-005 근거 카드 존재
+++ 
## Problem

The AI commentator has to know almost everything that happens in the game. If you build that with direct references, the commentator becomes a monster reaching into combat, inventory, conversation, and every world system, and it breaks every time one system is fixed. Also, AI reactions differ every time, so there is no way to confirm whether it "worked properly". Put simply: a baseball announcer does not go down to the field and grab players. They only watch and speak from the stands, and what they said remains in the broadcast record. This card is that stand and that broadcast record.

## Structure

- Location: `Assets/Scripts/Commentator/` — EventBus subscription → reaction generation → reaction log recording. [source: reference/unity_project_baseline.md baseline structure]
- Three-stage flow — (1) subscribe: receive events from the event bus, (2) judge and generate: decide whether to react and produce the reaction, (3) record: leave one log line. Each stage knows only the previous stage, not the next.
- The input is only event bus broadcasts. The commentator system depends solely on these broadcasts. Direct references are forbidden. [source: reference/unity_project_baseline.md broadcast rules]
- The output format is fixed — one line of `[time] [event ID] [reaction summary]` in `Logs/commentator.log`. [source: reference/unity_project_baseline.md logging rules]
- If reaction generation is an external AI call, it takes time. Therefore the request is asynchronous, and the game does not stop in the meantime. [interpretation] Response delay and failure must be treated as normal paths, and this is the same problem as the fragility ELEM-005 points out.

## Core Rules

- There is only one input path, the event bus. If even one piece of code reads another system's fields directly, that is a rule violation. [source: reference/unity_project_baseline.md]
- Leave a log every time it reacts. Logs are not optional; they are QA's basis for judgment. [source: reference/unity_project_baseline.md logging rules]
- Even when it decides not to react, it is better to record the judgment itself. [interpretation] If there is no way to tell whether silence is a bug or intentional, QA cannot make a judgment.
- The commentator does not change game state. It only reads and speaks. The moment it changes state it becomes game logic, and you can no longer verify that the game runs with it removed.
- An AI call failure does not stop the game. Even on failure the game continues, and the fact of failure remains in the log.

## Unity Implementation Steps

1. Create `Scripts/Commentator/CommentatorService.cs` — subscribe to the event bus in OnEnable and unsubscribe in OnDisable.
2. Implement a filter — reacting to every event is noisy and expensive. Set rules for which event kinds to react to and a minimum interval (cooldown).
3. Separate reaction generation — extract the generation part into a separate class so it can be swapped. Early on, returning pre-written sentences is enough to validate the pipeline.
4. Asynchronous handling — let the game proceed normally during a request, and decide how to handle the case where the situation has already passed by the time the response arrives (whether to discard a late reaction or speak it).
5. Implement log recording — append to `Logs/commentator.log` in the fixed one-line format. The format is read by QA machinery, so arbitrary changes are forbidden.
6. Failure handling — on call failure or timeout, leave only a failure log without affecting game progress.
7. Verify removability — take the commentator object out of the scene, run the game, and check that there are no errors.

## Anti-patterns

- Collecting direct references: the commentator grabbing PlayerController or the inventory directly. This is a rule violation, and the reference breaks and blows up on chunk unload.
- Reacting to every event: with no filter, reacting to everything fills the log with noise and the cost becomes unmanageable. First decide what **not** to react to.
- Synchronous waiting: stopping the game while waiting for the AI response. To the player the game looks frozen.
- Altering the log format: fixing it up to look nicer. QA parses it by machine, so if the format changes, judgment itself becomes impossible.
- The commentator intervening in the game: giving rewards or summoning enemies while reacting. Once the observer becomes a participant, the removal check is meaningless.
- Missing unsubscription: the problem where the subscription remains after a scene transition and a ghost commentator reacts twice.

## Verification

- 0 compile errors, 0 console errors. [source: reference/unity_project_baseline.md self-check criteria]
- Log format check: every line in `Logs/commentator.log` must be in the `[time] [event ID] [reaction summary]` format. [source: reference/unity_project_baseline.md logging rules]
- Event-to-log correspondence check: performing combat, acquisition, conversation, and entry once each must leave a corresponding log line (kinds excluded by the filter must have the exclusion reason stated).
- Independence check: even with the commentator object removed, the main game must run without errors. Failing means there is a direct reference or game intervention somewhere.
- Failure tolerance check: when the AI call is forced to fail, the game must keep running and a failure log must remain.
- Noise check: after playing for a set period, check that the number of log lines matches the cooldown rule.

## Synergy

- ARCH-001 (Event Bus): the only input path. Without the bus this pipeline does not hold.
- ARCH-010 (Logging Convention): the owner of the output format. Format changes happen only in that card.
- ELEM-005 (AI Integration): the design element this pipeline is trying to implement. The cost and fragility that card points out are exactly this structure's risks.
- ELEM-003 (Fourth Wall Break): good compatibility — it connects naturally with staging where the commentator speaks directly to the player.
- ELEM-041 (AI Observer/Commentator Combination): this pipeline is itself the "implementation bridge" that card demands — the subscribe → generate reaction → log flow is the ELEM-002+003+005 combination moved into code.
- Conflict caution — the tone may clash with immersive, commentary-free staging (such as exploration guided only by landmarks). Adjusting reaction frequency is itself adjusting tone.
