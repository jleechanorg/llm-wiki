---
name: PR 6843 Root Cause — Location Fallback Severed by Schema Validation
description: PR #5563 strict schema extraction broke the world_data.location fallback
type: feedback
bead: rev-kpm5u
---

PR #6843: `current_location_name` became stale because `_ensure_location_progress` in `preventive_guards.py` relied strictly on `location_confirmed` property. When the LLM omitted it or returned "Unknown", the guard ignored `world_data.location` and fell back to the previous location.

**Breaking PR**: #5563 (Schema Validation Infrastructure). This PR introduced strict schema extraction for `location_confirmed`, inadvertently severing the fallback to the legacy `world_data.location` object that LLMs were still using.

**Lesson**: When adding strict schema validation for a field, ALWAYS preserve the legacy fallback path. Removing a fallback without verifying the LLM has fully migrated to the new schema is a silent data-loss regression.

**How to apply**: Before removing any fallback path in `preventive_guards.py`, grep for all code paths that still produce the legacy field and verify the LLM prompt contract requires the new field. If the legacy field is still used, the fallback must remain.

**Verification**: PR #6843 adds 9 Layer 1 unit tests + `test_location_fallback_end2end.py` (163 LOC) with corrected mock patching.
