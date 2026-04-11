---
title: "PR #6191: docs(evidence): /er + /es as thin aliases, evidence-review skill, clean-computer rule"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6191.md
sources: []
last_updated: 2026-04-11
---

## Summary
While fixing PR #6161 (rewards_box atomicity), the browser GIF in the PR description was broken — it linked to a release asset on the **private** \`worldarchitect.ai\` repo, which returns 404 for anonymous viewers and does not render as an inline image in GitHub PR descriptions. This exposed three harness gaps:

1. No rule that GIF/MP4 hosting must be on a **public** repo
2. No explicit "self-contained" requirement (a stranger on a clean computer should be able to reproduce)
3. The \`/er\` slash

## Metadata
- **PR**: #6191
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +313/-39 in 4 files
- **Labels**: none

## Connections
