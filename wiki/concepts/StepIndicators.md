---
title: "Step Indicators"
type: concept
tags: [ui-component, wizard, progress, multi-step, user-experience]
sources: ["interactive-features-milestone-4"]
last_updated: 2026-04-08
---

Visual component showing progress through multi-step flows. Step indicators consist of numbered circles with labels below.

## States

| State | Circle Style | Label Style |
|-------|-------------|-------------|
| Active | Blue (#007bff), scaled 1.1x | Blue, bold |
| Completed | Green (#28a745) | Green |
| Pending | Gray (#e9ecef) | Gray (#6c757d) |

## Behavior
- Click to navigate to step
- Hover scales circle 1.05x with shadow
- Smooth 0.3s transitions between states

## Usage
Used in [[CampaignWizard]] and other multi-step interfaces.
