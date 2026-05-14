# Consulting Page iPad Layout Fix

## Problem
Consulting page had horizontal overflow on iPad (768-1024px) due to breakpoint at 760px sending iPads to the desktop layout with fixed width: 1440.

## Solution
- Breakpoint 760 → 1024
- width: 1440 → maxWidth: 1440 with fluid width: 100%
- useViewport hook for inline-style responsive layouts
- Strip marquee overflow fix with position: relative and maxWidth: 100vw

## Pattern
For React components with only inline styles (no CSS classes), use a useViewport hook returning window.innerWidth on resize, then compute style values based on breakpoints.
