---
name: gh pr checks reports cancelled jobs as "fail" — confirm conclusion before treating CI red as a defect
description: PR #7720 drive-to-green — mypy "fail" was actually cancelled; deploy-preview was a pool flake; both fixed by rerun, zero code changes
type: feedback
bead: rev-utdct
---

## Context

Driving PR #7720 (jleechanorg/worldarchitect.ai — iOS WebKit IndexedDB persistence
deadlock fix, merge commit `21cf81df85`) to green. Two CI checks went red. Both
were CI artifacts, not code defects. Recognizing that saved a wasted debug loop.

## Technical detail

1. **`gh pr checks <PR>` reports a job whose real conclusion is `cancelled` as
   "fail".** mypy ("Python Type Checking") showed `fail` in `gh pr checks`, but
   `gh run view <run_id> --json status,conclusion,jobs` revealed
   `concl=cancelled` (whole run cancelled — lifecycle/concurrency). Prior HEADs
   (`4c22f6bc`, `434facda`) had passed mypy, confirming no real type error.
   Remediation: `gh run rerun <id> --failed` → passed.

2. **deploy-preview (rotating Cloud Run pool)** failed at the "Build and Deploy
   PR Preview" step *after* successfully "Assign server from pool", with logs
   already expired (`BlobNotFound` from the job logs API). That post-assignment
   failure + expired logs is the signature of an infra/pool flake. Remediation:
   `gh run rerun <id> --failed` → passed.

3. **Runner saturation ≠ outage.** Green Gate + Design Doc Gate sat in `queued`
   because all 10 org self-hosted runners were `online busy=true` (10/10), not
   because zero runners were online. Check with
   `gh api orgs/jleechanorg/actions/runners --jq '.runners[]|"\(.name): \(.status) busy=\(.busy)"'`.
   Queued gates clear themselves as runners free; no action needed.

## Rule

Before treating a red `gh pr checks` line as a code defect:
- Run `gh run view <run_id> --json status,conclusion,jobs` and read the *actual*
  per-job `conclusion`. `cancelled` ≠ `failure`.
- For a job that failed at/after an infra-acquisition step (pool assignment,
  deploy) with expired logs, `gh run rerun <id> --failed` first; only debug code
  if it fails again with fresh, readable logs.
- `queued` is a runner-availability state; confirm runner count before assuming
  a stuck/zero-runner outage.

## Wiki reconciliation (open follow-up)

The wiki source `sources/pr7720-ios-webkit-indexeddb-persistence-deadlock.md`
and its concept pages describe the fix as
`Object.defineProperty(window,'indexedDB',{configurable:false,...})`. The MERGED
PR head reverted to `configurable: true` (merged `mvp_site/frontend_v1/auth.js`
line 41) to align with the proven/deployed HTTP-capture evidence (the `false`
version's capture was stale). Wiki should be reconciled to merged reality.
See [[pr7720-ios-webkit-indexeddb-persistence-deadlock]].

## Verification

- `gh pr checks 7720`: 27 passed / 0 failed after two reruns.
- `gh pr view 7720 --json mergeable,mergeStateStatus` → `MERGEABLE / CLEAN`.
- Merge `21cf81df85` present in `origin/main`; integrate.sh created
  `dev1781998093` tracking `origin/main`.

## Reusable pattern

CI red triage order: (1) read actual job `conclusion` via `gh run view --json`,
(2) cancelled/flake → rerun, (3) only then debug code. Distinguish runner
saturation (`queued` + busy runners) from outage (zero online runners).
