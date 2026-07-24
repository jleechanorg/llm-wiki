---
name: jleechanorg-cmux-has-zero-self-hosted-runners-ci-workflows-stay-pending-indefinitely
description: "PRs to jleechanorg/cmux have CI workflows that stay \"pending\" forever because no self-hosted runners are registered; mergeable state is the only reliable gate"
metadata: 
  node_type: memory
  type: reference
  bead: none
  originSessionId: c5b1d462-2cbc-435d-88ea-20932a77e93b
---

# `jleechanorg/cmux` has zero self-hosted runners

## Symptom

Open a PR → `mergeStateStatus` flips UNSTABLE → never moves to CLEAN even though there's no actual conflict. `gh pr checks` shows workflows like `Activation performance` and `CI` stuck in `pending`. `gh run list --branch <branch>` shows `status: pending`, `jobs: []` (no jobs ever created). `gh run view <run-id>` shows the run was created but never picked up.

## Root cause

```bash
$ gh api repos/jleechanorg/cmux/actions/runners
{"total_count":0,"runners":[]}
```

The repo has **zero registered self-hosted runners**. The `.github/workflows/ci.yml` uses `${{ vars.LINUX_RUNNER || 'warp-ubuntu-latest-x64-4x' }}` and `${{ vars.MACOS_RUNNER_15 || 'warp-macos-15-arm64-6x' }}` — those are self-hosted runner labels, not GitHub-hosted runners. With no runners matching those labels, jobs queue forever.

## Workaround for PRs to `jleechanorg/cmux`

`/green` per the cmux-project CLAUDE.md expects CI green + CR approved + mergeable. **CI cannot run for this repo right now.** Practical workflow:

1. **Open the PR** — `gh pr create`. The hermes-pr-tag-listener workflow will fire (it's a separate workflow that doesn't need self-hosted runners).
2. **Wait for `mergeStateStatus: CLEAN`** — this reflects GitHub's branch-protection state, NOT CI status. It clears once the branch has no conflicts with main.
3. **Check `gh pr checks` only for hermes-pr-tag-listener + Bugbot** — the workflows that don't need self-hosted runners.
4. **Skip the "CI green" gate** — explain to the user that the workflow is queued because there are no runners. Per CLAUDE.md "merge safety: explicit approval required": the user's `merge approved` (or `MERGE APPROVED`) literal phrase in the same turn authorizes the merge.
5. **`gh pr merge <N> --squash`** — works even with `pending` checks because mergeable is the actual gate.

## Reusable pattern

When working with a repo whose CI workflows appear stuck:

```bash
gh api repos/<owner>/<repo>/actions/runners | jq '.total_count'
```

If `total_count: 0` and the workflows reference self-hosted labels, the CI is infra-blocked, not PR-blocked. Don't loop waiting for `pending` workflows — explain to the user and ask for `merge approved` if the user is the merge authority.

If you want to actually verify the diff in a real build, run `./scripts/reload.sh --tag <branch-name>` locally — it builds into the same DerivedData path the CI would, AND with the shim-resilience fix it also installs to `/Applications/cmux DEV <branch-name>.app/` so you can manually run the binary.

## References

- cmux CLAUDE.md section "Local dev" — `./scripts/reload.sh --tag <name>` workflow.
- cmux CLAUDE.md section "Merge safety" — explicit approval literal phrases.
- cmux MEMORY entry `feedback_2026-06-28_app-management-tcc-prompt.md` — shim-resilience fix that makes local `reload.sh` builds produce durable `/Applications/` installs.