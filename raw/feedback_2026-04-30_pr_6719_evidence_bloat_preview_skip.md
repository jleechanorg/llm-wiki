---
name: PR 6719 evidence bloat skipped preview deploy
description: Large generated evidence/doc bundles can hide deploy-triggering files beyond GitHub's path-filter window; freeze SHA before evidence and keep preview deploy manually runnable.
type: feedback
bead: bd-6719learn
---

Context: On 2026-04-30, PR https://github.com/jleechanorg/worldarchitect.ai/pull/6719 was hard to merge because the branch accumulated 87 commits, 430 changed files, and roughly 397 generated evidence files. The preview workflow did not run for the final head even though production files changed.

Technical Detail: `.github/workflows/pr-preview.yml` uses `pull_request.paths`. GitHub only evaluates path filters against the first 300 changed files. The first preview-triggering files in the PR file list were beyond that window, so the deploy workflow was skipped before it could schedule. The final review also mixed stale evidence SHAs with newer production commits.

Solution Applied: Verified the current remote head, fixed the actual stale level-up bugs with TDD in commit https://github.com/jleechanorg/worldarchitect.ai/commit/ecca6c5f40c1a68abdd7db4ed23551cff51db372, and posted current-head Layer 1 evidence to the PR. Did not treat `rg` call-site hits as proof of a `NameError`; checked module-level aliases at the actual remote SHA.

Reusable Pattern: For large PRs, keep generated evidence/design-doc churn out of the production PR when possible, or commit deploy-triggering files where GitHub path filters can see them. Add `workflow_dispatch` to preview deploy workflows so a skipped path-filter run has an operator escape hatch. Freeze the PR SHA before Layer 3, Layer 4, and Skeptic evidence, and rerun evidence after any follow-up production commit.

Verification: Local verification for the fix passed with `./vpython -m pytest mvp_site/tests/test_rewards_engine.py -q`, `./vpython -m pytest mvp_site/tests/test_world_logic.py -q`, and `./vpython -m ruff check mvp_site/rewards_engine.py mvp_site/world_logic.py mvp_site/tests/test_rewards_engine.py mvp_site/tests/test_world_logic.py`.

Classification: Mandatory process rule.
