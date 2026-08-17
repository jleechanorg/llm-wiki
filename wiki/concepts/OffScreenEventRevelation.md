---
title: "Off-Screen Event Revelation Ordering"
type: concept
tags: [summarization, chronology, narrative-ordering, prompt-engineering]
sources: [2026-08-04-campaign-summary-prompt-design]
last_updated: 2026-08-04
---

# Off-Screen Event Revelation Ordering

A chronology rule proposed by [[Cursor]] Gemini for the [[CampaignSummaryPrompt]]: events that happened "off-screen" but were revealed later in the transcript should be **summarized at the point of revelation, not at their chronological occurrence**. Example: if a character reveals a betrayal that happened months earlier, the bullet is "Character X reveals they betrayed the party," placed where the reveal lands.

Rationale: the summary tracks the *narrative experience* of the campaign, and the transcript itself is the only reliable ordering source (per [[ChatGPT]]'s observation that transcripts often lack timestamps). Inserting off-screen events at their in-world time would require inference the transcript cannot support and would misrepresent what the players knew when. Complements [[RetconDMNote]], which handles the DM *changing* the past rather than *revealing* it.