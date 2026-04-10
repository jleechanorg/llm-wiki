---
title: "JeffreyWorkingStyle"
type: concept
tags: [jeffrey, workflow, engineering, process]
sources: [user-preferences-patterns-learnings, ai-coding, github-patterns]
last_updated: 2026-04-09
---

# Jeffrey's Working Style

Based on 27,923 user messages and git history from worldarchitect.ai (Jan–Apr 2026).

## Core Dev Environment

- **Claude Code** as primary IDE — heavily customized with hooks, skills
- **OpenClaw** for session management and model steering (cmux setup)
- **Worktree-per-PR isolation**: Each PR gets its own worktree
- **gh CLI** for all GitHub operations — non-negotiable
- **Never pushes directly to main** — always PRs, always feature branches

## Hook-Driven Automation

| Hook | Purpose |
|------|---------|
| `anti_demo_check_claude.sh` | Blocks placeholder/demo code |
| `detect_speculation_and_fake_code.sh` | Blocks "let me wait" patterns |
| `smart_fake_code_detection.sh` | Auto-runs /fake audit after any Write tool |
| `compose-commands-backup-2026-04-06.sh` | PR composition |
| `mem0_config.py` | Memory system (USER_ID=jleechan) |
| `python_async_lint.py` | Async code linting |
| `post_commit_sync.sh` | Auto-pushes after git commit |
| `git-header.sh` | Shows branch/PR in statusline |

## Engineering Values

### Minimal Code Changes
- Integration before creation: existing file > utility > __init__.py > test file > new file
- New file creation is last resort

### Fail-Closed Over Best-Effort
- "Prefer fail-closed cost controls over best-effort cleanup"
- Auth bypass disabled in production
- Input validation required for production

### Production Safety Over Speed
- Self-hosted runners for private repos
- "Do NOT run config-mutating commands (openclaw doctor, openclaw config set, cp/mv/jq edits on ~/.claude/)"

## Testing Philosophy

- Tests must pass before claiming completion
- TDD for complex fixes (Red-Green-Refactor)
- pytest -q for concise CI output
- asyncio.run() for async test patterns

## Quality Gates

1. Tests pass
2. CodeRabbit CHANGES_REQUESTED resolved
3. Skeptic/evidence gate — verifiable citations
4. /fake audit auto-runs after every Write
5. Hook compliance all green

## Commit Style

- ~526 fix: commits (dominant)
- Agent authorship tracking: [agento], [copilot], [antig]
- Detailed commit bodies: explain why, not just what
