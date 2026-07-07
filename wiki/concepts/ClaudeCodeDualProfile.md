# Claude Code Dual Profile (CLAUDE_CONFIG_DIR)

Two consumer Claude Code accounts on one machine without shared OAuth.

## Mechanism

- CLAUDE_CONFIG_DIR per wrapper (e.g. ~/.claude-wa)
- Local: .claude.json, .credentials.json, sessions/
- Symlink from ~/.claude: skills, hooks, settings.json, projects/

## Wrappers

| Command | Dir | Use |
|---------|-----|-----|
| clauded | ~/.claude | Personal |
| claudewa / claude2 | ~/.claude-wa | WorldArchitect |
| claudewac | ~/.claude-wa + --continue | WA resume |

Installer: ~/projects_other/user_scope/scripts/install-claude-wa-profile.sh

## Rules

1. Mutually exclusive GitHub repos per account.
2. Never symlink auth or sessions/.
3. Verify with /usage if /status email looks wrong (#49972).

## See also

- [[feedback-2026-07-06-claude-wa-dual-profile-setup]]
