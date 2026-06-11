---
name: Stale background daemon processes bypass codebase and configuration updates
description: Stale background processes (such as legacy lifecycle-workers) running older binaries bypass configuration-level changes until they are killed and canonically restarted.
type: feedback
bead: bd-stlw
---

# Stale Background Daemons Bypass Codebase and Configuration Updates

## Context
During troubleshooting of automated browser auto-openings to `localhost:3000` (regression: `bd-#667`), we deployed browser suppression options (`openBrowser: false`) globally in `~/.hermes/agent-orchestrator.yaml`. However, browser tabs continued to open. 

## Technical Detail
1. **The Root Cause**: 16 non-canonical `lifecycle-worker` background daemon processes were running stale binaries compiled prior to the browser auto-open suppression fix being built and integrated.
2. **Bypass Behavior**: Because these daemons run older versions of the binaries, they ignore/lack configuration parsing for `openBrowser: false`, continuing to execute the old behavior of launching browser windows when checking active project sessions.
3. **Resolution**:
   * Running `/Users/jleechan/bin/ao doctor` identifies the non-canonical background workers and lists their PIDs.
   * Running `ao doctor --fix` (with explicit human authorization `PROCESS KILL APPROVED`) terminates all stale worker processes.
   * Spawning new lifecycle workers canonically via `AO_CONFIG_PATH="/Users/jleechan/.hermes/agent-orchestrator.yaml" /Users/jleechan/bin/ao lifecycle-worker <project>` restarts them using the correct binary path, which then successfully honors `openBrowser: false`.

## Reusable Pattern
- **Verification Rule**: When configuration or behavioral changes are deployed, do not assume they are active simply because the config is updated. Stale background worker processes running older binary code will bypass the updates.
- **Diagnostic Step**: Run `ao doctor` to check for non-canonical lifecycle workers.
- **Remediation**: Obtain approval, run `ao doctor --fix` to clean up stale workers, and restart them using the new canonical binary. Confirm health via `ao doctor` returning `Results: XX PASS, 0 WARN, 0 FAIL`.

## References
- PR #679
- `ao doctor` diagnostics
- Bead: `bd-stlw`
