---
title: "Skill Consolidation Pattern"
type: concept
tags: [harness, agent-context, best-practice, zfc]
date: 2026-04-25
---

# Skill Consolidation Pattern

**Definition**: The practice of merging many overlapping skill/instruction files into a single authoritative source, optimized for agent working memory rather than human comprehensiveness.

## The Problem

Agents are told to "read X skill before working" but:
- **5+ fragmented skill files** cover the same domain
- **Some are personal** (`~/.claude/skills/`), some are project-level (`.claude/skills/`)
- **Stale references** to closed PRs and obsolete workflows persist
- **Total reading burden** exceeds what agents actually load into working memory

Result: Agents skip everything and rely on training data priors, which are often wrong for non-obvious architectural patterns.

## The Solution

1. **Audit all skills** covering the domain
2. **Extract the actually-enforced content** (~80 lines from 860 lines in the ZFC case)
3. **Create one project-level skill** that ships with every worktree
4. **Delete or redirect** all other skills
5. **Update config references** (AGENTS.md, CLAUDE.md) to point to the single source

## Design Principles

- **Project-level** > personal-level: ships with every worktree, reviewable by bots
- **~120 lines max**: Must fit in agent working memory alongside code context
- **Tables over prose**: File-responsibility tables, violation tables, contract freezes
- **Living sections**: Milestone status updates as work progresses
- **Stale-proof**: No PR-number references that become meaningless after merge/close

## Case Study: ZFC Leveling Skills

| Before | After |
|--------|-------|
| 5 skill files (860 lines) | 1 skill file (139 lines) |
| 2 personal + 3 project-level | 1 project-level |
| 100KB roadmap doc referenced everywhere | Roadmap referenced once as "canonical source" |
| 525-line AO orchestration with stale PR refs | Deleted |

## Related Concepts

- [[Agent PR Sprawl]] — The problem this pattern helps solve
- [[Harness5LayerModel]] — Skill consolidation addresses L2 (Context layer)
- [[ZeroFrameworkCognition]] — The architectural principles being consolidated
