---
title: "Keynote deck build — two lessons"
type: source
tags: [keynote, gog-cli, google-slides, harness-lessons]
date: 2026-08-25
source_file: raw/2026-08-25-keynote-deck-build-lessons.md
---

## Summary

Two harness-level lessons captured while building [[WorldAI]]'s presenter
[[Jeffrey]]'s "Develop at Idea Velocity" keynote deck for the Agentic AI
Summit LA talk, via `gog` CLI against a live Google Slides presentation. Both
lessons were corrections from the user mid-session, not self-discovered.

## Key Claims

- When the goal is backing up a rendered artifact (not editing it further), a
  render/export of the live output is strictly better than reconstructing a
  lost editable source — it can't drift from the shipped, already-verified
  result the way a reconstruction can.
- `gog slides export --format pdf` + `pdftoppm -png -r 150` produced a full
  connector-arrow-intact backup of an architecture diagram in two commands,
  after a pixel-histogram CSS reconstruction lost that same geometry.
- Categorization claims need the same traceability discipline as numeric
  claims: verify against the source's own section/module boundary before
  writing a summary, rather than trusting how content superficially reads.
- A real miscategorization: WorldAI's own engine internals (query-aware
  routing, token-budget context design, call avoidance) were mislabeled as
  generic "dev workflow" material in a conference-abstract draft, when the
  deck's own agenda already placed them under "WorldAI, in depth."

## Key Quotes

> "just screenshot it" — the user's correction that ended a costly source
> reconstruction

> "uh are you stupid. this is the worldai stuff, dev workflow is other
> slides" — the categorization correction

## Connections

- [[WorldAI]] — the product the keynote deck promotes; its own engine
  internals (routing, context budget, dice/faction call structure) were the
  subject of the categorization-lesson incident
- [[Jeffrey]] — presenter; the deck build was for his 2026-08-26 keynote talk
