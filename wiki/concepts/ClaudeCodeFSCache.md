---
title: "Claude Code FSCache Bug"
type: concept
tags: [Claude-Code, Claude-Code-v2, fsnotify, filesystem, bug]
last_updated: 2026-04-06
---

Home-dir workspace scope causes FSEvents overflow, renderer CPU saturation, and terminal I/O starvation on macOS.

## Symptoms

- Home-dir workspace scope causes FSEvents flood
- Language server receives 1500-5680 file changes per batch from broad workspace
- Stalls agent operations
- Renderer CPU saturation
- Terminal I/O starvation

## Root Cause

Broad workspace watch scope (home directory) floods FSEvents with too many change notifications.

## Files Affected

- `~/Library/Application Support/Antigravity/logs/*/window7/renderer.log`
- `~/Library/Application Support/Antigravity/logs/*/window7/exthost/google.antigravity/Antigravity.log`

## Fix

Scope workspace to project directory, not home directory.

## Also Observed

- Gemini quota exhaustion (RESOURCE_EXHAUSTED 429) creates zombie spinners
- Agent stale context on continue (references deleted dirs and 404 PRs)

## Connections

- [[ClaudeCodeSLO]] — Claude Code SLO and compaction
- [[ContextCompaction]] — Claude Code compaction
