# Self-Hosted Runner Infra-Flake vs Real Failure

A `(self hosted)` job FAILURE on GitHub Actions may be infrastructure
("runner lost communication with the server") rather than a real test
failure. Always check the annotations endpoint before diagnosing:

```bash
gh api repos/<owner>/<repo>/check-runs/<id>/annotations
```

Infra flake messages include "runner lost communication", "starves it
for CPU/Memory", "blocks its network access". GitHub Actions
auto-retries the job with a new check-run id.

## Monitor pattern
Filter for the LATEST check-run per name (not just any FAILURE):

```bash
real_fails=$(gh api "repos/X/Y/commits/$head/check-runs" --paginate | \
  jq '[.check_runs | group_by(.name)[] |
       sort_by(.started_at) | last |
       select(.conclusion == "failure")] | length')
```

## `gh pr checks` reports `cancelled` jobs as "fail" (PR #7720, 2026-06-20)

`gh pr checks <PR>` collapses a job whose real conclusion is `cancelled`
into the "fail" column. A cancellation is a lifecycle/concurrency event,
NOT a code defect. Before debugging, read the actual per-job conclusion:

```bash
gh run view <run_id> --json status,conclusion,jobs \
  --jq '"\(.status)/\(.conclusion)", (.jobs[]|"\(.name) [\(.conclusion)]")'
```

`cancelled` ≠ `failure`. In PR #7720, mypy showed "fail" in `gh pr checks`
but was `cancelled`; prior HEADs had passed mypy. `gh run rerun <id> --failed`
resolved it. A `deploy-preview` job that fails AFTER an infra-acquisition step
(rotating-pool "Assign server from pool") with expired logs (`BlobNotFound`)
is the same flake class — rerun first, debug only if it fails again with fresh
logs.

### Queued ≠ zero-runner outage
`queued` gates (e.g. Green Gate, Design Doc Gate) usually mean runner
SATURATION, not an outage. Confirm before assuming a stuck pipeline:

```bash
gh api orgs/<org>/actions/runners --jq '.runners[]|"\(.name): \(.status) busy=\(.busy)"'
```

10/10 `online busy=true` → wait for a runner to free; no action needed.
Zero `online` → real outage (see the runner-supervisor source below).

## Related
- [pr7048-location-centralization-merged](../sources/pr7048-location-centralization-merged.md)
- [feedback-2026-06-20-gh-pr-checks-cancelled-shows-fail](../sources/feedback-2026-06-20-gh-pr-checks-cancelled-shows-fail.md) — full PR #7720 drive-to-green triage
- [GreenGateWorkflow](GreenGateWorkflow.md)

## Source
- ~/.claude/projects/-Users-jleechan-projects-worktree-location-centralize/memory/feedback_2026-05-24_distinguish_runner_infra_flake_from_real_failure.md
- [feedback-2026-06-09-runner-supervisor-and-ops](../sources/feedback-2026-06-09-runner-supervisor-and-ops.md) — GH-side `busy=true` corruption on all org-runners (post-cancellation storm) is local-unrecoverable; wait ~1h for GH session-timeout or admin DELETE via `gh api -X DELETE /repos/{owner}/{repo}/actions/runners/{id}`. See also [SelfHostedRunnerNaming](SelfHostedRunnerNaming.md) for the stable-install path requirement.
