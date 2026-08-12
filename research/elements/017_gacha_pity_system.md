+++
card_id = "ELEM-017"
type = "mechanic"
title = "Gacha Probability & Pity System"
summary = "A dual device that makes players draw characters/items by probability while guaranteeing the desired outcome once a set number of draws is exceeded"
tags = ["gacha", "monetization", "randomness", "live-service", "mobile", "regulation", "divisive"]
updated = "2026-08-01"
confidence = "high"
+++
## Definition
Gacha is a method where you pay money and randomly draw a character or item. It is similar to putting a coin into a capsule machine.
If your luck is bad, the thing you want may keep failing to appear, and then you would be angry that "I only spent money and got nothing."
So many games put in a safety device called a "pity." For example, it is a promise that if you have drawn 90 times and the thing you want still has not appeared,
the 90th draw will give it to you unconditionally. This way it is not left entirely to luck, and it can give the belief that no matter how unlucky you are,
you will definitely receive it within at most a certain number of draws.

## Success Cases
- GAME-024 (Genshin Impact) - Built the trust that "even if you are unlucky, you will get it in the end" by combining a hard pity that guarantees a 5-star once you fill 90 draws with
  a soft pity where the rate rises sharply from draw 74 [source: composite of gacha guides such as BitTopup/Game8,
  verified 2026-07]. On the basis of that trust, it passed $10,000,000,000 in cumulative revenue as of the end of 2025,
  setting that record faster than any mobile game in history [source: STG Research (Shane The Gamer) tally, as of the end of
  2025].
- GAME-046 (Wuthering Waves) - Combined pity with character/weapon banner rotation and recorded
  a review score of 88/100 (52,627 reviews, Very Positive) after entering Steam [source: Steambase, verified 2026-07].
- GAME-047 (Zenless Zone Zero) - With the same style of banner rotation, recorded a review score of
  87/100 (8,194 reviews, Very Positive) immediately after its Steam release [source: Steambase, verified 2026-07].
- GAME-048 (NIKKE) - With the same style of character banners, recorded 1st place in mobile subculture revenue for 3 consecutive
  months [source: Gamers Scroll ranking coverage, as of 2026-05]. However, this revenue success is limited to mobile and
  was not repeated on the Steam version (see the GAME-048 card).

## Failure Cases
- GAME-025 (MapleStory) - The company secretly lowered the tier-up probability of the probabilistic enhancement item "Cube" and did not
  disclose it, and was fined 11,600,000,000 + 42,000,000 KRW by the Fair Trade Commission in January 2024 [source: reporting on the Fair Trade Commission
  sanction announcement, as of 2024-01].
  Failure point: it changed the probabilities without notifying users and posted a notice to the effect of "no change," which spread into
  a collapse of trust with claims that "the rates were manipulated."

## User Reaction Summary
- Liked: the certainty that "it will definitely come out within 90 draws" - the reassurance that the "maximum loss" is fixed rather than
  it being complete unlimited gambling [source: composite of community explanations in Genshin Impact gacha guides, verified 2026-07]
- Disliked: the suspicion that "the company can change the probabilities at will, in secret" - the distrust that the published rates and
  the actual rates may differ [source: reporting on the MapleStory Cube probability manipulation case, as of 2024-01]

## Synergy
- Genre anchor: GENRE-025 (Subculture Games) - this cluster names this element as a constituent.
- Good: ELEM-004 (Repetition Mechanic) - challenging the probability again each time itself becomes the reward cycle of the repetition loop
- Good: ELEM-019 (Random Loot Drop & Loot Table) - [interpretation] both are probabilistic rewards, but gacha has an upper bound (pity)
  that loot drops usually lack. The complaint GAME-028 (Destiny 2) faced of "running 978 matches and still
  not getting the target" has room to be reduced by layering the pity concept onto loot drops
- Conflict: ELEM-022 (Exponential Score Scaling) - [interpretation] pity is a device that promises a predictable
  upper bound of "definitely within at most N draws," whereas exponential scaling is by nature something whose upper bound even the designer does not know, so mixing them in the same
  system means one side keeps breaking the other's promise
- Conflict: GENRE-007 (Cozy Sim) - [interpretation] a low-stress design with no failure state and gacha, where loss can occur
  by probability, collide head-on in the tone of tension

## Risks
- [interpretation] Changing probabilities without disclosure can lead to legal sanctions and a collapse of trust as in GAME-025 - after this case, Korea
  made disclosure of probability information for probabilistic items mandatory through an amendment to the Game Industry Act [source: Game Industry Act amendment,
  effective March 2024]. In contrast, GAME-029 (Warframe) voluntarily published its entire drop table in July 2017, before
  regulation compelled it, as a case of turning trust into a brand [source: Massively Overpowered, as of 2017-07-04
  ], showing that hiding probabilities and being caught versus opening them first produce opposite outcomes [interpretation].
- [interpretation] If the pity count is designed excessively long, it becomes effectively unreachable for low-spending users, so there is a risk of the safety device being perceived not as a safety device but as
  "pure gambling in practice."
