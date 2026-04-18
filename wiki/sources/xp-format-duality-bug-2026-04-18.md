# XP Format Duality Bug — `experience.current` vs `xp` (2026-04-18)

**Bead:** rev-7vyc (streaming fix family)
**Fixed in:** commit 12bfbdba5, branch `fix/streaming-rewards-canonicalization`

## Root Cause

The server stores XP in two different formats depending on the execution path:

| Path | Field | Example |
|------|-------|---------|
| GOD_MODE raw input (test only) | `player_character_data.xp` | `{"xp": 250}` |
| Server-canonical (after processing) | `player_character_data.experience.current` | `{"experience": {"current": 320, "to_next_level": 900}}` |

`_extract_xp_robust` in `rewards_engine.py` previously only read `player_character_data.xp`. When the server stored XP canonically at `experience.current`, the function returned 0 — causing `resolve_level_up_signal` to see XP=0 and report no threshold crossing.

## Impact

- E2E Scenario A "Seed XP mismatch: expected 250, got 0" — seed verification failed because `pc.get("xp")` returned None after server normalization
- Scenario B `rewards_box.level_up_available` missing from streaming done payload — XP read as 0, no threshold crossing detected

## Fix

`_extract_xp_robust` now reads both formats with fallback:
```python
xp = player_data.get("xp", None)
if xp is None:
    exp = player_data.get("experience") or {}
    xp = exp.get("current", 0)
```

## Related Fix: `level_up_pending` Authoritative Signal

When a character's XP already crossed the threshold (auto-promoted: level already incremented), reading XP against the NEW level's threshold no longer shows a crossing. The fix adds a check for `custom_campaign_state.level_up_pending` and `level_up_in_progress` as authoritative fallback signals.

## Evidence

Iteration_007 of `testing_mcp/streaming/test_level_up_streaming_e2e.py`: 2/2 PASS, streaming path confirmed, `rewards_box.level_up_available=True` in done payload.
