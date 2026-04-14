# PR #8: fix: address PR #7 review issues

**Repo:** jleechanorg/jleechanclaw
**Merged:** 2026-02-28
**Author:** jleechan2015
**Stats:** +168/-8 in 8 files

## Summary
- Fix 5 issues identified in PR #7 code review + add integration test
- All 194 tests pass

## Raw Body
## Summary
- Fix 5 issues identified in PR #7 code review + add integration test
- All 194 tests pass

## Changes

| Bead | File | Fix |
|------|------|-----|
| ORCH-djx (P1) | `heartbeat_bridge.py` | Per-agent error handling in `_run()` loop — one failed POST no longer skips remaining agents |
| ORCH-o18 (P1) | `lifecycle_reactions.py` | Fixed `poll_fn: Optional[callable]` → `Optional[Callable[[LifecycleManager], None]]` |
| ORCH-cfg (P2) | `webhook_bridge.py` | Added explicit `webhook_url` parameter to `notify_mission_control()` |
| ORCH-hdt (P2) | `writer.py` | Replaced `**kwargs` forwarding in `write_all()` with explicit `goals`, `overwrite`, `extra_paths` params |
| ORCH-7yf (P2) | `lifecycle_reactions.py` | Annotated `escalate_after` as TODO for future time-based escalation |
| ORCH-ckr (P2) | `test_lifecycle_reactions.py` | Added integration test: full lifecycle flow (working → PR → CI fail → retry → approved → merged) |

## Testing
- `python -m pytest tests/ -v` → **194 passed in 0.30s**
- New tests: `TestLifecycleIntegration` (2 tests), `test_explicit_url_overrides_env` (1 test)

## Known Limitations
- `escalate_after` is still not evaluated at runtime (documented as TODO)
- Hardcoded paths in `config.py`/`memory.py` are acceptable for this personal repo

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Medium Risk**
> Medium risk due to a small API breaking change in `genesis.writer.write_all` (unknown kwargs now raise `TypeError`) and minor interface tweaks to webhook notification that could affect callers if not updated.
> 
> **Overview**
> Improves orchestration configurability and correctness by tightening public APIs and expanding coverage of end-to-end lifecycle/reaction behavior.
> 
> `genesis.writer.write_all` now uses an explicit signature (`goals`, `overwrite`, `extra_paths`) instead of forwarding `**kwargs`, so unexpected parameters fail fast. `notify_mission_control` accepts an optional explicit `webhook_url` override, and `LifecyclePoller`’s `poll_f
