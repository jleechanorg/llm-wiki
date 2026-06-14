---
title: "gh pr view --json files uses original base, may be stale"
type: source
tags: [gh-cli, pr-files-api, stale-base, scope-audit, worldarchitect-ai]
date: 2026-06-08
source_file: raw/feedback_2026-06-08_pr_files_api_stale_base.md
---

## Summary
When auditing a PR's scope or checking for unrelated changes, use 'git diff origin/main --name-only', NOT 'gh pr view --json files'. The GitHub PR Files API compares against the PR's original base commit, which may be far behind main if main has advanced since the PR opened. This produces false positives — files that look changed in the PR diff but actually match main (they were reverted or main caught up). In the PR #7280 audit, gh pr view --json files reported self-hosted-oss and testing_mcp/infra as changed, but git diff origin/main returned empty for all of them.

## Key Claims
- GitHub PR Files API compares against PR's original base commit, may be far behind main if main advanced since PR opened
- PR #7280 audit: gh pr view --json files reported self-hosted-oss and testing_mcp/infra as changed, but git diff origin/main returned empty for all of them
- Use: git diff origin/main --stat for scope audit; git show origin/main:<file> for deletion existence check; git diff origin/main --name-only | grep -v for true unrelated-file check

## Connections
- [[cleanup-commit-provenance-filter]]
- [[PrFilesApiStaleBase]]
- [[ScopeAuditMethod]]
