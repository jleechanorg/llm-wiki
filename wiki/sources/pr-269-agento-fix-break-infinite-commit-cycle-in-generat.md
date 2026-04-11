---
title: "PR #269: [agento] fix: break infinite commit cycle in generate-pr-design-docs.yml"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-269.md
sources: []
last_updated: 2026-03-29
---

## Summary
The `generate-pr-design-docs.yml` workflow fires on `pull_request.synchronize`, generates design docs, commits them as `github-actions[bot]`, which triggers another `synchronize` event → infinite commit loop. This is P0 blocking PR #259.

The existing `github.actor != 'github-actions[bot]'` check in the job `if:` condition doesn't catch this because `github.actor` reflects the user who triggered the workflow (the PR author who pushed), not the commit author.

## Metadata
- **PR**: #269
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +237/-0 in 3 files
- **Labels**: none

## Connections
