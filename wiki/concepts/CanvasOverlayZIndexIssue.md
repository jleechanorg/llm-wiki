---
title: "Canvas Overlay Z-Index Issue"
type: concept
tags: [testing, video-capture, frontend-bug, playwight, e2e-testing]
sources: []
last_updated: 2026-04-13
---

## Summary
A frontend rendering issue where a canvas element with `z-index: 0` visually dominates the viewport, covering game content during video capture. This prevents Playwright and other video recording tools from capturing clean evidence of game state.

## The Problem

In `AmbientBackground.web.tsx`, the ambient background canvas is rendered with `z-index: 0` (or `zIndex: 0` in JSX). Since 0 is the default z-index, this places the canvas above most content that doesn't have an explicit z-index set. The canvas displays a starfield/particle effect that visually dominates the viewport.

**Impact on testing:**
- Playwright video recording captures the DOM as rendered — the overlay is always visible
- Game text and chat bubbles are covered by the particle effect
- Video evidence is technically captured but visually useless for debugging

## The Workaround (Partial)

In `test_full_lifecycle_video.py`, a function `_screenshot_without_overlay()` was created to hide canvas elements before taking screenshots:

```python
def _screenshot_without_overlay(page):
    page.evaluate("""() => {
        document.querySelectorAll('canvas').forEach(el => el.style.display = 'none');
    }""")
    # ... take screenshot
    page.evaluate("""() => {
        document.querySelectorAll('canvas').forEach(el => el.style.display = 'block');
    }""")
```

**Limitation:** This workaround works for point-in-time screenshots but doesn't apply to video recording, where the canvas is always live during capture.

## The Fix

Two equivalent options:

### Option A: Negative z-index
```jsx
<canvas style={{ zIndex: -1, ... }} ... />
```

### Option B: Pointer events none
```jsx
<canvas style={{ zIndex: 0, pointerEvents: 'none', ... }} ... />
```

Option A is simpler and guaranteed to work. Option B maintains visual position but allows clicks through.

## Connections
- [[Harness5LayerModel]] — this is an L3 (Execution) failure: the harness cannot execute clean video capture due to DOM configuration
- [[OCRTeardownValidation]] — the L4 verification workaround for duration-only validation that passed despite the broken capture

## Sources
- worldarchitect.ai E2E testing infrastructure
- test_full_lifecycle_video.py (600+ line test file)
- AmbientBackground.web.tsx component