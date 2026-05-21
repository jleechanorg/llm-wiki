# PR6844 Combat Phase Enum and E2E Firestore Caching Learnings

**Date**: 2026-05-14
**PR**: #6844 (merged 2026-05-10, commit be47450feb9d)
**Bead**: rev-k3s41

## Learning 1: combat_phase enum uses "ended" not "resolved"

`COMBAT_PHASE_ENUM = {"initiating", "active", "ended", "fled"}` — the value `"resolved"` is NOT valid. Writing `cs["combat_phase"] = "resolved"` creates invalid state that prevents combat cleanup and traps the game in a CombatAgent loop.

**Root cause**: Two code paths in `world_logic.py` (line ~3301 streaming, line ~6885 non-streaming) wrote `"resolved"` instead of `"ended"` during god mode combat cleanup. The invalid phase value caused the combat state machine to never fully exit combat.

**Fix**: Changed both occurrences to `"ended"`. Grep for `combat_phase.*resolved` to catch regressions.

**Unit test**: `test_god_mode_stale_combat_cleanup.py` line 264 asserts `combat_phase == "ended"`.
**E2E test**: `test_god_mode_stale_combat_e2e.py` confirms cleanup with real server + Firebase.

## Learning 2: Firestore admin client caching in E2E tests

When E2E tests write to Firestore using `firebase_admin` in the test process, the server's own `firebase_admin` client may not see those writes immediately due to client-side caching. This makes direct Firestore writes from tests unreliable for setting up state that the server must then read.

**Fix**: Use server-side write paths (e.g., `GOD_MODE_UPDATE_STATE` API endpoint) to inject test state through the server's own Firestore client. This guarantees the server reads the exact state you wrote. Direct Firestore writes from test processes are only reliable for verifying persisted output, not for setting input state that the server must act on.
