+++ 
card_id = "ARCH-010"
type = "convention"
title = "Logging Convention (for QA Judgment)"
summary = "An agreement that nails down in advance the format and location of the records the game leaves, so the QA AI can judge pass or fail on observable evidence rather than a human's impression"
tags = ["logging", "convention", "qa", "verification", "observability", "unity"]
updated = "2026-07-29"
confidence = "high" # 프로젝트 기준 구조(reference/unity_project_baseline.md)의 로그 규칙 + QA 판정 체계(reference/qa_verification_policy.md)에서 도출
+++ 
## Problem

How do you confirm that a feature made by an AI works properly? A judgment of "it seems to work" is not a judgment. Especially for features like the AI commentator that produce different results every time, you cannot tell right from wrong by looking at the screen alone. To judge, visible evidence must remain in a fixed place in a fixed shape. Put simply: an exam answer sheet must have a designated box for writing your name in order to be graded. If the box is somewhere different every time, grading itself is impossible.

## Structure

- Baseline format: one line of `[time] [event ID] [reaction summary]` per reaction in `Logs/commentator.log`. [source: reference/unity_project_baseline.md logging rules]
- The format's three pieces — the time (when), the event ID (because of what), the reaction summary (what it did). With these three, a machine can match up the "event → reaction" correspondence.
- The one event = one line principle. Spanning multiple lines breaks parsing, and bundling several events into one line makes the correspondence uncountable.
- The consumer is the QA AI. QA judges by citing log lines as `[observed]` evidence, and anything not confirmed by the log is marked `[presumed]`. [source: the QA reply handling section of reference/unity_project_baseline.md]
- The Unity console log and the file log serve different purposes. The console is what a human looks at during development; the file log is the basis for judgment. Do not mix the two.

## Core Rules

- Do not change the format arbitrarily. Fixing it up to look nicer is also a change, and it breaks QA's judgment tooling. If a change is needed, get human approval.
- Leave a record every time it reacts. To QA, a missing log is indistinguishable from "it did not work". [source: reference/unity_project_baseline.md]
- Unify the time format into one. If different notations mix line by line, chronological sorting and interval calculation become impossible.
- The event ID uses the same value as the event kind in the event bus (ARCH-001). Creating a separate alias for logging makes cross-checking impossible.
- Do not put unnecessary personal information such as people's names or paths, or long raw text, in the log. Leave only summaries.
- Since 0 console errors is the self-check criterion, do not leave error logs on normal paths. If red lines appear when things are normal, you will not be able to find the real problem. [source: reference/unity_project_baseline.md self-check criteria]

## Unity Implementation Steps

1. Gather the log-writing points into one place — if several scripts each write to the file, the format diverges. Have one writing function and have everyone call it.
2. Keep the format string as a constant. If the format is scattered across the code, someday only one place will change.
3. Decide the time notation rule and produce it only inside that function.
4. Fix the file location under `Logs/`. The place QA looks for is itself the convention.
5. Open in append mode so the file is not wiped whole on every game run. But set a rotation rule (a new file when it gets long) so it does not grow indefinitely.
6. Record failures too — abnormal paths such as AI call failures and timeouts must remain in the log so QA can distinguish the cause of "no reaction".
7. Self-check — perform the four kinds of actions (combat, acquisition, conversation, entry) and directly confirm that log lines remain in the format.

## Anti-patterns

- Free-format logs: writing sentences however the developer finds convenient. Humans can read them but machines cannot judge them, so the QA system itself is disabled.
- Output only to the console: only doing Debug output without leaving it in a file. Turn the game off and the evidence disappears.
- Multi-line logs: splitting one reaction across several lines. Line counting and correspondence checks all go out of alignment.
- Unbounded log growth: the problem of appending forever with no rotation rule until the file reaches an unmanageable size.
- Error logs on normal paths: recording common situations as errors makes the "0 console errors" criterion meaningless and buries the real errors.
- Faking logs to pass judgment: leaving a log when nothing actually reacted. This is the most serious violation of verifier independence and loses the trust of the whole judgment system.

## Verification

- Format check: confirm by machine that every line in `Logs/commentator.log` has the three pieces `[time] [event ID] [reaction summary]`. [source: reference/unity_project_baseline.md logging rules]
- Correspondence check: after performing combat, acquisition, conversation, and entry once each, a line for each corresponding event ID must exist.
- Time ordering check: the lines must increase chronologically and the notation format must be identical.
- Location check: logs must be created only in the designated file under `Logs/`.
- Console cleanliness check: 0 console errors during normal play. [source: reference/unity_project_baseline.md self-check criteria]
- Failure recording check: when the AI call is forced to fail, the fact of failure must remain in the log.

## Synergy

- ARCH-007 (Commentator Pipeline): the biggest consumer of this convention. The last stage of that card's three-stage flow is this convention.
- ARCH-008 (Folder and Naming Convention): an agreement-type card of the same nature. What they share is that changes require human approval and that they must be written in a checkable form.
- ARCH-001 (Event Bus): the source of the event ID. Cross-checking only holds if the bus's event kinds and the log's IDs are the same values.
- ELEM-005 (AI Integration): essential compatibility — AI reactions differ every time and are hard to reproduce. Without logs, verification itself is impossible, so this convention is not an accessory to AI features but a precondition.
