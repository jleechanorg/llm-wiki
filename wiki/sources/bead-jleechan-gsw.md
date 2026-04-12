---
title: "Fix misleading benchmark in benchmark_pair_executors.py"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-gsw"
priority: P2
issue_type: bug
status: open
created_at: 2026-02-19
updated_at: 2026-02-19
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P2] [bug]** Fix misleading benchmark in benchmark_pair_executors.py

## Details
- **Bead ID:** `jleechan-gsw`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-19
- **Updated:** 2026-02-19
- **Author:** jleechan2015
- **Source Repo:** .

## Description

The pair executor benchmark reports a "748x speedup" (v1 avg 2031ms vs v2 avg 2.7ms) but this is misleading. The legacy run includes a hardcoded time.sleep(2) for launch verification (pair_execute.py line 1952: time.sleep(3)). The benchmark's monkey-patch of time.sleep is not fully effective — 2031ms avg is almost exactly 2s + overhead. Meanwhile v2 is pure simulation (no actual agent work). This benchmark measures import/setup time, not pair execution performance. Either properly neutralize the sleep or clearly document that it measures control-plane overhead only.

