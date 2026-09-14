---
title: "Ready-Gate Discipline"
type: concept
tags: [workflow, gates, ready, git, pr-lifecycle]
sources: [feedback-2026-09-13-ready-gate-and-heavydialog-prompt-invariants]
last_updated: 2026-09-13
---

# Ready-Gate Discipline

Ready-Gate Discipline is the operational invariant that **conditional or anticipatory "merge approved" instructions from a user do NOT waive the 6-gate checklist** defined in `~/.claude/skills/ready/SKILL.md`.

## The 6 Mandatory Gates

Before executing a merge under `MERGE APPROVED`:

1. **Gate 1 (`/es`)**: Published Gist linked via canonical `**Evidence**: <gist-url> (head <sha>)` marker in PR body.
2. **Gate 2 (`/er`)**: Adversarial evidence review verdict PASS at exact current HEAD SHA (or narrow doc-only allowlist).
3. **Gate 3 (`/advice`)**: ≥2 independent full-coverage approval reviewers from canonical `advice/SKILL.md` approval lanes.
4. **Gate 4 (`/green`)**: Current-head CI green (or 10m backlogged local-equivalent proof posted to PR) + `mergeable == MERGEABLE`.
5. **Gate 5 (Comments Handled)**: All unresolved review threads and actionable bot comments addressed/resolved.
6. **Gate 6 (Cross-Thread Regression Check)**: Audit open beads for shared touched files or root causes before merge.

## Invariant

A user saying "ensure tests pass, get advice approvals, then /ready and merge approved" is expressing an **ordered conditional pipeline**, not an immediate override. If any gate fails or is unperformed (such as omitting the `/es` Gist publication or skipping the `/er` adversarial review), the merge MUST NOT proceed until that gate is satisfied.

## Related
- [[7-Green-Proof-Artifact]]
- [[GreenGateWorkflow]]
- [[EvidenceStandards]]
- [[PR9861]]
