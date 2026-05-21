---
name: Codex skills mirror symlinks must match .claude/skills
description: .codex/skills/ entries must be symlinks to .claude/skills, not stale regular files
type: feedback
bead: none
---

## Context
Codex review (chatgpt-codex-connector) flagged that .codex/skills/worldai-mcp-server-usage/SKILL.md
was a stale regular file (6034 bytes, outdated headings, placeholder project names) while
the source at .claude/skills/worldai-mcp-server-usage.md had been updated. The sibling
.codex/skills/worldai-tools-mcp-proxy-testing/SKILL.md was already a symlink.

## Technical detail
- .codex/skills/ mirrors must be symlinks: `ln -s ../../../.claude/skills/<name>.md SKILL.md`
- Regular files become stale and diverge from the canonical .claude/skills source
- Codex agents see the stale copy, not the current version

## Solution / Rule
When adding or updating .claude/skills/<name>.md:
1. Check if .codex/skills/<name>/SKILL.md exists
2. If it's a regular file, replace with symlink to ../../../.claude/skills/<name>.md
3. If the directory doesn't exist, create it and add the symlink
4. Commit the mode change (100644 -> 120000)

## Verification
PR #6945 commit 530d99d9d replaced stale regular file with symlink.
Codex review thread resolved.

## References
- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6945
- Commit: 530d99d9d21f2a5b29e68bbdb799c3f0075572db
