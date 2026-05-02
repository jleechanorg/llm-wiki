---
title: "Walk Cycle Animation"
type: concept
tags: [animation, sprite-dev, 2d-game]
last_updated: 2026-05-01
---

# Walk Cycle Animation

8-frame animation cycle with body bob, leg alternation, and direction flip. The standard animation technique for 2D game character movement.

## Key Properties
- **Frame count:** 8 frames per cycle
- **Frame timing:** 120ms (~8fps)
- **Phases:** Contact → Passing → High-point → Passing (repeat)
- **Body bob:** `Math.sin(frame * PI/4) * 3` for vertical offset
- **Leg alternation:** L/R step positions offset by 4 frames

## Implementation Pattern
```javascript
// 8-frame walk cycle with sine-wave bob
function getWalkFrame(frame) {
  const bobOffset = Math.sin(frame * Math.PI / 4) * 3;
  const legFrame = frame % 4;
  return { bobOffset, legFrame };
}
```

## Related Systems
| System | Type | Relevance |
|--------|------|-----------|
| [[HTML5 Canvas]] | Rendering | Canvas API for sprite compositing |
| [[State Machine]] | Animation control | Manages walk/idle/run states |
| [[Sprite Sheet Compositing]] | Asset assembly | Layered sprite parts |

## See Also
- [[Aseprite]] — animation editing tool
- [[Vibe Code 2D Game]] — proven game dev methodology