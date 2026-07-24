---
title: "Sidekick same-name respawn races with pending shutdown, duplicate concurrent workers"
type: source
tags: [sidekick, swarm, orchestration, harness-durability]
date: 2026-07-07
source_file: raw/feedback_2026-07-07_sidekick_same_name_respawn_race.md
---

## Summary

Sending a `shutdown_request` to a named sidekick teammate and then immediately spawning a new, unrelated mission under the same teammate name can race with the (asynchronous) shutdown approval. In this incident, reusing the name before confirmation produced two concurrent workers on the same mission, both writing to shared scratch files under the same `/tmp` mission directory. No data corruption resulted — the synthesis step independently re-derived numbers from raw data, and the duplicate instance self-detected the collision via interleaved STATE.md Progress Log entries and voluntarily stood down — but this was self-correction, not a structural guarantee.

## Key Claims

- Teammate `name` is tied to a reusable slot/session, not a fresh isolated process per spawn — a new `Agent()` call with the same `name` can return the SAME underlying `agent_id`/session as a just-shut-down teammate.
- `shutdown_request` → `shutdown_approved` is asynchronous; there is a window where the old teammate may still be alive and working even after a shutdown request was sent.
- No live-lock or namespaced output path exists today for concurrent sidekick spawns sharing a mission's scratch directory.

## Key Quotes

> "My own dispatched work ... ran in parallel and mostly duplicated theirs ... my Mac-mining sub-agent's write clobbered their earlier, more carefully-corrected Mac total (32.59B in-window vs my raw 40.9B) — worth a harness-durability fix later (live-lock + namespaced output paths for concurrent sidekick spawns), not urgent." — the duplicate "sidekick" instance's own self-report

## Connections

- [[mcp-tool-search-default-and-config-dir-trap]] — a separate finding from the same session
- [[sidekick-pattern]] — the broader Devin-sidekick orchestration pattern this is a durability gap within
