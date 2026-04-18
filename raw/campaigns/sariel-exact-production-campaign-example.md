---
title: "Sariel Exact Production Campaign Example"
type: source
tags: [campaign, sariel, production, example]
source_file: "raw/sariel-exact-production-campaign-example.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Exact copy of a production campaign example from the Sariel storyline, demonstrating the campaign structure with 5 prompts across god mode and character mode interactions. The campaign features character relationships, narrative choices, and entity state tracking.

## Key Claims
- **Production-Ready Example** — Represents an actual production campaign structure used for testing
- **Dual Mode Structure** — Uses both god mode (initial_setup) and character mode (interactions 1-4)
- **Entity Tracking** — Each prompt is designed to generate state updates with specific expected entities
- **Auto-Continue Strategy** — Documented strategy for picking option 1 after exhausting prompts

## Prompt Flow
| # | Mode | Input | Expected Entities | State Updates |
|---|------|-------|------------------|---------------|
| 1 | god | Initial scene setup | Sariel | Yes |
| 2 | character | friends_3 | Sariel, Ser Gideon Vance, Lady Cressida Valeriana, Rowan Thorne | Yes |
| 3 | character | Speak_3 | Sariel, Raziel | Yes |
| 4 | character | Accept_1 | Sariel, Cassian val Artorius, Valerius val Artorius | Yes |
| 5 | character | 2 | Sariel, Cassian val Artorius, Valerius val Artorius | Yes |

## Connections
- [[Sariel]] — Protagonist of this campaign
- [[CharacterMode]] — Narrative mode for character-driven interactions
- [[GodMode]] — Narrative mode for world/setup narration
- [[EntityTracking]] — Game state system tracking characters across interactions
