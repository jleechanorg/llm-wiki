---
title: "PR #6269 — Port CR Fallback Logic to Skeptic Gates"
type: source
tags: [CI, skeptic, workflow, green-gate, CodeRabbit]
date: 2026-04-14
source_file: ../raw/pr6269_port_cr_fallback_skeptic_gates_2026-04-14.md
---

## Summary
Ports CodeRabbit (CR) fallback logic to Skeptic Gates in worldarchitect.ai. Adds retry/fallback behavior when CR is unavailable or returns unexpected responses.

## Files Changed (4 files, +88/-28)
- `.github/scripts/skeptic-evaluate.sh` — +2/-2
- `.github/workflows/green-gate.yml` — +23/-10
- `.github/workflows/skeptic-cron.yml` — +15/-6
- `.github/workflows/skeptic-gate.yml` — +48/-10

## Key Changes
- CR fallback logic: if CR review is unavailable, fall back to skeptic evaluation
- Retry mechanism for CR webhook responses
- Improved error handling for CR API errors

## Connections
- [[SkepticGate]] — the gate receiving the CR fallback logic
- [[GreenGateWorkflow]] — green-gate workflow updated
- [[CodeRabbitDismissedPattern]] — CR DISMISSED pattern (CR dismissed requires substantive push to re-trigger)
- [[AutorPR]] — autor PRs are evaluated by SkepticGate
