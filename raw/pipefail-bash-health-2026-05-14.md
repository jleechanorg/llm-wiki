---
name: pipefail-required-bash-health-scripts
description: Bash health-check scripts using tee must set -o pipefail or exit codes are masked
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 5e846711-556f-4eab-85b3-0883dbc44f75
---

Bash scripts that pipe through `tee` (e.g., `command 2>&1 | tee -a logfile`) silently mask the left-side exit code. Without `set -o pipefail`, the pipeline returns tee's exit code (always 0 for successful write), making failure detection impossible.

**Why:** health-check.sh line 98 (`command_ok bash "$LAUNCHD_SCRIPT" 2>&1 | tee -a "$LOG_FILE"`) would always appear successful even when install-launchagents.sh failed, preventing the self-heal loop from escalating. CodeRabbit flagged this as a merge blocker.

**How to apply:** Any script with `set -u` (without `pipefail`) that uses pipelines must add `set -uo pipefail`. Verify the setting wasn't corrupted by a prior edit (a previous edit produced `pipefailo pipefail` — always re-read the file after editing shell `set` directives).
