---
name: skeptic-importlib-cross-test-smell
description: Unit test importing integration test helper via importlib.util.spec_from_file_location is a coupling smell — extract to a shared module in mvp_site/ or testing_mcp/lib/
metadata:
  node_type: memory
  type: feedback
  originSessionId: accc5a5a-bae2-4e3c-96aa-4caa512ea998
---

When a unit test under `mvp_site/tests/` needs a helper that lives in `testing_mcp/test_*.py` (e.g., `_collect_completed_milestones` inside an integration test), the common antipattern is:

```python
# mvp_site/tests/test_X.py
import importlib.util, pathlib
spec = importlib.util.spec_from_file_location(
    "_it", pathlib.Path(__file__).parent.parent.parent / "testing_mcp/test_integration_X.py"
)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
helper = mod._collect_completed_milestones
```

The Skeptic cron flags this as a coupling defect (Gates vary by version, but the smell is stable): a syntax error or runtime change in the integration test file will silently fail the unit suite, and the cross-folder import makes ownership ambiguous. The fix is to extract the helper to a shared module:

- For mvp_site-importable helpers: `mvp_site/<feature>.py` (e.g., `mvp_site/milestone_completion.py` with `collect_completed_milestones`, `is_milestone_contradiction_choice`)
- For testing-only helpers: `testing_mcp/lib/<feature>.py` (matches the existing shared-lib convention)

Both unit and integration tests then `from mvp_site.milestone_completion import collect_completed_milestones` — clean module-level import, no spec_from_file_location, no test-as-module-loading.

**For PR #7386**: extracted `mvp_site/milestone_completion.py` (202 lines) containing the recursive walk + regex + is_milestone_contradiction_choice + gather_planning_block_text. Both `mvp_site/tests/test_planning_block_completed_milestone_7373.py` and `testing_mcp/test_planning_block_completed_milestone_green_7373.py` now import from the shared module. Diff for the refactor: +202 new module, −5 lines from the unit test (replaced importlib block with single import). 4 passed, 1 skipped in 0.93s.

**How to apply**: Trigger condition — Skeptic verdict cites "cross-test import" or "importlib coupling" as a Gate failure, or a unit test under `mvp_site/tests/` uses `importlib.util.spec_from_file_location`. Extract the helper to the lowest-level module that BOTH test files can import. If only the integration test uses it, leave it in `testing_mcp/lib/` instead. Always prefer module-level imports per the repo's CI-enforced import standards (no try/except around imports, no inline imports).

**Related**: `repo CLAUDE.md` "Import Standards (CI Enforced)"; `feedback_2026-06-08_red_baseline_pin_prefix_ref_not_head.md` (RED harness coupling class).
