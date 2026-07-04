---
title: "Bead-PR Bridge"
type: concept
tags: [beads, pr-lint, dark-factory, worldai, pre-commit]
last_updated: 2026-07-04
---

# Bead-PR Bridge

## Definition

The pattern of connecting an **internal git-tracked issue tracker** (the `br` Beads CLI's `.beads/issues.jsonl`) to the **external pull-request surface** (GitHub PR bodies and commit messages) so bead IDs surface in human-reviewable PR UI instead of staying silent inside JSONL commits.

## Why it matters

Without the bridge, beads live in JSONL commits that reviewers never see. PR authors don't declare which bead their work touches; reviewers can't trace a PR back to a tracker record; the bead DB drifts from the actual code that closes/fixes/refs it. With the bridge, every PR carries a `Beads: <id>` line in its body and the bead metadata flows both directions.

## Architecture (3-layer defense in depth)

1. **PR template** — `.github/PULL_REQUEST_TEMPLATE.md` with a `## Beads` section that prompts authors to declare bead references
2. **Lint workflow** — `.github/workflows/bead-pr-lint.yml` that fails PRs missing the `Beads:` line
3. **PR body parsing convention** — `Beads: REV-xxxx` (single ID), `Beads: REV-xxxx, REV-yyyy` (comma-separated list), or `Beads: none` (explicit opt-out)

## Companion patterns

The bridge is typically paired with **JSONL sort-guard** (preventing +1686/-1685 wholesale rewrites) and **`no-auto-flush: true` config** (preventing auto-flush churn on every `br` command). See [[NoAutoFlushConfig]] and [[PreCommitHookPattern]].

## References

- Source page: [[project-2026-07-04-bead-bridge-complete-architecture-and-pitfalls]]
- PRs: worldai #8154 #8155 #8159; dark-factory #135 #136 #137 #140; agent-orchestrator #745; worldarchitect-autor-eval #1
- Bead: `jleechan-xgz` (rollout learning), `jleechan-c5q` (architecture reference)

## Connections

- [[BeadsRustArchitecture]] — upstream library this integrates with
- [[NoAutoFlushConfig]] — root-cause config to prevent JSONL churn
- [[PreCommitHookPattern]] — Layer 2 defense for any git-tracked data file
- [[DarkFactoryRepo]] — primary implementation repo
- [[WorldArchitectAiRepo]] — first deployment target
- [[MergeUnionGitAttributes]] — subdir-vs-root gotcha relevant to JSONL config