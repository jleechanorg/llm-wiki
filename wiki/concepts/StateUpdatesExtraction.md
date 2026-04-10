---
title: "State Updates Extraction"
type: concept
tags: [llm-response, state-management, parsing]
sources: [llm-response-object-tdd-tests]
last_updated: 2026-04-08
---

## Definition
State updates extraction is the process of pulling structured state change data from LLM JSON responses. The state_updates field in NarrativeResponse contains a dictionary of changes to apply to the game state, such as player_character_data modifications.

## How It Works
1. LLM sends JSON response with state_updates block
2. parse_structured_response() extracts the block
3. LLMResponse.state_updates property returns the raw updates dict
4. Caller applies updates to GameState via apply_state_updates()

## Example
```json
{
  "state_updates": {
    "player_character_data": {
      "hp_current": 18,
      "level": 2
    }
  }
}
```

## Use Cases
- Updating player HP after combat or healing
- Modifying character inventory or abilities
- Tracking quest progress or story flags
- Managing location changes or world state

## Related Concepts
- [[LLMResponse]] — class that exposes state_updates property
- [[GameState]] — the object being updated with extracted state
- [[Debug Tags Detection]] — another extraction concern from same responses
