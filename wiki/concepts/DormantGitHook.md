---
title: "Dormant Git Hook"
type: concept
tags: [git, hooks, harness-safety]
date: 2026-09-17
---

## Definition
A git hook script that exists in a repository's checked-in hook directory (e.g. `.githooks/`), looks authoritative (prints enforcement-style errors, mandates specific remediation), but never actually runs because `core.hooksPath` points somewhere else (e.g. a Husky-managed `.husky/_` directory) that doesn't call it.

## Why it matters
An agent (or human) checking "does a gate require X" by grepping for the hook file's existence, or even reading its content, can be fooled into believing it's live. The correct check is `git config core.hooksPath`, followed by confirming the *active* hook chain actually invokes the script in question — not just that the script exists on disk.

The failure mode runs both directions:
- **False positive**: assume a dormant hook is enforced, and needlessly comply with instructions it prints (e.g. committing artifacts in-tree that should be published externally).
- **False negative**: check only the active/obvious enforcement surface (e.g. `.github/workflows/` CI) and miss a `.githooks/` script entirely, wrongly concluding no gate exists.

## How to detect
1. `git config core.hooksPath` — find the actually-wired hook directory.
2. Confirm the script at that path (not just any script with a matching name elsewhere) calls the validator/check in question.
3. Treat a script sitting unused in an unwired directory as dead code with misleading text, not a live gate.

## First documented instance
[[feedback-2026-09-17-dormant-git-hook-masquerades-as-repository-gate]] — worldarchitect.ai's `.githooks/pre-push` + `scripts/validate_pr_evidence.sh` require in-tree `docs/evidence/pr-<N>/` artifacts, but `core.hooksPath=.husky/_` (Husky) never calls it. 57 current / 128 historical `docs/evidence/pr-*/` directories across the repo suggest many prior sessions were fooled by this exact trap.

## Connections
- [[EvidenceStandardsSkill]] — fixed to require this check before asserting "no repository gate"
- [[Husky]] — common hook manager that silently overrides `core.hooksPath`
- [[PreCommitHookPattern]] — related but distinct: general hook-design guidance, not the wiring-detection problem
