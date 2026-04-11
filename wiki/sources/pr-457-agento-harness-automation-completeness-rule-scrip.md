---
title: "PR #457: [agento] harness: automation completeness rule — scripts must have callers"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-457.md
sources: []
last_updated: 2026-03-31
---

## Summary
PR #454 added staging-canary.sh with 6 checks but never wired it into CI. The canary existed on disk but prevented nothing because no automatic process called it. Root cause tracked in orch-dv6.

The deeper failure: even without Slack context, an agent should verify 'who calls this?' before declaring an automation task done. No harness rule existed to enforce this.

## Metadata
- **PR**: #457
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +49/-58 in 2 files
- **Labels**: none

## Connections
