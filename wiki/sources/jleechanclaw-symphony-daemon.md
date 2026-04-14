---
title: "jleechanclaw-symphony-daemon"
type: source
tags: [jleechanclaw, symphony, launchd, workflow]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/symphony_daemon.py
---

## Summary
Helpers for provisioning a launchd-managed Symphony daemon. Builds workflow YAML for Symphony's memory tracker, generates runner bash scripts with mise/exec pattern, and creates launchd plist dictionaries. Explicitly pins Symphony to codex app-server command.

## Key Claims
- build_workflow creates YAML with memory tracker, 1s polling interval, workspace root, max 1 concurrent agent, max 4 turns
- codex command pinned to "codex app-server" with 120s read timeout, never approval policy
- build_runner_script uses mise exec -- epmd -daemon then symphony with --port and --i-understand-that-this-will-be-running-without-the-usual-guardrails flag
- build_launch_agent returns a dict suitable for launchd plist with RunAtLoad and KeepAlive True

## Connections
- [[jleechanclaw-symphony-plugins]] — related Symphony integration

## Contradictions
- None identified