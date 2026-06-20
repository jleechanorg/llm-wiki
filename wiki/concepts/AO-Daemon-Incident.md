---
title: "AO Daemon Incident Masking"
type: concept
tags: [agent-orchestrator, daemon, launchd, AO, incident]
last_updated: 2026-06-18
---

AO monitor was reported "disabled" but the launchd label was enabled — the wrapper died under `set -u` while sourcing interactive shell init, masking the real blocker.

## Root Cause

Wrapper script `stability-report.launchd.sh` used `set -u` (nounset) while sourcing an interactive shell init file that referenced unset variables. The script exited silently, making the daemon appear dead.

## Real Blocker

Once fixed, AO logs showed the real blocker: PR backfill failing on a stale checked-out worktree branch lock.

## Pattern

AO daemon incidents can mask the real blocker. When a daemon appears dead, check:
1. Is the launchd label enabled?
2. Does the wrapper script have `set -u` or `set -e`?
3. Does it source interactive shell init files?
4. What's in the actual AO logs?

## Also Found

AO split-brain: duplicate lifecycle workers (`worldarchitect` x3 plus alias `worldarchitect.ai`) while `ai.agento.lifecycle-all` sat `not running` — claims looked attached briefly then lost durable registration.

## Related Case: MCP daemon stdio env drop + launchd silent death (2026-06-17)

A second instance of the "supervisor appears dead, real cause is upstream" pattern surfaced in the MCP daemon (`~/.config/mcp-daemon/start-mcp-daemons.sh`) supervised by `com.jleechan.mcp-daemon.plist`.

**Symptom 1: worldarchitect MCP timed out (port UP, child crashing).** Root cause: `start_stdio_server` function signature was `(name, cmd, port)` — the `envstr` argument was parsed by the SERVERS array loop but never applied. Every stdio server (worldarchitect/context7/gemini-cli/playwright/perplexity/sequential-thinking/memory/ddg/filesystem) had its declared env vars silently dropped. The worldarchitect child crashed with `ModuleNotFoundError: No module named 'mvp_site'` because the uv-tool editable install pointed to a deleted worktree path. The PYTHONPATH override was being parsed but discarded. **Diagnostic tell:** `lsof -i :<port>` shows the port bound, but `tail ~/.config/mcp-daemon/logs/<server>.log` shows `Child stderr: ModuleNotFoundError` on every connection attempt.

**Symptom 2: google-docs MCP unable to connect (port DOWN, no respawn).** Root cause: launchd job `com.jleechan.mcp-daemon` was in `state = not running, active count = 0` with no log entry. Despite `StartInterval=300`, the job had stopped re-firing on its 5-min schedule. When the prior supergateway crashed, nothing respawned it. **Diagnostic tell:** `launchctl print "gui/$(id -u)/com.jleechan.mcp-daemon"` shows the dead state. `tail ~/.config/mcp-daemon/logs/launchd.log` shows the last `[ready]` line but no subsequent `[starting MCP daemons v2]`.

**Fix pattern:**
1. **Code bug:** update `start_stdio_server` signature to `(name, cmd, port, envstr)` and apply env via the same `IFS=';'; for envpair in ...; do export KEY=val; done` loop as `start_http_server`. Update call site to pass `"${envstr:-}"`.
2. **launchd recovery:** `launchctl unload ~/Library/LaunchAgents/com.jleechan.mcp-daemon.plist && launchctl load -w ~/Library/LaunchAgents/com.jleechan.mcp-daemon.plist` re-triggers `RunAtLoad` and brings all 11 daemons back up.
3. **Durable prevention:** add `KeepAlive` or external watchdog to the plist, since `StartInterval=300` alone is fragile.

**Lesson:** the same anti-pattern (silent partial failure, surfaced only when a downstream user reports symptoms) manifests in two different ways here — a function signature mismatch that drops config silently, and a launchd job that stops scheduling silently. In both cases, the diagnostic order matters: check the supervisor state first (launchd, the script's status output), then the child state (lsof, log tail). Don't assume "the script is configured correctly" — verify each layer.

**References:**
- Source: `sources/feedback-2026-06-17-mcp-daemon-diagnosis-fixes.md` (bead rev-gu8bi, closed)
- Memory: `~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-17_mcp_daemon_diagnosis_fixes.md`
- Roadmap: `~/roadmap/learnings-2026-06.md` (entry: "MCP daemon: start_stdio_server env drop + launchd silent death")

## Connections

- [AO-Split-Brain](AO-Split-Brain.md) — AO split-brain with duplicate lifecycle workers
- [AO-Blocker-Matrix](AO-Blocker-Matrix.md) — PR blocker triage
- [AO-Claim-Fail-Closed](AO-Claim-Fail-Closed.md) — AO claim fail-closed execution
- [DaemonBootstrap](DaemonBootstrap.md) — daemon bootstrap patterns
- [Launchd](Launchd.md) — launchd job lifecycle and silent-death patterns
- [EnvironmentVariableConfiguration](EnvironmentVariableConfiguration.md) — env var precedence and configuration patterns
