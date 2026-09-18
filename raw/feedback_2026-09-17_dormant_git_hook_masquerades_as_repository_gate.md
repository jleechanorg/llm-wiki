---
name: dormant-git-hook-masquerades-as-repository-gate
description: "Before asserting 'no repository gate requires X', check .githooks/ + validator scripts + core.hooksPath wiring, not just .github/workflows/ — a hook script sitting unused while core.hooksPath points elsewhere still prints authoritative-sounding instructions"
type: feedback
bead: none
---

## Context

While consolidating PR #9494 (worldarchitect.ai) into a single non-stacked PR, I found `docs/evidence/pr-9494/claim_artifact_map.md` + `recording.cast` (288 lines) committed in-tree, violating `~/.claude/skills/evidence-standards/SKILL.md`'s rule: "Keep bundles out of `docs/evidence/` unless a repository gate requires in-tree paths." I checked only `.github/workflows/`, found no reference, and removed the files, asserting "no repository gate justifies this."

## What was actually true

A dispatched `/harness` subagent found the real picture: `.githooks/pre-push` + `scripts/validate_pr_evidence.sh` + a `.gitignore` re-include comment DO explicitly require and instruct the exact in-tree pattern I removed — the hook's own remediation text literally says `asciinema rec docs/evidence/pr-${PR_NUM}/recording.cast` and `Create: docs/evidence/pr-${PR_NUM}/claim_artifact_map.md`. But this repo's `core.hooksPath` is `.husky/_` (Husky), and Husky's pre-push never calls the validator — so `.githooks/pre-push` is dormant: real, authoritative-sounding code that doesn't actually run for a normal `git push` in this checkout.

A parallel `/history` search then established this is not an isolated PR-9494 mistake: 57 current / 128 historical `docs/evidence/pr-*/` directories exist across dozens of unrelated PRs, predating PR #9494 — a systemic habit across many sessions/models defaulting to in-tree commits because prior examples look like precedent, not a bug traceable to one bad instruction or plan doc.

## Fix

Edited `~/.claude/skills/evidence-standards/SKILL.md:294` to define "repository gate" precisely (a mechanically wired CI step or git hook that actually blocks — not precedent, not an unenforced skill recommendation) and to require checking `.githooks/`, `scripts/validate*evidence*`, and `.gitignore` re-includes, AND verifying the mechanism is actually wired into the active `core.hooksPath`, before asserting "no repository gate" in either direction (to add or to remove in-tree evidence).

## Why

A dormant hook script is a trap in both directions: an agent that finds it and doesn't check `core.hooksPath` will wrongly conclude a gate is enforced (and keep committing evidence in-tree unnecessarily); an agent that only checks `.github/workflows/` and misses `.githooks/` entirely will wrongly conclude no gate exists at all (as I did). Either error compounds across many independent sessions when the wrong conclusion looks like established precedent to the next agent.

## Not yet fixed (tracked, needs a separate authorized repo PR)

- `.claude/skills/pr-babysit/SKILL.md:225` (repo-local skill) still unconditionally instructs "copy to `docs/evidence/pr-<number>/`" with no reference to the avoid-by-default policy — a live contradiction.
- `.githooks/pre-push` should either be wired into Husky's chain or tombstoned so it stops asserting authority it doesn't have.

## How to apply

Before asserting "a repository gate does/doesn't require X" (evidence paths, or any other in-tree-vs-external-artifact question) in ANY repo: grep beyond CI workflow files — check `.githooks/`, `scripts/validate*`, `.gitignore` re-include comments, and run `git config core.hooksPath` to confirm whatever mechanism you found is actually the one that fires on the relevant git operation. A hook file existing on disk is not evidence it runs.
