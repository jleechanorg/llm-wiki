---
title: "Desync Measurement"
type: concept
tags: [testing, metrics, entity-tracking]
sources: [sariel-campaign-replay-desync-measurement]
last_updated: 2026-04-08
---

## Definition
Quantitative approach to measuring entity tracking accuracy by comparing expected entities (from test definition) against found entities (from actual LLM response) at each interaction step.

## Methodology
1. Define expected entities per interaction in test specification
2. Execute campaign replay with fixed inputs
3. Parse LLM response for entity mentions
4. Compare expected vs found
5. Calculate success rate and failure patterns

## Key Metrics
- **Success Rate**: (interactions with full entity match) / total interactions
- **Missing Entities**: Expected but not found
- **Extra Entities**: Found but not expected (potential hallucination)
- **Fields Checked**: Count of state fields validated per interaction

## Results from Sariel Campaign
| Metric | Value |
|--------|-------|
| Success Rate | 50% (5/10) |
| Total Fields Checked | 130 |
| First-mention Failures | 3 (Valerius, Lady Cressida, Kantos) |
| Recovery Rate | 33% (1/3 recovered) |

## Related
- [[EntityTracking]] — What is being measured
- [[CampaignReplay]] — Testing approach
