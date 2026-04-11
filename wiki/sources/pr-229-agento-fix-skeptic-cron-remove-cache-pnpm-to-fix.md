---
title: "PR #229: [agento] fix(skeptic-cron): remove cache: pnpm to fix workflow step ordering"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-229.md
sources: []
last_updated: 2026-03-27
---

## Summary
The `skeptic-cron.yml` workflow has been failing on every run since it was introduced. All recent runs show `failure` status, consistently failing at the "Install Node.js" step with:

\`\`\`
##[error]Unable to locate executable file: pnpm.
\`\`\`

## Metadata
- **PR**: #229
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +95/-5 in 6 files
- **Labels**: none

## Connections
