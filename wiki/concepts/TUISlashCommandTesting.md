---
title: "TUISlashCommandTesting"
type: concept
tags: [claude-code, cmux, tui, testing, slash-commands, interactive]
sources: [bestpractice-2026-06-23-test-tui-features-via-cmux.md]
last_updated: 2026-06-23
---

# TUI Slash Command Testing

## Definition

The practice of testing Claude Code TUI features (slash commands, dialogs, pickers, status indicators) by spawning a real interactive TUI session in cmux — **not** by using `claude --print "/feature"` from a non-interactive shell.

## Why --print is wrong for TUI features

`--print` mode is non-interactive. Slash commands like `/advisor`, `/config`, `/model`, `/effort` render inside the Ink TUI as menus, dialogs, or pickers — they have no `--print` representation. The binary correctly returns:

> `/<feature> isn't available in this environment.`

That error is **not a feature-gate failure** — it is the binary correctly reporting "you are in non-interactive mode, slash commands do not apply here." Mistaking this error for a config/auth/network failure leads to wasted time reading minified binary strings (`isFirstPartyApiBackend`, `xr()`, `VW()`) and trying every env-var combination.

## The correct test path

```bash
# 1. Spawn fresh Claude Code workspace in cmux
export CMUX_SOCKET_PATH=/private/tmp/cmux-debug-may-18.sock
WS_OUT=$(cmux new-workspace --cwd "$PWD" --command "claude")
WS=$(echo "$WS_OUT" | grep -oE 'workspace:[0-9]+' | head -1)

# 2. Find the auto-created surface
sleep 2
SURF=$(cmux list-pane-surfaces --workspace "$WS" 2>/dev/null \
       | grep -oE 'surface:[0-9]+' | head -1)

# 3. Wait for Claude to be ready (look for the `❯` prompt)
cmux read-screen --workspace "$WS" --surface "$SURF" --scrollback --lines 30

# 4. Send the slash command + press Enter
cmux send --workspace "$WS" --surface "$SURF" "/advisor"
cmux send-key --workspace "$WS" --surface "$SURF" enter

# 5. Read the result
sleep 2
cmux read-screen --workspace "$WS" --surface "$SURF" --scrollback --lines 50

# 6. Clean up
cmux send-key --workspace "$WS" --surface "$SURF" escape
cmux close-workspace --workspace "$WS"
```

## When --print IS valid evidence

- Simple completion tasks: `claude --print "what model are you?"`
- API contract tests: tool use, file reading, error handling
- Streaming behavior, response time, recovery patterns
- Anything that does **not** require a TUI slash command, dialog, picker, or status bar

`--print` is **not** evidence for any feature implemented as a TUI slash command, dialog, picker, or status indicator — even when the binary returns an error, that error specifically means "I cannot show you this in non-interactive mode," not "this feature is broken."

## Verified example (2026-06-23)

Test target: `advisorModel: "claude-opus-4-8"` in `~/.claude/settings.json` — was the advisor actually using Opus 4.8?

- `claude --print "/advisor"` (with and without various `ANTHROPIC_BASE_URL` settings) → always returned "isn't available in this environment"
- `cmux send "/advisor" + enter` in `workspace:30 surface:65` → opened the picker dialog showing `1. Fable 5 / ❯ 2. Opus 4.8 ✔ / 3. Sonnet 4.6 / 4. No advisor`
- The `✔` on Opus 4.8 = current selection = the `advisorModel` setting was being read correctly. Feature was working the whole time.

## Failure mode this prevents

- 30+ minute rabbit hole reading minified JS bundles
- Phantom-gate theorizing (`isFirstPartyApiBackend`, `xr()`, `VW()`)
- Adding redundant env vars to `settings.json` that don't change behavior
- Burning context on debug output that doesn't apply to the actual test environment

## Related

- [[cmux]] — the terminal multiplexer that makes TUI testing possible
- [[ClaudeCode]] — the binary being tested; its `--print` flag is the wrong tool for TUI features
- [[InteractiveTesting]] — broader concept: some features only exist in interactive mode and need interactive tests
- Source: [[bestpractice-2026-06-23-test-tui-features-via-cmux]]
