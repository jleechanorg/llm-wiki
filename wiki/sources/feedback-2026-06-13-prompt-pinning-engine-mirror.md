---
title: "2026-06-13 Prompt Pinning Engine Mirror"
type: source
tags: ["feedback", "dark-factory"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_prompt_pinning_engine_mirror.md
---

## Summary
When writing a unit test for a resolver

## Key Claims
- When writing a unit test that pins a resolver's path lookup, the helper
- version of it. The F6h prompt-pinning test initially resolved
- `@<ref>` against the .dot file's directory only. The engine's real
- resolver (`runner.handlers._render_prompt`) tries **workdir-relative
- first, then `factory_home()`-relative**. airbnb-clone's
- `@benchmarks/airbnb-clone/prompts/sprint-1-plan.md` paths are

## Connections
- [[DarkFactory]] — dark-factory pipeline memory
- [[KarpathyWikiPattern]] — wiki-ingest protocol
- Source: `raw/feedback_2026-06-13_prompt_pinning_engine_mirror.md`
