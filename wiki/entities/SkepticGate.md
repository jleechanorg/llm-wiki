---
title: "Skeptic Gate"
type: entity
tags: [skeptic, merge-gate, llm-verifier, ao, 7-green, ci]
sources: [agent-orchestrator-fork-summary.md]
last_updated: 2026-04-11
---

## Summary

The Skeptic Gate is the 7th and final merge gate in the [[AgentOrchestratorFork]] pipeline. It is an LLM-based PR verifier that independently evaluates whether a PR is ready to merge, providing a check that is orthogonal to CI, CodeRabbit, and human review. A PR must receive a `VERDICT:PASS` comment (not `SKIPPED`) for the gate to clear.

## What It Does

Skeptic evaluates a PR by:
1. Inspecting the PR diff, CI results, review comments, and evidence bundle
2. Running an LLM prompt via `ao skeptic verify`
3. Posting a structured VERDICT comment to the PR (authored by `SKEPTIC_BOT_AUTHOR`)
4. The GHA polling job (`skeptic-gate.yml`) reads the comment and exits PASS or FAIL

SKIPPED is treated as FAIL — the LLM must explicitly affirm the PR.

## Architecture

Skeptic runs via AO worker with local API keys. It never runs in GHA directly, and API keys are never stored in CI secrets.

| Component | Role | Runs where |
|---|---|---|
| `skeptic-gate.yml` | GHA check; polls for VERDICT comment | GHA (no API keys) |
| `skeptic-cron.yml` | Cron that triggers evaluation for open PRs | GHA — calls local `ao skeptic verify` |
| `ao skeptic verify` | CLI command that runs LLM evaluation | Local machine (has API keys via env/OAuth) |
| lifecycle-worker | Detects trigger comments, dispatches verify | Local machine (launchd plist) |

**The chain:** PR event → `skeptic-gate.yml` starts polling → lifecycle-worker detects PR → runs `ao skeptic verify` locally → posts VERDICT comment → `skeptic-gate.yml` sees VERDICT → exits PASS/FAIL.

## VERDICT Format

The VERDICT comment must contain `VERDICT:PASS` or `VERDICT:FAIL` as a parseable token. The LLM evaluation must be fail-closed: if parsing fails or the LLM produces ambiguous output, the result is treated as FAIL.

## LLM Routing

All LLM evaluation for skeptic routes through `packages/cli/src/lib/llm-eval.ts`:
- Primary: Codex (`tryCodexPrint`)
- Fallback: Claude (`tryClaudePrint` with `--dangerously-skip-permissions --print`)

`ao skeptic verify` runs `claude --print` from `/tmp` to avoid project `CLAUDE.md` hooks skewing the evaluation.

## False-PASS Bug History

A known false-PASS bug existed where Codex stdout echoed the prompt template (which contained `VERDICT:PASS` as an example). The grep for VERDICT matched the echoed prompt body rather than the actual verdict line, causing every evaluation to appear as PASS regardless of the LLM's actual response. Fixed by tightening the VERDICT parsing to require the token on its own line or in a structured position.

## Debugging the Chain

When skeptic is broken, check in order:
1. Is the lifecycle-worker running? (`launchctl print gui/$(id -u)/com.agentorchestrator.lifecycle-agent-orchestrator`)
2. Is the lifecycle-worker detecting PRs and dispatching skeptic? (check logs)
3. Is `ao skeptic verify` producing a VERDICT? (run manually: `ao skeptic verify -n <PR> --dry-run`)
4. Is the VERDICT being posted? (check PR comments for `SKEPTIC_BOT_AUTHOR`)
5. Is `skeptic-gate.yml` polling correctly? (check GHA run logs)

**Never** add ANTHROPIC_API_KEY to repo secrets or run the LLM in GHA as a fix.

## Relationship to 7-Green

Skeptic is gate #7 in the 7-Green checklist. The other six are: CI green, mergeable, CodeRabbit APPROVED, Bugbot clean, inline threads resolved, and evidence present. All seven must pass for an autonomous merge.

## Connections

- [[AgentOrchestratorFork]] — the system that owns Skeptic
- [[AgentOrchestrator]] — base AO system
- [[EvolveLoop]] — the evolve loop polls Skeptic status as part of merge readiness
