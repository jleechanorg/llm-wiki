---
name: Consulting page iPad layout fix
description: Fixed horizontal overflow on iPad by changing breakpoint from 760 to 1024 and making desktop layout fluid
type: feedback
bead: none
originSessionId: 0dd6444f-fc4b-461a-8f40-ac1e458421a5
---
## Context

The consulting page (`public/consulting.html` + `public/consulting-assets/consulting-mobile.jsx`) had a broken iPad layout. The responsive breakpoint at `w < 760` meant iPads (768-1024px) got the desktop layout, which had `width: 1440` and `minWidth: 1440`, forcing horizontal scroll.

## Root causes

1. **Breakpoint too low**: `760px` breakpoint let iPad (768px) fall into the desktop path
2. **Fixed-width desktop**: `Site` component used `width: 1440` instead of `maxWidth`
3. **Responsive wrapper**: Added `minWidth: 1440` wrapper forcing overflow
4. **Marquee Strip**: Scrolling text div expanded to ~5385px, parent `overflow: hidden` didn't clip when the parent's own width was unconstrained

## Solution

1. Changed breakpoint from `760` to `1024` — iPads now get mobile layout; iPad landscape (1024+) gets desktop
2. Changed `width: 1440` → `maxWidth: 1440, width: '100%', margin: '0 auto'`
3. Removed `minWidth: 1440` wrapper entirely
4. Made the `Site` component viewport-aware with a `useViewport` hook, adjusting grid columns, padding, font sizes, and nav layout below 1200px
5. Fixed Strip marquee by adding `position: 'relative', width: '100%', maxWidth: '100vw'` and `width: 'max-content'` on the inner scroller

## Key pattern: inline-style responsive layouts

Since these React components use only inline styles (no CSS classes), media queries aren't available. The solution is a `useViewport` hook that returns `window.innerWidth` on resize, then using computed values in inline styles based on breakpoints.

**Why:** File naming in `consulting-assets/` is counterintuitive — `consulting-mobile.jsx` contains the desktop `Site` component and design tokens, while `consulting-desktop.jsx` contains `MobileSite`. The HTML loads them in order: mobile (tokens + Site) first, then desktop (MobileSite).

## Verification

- `document.body.scrollWidth` === `clientWidth` at 1024px, 1100px, 1200px, 1440px
- All 370 unit tests pass
- Screenshots verified at 390px (mobile), 768px (iPad portrait), 1024px (iPad landscape), 1440px (desktop)
