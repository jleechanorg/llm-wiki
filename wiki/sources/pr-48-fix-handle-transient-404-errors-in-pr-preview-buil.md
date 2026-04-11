---
title: "PR #48: fix: Handle transient 404 errors in PR preview build polling"
type: source
tags: []
date: 2025-11-02
source_file: raw/prs-/pr-48.md
sources: []
last_updated: 2025-11-02
---

## Summary
Fixes HIGH severity issue where the PR preview build polling loop could fail on transient 404/NOT_FOUND responses from Cloud Build API immediately after async submit.

## Metadata
- **PR**: #48
- **Merged**: 2025-11-02
- **Author**: jleechan2015
- **Stats**: +9/-1 in 1 files
- **Labels**: none

## Connections
