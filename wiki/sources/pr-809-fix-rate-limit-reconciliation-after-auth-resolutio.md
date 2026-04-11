---
title: "PR #809: Fix rate limit reconciliation after auth resolution"
type: source
tags: [codex]
date: 2025-11-23
source_file: raw/prs-/pr-809.md
sources: []
last_updated: 2025-11-23
---

## Summary
- refine ConversationAgent rate-limit reconciliation to only rerun checks when a verified identity differs from the preliminary subject, keeping admin bypass while avoiding redundant evaluations
- ensure fallback anonymous identities are created when no auth resolver is present and update tests to explicitly simulate resolver-free deployments
- refresh shared-libs package-lock files from the latest prepare:shared-libs run

## Metadata
- **PR**: #809
- **Merged**: 2025-11-23
- **Author**: jleechan2015
- **Stats**: +1103/-5852 in 9 files
- **Labels**: codex

## Connections
