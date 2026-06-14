---
name: pr-files-api-stale-base
description: gh pr view --json files uses original PR base (may be stale); use git diff origin/main for true current scope
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b51e3c06-83e8-4d25-a647-b349db18658c
---

**Rule**: When auditing a PR's scope or checking for unrelated changes, use `git diff origin/main --name-only`, NOT `gh pr view --json files`.

**Why**: The GitHub PR Files API compares against the PR's original base commit, which may be far behind main if main has advanced since the PR opened. This produces false positives — files that look changed in the PR diff but actually match main (they were reverted or main caught up). In the PR #7280 audit, `gh pr view --json files` reported self-hosted-oss and testing_mcp/infra as changed, but `git diff origin/main -- <file>` returned empty for all of them (they matched main). The subagent audit nearly triggered unnecessary reverts based on stale diff data.

**How to apply**:
- Scope audit: `git diff origin/main --stat`
- File existence check for deletions: `git show origin/main:<file>` 
- True unrelated-file check: `git diff origin/main --name-only | grep -v <expected-patterns>`
- GitHub API files: only useful for reviewer navigation; not authoritative for scope analysis

See also [[cleanup-commit-provenance-filter]] for the related deletion safety rule.
