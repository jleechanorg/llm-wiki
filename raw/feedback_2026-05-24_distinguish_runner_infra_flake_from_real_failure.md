---
name: Self-hosted runner infra flakes show as CheckRun FAILURE — must distinguish from real test failures
description: A "Directory tests (core-mvp-N(self hosted))" FAILURE may be `runner lost communication`; the GitHub annotations endpoint reveals the cause. Auto-retry handles it.
type: feedback
bead: rev-igs3c
---

This session: `Directory tests (core-mvp-2(self hosted))` FAILED in mid-run
on PR #7048. The `gh run view --log-failed` returned empty (because the run
was still in progress overall). The actual cause was visible via the
check-run annotations endpoint:

```bash
gh api repos/<owner>/<repo>/check-runs/<job-id>/annotations
# returned: "The self-hosted runner lost communication with the server.
#  Verify the machine is running and has a healthy network connection."
```

Not a test failure — pure infrastructure flake. GitHub Actions auto-retried
the job within seconds (new job id, same check name). The retry passed
cleanly.

**How to apply:**
- When a self-hosted CI job FAILS, always check
  `gh api repos/X/Y/check-runs/<id>/annotations` BEFORE diagnosing test logic.
- "runner lost communication" / "starves it for CPU/Memory" annotations are
  infra flakes — wait for the auto-retry, don't push a fix commit.
- Monitor loops watching for "real failures" should compute the LATEST check-run
  per name (not just count any FAILURE), since the retry will land as a new
  check-run with the same name.

**Pattern (reusable monitor query):**
```bash
data=$(gh api "repos/X/Y/commits/$head/check-runs" --paginate)
real_fails=$(echo "$data" | jq '[.check_runs |
  group_by(.name)[] | sort_by(.started_at) | last |
  select(.conclusion == "failure")] | length')
# real_fails > 0 iff the LATEST run for any check-name name is failure.
```

Related: [[7green-proof-artifact]]
