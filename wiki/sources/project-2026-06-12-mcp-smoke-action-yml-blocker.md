---
title: "PR #7352 / #7315 mcp-smoke action.yml blocker — missing composite action on older branches"
type: source
tags: [ci-blocker, mcp-smoke, composite-actions, pr-7352, pr-7315, worldarchitect, branch-drift]
date: 2026-06-12
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-12_mcp_smoke_action_yml_blocker.md
last_updated: 2026-06-12
---

## Summary
After PR #7498 (`ad159590d8`) updated `mcp-smoke-tests.yml` to reference a new local composite action at `./.github/actions/run-pr-preview-test`, every open PR that branched from main before 2026-06-12 12:16 PDT fails the "Resolve deployed preview service URL" step with `Can't find 'action.yml'`. PRs #7352 and #7315 were confirmed affected. Fix is a no-force-push cherry-pick of the action onto the branch.

## Key Claims
- `mcp-smoke-tests.yml` on main now depends on `./.github/actions/run-pr-preview-test` (added in `c963a0ff83`, PR #7484; workflow integration polished in `ad159590d8`, PR #7498)
- Branches that don't carry the action dir produce the error `##[error]Can't find 'action.yml'...` even after a fresh `actions/checkout`
- Cherry-picking `c963a0ff83` (or its action dir) onto the branch is a no-force-push fix; conflict resolution on the workflow file is typically a no-op because the `.uses` path is unchanged
- The failure mode is "incomplete infra migration" — main was updated to depend on a path older branches don't have; a backwards-compat shim was not added

## Key Quotes
> "Every smoke run on PRs that branched off `main` BEFORE `ad159590d8` fails the 'Resolve deployed preview service URL' step" — symptom description

> "git ls-tree 8610bab652fcbb7f9edbbae081540c701223a776 .github/actions/run-pr-preview-test/ # empty — the action dir does NOT exist on PR #7352's tip" — reproduction proof

## Connections
- [[PostMergeFollowupWorkflow]] — same class of branch-drift hazard; bring infra forward to the branch
- [[WorktreeWorkflow]] — fix recipe uses a worktree, `git fetch origin main`, then `git checkout <branch>` + cherry-pick
- [[AOSkepticGateOps]] — re-trigger `/skeptic` after fix; the verifier is the gate that fails on the missing action
- [[AOSpawnGate]] — analogous pre-spawn check: verify infra paths exist on the branch before relying on them
