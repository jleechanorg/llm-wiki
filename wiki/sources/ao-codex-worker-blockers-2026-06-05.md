# AO Codex Worker Blockers — 2026-06-05

**Source:** agent-orchestrator session — `packages/plugins/agent-codex`, `packages/core/src/config.ts`, `packages/cli/src/commands/start.ts`
**Bead:** bd-40k8 (closed)

## Summary

Three blockers prevented spawning a Codex AO worker for PR #654 (`feat/skeptic-model-list`). All three were diagnosed and fixed in the same session.

## Blocker 1 — `--full-auto` flag removed from Codex CLI

**Symptom:** Worker pane exits immediately with `error: unexpected argument '--full-auto' found`.

**Root cause:** `appendApprovalFlags()` in `packages/plugins/agent-codex/src/index.ts:840` used `--full-auto` for `permissionless` mode. The installed Codex CLI version no longer accepts this flag.

**Fix:**
```typescript
// Before
parts.push("--full-auto");
// After
parts.push("--dangerously-bypass-approvals-and-sandbox");
```
Update tests and rebuild:
```bash
pnpm --filter @jleechanorg/ao-plugin-agent-codex build
pnpm --filter @jleechanorg/ao-cli build
```

## Blocker 2 — `ao spawn` needs `running.json` written only by `ao start`

**Symptom:** `ao spawn` errors "AO is not running — lifecycle polling is inactive" even when a lifecycle-worker process is active.

**Root cause:** `ao spawn` → `getRunning()` reads `~/.agent-orchestrator/running.json`. Only `ao start` writes this file. Individual `ao lifecycle-worker <project>` processes do not.

**RunningState shape:**
```json
{ "pid": number, "configPath": string, "port": number, "startedAt": string, "projects": string[] }
```

**Workaround:** Write `running.json` manually using a lifecycle-worker PID.

## Blocker 3 — `ao start` auto-opens browser via `waitForPortAndOpen`

**Symptom:** Browser tab opens to `http://localhost:<port>/sessions/<id>` every time `ao start` runs (or on `ao-manager.sh` restarts).

**Root cause:** `start.ts:892` unconditionally calls `waitForPortAndOpen()` which runs macOS `open <url>` once the port accepts connections.

**Fix:** Added `openBrowser: boolean` (default `true`) to config schema. Gate in `start.ts`:
```typescript
const shouldOpenBrowser =
  opts?.dashboard !== false &&
  config.openBrowser !== false &&
  !process.env["AO_NO_OPEN_BROWSER"];
```
Set `openBrowser: false` in `~/.hermes/agent-orchestrator.yaml` and `~/.hermes_prod/agent-orchestrator.yaml`.

## Related

- [[ao-spawn-workflow]] — `ao spawn` entry point and prerequisites
- [[codex-agent-plugin]] — `packages/plugins/agent-codex` architecture
