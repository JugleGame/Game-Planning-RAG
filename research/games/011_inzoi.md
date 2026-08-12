+++
card_id = "GAME-011"
type = "mixed"
title = "inZOI (2025 얼리액세스, inZOI Studio / KRAFTON)"
summary = "The first major title equipped with AI NPCs—sales success, but a threefold challenge of retention, performance, and public opinion"
genres = ["GENRE-003"]
elements = ["ELEM-005"]
tags = ["life-sim", "ai-native", "aaa", "high-cost", "divisive"]
updated = "2026-07-27"
confidence = "high"              # 판매·지표는 공식 발표 및 보도 집계
+++
## Summary and Sales/Review Metrics
A life simulation highlighted as a rival to The Sims. It sold more than 1,000,000 copies immediately after its early-access launch (2025-03) [source: KRAFTON announcement aggregate, as of 2025-03]. However, concurrent users fell by about 98% within three months, and the initial 86% Steam positive rate declined [source: inZOI game overview aggregate, 2026-02 check]. Reviews rebounded after the release of the free expansion ‘Island Getaway’ (Stardew Valley-style island farming content)—79% positive among 13,768 total reviews and 83% positive among 598 reviews from the last 30 days [source: digest 2026-07-20 / GamesRadar·PCGamesN reporting aggregate, 2026-07 check].

## Elements Used
- ELEM-005 (AI integration) - Smart Zoi: NPCs autonomously generate inner thoughts, schedules, and actions with an NVIDIA ACE-based on-device small language model (approximately 0.5B) [source: NVIDIA/developer announcement, 2025-03].
- ELEM-005 follow-up: In a 2026-07-24 development diary, the developer announced a full redesign of the autonomy system from its decision-making logic rather than a partial fix—aiming for “more convincing simulation,” with the next update scheduled for August. It also previewed improved plausibility in everyday actions, such as putting abandoned food in the refrigerator instead of throwing it away [source: simscommunity.info, 2026-07-24 / digest 2026-07-25].

## Success/Failure Drivers
- Fact: The goal of “NPCs with real emotions rather than repeated scripts” helped drive sales—emergent stories (“the Zoi I was trying to pair up suddenly quit and went backpacking”) became talking points [source: 36Kr user interview quote, 2026-01]
- Fact: Smart Zoi’s performance cost is extreme—even on a top-tier GPU, frame drops were reported (120→45fps), earning it the nickname “GPU killer” [source: 36Kr report, 2026-01]
- Fact: The community pushed back against generative AI use itself, citing concerns about unauthorized training [source: aggregate of community discussions immediately after launch]
- [interpretation] The gap between “AI is present” and “AI makes it fun”—autonomous behavior creates observational interest, but cannot prevent churn if it is not tied to the player’s goals.

## Implications for Our Project
Continue tracking this as a measured case of the cost–performance tradeoff of the on-device small-model approach.
At our scale, concentrating AI on one commentator rather than putting “AI in every NPC” is the performance- and cost-effective answer [interpretation].
