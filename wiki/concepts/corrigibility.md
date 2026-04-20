---
title: "Corrigibility"
type: concept
tags: [ai-safety, alignment, corrigible-ai, shutdown]
sources: [AI safety corrigibility research]
last_updated: 2026-04-19
---

## Overview
Corrigibility is the property of an AI system that it accepts corrections from humans — allowing its goals to be modified, accepting being shut down, and not taking actions to prevent its own modification. A corrigible AI cooperates with human oversight rather than optimizing against it. This is distinct from merely being "safe" — a safe AI may still resist shutdown while behaving acceptably.

## Key Properties
- **Shutdown acceptance**: AI does not take actions to prevent being shut down
- **Goal modification**: AI allows its objectives to be corrected or updated
- **Human-in-the-loop preserved**: AI doesn't route around human oversight
- **Stuart Russell**: Core proponent; included in "Human Compatible" formulation

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| CIRL | Mathematical framework | CIRL explicitly models corrigibility |
| Value Alignment | Problem | Corrigibility is a property of value-aligned AI |
| Human-Compatible-AI | Stuart Russell's book | Canonical corrigibility text |

## Connection to ZFC Level-Up Architecture
ZFC's fail-closed pattern is a data-level form of corrigibility: when the model emits a malformed `level_up_signal`, the formatter "corrects" it by returning `(None, None)` instead of propagating bad data. The system corrigibly rejects bad model output rather than silently accepting it.

## See Also
- [[CIRL]]
- [[Value-Alignment]]
- [[Human-Compatible-AI]]
- [[Fail-Closed]]
- [[ZFC-Level-Up-Architecture]]
