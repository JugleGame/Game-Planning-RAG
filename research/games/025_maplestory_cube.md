+++
card_id = "GAME-025"
type = "mixed"
title = "MapleStory - Cube Probability Manipulation Case (2003 launch, Nexon / 2024 KFTC sanction)"
summary = "A collapse of probability trust in which the odds of the probability-based enhancement item 'Cube' were secretly lowered and undisclosed, resulting in the largest fine on record"
genres = []
elements = ["ELEM-017"]
tags = ["probability-item", "mmorpg", "regulation", "trust-failure", "korea", "cautionary"]
updated = "2026-07-28"
confidence = "medium"
+++
## Summary and Sales/Review Metrics
Nexon’s 2D side-scrolling MMORPG launched on 2003-04-29 [source: Wikipedia, 2026-07 check]. Manipulation of the probability-based enhancement item 'Cube' was revealed, and in January 2024 the Korea Fair Trade Commission imposed a corrective order and a fine of 11,600,000,000 + 42,000,000 won—the largest amount ever reported in Korea’s game industry [source: Korea Fair Trade Commission sanction announcement report, as of 2024-01].

## Elements Used
- ELEM-017 (gacha probability & pity system) - It uses the same element in a variant form: not character-drawing gacha, but a probability-based enhancement item (Cube) that randomly rerolls the options of an equipped item [interpretation].

## Success/Failure Drivers
- Fact: The KFTC determined that Nexon adjusted Cube probabilities from 2010, changed them from 2011 so user-preferred duplicate options would appear less often, and gradually lowered the tier-up probability of the Black Cube launched in 2013 [source: Korea Fair Trade Commission sanction announcement report, as of 2024-01].
- Fact: It did not disclose that the probabilities had changed; instead, it misled users with notices implying “no functional changes,” which was included among the reasons for the sanction [source: Korea Fair Trade Commission sanction announcement report, as of 2024-01].
- [interpretation] The core trust-breaking point appears to have been discovering that “the company can secretly change it,” rather than the probability figures themselves.
<!-- 증거 부족: 사건 이후 매출/리텐션 변화를 보여주는 공식 수치를 찾지 못함 -->

## Implications for Our Project
Do not build a structure that allows probabilities to be quietly changed afterward; hard-code a procedure requiring disclosure whenever they change [interpretation]. After this case, South Korea made disclosure of probability information for probability-based items mandatory through an amendment to the Game Industry Act [source: Game Industry Act amendment, effective March 2024].
