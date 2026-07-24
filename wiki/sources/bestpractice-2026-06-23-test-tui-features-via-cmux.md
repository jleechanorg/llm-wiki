---
title: "Test TUI-only Claude Code features via cmux, not --print"
type: source
tags: [claude-code, cmux, tui, testing, best-practice, slash-commands]
date: 2026-06-23
source_file: ~/.claude/projects/-Users-jleechan--hermes-prod/memory/bestpractice_2026-06-23_test-tui-features-via-cmux.md
---

## Summary

When asked whether a Claude Code feature (slash command, dialog, picker, or status indicator) works, the only authoritative test is a real interactive TUI session spawned in cmux. `claude --print "/feature"` will always return `"/<feature> isn't available in this environment"` regardless of whether the feature actually works, because `--print` is non-interactive mode. Treating that error as a config/auth/network failure leads to wasted time chasing phantom gates in the binary.

## Key Claims

- `--print` mode is **not evidence** for TUI features (slash commands, dialogs, pickers, status indicators). The error "isn't available in this environment" specifically means "I cannot show you this in non-interactive mode," not "this feature is broken."
- The default verification path for any "does Claude Code feature X work" question (when X is TUI-only) is: `cmux new-workspace --command claude` → wait for `❯` prompt → `cmux send "/feature"` + `cmux send-key enter` → `cmux read-screen --scrollback --lines 50`.
- Verified 2026-06-23 on `/advisor`: advisor with `advisorModel: claude-opus-4-8` in `~/.claude/settings.json` was working the whole time. The cmux test showed the picker with Opus 4.8 pre-selected.
- The user (Jeffrey) had to push back twice ("are you opening claude code itself and typing /advisor?", "use cmux stop being lazy") before the correct test was performed.

## Key Quotes

> `/<feature> isn't available in this environment.
> That error is **not a feature-gate failure** — it is the binary correctly reporting "you are in non-interactive mode, slash commands do not apply here." Mistaking this error for a config / auth / network failure leads to a 30-minute rabbit hole of reading minified binary strings, guessing at gates (`isFirstPartyApiBackend`, `xr()`, `VW()`), and trying every env-var combination under the sun. — memory file

## Connections

- [[cmux]] — terminal multiplexer; provides the `new-workspace`/`send`/`send-key`/`read-screen` primitives that make TUI testing possible without opening a GUI
- [[ClaudeCode]] — the binary being tested; its `--print` flag is the wrong tool for TUI features
- [[HermesTUI]] — the broader Hermes product line that also uses cmux for TUI workflows
- [[InteractiveTesting]] — generic concept: some features only exist in interactive mode and need interactive tests
