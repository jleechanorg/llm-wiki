---
title: "Ragnarok Online Quality Game Demo - Evidence Criteria"
type: source
tags: [game-dev, sprite-generation, evidence-review, ragnarok, walk-cycle]
date: 2026-05-01
source_file: raw/ragnarok-quality-game-demo-criteria.md
---

## Summary
Defining quality criteria for 2D game demos to match Ragnarok Online visual standards. Evidence reviewer validates video evidence against these criteria. **Goal**: crisp pixel art sprites, 8-frame walk cycles, tile-based environments, responsive WASD controls.

## ⚠️ MANDATORY EXECUTION

**This criteria is USELESS without real analysis.** When validating evidence:

1. **MUST** extract frames with ffmpeg (don't just describe it)
2. **MUST** run Python pixel analysis (get actual numbers)
3. **MUST** calculate frame diff (proves animation exists)
4. **MUST** report specific pixel counts (not "some warm pixels")

## Quality Criteria

### Sprite Quality (Ragnarok Standard)
| Criterion | Target | Threshold | How to Measure |
|-----------|--------|-----------|----------------|
| Resolution | 256x256 sprites | Frame size ≥ 960x480 | ffprobe output |
| Color depth | 256-color style | Unique colors > 128 | Python: `len(set(img.getdata()))` |
| Animation frames | 8-frame walk cycle | Frame diff > 1000 pixels | Compare frame 0 vs 15 |
| Pixel density | Crisp, not blurry | No anti-aliasing | Visual inspection of edges |

### Animation Quality
| Criterion | Target | Threshold | How to Measure |
|-----------|--------|-----------|----------------|
| Walk cycle | 8 distinct frames | Frame 0 vs 15 diff > 1000 | ffmpeg extract + Python diff |
| Body bob | Sine-wave vertical | Visible offset | Frame analysis |
| Leg alternation | L/R step positions | 4-frame offset | Compare sequential frames |
| Character shadow | Ground shadow | Dark blob present | Pixel analysis of lower region |

### Environment Quality
| Criterion | Target | Threshold | How to Measure |
|-----------|--------|-----------|----------------|
| Tile consistency | Clean edges | Sharp boundaries | Visual + pixel edge detection |
| Depth layers | Floor < objects < chars | Characters above tiles | Frame analysis |
| Color harmony | Cohesive palette | No clashing regions | Color histogram |
| Grid alignment | Snap to grid | No sub-pixel drift | Position analysis |

### Game Feel
| Criterion | Target | Threshold | How to Measure |
|-----------|--------|-----------|----------------|
| Responsive controls | WASD immediate | Movement within 100ms | Frame sequence shows movement |
| Collision | Wall blocking | Cannot pass through | Boundary analysis |
| Camera follow | Smooth tracking | Player centered | Position tracking |
| NPC presence | Characters alive | NPCs with names | Frame analysis |

## Validation Pipeline (MANDATORY EXECUTION)

### Step 1: Extract Frames
```bash
ffmpeg -y -i [video.gif] -vf "select=eq(n\,0)" -frames:v 1 /tmp/game_er_frame0.png
ffmpeg -y -i [video.gif] -vf "select=eq(n\,15)" -frames:v 1 /tmp/game_er_frame15.png
ffmpeg -y -i [video.gif] -vf "select=eq(n\,29)" -frames:v 1 /tmp/game_er_frame29.png
```

### Step 2: Video Properties
```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=width,height,frame_rate [video]
```

### Step 3: Pixel Analysis (Python - MANDATORY)
```python
python3 << 'EOF'
from PIL import Image
import os

frames = ['/tmp/game_er_frame0.png', '/tmp/game_er_frame15.png', '/tmp/game_er_frame29.png']
for f in frames:
    if not os.path.exists(f):
        print(f"MISSING: {f}")
        continue
    img = Image.open(f)
    data = list(img.getdata())
    unique = len(set(data))

    # Count pixel types
    warm = sum(1 for p in data if p[0] > 150 and p[1] > 80 and p[2] < 150)  # skin
    cool = sum(1 for p in data if p[2] > 150 and p[0] < 100)  # sky/water
    green = sum(1 for p in data if p[1] > 80 and p[1] > p[0])  # grass
    gray = sum(1 for p in data if abs(p[0]-p[1]) < 10 and abs(p[1]-p[2]) < 10)  # stone

    print(f"{os.path.basename(f)}: {img.size}, unique:{unique}, warm:{warm}, cool:{cool}, green:{green}, gray:{gray}")

# Animation check
f0 = Image.open('/tmp/game_er_frame0.png')
f15 = Image.open('/tmp/game_er_frame15.png')
data0 = list(f0.getdata())
data15 = list(f15.getdata())
diff = sum(1 for i in range(len(data0)) if data0[i] != data15[i])
print(f"\nFrame diff (0 vs 15): {diff} pixels")
print(f"Status: {'ANIMATED' if diff > 1000 else 'SOME MOVEMENT' if diff > 100 else 'STATIC'}")
EOF
```

## Pass/Fail Determination

### STRONG PASS (all must be true)
- [ ] Unique colors > 128
- [ ] Frame diff > 1000 (animated)
- [ ] Warm pixels > 500 (character present)
- [ ] Green pixels > 1000 (environment present)

### WEAK PASS
- [ ] Animation present but frame diff < 1000
- [ ] Sprites visible but unique < 128

### FAIL (any one = fail)
- [ ] Frame diff < 100 (static or broken)
- [ ] No warm pixels (no character)
- [ ] Video is blank/black/corrupted
- [ ] Unique colors < 32 (severely degraded)

## Related Pages
- [[Walk Cycle Animation]] — 8-frame animation technique
- [[Sprite Sheet Compositing]] — Layer-based sprite assembly
- [[Pollinations.ai]] — Free sprite generation
- [[Vibe Code 2D Game]] — Game dev methodology