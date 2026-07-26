---
title: "EvidenceHarnessDiscipline"
type: concept
tags: [dk2d-chrono]
date: 2026-07-14
last_updated: 2026-07-14
---

Evidence-capture pipelines have their own failure modes distinct from the system under test: (1) CLI flags may be accepted-and-ignored — verify CONSUMPTION via the tool's own output (header/paths), never mere acceptance; (2) write primary evidence to janitor-safe storage from the first byte — the /tmp janitor deletes files MID-RUN, not just between runs; (3) in STRICT gate modes, distinguish `pass: null` (unmeasurable this run, e.g. zero dice sampled) from `pass: false` (regression) before classifying a failure; (4) capture timeouts must be budgeted against the slowest legitimate operation (wc-pk9z: coordinated 120s turn budget) and aborts must preserve partial evidence.

Source: [[feedback-2026-07-14-dk2d-chrono-operational-lessons]] · Related: [[DragonKnight2D]]
