---
title: "Faction Updates"
type: concept
tags: [faction, system, tracking]
sources: [debug-events-export-tests]
last_updated: 2026-04-08
---

## Description
Tracking system for faction progress in the Living World. Each faction update includes current_objective, progress, and resource_change.

## Fields
- **current_objective** — What the faction is working toward
- **progress** — Percentage completion of objective
- **resource_change** — Gold/resources gained or lost

## Example
```python
{
    "Zhentarim": {
        "current_objective": "Control trade routes",
        "progress": "50% complete",
        "resource_change": "+500 gold",
    }
}
```

## Connections
- [[LivingWorld]] — manages faction updates
- [[Zhentarim]] — example faction with updates
- [[DebugEventsExport]] — exports faction updates
- [[ResourceTracking]] — resource change mechanics
