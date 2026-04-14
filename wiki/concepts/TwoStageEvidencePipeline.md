---
title: "Two-Stage Evidence Pipeline"
type: concept
tags: [evidence-review, stage1, stage2, self-review, independent-review, merge-gate]
last_updated: 2026-03-16
sources: [jleechanclaw-evidence-review-schema]
---

## Summary
The Two-Stage Evidence Pipeline is a merge gate requiring that code PRs include a git-tracked evidence bundle with a machine-readable verdict. Stage 1 is agent self-review; Stage 2 is an independent verification by a different model family. This replaces the prior weak "PASS comment" gate that agents could self-stamp.

## Stage 1: Agent Self-Review

Triggered after agent completes coding task. Process:
1. Create evidence directory: `docs/evidence/{repo}/PR-{N}/{date}_{time}_utc/`
2. Write `claims.md`: list each change and what it accomplishes
3. Collect artifacts:
   - `pytest ... > artifacts/pytest_output.txt 2>&1`
   - `gh api .../check-runs > artifacts/ci_check_runs.json`
   - `gh api .../reviews > artifacts/coderabbit_review.json`
4. Run `/er` and save output to `self_review.md`
5. If FAIL: fix issues, recollect artifacts, rerun (max 3 iterations)
6. If PASS: write `verdict.json` with stage1 PASS, commit bundle
7. Stage 2 runs automatically after commit

## Stage 2: Independent LLM Verification

Triggered automatically when stage 1 PASS is committed. Requirements:
- MUST use different model family than the coding agent (stage 1)
- Reads `claims.md` + all `artifacts/`
- Verifies each claim has supporting evidence
- Checks for: circular citations, empty/missing artifacts, statistical weakness, unverified assertions

**Dispatcher** writes independence attestation fields (the reviewer cannot forge these):
- `stage2.independence_verified: true`
- `stage2.model_family_differs_from_stage1: true`

## Evidence Bundle Structure

```
docs/evidence/{repo}/PR-{N}/{YYYYMMDD}_{HHMM}_utc/
  claims.md                  # what the agent claims
  artifacts/
    pytest_output.txt        # raw pytest output
    ci_check_runs.json       # GitHub check runs
    coderabbit_review.json   # CodeRabbit review
    gateway_traces.jsonl     # gateway traces
  self_review.md             # stage 1 output
  independent_review.md      # stage 2 output
  verdict.json               # machine-readable verdict
```

## Merge Gate Enforcement

`check_evidence_pass()` in merge_gate.py:
- Requires `verdict.json` in PR's changed files
- Requires `overall == "PASS"` AND `stage2.status == "PASS"`
- Requires `stage2.independence_verified == true`
- Requires `stage2.model_family_differs_from_stage1 == true`
- Legacy PASS comment fallback **removed** — all code PRs require full two-stage bundle

## Reviewer Priority Order

Must be different model family than stage 1:
1. **Codex CLI** (`codex exec --yolo`) — OpenAI family, preferred
2. **Gemini CLI** — Google family, second choice
3. **Claude CLI** — Anthropic family, last resort (only if stage 1 used a different family)

## Limitations
- Only required for code PRs (src/orchestration/, scripts/, lib/, SOUL.md, TOOLS.md)
- Docs-only PRs skip evidence
- Stage 2 reviewer cannot see the coding agent's session — it's a different context

## Related Concepts
- [[IndependentVerification]]
- [[MergeReadinessContract]]
- [[AutonomousAgentLoop]]