+++
card_id = "GENRE-003"
type = "genre"
title = "AI-native Games"
summary = "An early-forming cluster in which real-time AI generation is the game's core mechanic"
elements = ["ELEM-005"]
example_games = ["GAME-010", "GAME-011"]
tags = ["ai-native", "emerging", "fragile", "high-cost"]
updated = "2026-08-01"
confidence = "medium"            # 군집 자체가 형성 초기 - 신호 변동 큼, 주간 추적 필수
+++
## Components
- ELEM-005 (AI integration) - the very definition of the cluster. Works that do not hold together if you remove the AI.

## Market Saturation
Extremely early. Meaningful cases are at the level of GAME-010 (Suck Up! - Mixed 60% after going viral) and GAME-011
(inZOI - 98% drop in concurrent players after 1,000,000 units), and both are mixed - **there is still no
pure success** [source: each GAME card]. Platform-level infrastructure build-out is underway (spread of on-device models such as NVIDIA ACE
) [source: NVIDIA announcement, 2025-03]. Competitive density is low and
the entry opportunity is large, but works that fail to hold the quality floor are being weeded out first. On Steam,
games disclosing AI content surged to roughly 7,300 to 9,400 (as of 2026-03), yet among these
the genuinely AI-native games that use inZOI-style "real-time AI generation aimed at the player" as a core mechanic
are reported to be extremely few [source: digest 2026-07-20 /
Tom's Hardware / SteamDB tally, as of 2026-03] - suggesting that the gap between tag proliferation and actual core-mechanic
adoption is being maintained [interpretation].
NVIDIA ACE (a combination of speech recognition + the small language model Nemotron + neural TTS + Audio2Face) has begun to ship in actual release builds beyond the demo stage in inZOI, NARAKA: BLADEPOINT and others, and multiple studios including Krafton and Creative Assembly are adopting it [source: NVIDIA GeForce News/PCGamer, verified 2026-07 / digest 2026-07-27]. [interpretation] A signal that the existing description "platform-level infrastructure build-out underway" is becoming one step more concrete, moving from demo to actual release.
The share of new releases carrying an AI disclosure label rose from 10.9% in the early period after disclosure became mandatory in 2024-01, to 19.9% at the same point in 2025, to about 30% in the first half of 2026 - and the release frequency of labeled new titles also grew from about 13 per month before the mandate to about 530 per month [source: Steam AI disclosure data analysis (coverage re-citing the Substack "Three years of AI on Steam"), as of the first half of 2026 / digest 2026-07-14 (re-investigated 2026-07-27)]. [interpretation] Tag adoption itself keeps accelerating, so whether the gap with actual core-mechanic adoption narrows needs continued tracking in the next digest.
## Conventions and Expectations
- Conventions are still forming - only the minimum line of user expectation is confirmed: response without delay, memory retention (not forgetting prior conversations and actions), and speech that does not smell of AI [source: GAME-010 review complaints / GAME-011 coverage]
- Comparison with script-based masterpieces is the default - "not bad for an AI" is no indulgence [interpretation]
- Antipathy toward generative AI exists as a constant - the mere fact of using it can become a controversy [source: GAME-011 community controversy]
- A signal confirmed that stability and fundamentals (completeness of the core simulation) are being absorbed as a new expectation -
  when inZOI shifted to a 'Fundamentals First' stance prioritizing stabilization over expanding new features,
  the community reaction changed from criticism that it was "empty" to support for the direction
  [source: digest 2026-07-20 / inZOI official roadmap notice, as of 2026-07-04]

## Gaps
[interpretation] ★ In existing cases the AI plays only two roles: "target of persuasion" (GAME-010 - the player
talks to the AI) or "autonomous simulation" (GAME-011 - AIs live among themselves). The third
role, "observer/commentator" (the AI watches the player's play and speaks to them), is unoccupied in game
form - the aiming point of our project. The stage on which the ELEM-002+003+005 combination is executed is this cluster.
The card that synthesizes this combination itself is ELEM-041 (AI observer/commentator combination).
- Verification method: full check of new releases under the Steam 'Artificial Intelligence' tag + AI game showcase coverage
- Verified on: 2026-07-15 / Re-check cycle: biweekly (a forming cluster changes fastest)
