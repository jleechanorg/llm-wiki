# OpenCode TUI Wrapper

**Category**: CLI / Tool Integration

## Pattern

When wrapping `opencode` in a shell function, the TUI (`opencode [project]`) and run (`opencode run`) subcommands have different flag sets.

| Mode | Command | Flags |
|------|---------|-------|
| Interactive TUI | `opencode --model provider/model [path]` | `-m/--model` accepted |
| Non-interactive | `opencode run --model ... --dangerously-skip-permissions msg` | Both flags accepted |

## Anti-Pattern

Using `--dangerously-skip-permissions` with the TUI invocation causes silent help-exit (no error, just help text + prompt return).

## Canonical wrapper (opencodew in ~/.bashrc)

```bash
opencodew() {
  case "${1:-}" in
    "")   opencode --model wafer.ai/GLM-5.1 . ;;
    /*)   opencode --model wafer.ai/GLM-5.1 "$@" ;;
    run)  shift; opencode run --model wafer.ai/GLM-5.1 --dangerously-skip-permissions "$@" ;;
    models|providers|debug|...) opencode "$@" ;;
    *)    opencode run --model wafer.ai/GLM-5.1 --dangerously-skip-permissions "$@" ;;
  esac
}
```

## Related

- Wafer Pass provider: `OPENAI_API_KEY=$WAFER_API_KEY OPENAI_BASE_URL=https://pass.wafer.ai/v1`
- Source: `feedback_2026-05-07_opencode-tui-run-flag-split.md`
