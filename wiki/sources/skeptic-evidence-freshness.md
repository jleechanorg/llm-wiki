# Skeptic Evidence Freshness

**Date**: 2026-05-13
**Source**: PR [#551](https://github.com/jleechanorg/agent-orchestrator/pull/551)

## Rule
Run `ao skeptic verify` only after all non-skeptic CI checks are in terminal state. Before running, verify: evidence SHA matches HEAD, gist content matches diff, no scope-creep files, PR body file count matches actual diff.

## Top Skeptic FAIL Causes (from PR #551, 5 consecutive FAILs)
1. **Stale evidence SHA** — gist referenced old SHA but HEAD had advanced
2. **Scope creep** — files in diff not described in PR scope (wholesome.test.ts)
3. **CI still in-progress** — Bugbot/other checks not terminal when skeptic ran

## Pattern
```
gh pr view <PR> --json statusCheckRollup --jq '.statusCheckRollup[] | select(.status == "IN_PROGRESS" or .status == "QUEUED") | .name'
# If non-empty, wait before running skeptic
```

## Related
- [[pr-551-corepack-shim]] — Corepack pnpm bypass in CI tests
- [[skeptic-false-pass-codex-echo]] — Codex echo matching VERDICT template
