---
title: "dark-factory gate_es: head_sha echo required — outcome=error if missing"
type: source
tags: [dark-factory, gate-es, evidence-standards, head-sha-binding, ci]
date: 2026-06-24
source_file: raw/feedback_2026-06-24_dark_factory_gate_es_head_sha_echo_required.md
---

## Summary

When dark-factory routes `gate_es` through `_slash_gate("es")` (triggered when `.claude/commands/es.md` exists), the Claude agent running `/es` must include `head_sha: <sha>` explicitly in its response. `_verify_head_sha_echo()` in `handler_dispatch.py` checks for this line; if absent, `outcome` is set to `"error"` regardless of any `verdict: pass` text. Retry resolves in most cases — the agent includes the echo on the next attempt. Discovered during dark-factory run `762b6d1df955` for PR #7871.

## Key Claims

- `_slash_gate("es")` adds a machine contract requiring `head_sha: <sha>` echo in the response
- `_verify_head_sha_echo()` returns `(False, "")` if the line is absent
- `_run_gate_once()`: `if not sha_ok: outcome = "error" if normalized in ("success", "unknown") else normalized`
- A PASS verdict with no SHA echo → `normalized = "success"` → `outcome = "error"` (not "success")
- In run `762b6d1df955`: seq 16 and 20 failed (PASS text, no echo), seq 24 succeeded (explicit `head_sha:` line)
- This is intentional — prevents stale-SHA gate results from being accepted as valid

## Key Quotes

> Attempts 1 and 2: agent produced "**Overall verdict: PASS**" without head_sha line → outcome:error
> Attempt 3: agent included head_sha: 19f5ce3543cb355eb7fd79c896f9d8a7ce5087ff → outcome:success

## Connections

- [[DarkFactoryGatePattern]] — gate_es / gate_er routing and SHA binding mechanism
- [[EvidenceStandards]] — the /es command this gate invokes
