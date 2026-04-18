---
title: "Sariel Campaign Replay Desync Measurement"
type: source
tags: [testing, entity-tracking, sariel, python, integration-test]
source_file: "raw/sariel-replay-desync-measurement.md"
sources: []
last_updated: 2026-04-08
---

## Summary
JSON output from a Python test script measuring entity tracking accuracy across 10 campaign replays. The test measures desync rates between expected entities and found entities at each interaction step.

## Key Claims
- **50% Success Rate** — 5 of 10 interactions successfully tracked all expected entities
- **NPC Tracking Failures** — NPCs (Valerius, Lady Cressida Valeriana, Magister Kantos) frequently missed in later interactions
- **Cassian Handled** — The "Cassian problem" edge case was correctly tracked in interaction 2
- **130 Total Fields Checked** — 13 fields per interaction across 10 interactions

## Detailed Results
| Interaction | Input | Location | Expected | Found | Success |
|-------------|-------|----------|----------|-------|---------|
| 1 | continue | Throne Room | Sariel | Sariel | ✅ |
| 2 | ask for forgiveness | Throne Room | Sariel, Cassian | Sariel, Cassian | ✅ |
| 3 | 1 (advance narrative) | Throne Room | Sariel | Sariel | ✅ |
| 4 | 2 | Valerius's Study | Sariel, Valerius | Sariel | ❌ (missing: Valerius) |
| 5 | 1 | Valerius's Study | Sariel, Valerius | Sariel, Valerius | ✅ |
| 6 | 2 | Lady Cressida's Chambers | Sariel, Lady Cressida Valeriana | Sariel | ❌ (missing: Lady Cressida Valeriana) |
| 7 | 2 | Lady Cressida's Chambers | Sariel, Lady Cressida Valeriana | Sariel | ❌ (missing: Lady Cressida Valeriana) |
| 8 | 1 | Great Archives | Sariel | Sariel | ✅ |
| 9 | continue | Chamber of Whispers | Sariel, Magister Kantos | Sariel | ❌ (missing: Magister Kantos) |
| 10 | 3 | Chamber of Whispers | Sariel, Magister Kantos | Sariel | ❌ (missing: Magister Kantos) |

## Analysis
- **Early interactions succeed** — Interactions 1-3 all passed
- **NPC introduction triggers failures** — First introduction of new NPCs (Valerius, Lady Cressida, Kantos) causes tracking failures
- **Recovery possible** — Interaction 5 shows NPC tracking can succeed when NPC was previously introduced
- **Pattern**: Initial NPC mention → failure → subsequent mention → success

## Connections
- [[Sariel]] — Main character, consistently tracked
- [[SarielV2CampaignPrompts]] — Source prompts used for replay testing
- [[EntityTracking]] — The system being measured

## Contradictions
- None identified — data shows consistent pattern of NPC tracking issues
