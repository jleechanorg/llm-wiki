# Codex Slash Autocomplete Proof Boundary (2026-05-26)

Source: `raw/feedback_2026-05-26_codex_slash_autocomplete_proof_boundary.md`

## Summary

`codex exec --yolo` resolving a prompt that begins with a slash command is not
native Codex TUI autocomplete proof. It only proves model-side slash-command
translation or file-reading behavior.

## Finding

In Codex CLI `0.128.0`, custom files under:

- `/Users/jleechan/.codex/commands/code-standards.md`
- `/Users/jleechan/.codex/prompts/code-standards.md`

did not appear in the interactive slash autocomplete menu. Fresh TUI and tmux
captures showed only built-in commands:

- `/model`
- `/fast`
- `/permissions`
- `/keymap`
- `/experimental`
- `/autoreview`
- `/memories`
- `/skills`

Typing `/code-standards` left it as plain prompt input. Enabling
`external_migration = true` did not change autocomplete behavior.

## Operational Rule

When validating Codex slash UX:

- Use tmux or another real interactive TUI capture for autocomplete claims.
- Use `codex exec` only for model-side translation/resolution checks.
- Report those evidence classes separately.

## Jeffrey Oracle Impact

This does not affect `[[jeffrey-oracle]]`; it is a local operator workflow
lesson about Codex CLI verification boundaries.
