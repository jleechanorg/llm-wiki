---
name: project-2026-06-12-mcp-smoke-action-yml-blocker
description: PR
metadata: 
  node_type: memory
  type: project
  originSessionId: 33b6218a-1fc0-42b9-b4f8-1814474904eb
---

# PR #7352 and #7315 smoke gate blocker — missing `run-pr-preview-test/action.yml`

**Date**: 2026-06-12
**Bead**: N/A (workflow plumbing defect, not user-facing)

## Symptom

`mcp-smoke-tests.yml` on `origin/main` (post `ad159590d8` / PR #7498) references a local composite action at `./.github/actions/run-pr-preview-test`. Every smoke run on PRs that branched off `main` BEFORE `ad159590d8` fails the "Resolve deployed preview service URL" step with:

```
##[error]Can't find 'action.yml', 'action.yaml' or 'Dockerfile' under
'/_work/worldarchitect.ai/worldarchitect.ai/.github/actions/run-pr-preview-test'.
Did you forget to run actions/checkout before running your local action?
```

## Affected PRs (as of 2026-06-12)

- **PR #7352** (`feat/dice-audit-alerting-iac`) — base `2cca3481dc`, behind main by 8+ commits
- **PR #7315** (`fix/daily-gemini-wait-for-export`) — branched earlier, missing the action dir

The action was added 2026-06-12 12:16 PDT in commit `c963a0ff83` (PR #7484) and then had its workflow integration polished in `ad159590d8` (PR #7498).

## Reproduction (verified)

```bash
$ git ls-tree 8610bab652fcbb7f9edbbae081540c701223a776 .github/actions/run-pr-preview-test/
# empty — the action dir does NOT exist on PR #7352's tip
$ git ls-tree e08437e0117871a491868bcda90fa01ec4a122c8 .github/actions/run-pr-preview-test/
100644 blob d77f66174f724cf872a0247144f40ca21fe4851c .github/actions/run-pr-preview-test/action.yml
# main has the action
```

Smoke run log reference: 2026-06-13T03:07:12Z (run id 27454614457), self-hosted runner `org-runner-mac-2`, 30+ min after action was added.

## Fix (non-force-push)

Cherry-pick the action (and any needed workflow tweak) onto the branch as a new commit. No force-push required. Example:

```bash
# In a worktree on the PR branch
git fetch origin main
git checkout feat/dice-audit-alerting-iac  # or fix/daily-gemini-wait-for-export
git cherry-pick c963a0ff83                # adds action.yml
# resolve conflicts in mcp-smoke-tests.yml if needed (the .uses reference should match)
git push origin <branch>                   # plain push, no --force
# Re-trigger /skeptic
```

If conflicts on the workflow file: the action reference `./.github/actions/run-pr-preview-test` is the same string the existing workflow uses, so a no-op conflict resolution works.

## Related

- [[project_2026-06-11_dice_audit_3pr_7green_status]] — context on the 3 dice-audit PRs
- [[project_2026-06-11_10pr_rebase_sweep]] — 10-PR rebase pattern that handled similar base-drift issues
- [[feedback_2026-06-11_rebase_clears_presubmit_base_drift]] — rebase clears presubmit base-drift; analogous mechanism
- [[feedback_2026-06-11_workflow_dispatch_requires_ref]] — `ref=main` required for smoke dispatches

## Why it matters

Affecting every open PR that was open before 2026-06-12 12:16 PDT. A clear "incomplete infra migration" pattern: workflow on main was updated to depend on a new path that older branches don't have. A backwards-compat shim (e.g., fallback inlined steps if the action dir is missing) would have avoided this, but now the simplest fix is to bring the action forward on each branch.
