---
title: "Sprite Sheet Compositing"
type: concept
tags: [sprite-dev, game-dev, compositing]
last_updated: 2026-05-01
---

# Sprite Sheet Compositing

Layer-based assembly of head/body/arms/legs/feet from separate sprite files. Enables modular character customization and animation.

## Key Properties
- **What:** Z-order layering of sprite parts onto canvas
- **Layer order:** BEHIND → BELT → BODY → LEGS → FEET → HANDS → TORSO → HEAD
- **Why matters:** Modular customization, animation reuse, smaller asset footprint

## Implementation Pattern
```javascript
// Canvas layer compositing
ctx.drawImage(sprites.BEHIND, x, y);
ctx.drawImage(sprites.LEGS, x, y + legOffset);
ctx.drawImage(sprites.BODY, x, y + bobOffset);
ctx.drawImage(sprites.HEAD, x, y + bobOffset);
```

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| [[ParametricBodyPartGenerator]] | Generation | Procedural body parts |
| [[Walk Cycle Animation]] | Animation | Animated compositing |
| [[Texture Atlas]] | Optimization | Efficient sprite storage |

## See Also
- [[LPC]] — source sprites for compositing
- [[Body Parts Pipeline]] — failed approach using LLM generation