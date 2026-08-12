+++
card_id = "GAME-027"
type = "mixed"
title = "Rogue Tower (2022, Die of Death Games)"
summary = "An indie title combining roguelike and tower defense through random branching paths and a draft of more than 400 cards"
genres = ["GENRE-010"]
elements = ["ELEM-018"]
tags = ["tower-defense", "roguelike", "randomness", "indie", "divisive"]
updated = "2026-07-29"
confidence = "medium"
+++
## Summary and Sales/Review Metrics
Released on Steam by Die of Death Games on 2022-01-28 [source: aggregate search results (store·guide sites),
2026-07 check]. 80% positive among 4,356 Steam user reviews [source: review aggregation site, 2026-07 check].

## Elements Used
- ELEM-018 (roguelike random upgrade/path draft) - Each round randomly draws from a card pool of more than 400 to build or upgrade towers, while branching paths also expand randomly [source: aggregate search results,
  2026-07 check].

## Success/Failure Drivers
- Fact: 80% positive among 4,356 reviews [source: review aggregation site, 2026-07 check]. Some evaluations say its 20–30 minute run length is short and suited to repeated play [source: aggregate review results, 2026-07 check].
- [interpretation] Short runs and a draft that changes each game appear to create replayability.
- Fact: Some users complained that random paths with the next tile hidden let randomness determine outcomes too strongly, making it feel like “an unfair gamble” [source: aggregate Steam user reviews, 2026-07 check].
  Failure point: when randomness feels more influential than skill, it turns into backlash calling it a “luck game.”

## Implications for Our Project
When using random drafts and paths, failing to specify a lower bound (“at least this much is guaranteed”) makes controversy over unfairness like ELEM-018 likely [interpretation]. ELEM-017’s pity concept is worth consulting.
There are alternatives to a pity system that changes the probabilities themselves—GAME-030 (Slay the Spire) eliminated “blame luck” controversy through a daily mode in which all players share the seed generated for each game [source: Slay the Spire Wiki 'Daily
Climb' document, 2026-07 check]. [interpretation] This may be lighter to implement because it does not require redesigning probability balance.
