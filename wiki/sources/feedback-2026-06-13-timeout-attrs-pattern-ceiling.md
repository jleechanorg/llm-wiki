---
title: "2026-06-13 Timeout Attrs Pattern Ceiling"
type: source
tags: ["feedback", "dark-factory"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_timeout_attrs_pattern_ceiling.md
---

## Summary
The F5/F6 contract-test pattern (extract + assert on existing artifacts + add to canonical allow-list) reached a stable plateau at 4 pipeline families (factory, slim, airbnb-clone, amazon-clone). A 5th is mechanical but adds limited value.

## Key Claims
- The F5/F6 contract-test pattern (PRs #61, #62, #63, #64, #65) extracts a small testable contract, asserts on existing artifacts, and adds the result to a canonical allow-list. It has scaled to 4 pipeline families in dark-factory:
- - factory/ (`pipelines/factory/{gates,pr_gates}.dot`) — PR #62
- - slim/ (`pipelines/slim/{minimal_feature_cs,levelup_pra_validate}.dot`) — PR #63
- - airbnb-clone/ (`benchmarks/airbnb-clone/pipelines/{master,sprint-1/2/3}.dot`) — PR #64
- - amazon-clone/ (`benchmarks/amazon-clone/pipelines/{dark_factory,kilroy,mammoth,slim,smasher,tracker}.dot`) — PR #65
- A 5th family is now <15 min of mechanical work (copy test, scope allow-list, scan for codergen nodes, add timeouts) but the marginal value drops. The 4th family in a single session is the natural ceiling for this pattern.

## Connections
- [[DarkFactory]] — dark-factory pipeline memory
- [[KarpathyWikiPattern]] — wiki-ingest protocol
- Source: `raw/feedback_2026-06-13_timeout_attrs_pattern_ceiling.md`
