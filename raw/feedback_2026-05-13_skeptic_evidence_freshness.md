---
name: skeptic-evidence-freshness
description: "Skeptic FAIL top causes: stale evidence SHA, scope creep files, CI still in-progress. Run skeptic only after all non-skeptic CI is terminal green."
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 9b230405-c16a-4112-81a6-cccb8a95447a
---

**Rule:** Run `ao skeptic verify` only after all non-skeptic CI checks are in terminal state (SUCCESS/FAILURE). Before running, verify: (1) evidence SHA matches current HEAD, (2) gist content matches current diff, (3) no scope-creep files in the diff that aren't described in the PR body, (4) PR body file count matches the actual diff file count.

**Why:** PR #551 had 5 consecutive skeptic FAIL verdicts across 3 different SHAs. The top three failure causes were:
1. **Stale evidence SHA** — gist referenced SHA `033686ff` but HEAD was `c3298312`. Skeptic gate-4 and gate-6 both flag SHA mismatches.
2. **Scope creep** — `wholesome.test.ts` added `[antig]` prefix relaxation not described in PR scope. Skeptic gate-8 (scope boundary) flagged it.
3. **CI still in-progress** — Bugbot was IN_PROGRESS when skeptic ran, causing gate-4 FAIL. Running skeptic before all CI is terminal wastes an evaluation.

**How to apply:**
- Before running `ao skeptic verify -n <PR>`, run: `gh pr view <PR> --json statusCheckRollup --jq '.statusCheckRollup[] | select(.status == "IN_PROGRESS" or .status == "QUEUED") | .name'` — if non-empty, wait.
- Update PR evidence SHA to match `gh pr view <PR> --json headRefOid --jq '.headRefOid'` BEFORE running skeptic.
- Update gist content to match the current diff (file count, changed files, test results).
- Remove any files from the diff that aren't described in the PR scope, or add them to the scope description.

**Related:** [[feedback_2026-05-12_pr551-ci-corepack-shim]], [[feedback_skeptic_false_pass_codex_echo]]
