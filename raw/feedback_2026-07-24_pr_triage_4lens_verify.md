---
name: PR triage 4-lens verify pipeline catches 26+ misclassifications
description: 3 sonnet adversarial lenses + 1 codex cold review caught 26 misclassifications across 73 PRs that a single-model triage missed; the pipeline is mandatory for any merge-readiness classification
type: feedback
bead: rev-p8gin
---

## Context

PR triage mission at jleechanorg/worldarchitect.ai on 2026-07-24: 73 non-draft open PRs classified via 8 parallel sonnet triage agents. Phase 1 produced: 45 KEEP, 13 NON-PROD-DOCS, 7 NEEDS-REBASE, 8 CLOSE. A single-model triage of that scale is too prone to title-prefix shortcut.

## 4-lens verify pipeline (the standard)

**Lens 1 (Evidence)** — refute close recommendations by checking actual file diffs and branch state
**Lens 2 (Design)** — refute NON-PROD-DOCS classification by checking if files touched mvp_site/** (production per CLAUDE.md)
**Lens 3 (Severity)** — refute KEEP classification by checking age, supersession, WIP markers, blocking beads
**Lens 4 (Codex cold review)** — full adversarial pass with codex CLI (gpt-5.3-codex-spark)

## Results (73 PRs)

- Lens 1: 1 of 8 CLOSE refuted (#8289 — would have lost only production fix for #8059 in mvp_site/world_logic.py)
- Lens 2: 5 of 13 NON-PROD refuted (e.g., #8428 title "docs(specs)" but diff touches mvp_site/action_resolution_utils.py)
- Lens 3: 13 of 45 KEEP refuted (stale WIPs, broken stacks, missing production code)
- Codex: 7 more refutations (including 2 PRs that were already MERGED/CLOSED during triage)
- **Total: 26 misclassifications caught**

## Key rules learned

1. **Title-prefix triage is insufficient.** A PR with title "docs(specs):" can still modify mvp_site/. The verify pass MUST check `gh api repos/.../pulls/N/files` and grep for mvp_site/, mvp_site/prompts/**, or .github/workflows/ before accepting docs-only.

2. **Lens 1 caught the highest-stakes defect.** #8289 was classified as "superseded by #8178" based on title alone. Direct byte-content inspection of mvp_site/world_logic.py showed #8289 contains the ONLY production fix functions for issue #8059; #8178 is tests + CI scaffold only. Closing #8289 would have lost the production fix.

3. **Codex found 2 stale-state PRs the sonnet lenses missed:** #8545 was already MERGED 2026-07-24T06:07:16Z and #8550 was already CLOSED 2026-07-24T05:34:40Z. A "live state" check (gh pr view --json state,mergedAt,closedAt) is mandatory before final classification.

4. **Cross-model review is non-optional.** Same-model verification shares blind spots. The 3-sonnet pass caught 19 issues; codex caught 7 more that the sonnet agents either overlooked or got wrong. The 4-lens pipeline is the floor for any merge-readiness classification.

## Concrete commands

```bash
# Lens 2 (NON-PROD refutation) — single most-valuable check
gh api repos/OWNER/REPO/pulls/N/files | jq '.[] | .filename' | grep -E "^(mvp_site/|\.github/workflows/)"

# Lens 1 (CLOSE refutation) — for each PR marked CLOSE
gh api repos/OWNER/REPO/pulls/N/files | jq '.[] | .filename' | sort -u
gh pr view N --json state,mergedAt,closedAt

# Lens 3 (KEEP refutation) — check for staleness signals
gh pr view N --json createdAt,updatedAt,reviewDecision,mergeStateStatus
br list --search PR-N
```

## Verification

- Final counts after 4-lens verify: 32 KEEP, 2 KEEP-BLOCKED, 8 NON-PROD-DOCS, 9 NEEDS-REBASE, 1 NEEDS-USER-DECISION, 10 CLOSE, 1 INCONCLUSIVE
- All artifacts committed: docs/triage/2026-07-24-pr-triage/ (final-triage.md, verify-lens{1,2,3}-*.json, corrected-triage.{json,md}, cross-model-codex-review.json, close-recommendations.md, merge-plan.md, triage-final-report.md)
- Bead: rev-p8gin
- Mission goal: /cmux-goal "Triage 100 open PRs: drive keep-PRs to /green /er /advice approved, recommend close for superseded, merge non-prod/docs after /advice"

## Reusable pattern

For any merge-readiness classification:
1. Single-model triage (8-15 wide staggered fan-out per /swarm rule 4)
2. 3 sonnet adversarial lenses (evidence, design, severity) — refute-by-default
3. 1 codex cross-model cold review (full file inspection, not just reading JSON)
4. Aggregate corrected triage
5. Phase 7 close-recommendations with exact close commands

Skip a lens only if the cost (extra 5-10 min agent time) clearly exceeds the value of catching one more misclassification — and the answer is almost always "don't skip" for production PRs.
