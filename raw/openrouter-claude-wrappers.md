---
name: openrouter-claude-wrappers
description: "claudeor/claudeorop/claudeg/claudek OpenRouter wrappers on BOTH machines; all route via _or_proxy_base → or-anthropic-proxy (8767). Unified 2026-07-20 — Mac no longer hits OpenRouter directly."
metadata: 
  node_type: memory
  type: project
  originSessionId: c1483569-9051-4de8-9c0b-f0a3e542a697
---

Claude Code OpenRouter wrappers (set up on MacBook 2026-07-16, ported to jeff-ubuntu 2026-07-17) live in `~/.bashrc` on both machines: `claudeor`/`claudeoroc` (anthropic/claude-sonnet-4.5), `claudeorop`/`claudeoropc` (anthropic/claude-opus-4.7), `claudeg`/`claudegc` (z-ai/glm-5.2), `claudek`/`claudekc` (moonshotai/kimi-k3), plus `openrouter-check`.

**Why:** Direct `ANTHROPIC_BASE_URL=https://openrouter.ai/api` breaks Claude Code `-p` print mode — exit 0 but zero stdout (verified on both machines 2026-07-17; raw curl works fine). The local proxy `~/.local/bin/or-anthropic-proxy.py` (port **8767** = `$OR_ANTHROPIC_PROXY_PORT`, log `/tmp/or-anthropic-proxy.log`) buffers responses with Content-Length and strips thinking blocks, fixing it.

**Port collision (2026-07-17):** the proxy's original default 8765 collides with `MCP_AGENT_MAIL_PORT=8765` (documented in `~/.bashrc`). On the Mac, agent-mail held 8765 and the wrappers' bare `lsof` port check routed Claude Code INTO the agent-mail server. Moved to 8767 on both machines; wrappers now pass `LISTEN_PORT` explicitly when starting the proxy. The wrapper port check only tests "something listens" — a foreign process on the port silently hijacks the wrappers.

**How to apply:** All wrappers must call `_or_proxy_base` — never point at OpenRouter directly. `OR_PROXY_DISABLED=1` bypasses. On Linux, `claudeo` is NOT an OpenRouter alias (it's the pre-existing `claudedo` opus alias); on Mac `claudeo` is its own OpenRouter/GLM-5.2 wrapper (back-compat). Linux OPENROUTER_API_KEY was dead (401) and was replaced with the Mac's working key (sk-or-v1-79e8d4ff…).

**Unified 2026-07-20 (both machines):** Mac's `.bashrc` previously had NO `_or_proxy_base` helper — `claudeg`/`claudek` inlined the proxy block (2 copies) and `claudeor`/`claudeorop`/`claudeo` pointed at OpenRouter directly (broken `-p`: exit 0, empty stdout, verified). Ported the Linux `_or_proxy_base()` helper to the Mac and refactored `claudeor`/`claudeorop`/`claudeo`/`claudek`/`claudeg` to all delegate to it. Both machines now structurally identical: 1 helper, 0 inlined wrapper proxy blocks, 0 direct-OR wrappers. `claudeor -p` on Mac verified returns `PONG`. Backup at `~/.bashrc.bak-20260720-orproxy-unify` on the Mac.

**Proxy crash fix (2026-07-17, both machines):** `_rewrite_data_line` passed json.dumps output (with `\uXXXX` escapes for non-ASCII) as re.sub's repl string → `re.error: bad escape \u` on ANY unicode in SSE content → unhandled exception, no HTTP response, TUI shows "API error · Retrying" (`-p` with plain-ASCII replies dodged it). Fixed with `lambda _m: new_data` as repl. Also: the proxy reads OPENROUTER_API_KEY at STARTUP — restarting it from a shell/env holding the old dead key causes upstream 401 "User not found" retry loops; always restart from an interactive shell (or with the key explicitly sourced from ~/.bashrc).

## Full Claude Code wrapper family (verified 2026-07-20)

Three distinct families of Claude Code wrappers live in `~/.bashrc` on jeff-ubuntu (Linux) and the MacBook. They are NOT interchangeable:

**Family A — OpenRouter-backed, must route via `_or_proxy_base` → 127.0.0.1:8767:**
| Wrapper | Model | `-c` variant | Notes |
|---|---|---|---|
| `claudeor` | anthropic/claude-sonnet-4.5 | `claudeoroc` | |
| `claudeorop` | anthropic/claude-opus-4.7 | `claudeoropc` | |
| `claudeg` | z-ai/glm-5.2 | `claudegc` | Default small/fast model = glm-4.5-air |
| `claudek` | moonshotai/kimi-k3 | `claudekc` | Reasoning model — always emits thinking blocks; proxy MUST strip them or the SDK chokes |

All Family A wrappers use `--dangerously-skip-permissions --effort high`. Setting `OR_PROXY_DISABLED=1` makes them hit `https://openrouter.ai/api` directly, which **silently breaks `-p` print mode** (exit 0, zero stdout — raw curl still works fine; the failure is in Claude Code's SSE consumption of the unproxied response).

**Family B — direct provider, NO proxy (do NOT route via 8767):**
| Wrapper | Backend | Model |
|---|---|---|
| `claudew` | wafer.ai (`https://pass.wafer.ai`) | GLM-5.1 (`$WAFER_MODEL`) |
| `claudem` / `claudemc` | minimax.io (`https://api.minimax.io/anthropic`) | MiniMax-M3 |

Family B sets `ANTHROPIC_BASE_URL` directly to the provider because those providers return Anthropic-shaped SSE that Claude Code can consume without buffering. They use `--teammate-mode=tmux`.

**Family C — direct Anthropic opus, host-local only:**
- `claudeo` on **Linux** = the pre-existing `claudedo` opus alias (NOT an OpenRouter wrapper). On **Mac**, `claudeo` is its own OpenRouter/GLM-5.2 wrapper (back-compat). This cross-machine name collision is a known gotcha — never assume `claudeo` is the same thing on both machines.

## Verified ground truth (2026-07-20, both machines)

Confirmed via `-p` fibonacci write-file-and-run tests on BOTH jeff-ubuntu and the MacBook:
- `claudeor`, `claudeg`, `claudek` all work in `-p` print mode (write a file, run it, return output) on both machines — the proxy route is required and sufficient.
- `claudek` (kimi-k3) is a reasoning model that **always** emits thinking blocks in its SSE; the proxy strips them or the SDK chokes. Any future "thinking-block-capable" reasoning model added as a wrapper inherits the same requirement.
- Direct `ANTHROPIC_BASE_URL=https://openrouter.ai/api` breaks `claude -p` stdout (exit 0, zero output) — this is WHY the proxy exists. The proxy buffers `Content-Length` and strips thinking blocks.
- Linux `OPENROUTER_API_KEY` was dead (401) and was replaced with the Mac's working key (`sk-or-v1-79e8d4ff…`, stored in `~/.bashrc:256`).
- Before 2026-07-20 the MacBook had NO `_or_proxy_base` helper — `claudeg`/`claudek` inlined the proxy block (2 copies) and `claudeor`/`claudeorop`/`claudeo` pointed at OpenRouter directly (broken `-p`). Fixed by porting the Linux helper to Mac and refactoring all 5 wrappers to delegate. Backup at `~/.bashrc.bak-20260720-orproxy-unify` on the Mac.

## Reusable rule — adding a new model-backed Claude wrapper

1. If the provider is OpenRouter → MUST delegate to `_or_proxy_base` (set `ANTHROPIC_BASE_URL="$(_or_proxy_base)"`). Never hardcode `https://openrouter.ai/api` — `-p` mode silently breaks (exit 0, empty stdout) without the proxy's Content-Length buffering.
2. If the provider is a direct Anthropic-shaped endpoint (wafer.ai, minimax.io) → set `ANTHROPIC_BASE_URL` directly; do NOT route via 8767.
3. If the model is a reasoning model that emits thinking blocks (e.g. kimi-k3) → the proxy's thinking-block stripping is load-bearing; verify `-p` end-to-end (write file → run → return output), not just "PONG".
4. Cross-machine: `claudeo` is NOT portable. On Linux it's `claudedo` opus; on Mac it's OpenRouter/GLM-5.2. When documenting a wrapper, name the machine explicitly.
5. Proxy restart discipline: `or-anthropic-proxy.py` reads `OPENROUTER_API_KEY` at startup. Restarting from a shell holding a stale/dead key causes upstream 401 "User not found" retry loops in the TUI. Always restart from an interactive shell (or with the key sourced from `~/.bashrc`).
6. Proxy port is 8767 (NOT 8765 — 8765 collides with `MCP_AGENT_MAIL_PORT`).

## References

- Linux wrappers: `~/.bashrc:507` (`claudew`), `~/.bashrc:521` (`claudem`/`claudemc`), `~/.bashrc:623` (`_or_proxy_base`), `~/.bashrc:647–716` (claudeor/orop/oroc/oropc/k/kc/g/gc), `~/.bashrc:719` (`openrouter-check`)
- Proxy script: `~/.local/bin/or-anthropic-proxy.py`, log `/tmp/or-anthropic-proxy.log`
- Backup (Mac): `~/.bashrc.bak-20260720-orproxy-unify`
- Memory file: `~/.claude/projects/-home-jleechan-projects/memory/openrouter-claude-wrappers.md`
