---
title: "Mobile Responsive Design"
type: concept
tags: [css, mobile, responsive, ui]
sources: []
last_updated: 2026-04-08
---

CSS technique for adapting UI layout and sizing to different device screen widths using @media queries. Common breakpoints: 320px (mobile), 768px (tablet), 1200px (desktop).

## Key Patterns
- @media (max-width: 768px) — applies styles when viewport <= 768px
- rem units — relative to root font-size, scales proportionally
- Viewport testing — verifying design across multiple device widths

## Connections
- Tested in [[Mobile Responsive Choice ID Tests]] for choice-id font scaling
- Related to [[Loading Spinner Messages Tests]] — both validate UI responsiveness
