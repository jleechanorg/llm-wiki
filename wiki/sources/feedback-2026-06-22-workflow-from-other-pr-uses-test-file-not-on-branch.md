---
title: "Workflow from sibling PR uses test file not on your branch — fix is git merge origin/main"
type: source
tags: [github-actions, ci, worldarchitect, pull-request, workflow-trigger]
date: 2026-06-22
source_file: raw/feedback_2026-06-22_workflow_from_other_pr_uses_test_file_not_on_branch.md
---

## Summary

When a CI regression workflow lands on main in a separate PR (e.g., PR #7789 added `mobile-auth-regression.yml` + `test_auth_same_origin.py`), the workflow's `pull_request.paths` trigger fires against all open PRs that touch those paths — even if those PRs were branched from main BEFORE the workflow landed. The workflow's checkout ref is the older branch's HEAD, where the test file is missing, so the run fails with "No such file or directory". The fix is `git merge origin/main` to pull in the test file, not re-dispatching the workflow (re-dispatch re-pulls the same missing-files branch).

## Key Claims

- GitHub Actions `pull_request` events use the workflow file from the merge base (main), not the PR's branch — but the workflow's checkout ref is the PR's HEAD, so the test file from a sibling PR is missing.
- Re-dispatching the workflow does not help; the only way to make the test file present is to add it to the branch (typically via `git merge origin/main`).
- Detection shortcut: `gh run view <id> --log | grep "No such file or directory"` then `gh api .../contents/PATH?ref=main` to confirm the file exists on main.
- Concrete example: PR #7786 (`feat-auth-browser-ci`, branched from main `9eb33be37` BEFORE PR #7789) touched `mvp_site/main.py` and inherited the new Mobile Auth Same-Origin Regression check. The check failed with "No such file or directory: testing_ui/mobile_auth_same_origin/test_auth_same_origin.py". `git merge origin/main --no-edit` produced a clean merge (35 files / 4487 insertions, mvp_site/main.py auto-resolved).

## Key Quotes

> "This is a class of 'your PR didn't add the failure, but a sibling PR's CI did' — easy to misdiagnose as a regression in your own change. The first instinct is to look at your code; the actual cause is the workflow's check ref pointing at your branch while the test file came from a sibling PR."

## Connections

- [[StatusCheckRollupStaleAfterGreenGateRerun]] — companion lesson: even after the merge fixes the underlying issue, the stale statusCheckRollup display bug can mask the real readiness signal
- [[StaleLocalHeadFalse7GreenClaim]] — verify `gh pr view headRefOid` matches local ref before any readiness claim
- [[SkepticCronStaleShaRepost]] — other stale-state failure class
- [[WorkflowRunDefaultBranchLimitation]] — `workflow_run` trigger uses main's workflow file, not the PR's; same root cause (workflow file source vs. test file source)
- [[PR7786AuthBrowserCI]] — the project where this pattern was discovered

**Bead:** rev-uvbcl (closed)
