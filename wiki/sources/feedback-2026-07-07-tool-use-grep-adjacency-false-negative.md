---
title: "tool_use grep adjacency false-negative — '0 usage' claims were wrong"
type: source
tags: [claude-code, mcp, methodology, adversarial-review]
date: 2026-07-07
source_file: raw/feedback_2026-07-07_tool_use_grep_adjacency_false_negative.md
---

## Summary

A grep pattern assuming `"type":"tool_use","name":"mcp__X__` are adjacent in serialized JSONL transcript lines silently misses the common case where an `"id"` field sits between them, producing false "0 usage" results. This bug drove real removal decisions in a 2026-07-07 MCP cleanup session — ios-simulator-mcp (279 real calls) and playwright-mcp (221 real calls) were removed from Claude Code config based on wrong "confirmed 0 usage" claims. Caught by dispatching an adversarial `codex` CLI reviewer instructed to verify every claim against real files rather than trust the report.

## Key Claims

- Only `context7` turned out to be a genuine 0-usage server; every other "0 usage" claim made with the broken grep was wrong.
- Fix: use a JSON parser (or a regex allowing arbitrary fields between the two keys) rather than an adjacency-assuming grep, especially when the result will drive a deletion/removal decision.
- Verify any "0 result" grep pattern against a known-true-positive case before trusting negative results elsewhere.

## Connections

- [[claude-code-mcp-tool-search]] — the broader MCP cleanup session this bug surfaced within
- [[sidekick-pattern]] — a separate harness-durability finding from the same day's work
