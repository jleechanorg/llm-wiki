---
title: "Dorodango"
type: concept
tags: [attractor-pattern, codegen, disposable-code, mental-model]
date: 2026-05-24
---
## Overview
Dorodango is the Japanese art of polishing a ball of mud into a high-gloss sphere. Applied to codegen software: generated code is disposable — polish what comes out, and when fundamentally wrong, throw it away and rebuild from the spec. Coined by Jesse Vincent.

## Key Properties
- **What**: Mental model for treating codegen software as disposable — specs are the expensive part, code is cheap
- **Why matters**: Changes the economics of building — you can afford to build three implementations and keep the best one, or throw one away and start over
- **Key insight**: "Software is cheap now. Specs are the expensive part." — Jesse Vincent
- **Wikipedia disambiguation**: "mud ball" redirects to "Big Ball of Mud" (the software anti-pattern) — Jesse leaned into it

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| [[JesseVincent]] | Person | Coined the dorodango framing |
| [[AttractorPattern]] | Pattern | Dorodango is the key mental model |
| [[DOTAsArtifact]] | Pattern | DOT files are the spec; code is dorodango |

## Connection to Attractor Pattern
Dorodango is the economic foundation of the Attractor pattern. If code is disposable and specs are durable, then: (1) you can build multiple implementations cheaply, (2) convergence proves the spec is an attractor, (3) the pipeline .dot files are the product, not the runner code.

## See Also
- [[JesseVincent]]
- [[AttractorPattern]]
- [[DOTAsArtifact]]
