---
title: "claude-code-cli"
type: concept
tags: [tooling, cli, anthropic]
last_updated: 2026-07-20
---

# claude-code-cli

Anthropic's official CLI for Claude. The thing all `~/.bashrc` wrappers (claudeor, claudew, claudem, etc.) ultimately invoke. Native `claude` command. All wrappers in this user's setup pass `--dangerously-skip-permissions`; OpenRouter-backed ones additionally pass `--effort high`.

## Notable behaviors

- `-p` / `--print` print mode is sensitive to SSE response shape. Direct OpenRouter responses break it (exit 0, zero stdout) — this is why `[[or-anthropic-proxy]]` exists.
- `--teammate-mode=tmux` used by direct-provider wrappers (claudew, claudem) for Agent Teams integration.
- Reads `ANTHROPIC_BASE_URL`, `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_API_KEY`, `ANTHROPIC_MODEL`, `ANTHROPIC_DEFAULT_*_MODEL` env vars.

## See also

- [[openrouter-claude-wrappers]] — the wrapper family
- [[or-anthropic-proxy]] — required for OpenRouter-backed usage
