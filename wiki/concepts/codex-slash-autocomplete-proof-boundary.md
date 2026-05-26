# Codex Slash Autocomplete Proof Boundary

Codex has separate evidence surfaces for slash-looking inputs:

- **Native TUI autocomplete**: the interactive popup opened by typing `/`.
- **Model-side slash translation**: the agent reads local command/skill files
  after receiving a prompt that begins with a slash token.
- **Skill visibility**: the model sees skill metadata or loads `SKILL.md` files.

These are not interchangeable.

As of the 2026-05-26 test on Codex CLI `0.128.0`, `~/.codex/commands` and
`~/.codex/prompts` files were resolvable by model-side workflows but did not
appear in native TUI autocomplete. The `/` popup listed built-ins only.

Use tmux capture or another real interactive session to prove autocomplete.
Use `codex exec` only to prove model-side translation/resolution.
