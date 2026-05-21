---
title: "GreenGateWorkflow"
type: concept
tags: [CI, workflow, green-gate, GitHub-actions]
date: 2026-04-16
---

## Definition
GreenGateWorkflow (`.github/workflows/green-gate.yml`) is the trigger-only + polling CI workflow for PR evaluation. It does NOT run LLM evaluation directly in GHA — instead it triggers AO workers that run skeptic evaluation and posts results back as PR comments.

## Current Flow (After PR #6325)
```
pre-check 6-green eligibility → post trigger comment →
lifecycle-manager runs: ao skeptic verify →
posts VERDICT comment → GHA polling step detects verdict → PASS/FAIL
```

## Previous Flow (Before PR #6325)
```
design_doc_gate (blocking) → skeptic_gate → post trigger comment →
lifecycle-manager runs: ao skeptic verify → VERDICT → GHA polling → PASS/FAIL
```

## Key Files
- `.github/workflows/green-gate.yml` — the workflow definition
- `.github/workflows/doc-size-check.yml` — related doc size check workflow
  - Bug fix in PR #6325: `retry-self-hosted` now correctly `needs: doc-size-check`

## Grep Gates
The workflow historically used grep patterns to check for design doc compliance in PRs touching production files (`world_logic.py`, `constants.py`, `llm_parser.py`, `llm_service.py`).

Pattern portability fix (PR #6309):
- GNU grep: `\s` matches whitespace
- BSD/mawk grep: `\s` not recognized → use `$'^[ \t]*#'` (ANSI-C quoting)

## Lite-green Bypass (2026-05-16)

For **docs-only PRs**, Green Gate times out polling for Skeptic VERDICT (10–15 min wait). Classify as lite-green and check 3 gates directly:
1. `gh api .../commits/<SHA>/status --jq '.state'` = `success`
2. `gh pr view N --json mergeable` = `MERGEABLE`
3. Latest CR review = `APPROVED`

Merge directly without waiting for Green Gate. See `feedback_2026-05-16_lite-green-merge-bypass.md`.

## Connections
- [[SkepticGate]] — runs within green-gate workflow
- [[DesignDocGate]] — removed gate that was part of the workflow
- [[AWKCompatibility]] — POSIX grep portability fix
