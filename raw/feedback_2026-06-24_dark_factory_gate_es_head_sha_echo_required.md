---
name: dark-factory-gate-es-head-sha-echo-required
description: "dark-factory gate_es via _slash_gate(\"es\") requires explicit head_sha echo — outcome=error if missing even when verdict is PASS"
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: cbf71cb9-9eec-4fef-b34b-20233fa240dc
---

## Rule

When dark-factory routes `gate_es` through `_slash_gate("es")` (because `.claude/commands/es.md` exists in the repo), the Claude agent running `/es` MUST include the exact line:

```
head_sha: <40-char SHA>
```

at the top (or anywhere) in its response. If this line is absent, `_verify_head_sha_echo()` returns `(False, "")`, and `_run_gate_once()` sets `outcome = "error"` regardless of any `verdict: pass` text in the response.

**Why:** `_run_gate_once` in `handler_dispatch.py`:
```python
sha_ok, observed_sha = _handlers_shim._verify_head_sha_echo(combined, expected_sha)
if not sha_ok:
    outcome = "error" if normalized in ("success", "unknown") else normalized
```

A PASS verdict with no SHA echo → `normalized = "success"` → `outcome = "error"`.

## Pattern

In PR #7871 dark-factory run `762b6d1df955`:
- Attempts 1 and 2 (seq 16, 20): agent produced "**Overall verdict: PASS**" without `head_sha:` line → `outcome: error`
- Attempt 3 (seq 24): agent included `head_sha: 19f5ce3543cb355eb7fd79c896f9d8a7ce5087ff` at the top → `outcome: success`

## How to apply

If gate_es returns `outcome: error` in dark-factory but the transcript shows "PASS" verdict text — check for missing `head_sha:` echo. The `/es` command's machine contract requires it for the SHA binding check. The `/es` command prompt instructs the agent to include it, but some agent invocations omit it.

**This is expected dark-factory behavior** — the SHA binding check exists to prevent stale-SHA gate results from being accepted. If the agent omits it, retry; the next attempt usually includes it.

**References**: PR #7871, dark-factory run `762b6d1df955`, transcripts `16_gate_es_1.txt`, `20_gate_es_1.txt` (error), `24_gate_es_1.txt` (success). `handler_dispatch.py:_run_gate_once`, `handler_universal_prompts.py:_slash_gate`.
