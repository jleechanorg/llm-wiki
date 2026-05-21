# Codex Mirror Pointer Pattern

**Ingested**: 2026-05-18
**Source**: ~/llm_wiki/raw/codex-mirror-pointer-pattern-2026-05-18.md

## Summary

`.codex/skills/` mirrors in the worldarchitect.ai repo must use the pointer pattern (frontmatter + one-liner referencing the canonical `.claude/skills/` file) rather than duplicating full content. Full duplicates drift immediately in workflow steps, report format, and reconciliation language. User-scope skills (`~/.claude/skills/`) must be annotated explicitly so automated reviewers don't flag them as "missing."

## Rule

Pointer pattern for `.codex/skills/<name>/SKILL.md`:
```yaml
---
name: <name>
description: <description>
---
See `.claude/skills/<name>/SKILL.md` as the single source of truth for this skill.
```

Some Codex skills use symlinks instead (e.g., `babysit -> ../../.claude/skills/babysit`), which also prevents drift.

## Evidence

PR [#6948](https://github.com/jleechanorg/worldarchitect.ai/pull/6948) — duplicate Codex mirror caused 3 review findings (Bugbot Low, CR Major, CR Critical). Fixed by replacing with pointer in commit 6985b7ec0.
