+++
card_id = "ELEM-006"
type = "tech"
title = "AI-driven interrogation"
summary = "Rather than pre-written lines, real-time generated AI moves the characters to instantly answer the player's questions."
tags = ["AI", "dialogue", "local-llm", "divisive"]
updated = "2026-07-16"
confidence = "medium-low"   # 조합 궁합 근거 없음 + AI Interrogation Simulator는 미출시로 유저 반응 근거 없음
+++
## Definition
This is a method in which artificial intelligence (AI) moves the characters in the game in real time, making them answer differently depending on what the player asks. Rather than using predetermined lines, AI generates answers on the spot. There are several separate games that use this method, and this card was created based on the two most identified games (Verbal Verdict, AI Interrogation Simulator) [[source: Steam store page].

## Success Cases
- Verbal Verdic - It was created to operate as a local (offline) LLM, and the developer explains that this is for the purpose of protecting player privacy and allowing the game to continue to be enjoyed even if the server is closed in the future. [source: Beehaw (404 Media re-post/discussion)]. One review called the game one of the best implementations of generative AI [[source: 404 Media]. There was a response from the community that it would be a must-buy game when it is officially released, citing the fact that local LLM works right away without any additional settings [[Steam Community].
- An industry report describes Verbal Verdict as one of the earliest examples of real-time, on-device (local) LLM conversations at the commercial stage [[source: Hartmann Capital Q3 2025 report].

## Failure Cases
- Verbal Verdict - The AI-generated lines sometimes produced gibberish results, and each character's voice was also similar to that of L.A. [[source: 404 Media]. In a later update, it was changed to require a monthly subscription fee to hear the character's voice, and complaints about the interaction controls (UI) were also raised [[source: Steam Community]. As of the time of the investigation, the last developer update has not been made in over 2 years, so the aforementioned roadmap or schedule may have already changed [[source: Steam].
- AI Interrogation Simulator - As of the time of the investigation, it has not been released yet and has no user reviews as "Coming soon" [source: Steam store page]. To run the game, players must directly connect their AI account (choose from OpenAI, Anthropic, or local model) [source: Steam (developer description)]. This can act as a barrier to entry [interpretation].

※ Verbal Verdict is classified as a mixed case because both success and failure grounds are confirmed. [interpretation].

## User Reaction Summary
- Preferred: Local LLM works right away without any additional settings. This is a must-buy game when it is officially released. [source: Steam Community]
- Preferred: Evaluation of the most impressive implementation of generative AI conversation [source: 404 Media]
- Dislike: AI dialogue is sometimes jumbled, character voices are dull [source: 404 Media]
- Dislike: There is a monthly subscription fee to listen to audio, the operation (UI) is inconvenient [source: Steam Community]

## Synergy
<!-- No evidence: JSON 근거 자료에 ELEM-006과 다른 요소 간의 조합 관련 서술이 없음 -->

## Risks
- [interpretation] Real-time generated AI dialogue is unpredictable, so there is a risk of it going in a different direction from the tone or intention of the game (based on the mixed case of Verbal Verdict).
- [interpretation] The structure that requires an external AI account increases the barrier to entry, and if the service is discontinued, there is a risk of making the game itself unplayable (AI Interrogation Simulator case).
- The introduction of additional monetization (monthly subscription fee) may lead to user dissatisfaction [[source: Steam Community].

