---
name: Verify campaign-bible deduplication from decoded BQ payloads
description: Raw provider envelopes must be decoded before counting canonical campaign lore.
type: feedback
bead: rev-mwjbs
---

# Verify campaign-bible deduplication from decoded BQ payloads

## Context

PR [#9153](https://github.com/jleechanorg/worldarchitect.ai/pull/9153) moved
campaign lore to the canonical
`game_state.custom_campaign_state.god_mode.description` channel and removed its
Turn-0 continuation-history duplicate. A live campaign check used
`llm_forensics.llm_payloads`, not `log_events`.

## Rule

For Gemini gameplay rows, `request_json` is a provider envelope. The
model-bound game payload is JSON encoded inside `contents[0].parts[0].text`.
Parse that text before measuring duplication. Do not count raw escaped bytes:
newline and Unicode escaping can produce false failures.

## Verification

Campaign `ArYA47Fvx8HTYC8jpleO`, request
`ArYA47Fvx8HTYC8jpleO_382b275a723143c5b0778a6a9f4cfcce`, recorded at
2026-08-20 22:40:25 UTC, had a 180,126-character canonical description. Its
decoded payload contained that value exactly once across all string fields and
zero times in `story_history`.

Exports were saved for manual review in:

- `/Users/jleechan/Downloads/ArYA47Fvx8HTYC8jpleO-bq-llm-request-duplication-report.md`
- `/Users/jleechan/Downloads/ArYA47Fvx8HTYC8jpleO-latest-bq-gameplay-payload.json`

## Reusable pattern

1. Query `worldarchitecture-ai.llm_forensics.llm_payloads` for nonempty
   `request_json` rows and select the intended gameplay event.
2. Decode the provider envelope and then the text-part JSON payload.
3. Take the canonical value from `game_state.custom_campaign_state.god_mode.description`.
4. Count that value across decoded payload strings and separately in decoded
   `story_history`.
5. Save the raw row, parsed payload, and a short count report for review.

## References

- PR #9153, commit `33d2bd8b019b7508702bfeceea6f32196924150d`
- Existing regression bead `rev-mwjbs`
