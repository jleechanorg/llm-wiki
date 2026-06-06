# AO Codex Worker Blockers — 2026-06-05

Source: agent-orchestrator session, fixes applied to agent-codex plugin, core config, CLI start.

## Finding 1 — codex --full-auto flag removed from Codex CLI

The `ao-plugin-agent-codex` `appendApprovalFlags()` pushed `--full-auto` for
permissionless mode. The installed Codex CLI no longer recognises this flag and
exits with `error: unexpected argument '--full-auto' found`.

Fix: replace with `--dangerously-bypass-approvals-and-sandbox`.
Files: `packages/plugins/agent-codex/src/index.ts:840`, `src/index.test.ts`.
Rebuild both the plugin and `ao-cli` after edit.

## Finding 2 — ao spawn requires running.json written only by ao start

`ao spawn` calls `getRunning()` → reads `~/.agent-orchestrator/running.json`.
This file is written exclusively by `ao start`, not by per-project lifecycle-worker
processes. When the machine boots or `ao start` was never run, `running.json` is
absent and `ao spawn` errors "AO is not running".

Workaround: write the file manually using a lifecycle-worker PID and the correct
config path/port (RunningState shape).

## Finding 3 — ao start auto-opens browser tab via waitForPortAndOpen

`packages/cli/src/commands/start.ts:892` calls `waitForPortAndOpen(port, url, signal)`
which runs macOS `open <url>` once the port becomes active. No config option existed to
suppress this. Fix: added `openBrowser: boolean` (default true) to config schema and
types; gated the open call on `config.openBrowser !== false && !process.env.AO_NO_OPEN_BROWSER`.
Set `openBrowser: false` in `~/.hermes/agent-orchestrator.yaml` and `~/.hermes_prod/agent-orchestrator.yaml`.

Bead: bd-40k8 (closed)
