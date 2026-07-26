---
title: "DK2D CHRONO mission operational lessons — 5 generalizable failure classes (2026-07-14)"
type: source
tags: [evidence-harness, cli-flags, tmp-janitor, llm-provider-scheduling, sprite-pipeline, agent-governance]
date: 2026-07-14
source_file: raw/feedback_2026-07-14_dk2d_chrono_operational_lessons.md
last_updated: 2026-07-14
---

## Summary

Operational lessons from the DK2D CHRONO mission (2026-07-13/14), which unified the Dragon Knight 2D game onto the game2d LPC engine that was already present in the same source tree and sealed 15/15 harness gates at HEAD c26bd3d8. Five failure classes generalize beyond the project: silently-ignored CLI flags, mid-run /tmp janitor destruction, LLM-provider time-of-day scheduling, art-pipeline fake-alpha/quantizer defects, and a stop-hook vs autonomy-time-box governance dispute.

## Key Claims

- A CLI flag that runs without error may be silently ignored: `run_dk2d_evidence.py --out` was accepted-and-ignored for 3 runs (argv only scanned for `--partial`). Verify flag CONSUMPTION via the tool's own output, never acceptance. Fixed same day: `--out` wired as `DK_EVID` alias, unknown flags now FATAL.
- The /tmp janitor destroys evidence MID-RUN, not just between runs: it deleted `static_frames/f0143.png` while the harness's imagehash pass was reading the sequence, producing a false gate failure. Evidence pipelines must write janitor-safe from the first byte.
- MiniMax long-generation (2-6k char) streams hang >120s overnight PT while short turns stay at ~2.05s first-token (run trend 15/15 → 13 → 13 → 14 → 10 overnight; 14 → 14 → 15 morning). Schedule real-LLM evidence runs morning/midday PT. A STRICT harness fails runs on `pass: null` gates — null-sampled (e.g., GM rolled zero dice) is not a regression.
- Grok bakes "translucency" as RGB blends WITH its own magenta background (no real alpha), and PIL median-cut quantization AFTER keying remaps edge pixels back onto magenta palette entries. Fix pattern: hue-FAMILY channel test (G clearly below both R and B, R≈B) at every pipeline stage, key BEFORE quantize, re-verify final shipped bytes at zoom.
- When a session Stop-hook goal collides with an expired autonomy time-box: never route the disputed action through a refusing agent (permission laundering); own it from the seat with the authority claim; record BOTH readings in the mission file; hand the user a concrete kill switch.

## Key Quotes

> "Ran without erroring proves nothing — most hand-rolled arg scanners ignore unknown flags."

> "A run that both writes and reads /tmp within ~15 minutes is still vulnerable."

> "Outcome resolved it (15/15 seal) without either agent capitulating."

## Connections

- [[WorldArchitectAI]] — sibling project whose game-loop contract DK2D mirrors
- [[DragonKnight2D]] — the game this mission sealed (engine unification, coda system)
- [[EvidenceHarnessDiscipline]] — janitor-safe output, gate-null vs gate-fail, flag-consumption verification
- [[LLMProviderWindowScheduling]] — time-of-day scheduling for real-LLM evidence runs
- [[SpriteChromaKeyPipeline]] — fake-alpha magenta blends + quantizer resurrection defects
- [[AgentGovernanceDisputes]] — stop-hook vs time-box protocol, permission laundering boundary
