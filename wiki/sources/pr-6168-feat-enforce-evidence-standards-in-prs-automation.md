---
title: "PR #6168: feat: enforce evidence standards in PRs + automation"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldarchitect-ai/pr-6168.md
sources: []
last_updated: 2026-04-09
---

## Summary
Implements 4 improvements to enforce evidence standards across all PRs:

### 1. Improved skeptic-cron evidence request message
- Better message with links to evidence-standards.md
- Specific requirements for terminal vs video evidence
- Example evidence bundle path

### 2. PR Description Validator
- New script: `scripts/validate_pr_evidence.sh`
- Checks PR has: evidence section, terminal recording, test results, git provenance
- Usage: `./scripts/validate_pr_evidence.sh <pr-number>`

### 3. Evid

## Metadata
- **PR**: #6168
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +200/-5 in 4 files
- **Labels**: none

## Connections
