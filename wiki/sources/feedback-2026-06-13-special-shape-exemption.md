---
title: "2026-06-13 Special Shape Exemption"
type: source
tags: ["feedback", "dark-factory"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_special_shape_exemption.md
---

## Summary
When writing a contract test that pins

## Key Claims
- When pinning the contract "every codergen node has a non-empty prompt"
- (or any other codergen-specific attribute), the test must mirror the
- engine's handler dispatch — which means exempting special shapes that
- | Shape | Handler | Why exempt |
- | `point` (width=0, height=0) | none | Topology anchor (e.g. `_base.dot`'s `explore_in`/`explore_out`); never reached by `_codergen` |
- | `component` (no explicit type) | parallel | Fan-out node; engine handles via the parallel branch |

## Connections
- [[DarkFactory]] — dark-factory pipeline memory
- [[KarpathyWikiPattern]] — wiki-ingest protocol
- Source: `raw/feedback_2026-06-13_special_shape_exemption.md`
