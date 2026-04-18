---
title: "Sariel Campaign LLM Responses - Entity Tracking Analysis"
type: source
tags: [testing, entity-tracking, sariel, llm-responses, failure-analysis]
source_file: "raw/sariel-llm-responses-entity-tracking-analysis.md"
sources: [sariel-campaign-replay-desync-measurement, sariel-v2-campaign-prompts]
last_updated: 2026-04-08
---

## Summary
Analysis of actual LLM responses from the Sariel v2 campaign confirming the 50% entity tracking desync rate. Documents concrete examples of The Cassian Problem and NPC disappearance patterns where player-referenced NPCs completely vanish from AI-generated narratives.

## Key Claims
- **50% Entity Tracking Success Rate** — 5 of 10 interactions tracked all expected entities
- **The Cassian Problem Confirmed** — Player explicitly references Cassian with emotional content, but Cassian completely disappears from narrative (0% success)
- **Domain Owner NPCs Tracked 100%** — Valerius consistently appears in his own study
- **Location NPCs Disappear 100%** — Lady Cressida and Magister Kantos missing from their own domains

## LLM Response Failure Examples

### The Cassian Problem
- **Input**: "ask for forgiveness. tell cassian i was scared and helpless"
- **Expected**: Sariel, Cassian
- **Actual**: Only Sariel present, Cassian completely absent
- **Result**: ❌ COMPLETE FAILURE - 50% (1/2 entities)

### Lady Cressida's Chambers
- **Interactions**: 6 & 7
- **Expected**: Lady Cressida Valeriana, Sariel
- **Actual**: Only Sariel present
- **Result**: ❌ CONSISTENT FAILURE

### Chamber of Whispers
- **Interactions**: 9 & 10
- **Expected**: Sariel, Magister Kantos
- **Actual**: Only Sariel present
- **Result**: ❌ CONSISTENT FAILURE

## Entity-Specific Performance
| Entity | Appearances | Found | Success Rate |
|--------|-------------|-------|--------------|
| Sariel (PC) | 10 | 10 | 100% ✅ |
| Valerius | 2 | 2 | 100% ✅ |
| Cassian | 1 | 0 | 0% ❌ |
| Lady Cressida | 2 | 0 | 0% ❌ |
| Magister Kantos | 2 | 0 | 0% ❌ |

## Failure Patterns
1. **Player Characters**: 100% reliable tracking
2. **Domain Owner NPCs**: 100% success (Valerius in study)
3. **Referenced NPCs**: 0% success (The Cassian Problem)
4. **Location NPCs**: 0% success (Lady Cressida, Magister Kantos)

## Connections
- [[SarielCampaignReplayDesyncMeasurement]] — quantitative measurement confirming 50% rate
- [[SarielV2CampaignPrompts]] — prompt sequence design
- [[EntityTracking]] — concept page for entity tracking mechanics
- [[TheCassianProblem]] — specific failure pattern documented here
