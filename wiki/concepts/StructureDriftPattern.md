---
title: "Structure Drift Pattern"
type: concept
tags: [agent-patterns, code-quality, worldarchitect-ai]
sources: []
last_updated: 2026-04-11
---

## What It Is
A class of bugs where fields get accidentally nested inside conditional blocks they don't logically belong to. An agent adding a new field places it inside an existing `if hasattr(...)` block because that's where the cursor is, not because the field semantically depends on that condition.

## This Case Study
In `mvp_site/world_logic.py`, the `debug_info` field was placed inside:
```python
if hasattr(structured_response, "rewards_box"):
    unified_response["rewards_box"] = structured_response.rewards_box
    ...
    if debug_mode and hasattr(structured_response, "debug_info"):
        unified_response["debug_info"] = structured_response.debug_info
```

This caused `debug_info` to only be emitted on turns that had a rewards_box — pure narrative turns had no debug_info, breaking system warnings and dice roll display data.

## Root Cause
PR #5782 merge incorporated a checkpoint session (fac29f6a4) from PR #2162 that contained world_logic.py changes. The checkpoint agent placed `debug_info` inside the rewards_box block as a structural accident.

## The Fix
Pull `debug_info` outside the rewards_box conditional (PR #6197):
```python
# Before: inside if hasattr(structured_response, "rewards_box"):
# After: same level as rewards_box
if debug_mode and hasattr(structured_response, "debug_info"):
    unified_response["debug_info"] = structured_response.debug_info
```

## Oracle Rule
When adding fields to structured_response assembly, ensure they are at the correct nesting level — not inside unrelated conditional blocks.
