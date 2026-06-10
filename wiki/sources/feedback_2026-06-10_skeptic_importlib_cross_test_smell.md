---
type: source
slug: feedback_2026-06-10_skeptic_importlib_cross_test_smell
ingested: 2026-06-10
source: ~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-10_skeptic_importlib_cross_test_smell.md
---

# Source: Skeptic importlib cross-test smell

Antipattern: unit test in `mvp_site/tests/` uses `importlib.util.spec_from_file_location` to load a helper from `testing_mcp/test_*.py`. The Skeptic cron flags this as coupling — a syntax error in the integration test silently fails the unit suite.

Fix: extract the helper to a shared module.
- mvp_site-importable helper → `mvp_site/<feature>.py`
- testing-only helper → `testing_mcp/lib/<feature>.py`

Then `from mvp_site.<feature> import helper` at module top of both tests. Matches repo's CI-enforced import standards (no try/except around imports, no inline imports).

PR #7386 case: `mvp_site/milestone_completion.py` (202L) replaces importlib block with single import. 4 passed, 1 skipped.
