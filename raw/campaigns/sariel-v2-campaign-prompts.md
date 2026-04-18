---
title: "Sariel V2 Campaign Prompts (June 2025)"
type: source
tags: [campaign, sariel, prompts, entity-tracking]
source_file: "raw/sariel-v2-campaign-prompts.json"
sources: []
last_updated: 2026-04-08
---

## Summary
Campaign prompt sequence from 2025-06-30 containing 11 prompts for the Sariel v2 campaign, with god mode initial setup followed by 10 main character interactions tracking entities across various locations.

## Key Claims
- **11-Prompt Structure** — Complete campaign flow from initial_setup through interaction_10
- **Entity Tracking Across Locations** — Throne Room → Valerius's Study → Lady Cressida's Chambers → Great Archives → Chamber of Whispers
- **Cassian Problem Identification** — interaction_2 marked as "cassian problem" edge case for entity tracking
- **Dual Mode Architecture** — Uses god mode for initial_setup, main character mode for all subsequent interactions

## Prompt Sequence
| # | Mode | Location | Expected Entities |
|---|------|----------|-------------------|
| initial_setup | god | Throne Room | Sariel |
| interaction_1 | main character | Throne Room | Sariel |
| interaction_2 | main character | Throne Room | Sariel, Cassian (CASSIAN PROBLEM) |
| interaction_3 | main character | Throne Room | Sariel |
| interaction_4 | main character | Valerius's Study | Sariel, Valerius |
| interaction_5 | main character | Valerius's Study | Sariel, Valerius |
| interaction_6 | main character | Lady Cressida's Chambers | Lady Cressida Valeriana, Sariel |
| interaction_7 | main character | Lady Cressida's Chambers | Lady Cressida Valeriana, Sariel |
| interaction_8 | main character | Great Archives | Sariel |
| interaction_9 | main character | Chamber of Whispers | Sariel, Magister Kantos |
| interaction_10 | main character | Chamber of Whispers | (truncated in source) |

## Connections
- [[Sariel]] — Player character, member of House Arcanus
- [[Cassian]] — NPC with known entity tracking edge case
- [[Valerius]] — NPC encountered in study location
- [[LadyCressidaValeriana]] — NPC encountered in her chambers
- [[MagisterKantos]] — NPC encountered in Chamber of Whispers
- [[EntityTracking]] — Core mechanic being validated by this campaign sequence
- [[GodMode]] — Prompt mode for initial campaign setup
- [[MainCharacterMode]] — Prompt mode for player interactions

## Contradictions
- []
