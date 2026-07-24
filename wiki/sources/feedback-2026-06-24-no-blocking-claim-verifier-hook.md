---
title: "No blocking claim-verifier hook — /advice verdict 2026-06-24"
type: source
tags: [worldarchitect, hooks, advice, false-positive, agent-discipline]
date: 2026-06-24
source_file: raw/feedback_2026-06-24_no_blocking_claim_verifier_hook.md
---

## Summary

Two convergent reviews (Opus subagent high confidence + research medium confidence) reached the same verdict: **do NOT ship a blocking PreToolUse hook that scans agent output for "X is working" claim phrases**. The 4-layer harness fix (Instructions + Memory + Skill + Test) handles the WORLDAI_TEST_CACHE false-claim class durably at the right layer.

## Why Not a Blocking Hook

| Concern | Impact |
|---|---|
| Frequency | Hook fires on every SendMessage (5-20x/session) |
| False-positive floor | "is enabled" / "is ready" / "is active" match normal agent prose constantly |
| Probe detection | Grep on tool output history is brittle (tool formats vary) |
| Quota cost | Blocking burns retries; trains user to disable hook |
| Maintenance | Brittle — every new feature requires new phrase list |

Anthropic's hooks docs explicitly recommend `additionalContext` advisory over blocking. The repo's own evolution from `detect_speculation_and_fake_code.sh` (substring → brittle) to `smart_fake_code_detection.sh` (LLM auditor → advisory) is the case study.

## What to Ship Instead (already done 2026-06-24)

| Layer | File | Status |
|---|---|---|
| Instructions | `~/.claude/CLAUDE.md` | shipped |
| Memory (existing strengthened) | `feedback_2026-06-24_worldai_test_cache_never_activated_root_cause.md` | shipped |
| Memory (new generalization) | `feedback_2026-06-24_runtime_activation_claim_required.md` | shipped |
| Skill | `~/.claude/skills/runtime-activation-claim/SKILL.md` | shipped |
| Test (contract) | `testing_mcp/test_multi_gate_activation_contract.py` | shipped |
| Test (probe) | `testing_mcp/harness_runtime_activation_probe.py` | shipped |

## When to Ship a Hook (if ever)

Only if the false-claim pattern recurs AFTER the 4-layer fix has been in production for a week. When/if shipped:

- Use `additionalContext` pattern, never block.
- Modeled on existing `smart_fake_code_detection.sh`: always exit 0, reuse an LLM auditor, inject findings as stderr.
- Per-session opt-in via `CLAIM_VERIFIER_STRICT=1` env var, not default-on.

## Connections

- [[ActivationContract]] — the underlying failure class
- [[ServerCacheManager]] — the affected feature
- [[smart_fake_code_detection]] — the right pattern (advisory LLM auditor) to model after
- [[runtime-activation-claim-required]] — the skill that auto-loads and self-corrects
