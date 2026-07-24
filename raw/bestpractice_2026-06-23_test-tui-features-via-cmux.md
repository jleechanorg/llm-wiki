---
name: Test TUI-only Claude Code features via cmux, not --print
description: Claude Code slash commands (e.g., /advisor, /config) are TUI-only. Verify them by spawning a real interactive session in cmux — never via `claude --print "/feature"`.
type: feedback
bead: none
---

# Test TUI-only Claude Code features via cmux, not `--print`

## Context

When asked "does Claude Code's `<feature>` work?", the natural reflex from a
non-interactive shell is to test it via:

```bash
claude --print "/advisor"   # ← this is the wrong test
```

`--print` mode is non-interactive. Slash commands (`/advisor`, `/config`,
`/model`, `/effort`, etc.) render inside the Ink TUI as menus, dialogs, or
pickers — they have no `--print` representation. The binary correctly
returns:

> `/<feature> isn't available in this environment.`

That error is **not a feature-gate failure** — it is the binary
correctly reporting "you are in non-interactive mode, slash commands do
not apply here." Mistaking this error for a config / auth / network
failure leads to a 30-minute rabbit hole of reading minified binary
strings, guessing at gates (`isFirstPartyApiBackend`, `xr()`,
`VW()`), and trying every env-var combination under the sun.

## Solution

For any "does this Claude Code feature actually work" question, the
default verification path is a **real interactive TUI session in
cmux**:

```bash
# 1. Spawn a fresh Claude Code workspace in cmux
export CMUX_SOCKET_PATH=/private/tmp/cmux-debug-may-18.sock
WS_OUT=$(cmux new-workspace --cwd "$PWD" --command "claude")
WS=$(echo "$WS_OUT" | grep -oE 'workspace:[0-9]+' | head -1)

# 2. Find the auto-created surface in that workspace
sleep 2
SURF=$(cmux list-pane-surfaces --workspace "$WS" 2>/dev/null \
       | grep -oE 'surface:[0-9]+' | head -1)

# 3. Wait for Claude to be ready (look for the `❯` prompt in the screen)
cmux read-screen --workspace "$WS" --surface "$SURF" --scrollback --lines 30

# 4. Send the slash command + press Enter
cmux send --workspace "$WS" --surface "$SURF" "/advisor"
cmux send-key --workspace "$WS" --surface "$SURF" enter

# 5. Read the result (dialog, picker, error message, etc.)
sleep 2
cmux read-screen --workspace "$WS" --surface "$SURF" --scrollback --lines 50

# 6. Clean up — Esc out + close workspace
cmux send-key --workspace "$WS" --surface "$SURF" escape
cmux close-workspace --workspace "$WS"
```

For TUI features that involve real-time interaction (pickers, dialogs,
multi-step flows), `--print` will never replicate them. The cmux path
is the only honest test.

## Verification (2026-06-23)

Tested: `claude --print "/advisor"` (with and without various
`ANTHROPIC_BASE_URL` settings) — always returned
"`/advisor` isn't available in this environment."

Then in a fresh cmux workspace (`workspace:30 surface:65`):

- Status bar pre-`/advisor`: `Advisor Tool (experimental) is on and may use more tokens · /advisor`
- After `cmux send "/advisor" + enter`: opened the picker dialog
- Picker showed: `1. Fable 5 / ❯ 2. Opus 4.8 ✔ / 3. Sonnet 4.6 / 4. No advisor`
- Opus 4.8 was pre-selected (the `✔` = current value), confirming the
  `advisorModel: "claude-opus-4-8"` setting in `~/.claude/settings.json`
  was being read correctly.

**Conclusion**: The advisor was working from the moment the setting was
added. The 30+ minutes spent reading minified binary strings,
inspecting `llm-inspector` capture proxy, and trying experimental env
vars was wasted because the actual test (`--print`) could not
demonstrate TUI behavior.

## When `--print` IS valid evidence

- Simple completion tasks: `claude --print "what model are you?"` → if
  the model responds, auth + firstParty + base URL are all working.
- API contract tests: `claude --print "list these files"` exercises
  tool use, file reading, etc. without needing a TUI.
- Streaming behavior, response time, error recovery — all observable
  in `--print`.

`--print` is **not** evidence for any feature that is implemented as a
TUI slash command, dialog, picker, or status-bar annotation.

## References

- cmux skill: `~/.hermes_prod/skills/cmux/SKILL.md`
- `~/.claude/settings.json` (advisorModel + env block)
- Session transcript: Slack C09GRLXF9GR thread 1782248089.973629
  (2026-06-23 advisor opus 4.8 request)
- Related (out of scope here): `jleechan-9yt` bead about advisor
  orchestration layer in agent-orchestrator

## Reusable pattern

Any time a question is "does Claude Code feature X work" and X is a
slash command, dialog, picker, or status indicator, the cmux test is
the *only* authoritative answer. Treat `--print` as a **non-test** for
those features — even when the binary returns an error, that error
specifically means "I cannot show you this in non-interactive mode",
not "this feature is broken."
