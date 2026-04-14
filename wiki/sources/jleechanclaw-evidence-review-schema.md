---
title: "Evidence Review Schema"
type: source
tags: [evidence-review, two-stage-pipeline, merge-gate, verdict-json, stage1-stage2, codex]
date: 2026-03-16
source_file: /home/jleechan/project_jleechanclaw/jleechanclaw/roadmap/EVIDENCE_REVIEW_SCHEMA.md
---

## Summary
The Evidence Review Schema replaces the weak "PASS comment" merge gate with a two-stage verification pipeline. Stage 1 is agent self-review (`/er` command), Stage 2 is an independent LLM verification using a different model family. Evidence bundles are git-tracked, include raw artifacts, and have a machine-readable `verdict.json` that the merge gate reads to enforce the gate.

## Key Claims

### Problems with Old PASS Comment Gate
1. **No audit trail** — PR comments are editable, deletable, not git-tracked
2. **No independence** — the coding agent can post "evidence PASS" on its own work
3. **No schema** — evidence artifacts (test logs, traces, screenshots) not collected in standard location

### Two-Stage Pipeline

**Stage 1: Agent Self-Review**
1. Agent completes coding task
2. Agent runs `/er` against own work
3. Collects: pytest output → `artifacts/pytest_output.txt`, CI status → `artifacts/ci_check_runs.json`, CR review → `artifacts/coderabbit_review.json`
4. Maps claims to artifacts in `claims.md`
5. Writes `self_review.md` with verdict
6. If FAIL: fixes issues and reruns (max 3 iterations)
7. If PASS: commits evidence bundle, moves to stage 2

**Stage 2: Independent LLM Verification**
1. Triggered automatically when stage 1 PASS is committed
2. MUST use a different model/context than the coding agent
3. Reads `claims.md` + all `artifacts/`
4. Verifies each claim has supporting evidence
5. Checks for: circular citations, empty/missing artifacts, statistical weakness, unverified assertions
6. Writes `independent_review.md` + `verdict.json`
7. If FAIL: posts PR comment with specific failures

**Reviewer priority (must differ from stage 1 model family):**
1. Codex CLI (OpenAI family) — preferred
2. Gemini CLI (Google family) — second choice
3. Claude CLI (Anthropic family) — last resort

### Independence Guarantee
`independence_verified` and `model_family_differs_from_stage1` are written by the **dispatcher**, not the reviewer. A stage-2 reviewer cannot forge these fields because it only produces `independent_review.md` text. The dispatcher parses that text and controls what goes into `verdict.json`.

### verdict.json Schema

```json
{
  "pr": 255,
  "repo": "jleechanorg/jleechanclaw",
  "overall": "PASS",
  "stage1": {
    "status": "PASS",
    "reviewer": "self",
    "model": "claude-4.5-sonnet",
    "claims_verified": 5,
    "claims_failed": 0
  },
  "stage2": {
    "status": "PASS",
    "reviewer": "independent",
    "model": "codex/gpt-5.3-codex",
    "independence_verified": true,
    "model_family_differs_from_stage1": true
  }
}
```

### Merge Gate Integration
`check_evidence_pass()` in `src/orchestration/merge_gate.py`:
- Requires `docs/evidence/{repo}/PR-{N}/*/verdict.json` in PR's changed files
- Requires `overall == "PASS"` AND `stage2.status == "PASS"` AND independence verified
- Legacy PASS comment fallback has been **removed**

### Which PRs Require Evidence?
Required for: `src/orchestration/`, `scripts/`, `lib/`, SOUL.md, TOOLS.md
NOT required for: `docs/`, `roadmap/`, `.beads/`, `launchd/`, `agents/`, test-only changes

## Related Concepts
- [[TwoStageEvidencePipeline]]
- [[IndependentVerification]]
- [[MergeReadinessContract]]