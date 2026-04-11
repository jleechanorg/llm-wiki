---
title: "PR #5767: CI: use single self-hosted runner label"
type: source
tags: []
date: 2026-02-25
source_file: raw/prs-worldarchitect-ai/pr-5767.md
sources: []
last_updated: 2026-02-25
---

## Summary
- Remove extra runner labels (claude/macOS/ARM64/ubuntu) from self-hosted jobs in impacted workflows.
- Keep fallback-to-GitHub-hosted logic unchanged.
- Update workflow docs/examples to match current label strategy.

This avoids pending queue due to label mismatch on older online runners.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> CI-only change that relaxes runner selection constraints; main risk is self-hosted jobs may land on an unintended runner if multiple self-hosted runners

## Metadata
- **PR**: #5767
- **Merged**: 2026-02-25
- **Author**: jleechan2015
- **Stats**: +13/-13 in 9 files
- **Labels**: none

## Connections
