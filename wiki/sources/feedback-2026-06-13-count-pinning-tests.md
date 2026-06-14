---
title: "2026-06-13 Count Pinning Tests"
type: source
tags: ["feedback", "dark-factory"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_count_pinning_tests.md
---

## Summary
A test that asserts a count (e.g., \

## Key Claims
- When shipping a contract test for a multi-instance structure (e.g., one pipeline per sprint, one node per stage), also ship a count-pinning test that asserts the EXPECTED count of instances. The pattern is:
- def test_codergen_count_is_stable() -> None:
- n = sum(1 for ... if node_type == "codergen")
- assert n == EXPECTED, "if you added an X, update the contract test too"
- 1. Any time you ship a contract test for a multi-instance structure (per-sprint, per-stage, per-foo), add a count-pinning test alongside it.
- 2. The count-pinning test reads as documentation: "this is the expected count, and the count is the contract."

## Connections
- [[frozen-set-allow-list-as-contract]]
