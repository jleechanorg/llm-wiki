---
name: Claude Code dual-profile setup (claudewa)
description: Separate OAuth via CLAUDE_CONFIG_DIR; share projects symlinks; mutually exclusive repos; backup claude-wa local state
type: feedback
bead: jleechan-skk
---

# Claude Code dual-profile setup (claudewa / claude2)

## Context

WorldArchitect work uses jleechan@worldarchitect.ai; personal tooling uses Gmail. Both are paid Max subscriptions on the same human. Goal: separate auth/sessions, shared tooling and conversation discoverability, low ToS risk.

## Technical pattern (canonical)

Installer: /Users/jleechan/projects_other/user_scope/scripts/install-claude-wa-profile.sh

- ~/.claude-wa symlinks shared paths from ~/.claude: skills, hooks, commands, settings.json, projects/, etc.
- LOCAL_ONLY (never symlink): .claude.json, .credentials.json, sessions/, history.jsonl, cache, chrome, telemetry
- Shell: claudewa() sets CLAUDE_CONFIG_DIR=~/.claude-wa; claudewac() = claudewa --continue
- Mac Aside: u1 for WA; Linux jeff-ubuntu: same installer + bashrc

Do NOT symlink entire ~/.claude — collapses OAuth.

## Usage rule (Best Practice)

Mutually exclusive GitHub repos: WA repos → claudewa only; personal/tooling repos → claude/clauded only.

## ToS / ban risk (researched 2026-07-06)

Consumer Terms §2: no credential sharing with others. AUP: multi-account abuse = ban evasion / coordinated circumvention. Claude Code Legal: OAuth for ordinary individual use.

Community: GitHub #43911, #49972, t3code#1444 document personal+work via CLAUDE_CONFIG_DIR. No verified ban reports; 429 complaints exist.

Low ban risk if: separate OAuth, sole user, both paid, not evading prior ban, not parallel-limit farming on same workload.

## Backup (user_scope)

backup-home.sh: ~/.claude/projects/ (shared convos) + ~/.claude-wa/ → claude/claude-wa/ + ~/.bashrc

## References

- /Users/jleechan/roadmap/nextsteps-2026-07-06-user-scope-backup-claude-wa.md
- jleechanorg/claude-commands (user_scope)

Jeffrey oracle: NO
