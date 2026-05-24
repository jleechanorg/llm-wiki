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

## Related
- [[pr7048-location-centralization-merged]]

## Source
- ~/.claude/projects/-Users-jleechan-projects-worktree-location-centralize/memory/feedback_2026-05-24_distinguish_runner_infra_flake_from_real_failure.md
