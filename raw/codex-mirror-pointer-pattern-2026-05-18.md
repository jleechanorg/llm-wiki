---
name: Codex mirrors must use pointer pattern, not full duplicates
description: .codex/skills/ mirrors should be short pointer files referencing the canonical .claude/skills/ version, never full content copies
type: feedback
bead: rev-5ec4h
---

## Context

PR [#6948](https://github.com/jleechanorg/worldarchitect.ai/pull/6948) added a `code_standards` skill with a Codex mirror under `.codex/skills/code_standards/SKILL.md`. The mirror duplicated the full content from `.claude/skills/code_standards/SKILL.md` instead of using the repo-standard pointer pattern. This caused three review issues:

1. **Bugbot (Low)**: Codex mirror duplicates content instead of pointer pattern
2. **CR (Major)**: Report format and reconciliation language drift between Codex and Claude versions
3. **CR (Critical)**: Source skill files appear "missing" — they are user-scope at `~/.claude/skills/`

## Technical Detail

The established pattern in this repo is:
- `.codex/skills/<name>/SKILL.md` = frontmatter + one-liner pointer to `.claude/skills/<name>/SKILL.md`
- Example: `.codex/skills/zero-framework-cognition/SKILL.md` → `See .claude/skills/zero-framework-cognition/SKILL.md as the single source of truth for this skill.`
- Some use symlinks (`.codex/skills/babysit -> ../../.claude/skills/babysit`)

The duplicate mirror already had content drift in:
- Workflow step 4 (Codex version omitted "so one reviewer is not relying on the same model/context")
- Workflow step 6 (Codex: "A required lane's FAIL remains a blocker" vs Claude: "Do not dilute a FAIL from any required lane into a PASS")
- Report format (Codex: simple bullet list vs Claude: detailed markdown template)

## Solution / Rule

**Always use the pointer pattern for `.codex/skills/` mirrors.** The mirror SKILL.md should contain only:
1. YAML frontmatter (name, description)
2. One line: `See .claude/skills/<name>/SKILL.md as the single source of truth for this skill.`

Additionally, when source skills are user-scope (`~/.claude/skills/`), add explicit annotations in the command and skill files so reviewers understand the resolution path:
- `Source skills live at ~/.claude/skills/ (user-scope, shared across all repos) and are mirrored under .codex/skills/ as pointer files. Skill discovery resolves personal skills before project skills.`

## Verification

- `Codex skill symlink drift` CI check passes with pointer pattern
- CodeRabbit approves after fix
- Bugbot finds zero issues after fix

## References

- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6948
- Commit: 6985b7ec0
- Bead: rev-5ec4h
