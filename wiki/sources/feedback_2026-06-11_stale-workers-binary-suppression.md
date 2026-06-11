---
title: "Stale background daemon processes bypass codebase and configuration updates"
type: source
tags: [daemon, configuration, process-management, browser-suppression, doctor]
source_file: "raw/feedback_2026-06-11_stale-workers-binary-suppression.md"
sources: []
last_updated: 2026-06-11
---

## Summary
Deploying codebase fixes (like browser auto-open suppression) and updating config files (setting `openBrowser: false`) will be completely bypassed if background daemons (such as the 16 legacy `lifecycle-worker` processes) are still running outdated binaries from prior sessions. Identifying and terminating stale daemon processes via `ao doctor --fix` (with explicit human authorization `PROCESS KILL APPROVED`) and canonically restarting them is required to ensure behavioral changes are active.

## Reusable Pattern
- **Verification Rule**: When configuration or behavioral changes are deployed, do not assume they are active simply because the config is updated. Stale background worker processes running older binary code will bypass the updates.
- **Diagnostic Step**: Run `ao doctor` to check for non-canonical lifecycle workers.
- **Remediation**: Obtain approval, run `ao doctor --fix` to clean up stale workers, and restart them using the new canonical binary. Confirm health via `ao doctor` returning `Results: XX PASS, 0 WARN, 0 FAIL`.

## References
- PR #679
- `ao doctor` diagnostics
- Bead: `bd-stlw`
- Does this affect `[[jeffrey-oracle]]`? No.
