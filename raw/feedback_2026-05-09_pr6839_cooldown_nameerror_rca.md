---
name: PR 6839 Root Cause — Duplicated Cooldown Lists Cause NameError
description: PR #6308 fractured LW stripping logic across files; merge rebases caused variable name drift
type: feedback
bead: rev-s0vy7
---

PR #6839: Application crashed with `NameError` for `_cooldown_lw_fields` in `world_logic.py`. The logic for stripping cooldown fields (`world_events`, `faction_updates`, `rumors`) was duplicated across `world_logic.py` and `llm_parser.py` using inline tuples. During a merge/rebase, one variable name was lost (`_cooldown_lw_fields_resp` vs `_cooldown_lw_fields`).

**Breaking PR**: #6308 / commit `6d29d8eed` (Rewards engine single-responsibility + llm_parser single orchestration root). This major refactor fractured the Living World stripping logic across multiple files, introducing duplicated inline lists.

**Lesson**: Duplicated constant lists across files are a merge-rebase bomb. When two files define the same list independently, a rebase can update one copy without updating the other, causing NameError or stale-field bugs. The fix is a single source of truth — `living_world_contract.py` now owns the canonical list.

**How to apply**: Any list of fields/constants used in multiple files must be defined ONCE in a shared module and imported. Never duplicate inline tuples across files, even temporarily.

**Verification**: PR #6839 adds `mvp_site/tests/test_end2end/test_non_streaming_cooldown_strip_end2end.py` (5 Layer 2 E2E tests, all PASS).
