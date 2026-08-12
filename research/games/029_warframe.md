+++
card_id = "GAME-029"
type = "success"
title = "Warframe (2013, Digital Extremes)"
summary = "A free-to-play looter shooter that voluntarily published its entire drop table before regulation forced it to, turning probability transparency into a brand asset"
genres = ["GENRE-011"]
elements = ["ELEM-019"]
tags = ["looter-shooter", "free-to-play", "transparency", "drop-table", "live-service", "long-tail"]
updated = "2026-07-29"
confidence = "medium"
+++
## Summary and Sales/Review Metrics
A free-to-play looter shooter released on PC in 2013, it recorded more than 85,000,000 cumulative registered players as of July 2026
[source: Digital Extremes TennoCon official press release (Business Wire), as of 2026-07-11]. Per the same press release,
it is in its 14th year of service and operates more than 60 playable Warframes, more than 18 planets and 4 open worlds
[source: Digital Extremes press release, as of 2026-07-11].
<!-- Insufficient evidence: revenue figures were only available as estimates for a private company, so they are not carried in this card -->

## Elements Used
- ELEM-019 (Random Loot Drops & Loot Tables) - most acquisition paths, including missions, relics and enemy kills, are
  built on probability tables, and Digital Extremes publishes those tables in full on the official site (warframe.com/droptables)
  [source: WARFRAME Wiki 'Drop Tables' page, verified 2026-07]. This page is auto-generated from the game's internal data
  [source: WARFRAME Wiki, verified 2026-07].

## Success/Failure Drivers
- Fact: In July 2017, Digital Extremes published the drop rate tables for all loot, stated that they were the first developer
  to post this kind of material, and said they wanted to "start a trend" [source: Massively Overpowered,
  as of 2017-07-04]. The company said its intent was to "set a new standard for transparency with the community and show players
  more of the process by which rewards are assigned" [source: PC Gamer / WARFRAME Wiki citation composite, verified 2026-07].
- Fact: The backdrop at the time of publication was that China had passed a law mandating probability disclosure and other publishers
  such as Blizzard had begun disclosing rates [source: search result composite (TechRaptor, PSU and other coverage), verified 2026-07].
- [interpretation] The key point is that they disclosed before regulation reached their own market. Disclosing the same information later under
  compulsion reads as "they were caught and had to disclose," but disclosing first turns it into a brand asset. GAME-025 (MapleStory cubes) is
  exactly the opposite case.
- Fact: That said, the company stated that because of the game's complexity this material is "not complete" and that they do not guarantee its
  accuracy, and that they do not update it with every hotfix in order to avoid revealing items ahead of time [source: WARFRAME Wiki 'Drop
  Tables' page, verified 2026-07].
  Weakness: "we published it" and "it is always current" are not the same thing. The disclosure itself builds trust, but update lag remains a
  seed of distrust.
- Fact: External tools that reprocess the official data into a form the community can parse more easily (WFCD/warframe-drop-data,
  drops.warframestat.us) are being maintained [source: those repositories and sites, verified 2026-07].
- [interpretation] When you publish probabilities, the community layers tools on top of them and builds the information ecosystem for you. In effect
  the community absorbs a maintenance cost the developer would otherwise have to carry itself.

## Implications for Our Project
Publishing probabilities is not a loss but a trust device [interpretation]. However, if you decide to publish, you have to commit to the update
cadence along with it - Warframe also attached the caveat "not complete," and that is the remaining point of distrust [interpretation].
Read this against GAME-025, where hiding probabilities led to sanctions.
