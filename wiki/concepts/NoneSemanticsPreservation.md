---
title: "None Semantics Preservation"
type: concept
tags: [serialization, pattern, None-vs-default]
sources: []
last_updated: 2026-04-08
---

Pattern of preserving None values during serialization to distinguish between "no value exists" and "empty value exists". Critical in GameState where None vs {} have different meanings for fields like rewards_pending.

## Implementation
- Use model_dump(mode='python') instead of default JSON serialization
- None is preserved; {} is preserved as empty dict
- Test with [[GameState None Semantics Preservation Tests]]
