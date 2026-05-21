---
title: Lite-Green Docs-Only PR Workflow
date: 2026-05-18
type: learning
pr: https://github.com/jleechanorg/worldarchitect.ai/pull/6945
head_sha: 530d99d9d21f2a5b29e68bbdb799c3f0075572db
---

# Lite-Green Workflow for Docs-Only PRs

## Summary
Docs-only PRs (no production code under `mvp_site/**`) use lite-green: 3 gates (CI core, mergeable, CR APPROVED). Full 7-green is not required. The Green Gate workflow does not distinguish and will fail at Gate 6 (evidence), but this is expected and non-blocking.

## Key Rules
1. Classify docs-only PRs as lite-green
2. Only verify: CI core checks, mergeable=true, CR APPROVED
3. Ignore non-required workflow failures (deploy-preview, design-doc-gen, self-hosted runners)
4. Report lite-green verdict explicitly

## Related
- [[CodeRabbit Incremental Review]] — CR doesn't re-issue APPROVED for new commits
- [[Codex Skills Symlink Mirror]] — .codex/skills must symlink to .claude/skills

Does not affect [[jeffrey-oracle]].
