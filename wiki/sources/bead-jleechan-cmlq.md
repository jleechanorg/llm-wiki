---
title: "task_engine: add ClaudeProvider / SubprocessProvider for real inference"
type: source
tags: ["feature", "p2", "bead"]
bead_id: "jleechan-cmlq"
priority: P2
issue_type: feature
status: open
created_at: 2026-02-21
updated_at: 2026-02-21
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P2] [feature]** task_engine: add ClaudeProvider / SubprocessProvider for real inference

## Details
- **Bead ID:** `jleechan-cmlq`
- **Priority:** P2
- **Type:** feature
- **Status:** open
- **Created:** 2026-02-21
- **Updated:** 2026-02-21
- **Author:** jleechan2015
- **Source Repo:** .

## Description

task_engine only has MockProvider — cannot dispatch real tasks. Need either ClaudeProvider (wraps anthropic SDK, ~30 lines) or SubprocessProvider (calls `claude` CLI via subprocess, ~20 lines) to enable real agent task execution against .claude/agents configs.

