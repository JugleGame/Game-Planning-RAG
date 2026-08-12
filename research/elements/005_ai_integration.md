+++
card_id = "ELEM-005"
type = "tech"
title = "AI Integration" # Typo correction: integration → Integration
summary = "Technology where AI sees the player's words and actions and generates a response on the spot"
tags = ["requires-ai", "high-cost", "viral-hook", "fragile", "divisive"]
updated = "2026-07-31"
confidence = "medium"            # 사유: 시장 초기 단계 - 순수 성공 사례 부재, 신호 변동 큼. 분기별 재평가.
+++
## Definition
A game character's dialogue is usually a pre-written script. However, if you use this technique
Without a script, the character sees what the player just said and did and acts on the spot.
generates an answer. As if talking to a real person, not a recorded announcement.
There is a different reaction every time.

## Success Cases
- GAME-010 (Suck Up!) - A game where you become a vampire and trick AI residents into their houses. The experience of “persuading with my real voice” spread to streamer content, proving for the first time that AI can be a core mechanic (2023~24 viral).
- GAME-011 (inZOI) - NVIDIA ACE-based on-device small language model that generates internal thoughts, schedules, and actions of NPCs (Smart Zoi). Sold over 1,000,000 copies since early access launch - first commercial success of a large title with AI NPC [source: inZOI game overview/KRAFTON announcement, based on 2025-03].

## Failure Cases
- GAME-010 (Suck Up!) - Failed to maintain after gaining popularity. Steam official release rating "Mixed", 60% positive out of 189. Core complaints: "AI's unique repetitive speech style even with good prompts", hallucinations (creating unreasonable situations that can be resolved only with agreement), bugs [source: Steam store/review, 2026-07 confirmed].
- GAME-011 (inZOI) - Simultaneous connections decreased by approximately 98% within 3 months of launch, and the positive rate decreased from the initial 86%. Smart Zoi is nicknamed the "GPU killer" due to its frame rate plummets (120→45fps reported) even on top-end GPUs [source: inZOI Game Overview / 36Kr reports, 2026-01].
Failure point: Creates initial buzz, but repetition, hallucination, and performance costs destroy retention. The current state of this factor is that the same game has both success and failure.

## User Reaction Summary
- Preferred: "It's really funny to deceive NPCs with words" - The power of creating moments for broadcasts and clips [source: GAME-010 Store quote Creator reaction and YouTube play video, 2023-12]
- Preferred: NPC's unexpected behavior becomes a topic of conversation - Emergent narrative of the "Zoi, whom I was trying to mate with, suddenly quit the company and went on a backpacking trip" type [source: 36Kr user interview quote, 2026-01]
- Dislike: “AI speech patterns are all the same”, hallucinations, delayed reactions, frame drops [source: GAME-010 Steam review 2025-12 / GAME-011 related reports]
- Dislike: Community backlash against the use of generative AI itself - Controversy over concerns about unauthorized learning [source: GAME-011 Community discussion record immediately after release]

## Synergy
- Good: ELEM-003 (Z4 Wall Collapse) - Real-time response makes Force Wall's "1 replay limit" repeatable. Risk-relieving combination of ELEM-003 cards.
- Good: ELEM-002 (campy) - AI's awkward speech and unexpected behavior are absorbed as a joke rather than a defect in the campy tone [interpretation]
- Good[interpretation]: ELEM-004 (repeat mechanic) - A combination of AI mentioning the player's past loops in real time. No launch cases - GENRE-001 Same point as the blank hypothesis.
- Note: Always compared to script-based personality - Community rates AI commentary based on scripted narrator from GAME-013 (The Stanley Parable) [interpretation]
- Contrast: ELEM-007 (Optional Responsive Non-LLM Narrative) - An alternative that achieves the same goal as a script. Since GAME-041 shows that top-tier performance can be achieved without an LLM, AI integration is justified by first answering “what can’t be scripted?” [interpretation]
- Sub-branch: ELEM-006 (AI-based interrogation) / ELEM-025 (On-device SLM real-time voice conversation NPC) - Each is a version specialized for the purpose of this element (interrogation) and a version specialized for the delivery method (voice/on-device). When the three are used together, the risks are not combined but multiplied [interpretation].
- Genre anchor: GENRE-003 (AI native game) - This cluster points to this element as a component.

## Risks
- Fact: Server costs are incurred for each NPC conversation - GAME-010 has a structure that consumes AI tokens per 1 conversation [source: The Magic Rain reports, 2024-04]. Operating expenses continue to accrue even after the sale.
- [interpretation] “AI is included” itself is not a selling point - the characters should be fun and AI is a means. Personality created through script + gap in response filled by AI is a winning formula.
- [interpretation] The lower limit of quality is low - The worst of the script is “flat,” but the worst of the AI ​​is “hallucinations and nonsense,” so the damage to immersion is high.
- [interpretation] Risk of anti-AI public opinion - Controversy over generated AI may transfer to the evaluation of the game itself (GAME-011 case).
- Fact: Technical perfection and actual gameplay fun are two separate things - Skyrim AI NPC mod
After overwhelming positive reviews at the beginning of its release, interest waned as “What can I do now?”, 2 years later.
Only topical videos remain and actual use has almost disappeared [source: Digest 2026-07-20 /
Frisson Labs blog, 2026-05-21].
- [interpretation] NVIDIA ACE-based real-time voice NPC is spreading beyond demos to actual release builds.
More and more studios are adopting [source: NVIDIA GeForce News/PCGamer confirms 2026-07 /
Digest 2026-07-27] - As the infrastructure matures, “the fact that AI has entered
The existing risk that “it is not a selling point” is expected to be put to the test sooner.
- Fact: The proportion of new works displayed as AI disclosures increased from 2024-01 10.9% → 19.9% in 2025 to about 30% in the first half of 2026, and the number of new works displayed monthly also increased from about 13 to about 530 [source: Steam AI disclosure data Analysis (Substack "Three years of AI on Steam" requote report), based on the first half of 2026 / digest 2026-07-14 (reinvestigation 2026-07-27)]. As [interpretation] disclosure itself becomes more common, the power of “AI-equipped” as a differentiating factor may weaken, and the core risk of ELEM-005 (“AI-included itself is not a selling point”) is expected to become more significant over time.


