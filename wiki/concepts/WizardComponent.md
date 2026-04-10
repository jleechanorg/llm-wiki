---
title: "Wizard Component"
type: concept
tags: [ui, component, state-management]
sources: []
last_updated: 2026-04-08
---

## Description
UI component that manages multi-step workflows with enable/disable states. Requires explicit `enable()` calls to become interactive after state changes like route transitions.

## State Transitions
- `disable()`: Makes wizard non-interactive
- `enable()`: Re-enables wizard for user interaction
