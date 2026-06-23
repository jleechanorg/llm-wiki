---
title: "Green Gate Gate-8 requires real-mode smoke tests"
type: source
tags: [worldarchitect, ci, gate-8, smoke-tests, green-gate]
date: 2026-06-23
source_file: raw/feedback_2026-06-23_gate8_requires_real_smoke_mode.md
last_updated: 2026-06-23
---

## Summary

`mcp-smoke-tests.yml` defaults `test_mode` to `mock`. Green Gate Gate-8 requires `<!-- mcp-smoke-mode: real -->` in the PR smoke comment. Always pass `-f test_mode=real` when dispatching smoke tests to satisfy Gate-8.

## Key Claims

- Default `workflow_dispatch` of `mcp-smoke-tests.yml` uses mock mode → Gate-8 FAIL.
- Gate-8 message when wrong mode: "GATE-8 FAIL: exact mcp-smoke-tests succeeded in MOCK mode — run /smoke for real-service coverage"
- Fix: `gh workflow run mcp-smoke-tests.yml --ref <branch> -f pr_number=<N> -f test_mode=real`
- Real mode takes ~24 min (3 providers × ~8 min).

## Connections

- [[worldarchitect-ai]] — repo
- [[green-gate]] — workflow that enforces Gate-8
