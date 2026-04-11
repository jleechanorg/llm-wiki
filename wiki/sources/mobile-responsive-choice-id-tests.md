---
title: "Mobile Responsive Choice ID Tests"
type: source
tags: [playwright, testing, mobile, responsive, css]
source_file: "raw/test_choice_id_mobile_responsive.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Playwright tests validating .choice-id font-size scaling at mobile breakpoints (320px, 768px, 1200px). Tests verify CSS media queries apply correct font sizes across device viewports.

## Key Claims
- **Desktop viewport**: Default font-size applied at 1200px width
- **Tablet breakpoint**: 768px triggers @media (max-width: 768px) rules
- **Mobile breakpoint**: 320px viewport shows smallest font-size (~11.2px for 0.7rem)
- **Responsive behavior**: Mobile font-size must be smaller than desktop

## Key Quotes
> "font size progression: Desktop {desktop_px}px → Tablet {tablet_px}px → Mobile {mobile_px}px"

## Connections
- Related to [[Loading Spinner Messages Tests]] — both test UI responsive behavior
- Related to [[Missing Structured Fields UI Tests]] — frontend testing patterns

## Contradictions
- None
