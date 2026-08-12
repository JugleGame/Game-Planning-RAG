# QA Verification Policy — Active ARCH Citation Guide

This is the English citation source for new ARCH cards' `Verification` sections. It extracts
the RAG-relevant policy from `qa_verification_policy.md`, which remains the Korean archival
original. It is not an instruction to operate a QA pipeline in this repository.

Use only observable evidence. A verification claim is valid when it can be checked through one
of these means:

1. Unity compile or console output.
2. Unity Test Framework EditMode or PlayMode tests.
3. Scene, object, component, or folder-structure inspection.
4. System logs such as `Logs/commentator.log`.

If none of those means can verify a criterion, mark the criterion `BLOCKED` and leave the
decision to a human. Do not turn an unmeasurable quality claim into a pass or fail claim.

For nondeterministic output, verify observable behaviour rather than subjective content:

- Did the system react?
- Did it react within the stated time limit?
- Did it react to the expected event?

When writing a verification rule, state the evidence location: a console line, test name, scene
inspection result, or log line. Keep observed facts separate from interpretation.

## Provenance

Derived from the Korean archival source `qa_verification_policy.md`. If historical wording or
a disputed interpretation matters, a human reviewer may compare the archive; English-only
authoring agents do not load the archive during normal work.
