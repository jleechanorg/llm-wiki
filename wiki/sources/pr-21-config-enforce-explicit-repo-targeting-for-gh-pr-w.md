---
title: "PR #21: config: enforce explicit repo targeting for GH PR workflows"
type: source
tags: []
date: 2026-03-03
source_file: raw/prs-worldai_claw/pr-21.md
sources: []
last_updated: 2026-03-03
---

## Summary
- Add hard repo-targeting guardrails to OpenClaw guidance so PR actions always resolve and pin the intended repository.
- Prevent implicit/default-repo `gh` usage for create/edit/merge operations.
- Define wrong-repo remediation workflow (recreate in correct repo, link, close wrong PR).
- Add explicit repo ownership defaults for `worldarchitect.ai`, `worldai_claw`, and `jleechanclaw`.

## Metadata
- **PR**: #21
- **Merged**: 2026-03-03
- **Author**: jleechan2015
- **Stats**: +71/-0 in 2 files
- **Labels**: none

## Connections
