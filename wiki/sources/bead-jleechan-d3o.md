---
title: "Add launcher smoke checks for Darwin terminal-spawn and logging behavior"
type: source
tags: ["task", "p2", "bead"]
bead_id: "jleechan-d3o"
priority: P2
issue_type: task
status: open
created_at: 2026-02-20
updated_at: 2026-02-20
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P2] [task]** Add launcher smoke checks for Darwin terminal-spawn and logging behavior

## Details
- **Bead ID:** `jleechan-d3o`
- **Priority:** P2
- **Type:** task
- **Status:** open
- **Created:** 2026-02-20
- **Updated:** 2026-02-20
- **Author:** jleechan2015
- **Source Repo:** .

## Description

Current launcher changes were not protected by an automated smoke test for Darwin branch behavior. Add test coverage (or script-level self-check mode) to validate temp-script creation, terminal command construction, and fallback behavior without manual debugging.

