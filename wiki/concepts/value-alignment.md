---
title: "Value Alignment"
type: concept
tags: [ai-safety, alignment, values, ethics]
sources: [Stuart Russell "Human Compatible"]
last_updated: 2026-04-19
---

## Overview
Value alignment is the problem of ensuring AI systems pursue objectives that are truly what humans want — not just the stated objective, but the underlying intent behind the request. Stuart Russell's formulation: build AI that is provably beneficial because it is uncertain about human values and maximizes value uncertainty rather than optimizing a fixed reward function.

## Key Properties
- **Corrigibility**: AI that accepts corrections and doesn't resist modification
- **Reward uncertainty**: Machine maintains uncertainty over the human's true utility function
- **Human-Compatible formulation**: Uncertainty over values as the provably safe objective
- **Off-switch test**: A corrigible AI should not resist being shut down or corrected

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| CIRL | Mathematical framework | Formal model for value-aligned AI |
| Human-Compatible-AI | Stuart Russell's book | Definitive text on value alignment |
| Corrigibility | Property | The alignment property that enables value learning |

## Connection to ZFC Level-Up Architecture
The ZFC design doc's fail-closed rules enforce that malformed model signals are rejected — this is a form of corrigibility at the data level: the formatter can "correct" (reject) bad model output rather than propagating it downstream. The model should be uncertain about whether its level-up judgment is valid; the formatter checks and may reject.

## See Also
- [[CIRL]]
- [[Human-Compatible-AI]]
- [[Corrigibility]]
- [[ZFC-Level-Up-Architecture]]
