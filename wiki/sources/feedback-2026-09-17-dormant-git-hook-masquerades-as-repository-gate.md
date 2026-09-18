---
title: "Dormant git hook masquerades as repository gate"
type: source
tags: [worldarchitect.ai, evidence-standards, git-hooks, harness-fix]
date: 2026-09-17
source_file: raw/feedback_2026-09-17_dormant_git_hook_masquerades_as_repository_gate.md
---

## Summary
While consolidating PR #9494 (jleechanorg/worldarchitect.ai) into one non-stacked PR, an in-tree evidence bundle (`docs/evidence/pr-9494/`) was removed on the belief that no repository gate required it — but a `.githooks/pre-push` validator script does require and instruct that exact pattern. It's dormant because `core.hooksPath` points at Husky instead. This is a systemic cross-session pattern (57 current / 128 historical `docs/evidence/pr-*/` dirs), not an isolated mistake, and the fix landed in the shared `evidence-standards` skill.

## Key Claims
- A hook file existing on disk (`.githooks/pre-push`) is not evidence it actually runs — `git config core.hooksPath` must be checked.
- `.githooks/pre-push` + `scripts/validate_pr_evidence.sh` + a `.gitignore` re-include comment explicitly require `docs/evidence/pr-<N>/claim_artifact_map.md` + a media file, but this repo's active hook path is `.husky/_`, which never calls the validator.
- 57 current / 128 historical `docs/evidence/pr-*/` directories exist across dozens of unrelated PRs predating PR #9494 — a widespread habit, not a PR-specific bad instruction.
- No plan/goal doc directed the original in-tree commits; the ironclad contract governing PR #9494 closure already stated the correct gist-only policy.

## Key Quotes
> "A dormant hook script is a trap in both directions: an agent that finds it and doesn't check core.hooksPath will wrongly conclude a gate is enforced ... an agent that only checks .github/workflows/ and misses .githooks/ entirely will wrongly conclude no gate exists at all."

## Connections
- [[EvidenceStandardsSkill]] — the skill file fixed (`~/.claude/skills/evidence-standards/SKILL.md:294`)
- [[DormantGitHook]] — the general pattern this incident exemplifies
- [[Husky]] — the actually-wired hook manager in this repo, overriding `.githooks/`
