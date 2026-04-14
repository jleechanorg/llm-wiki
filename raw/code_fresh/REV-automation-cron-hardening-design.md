# Automation Cron Hardening Design (Orchestration/Pr Monitor Reliability)

## GOAL
- Stop cron-driven automation failures caused by environment/path/binary drift.
- Make cron jobs deterministic across runs and recoverable without manual shell fiddling.
- Separate immediate operational fixes that should ship in this PR from broader re-architecture work.

## MODIFICATION
- Add a small design artifact under `.beads/` that drives the following implementation plan:
  - `automation/install_cron_entries.sh`
    - Pin and normalize user home before writing managed env.
    - Generate `BASH_ENV` in a stable user-home path, not a temp `HOME` value.
    - Prefer an absolute `jleechanorg-pr-monitor` binary path in managed jobs.
  - `automation/crontab.template`
    - Replace bare command calls with stable wrapper or absolute command path references.
  - `automation/run_automation_cron_one_minute.sh`
    - Add explicit backup/restore invariants for one-minute validation window.
    - Ensure command environment checks run under the same launcher as production jobs.
  - `automation/tests/test_install_cron_entries.sh`
    - Add/extend tests for:
      - install script with overridden `HOME`
      - generated `BASH_ENV` path stability
      - binary path resolution in managed entries
  - `automation/tests/test_crontab_restore_safety.sh`
    - Add assertions that existing user-managed entries are preserved while managed block is replaced.

## NECESSITY
Recent logs show cron and script failures that map directly to these issues:
- `/bin/bash: jleechanorg-pr-monitor: command not found` during cron runtime.
- `codex` runs completing but cron jobs still using unexpected paths in practice.
- `BASH_ENV` pointing at non-user-home temporary directories, suggesting unstable `HOME` during script installation or runtime.

Both are environment determinism failures, not core orchestration logic failures.

## INTEGRATION PROOF
- Manual and scripted checks in this repo can validate that:
  - managed crontab block contains `SHELL=/bin/bash`.
  - managed block contains stable, explicit env bootstrap path.
  - all automation jobs execute with explicit `which jleechanorg-pr-monitor` and expected `PATH`/NVM state.
  - user crontab entries outside managed block are preserved.

## Root-Cause Model

1. Environment mismatch in non-interactive cron context
- Cron does not source interactive shell startup files.
- `install_cron_entries.sh` and existing scripts currently trust `$HOME`, which can be non-user temp in certain execution contexts.
- `BASH_ENV` generated from unstable `$HOME` points to transient paths, especially visible as `/var/folders/.../.codex/cron_bash_env.sh` in managed block.

2. Implicit command resolution in jobs
- `jleechanorg-pr-monitor` in crontab depends on `PATH` correctness.
- If PATH is wrong or wrong binary shadows expected binary, cron runs the wrong executable.
- This can coexist with valid CLI logic and still fail at runtime.

3. Missing binary provenance checks
- No explicit per-job assertion that the binary currently launched is the intended installed binary for this host.
- Weak observability during cron failures increases MTTR.

## Design (This PR)

### A. Stabilize home/env bootstrap
- Add a helper in `automation/install_cron_entries.sh`:
  - Resolve canonical user home via account lookup (`$USER`/`$LOGNAME`).
  - Fallback to current `$HOME` only if lookup fails.
  - Always write managed env files under canonical home.
- Ensure `BASH_ENV` and generated `.codex/cron_bash_env.sh` are written using that canonical home.

### B. Remove command discovery ambiguity for managed jobs
- Option 1 (immediate): replace managed cron command names with absolute binary path resolved at install time:
  - `/Users/<user>/.local/bin/jleechanorg-pr-monitor` (or resolved canonical path).
  - Use one helper (`resolve_pr_monitor_binary`) to keep installs deterministic.
- Option 2 (safer): replace each cron command with wrapper command path (`$HOME/.local/bin/automation-runner.sh`) that:
  - sources the bootstrap
  - validates `command -v jleechanorg-pr-monitor`
  - logs resolved path and key env keys
  - execs the target command with `"$@"`.

### C. One-minute test harness hardening
- Keep `run_automation_cron_one_minute.sh` backup and restore logic.
- Add explicit post-install self-test command:
  - `jleechanorg-pr-monitor --version` must run.
  - managed jobs must print resolved binary path when executed.

### D. Testing
- Extend existing shell tests to reproduce the known failure mode:
  - fake cron shim with `HOME=/var/folders/...` and template install.
  - assert generated managed block uses canonical home not fake temp.
  - assert managed entries include either absolute executable or wrapper invocation.
  - assert legacy user entries survive replacement.

## What to fix in this PR vs later

### Fix in this PR (high urgency)
- Path/`HOME` stability and managed `BASH_ENV` hardening.
- Deterministic `jleechanorg-pr-monitor` resolution for managed jobs.
- Regression tests for installation and duplicate-removal behavior.
- Log evidence in this branch for at least one successful one-minute run after install.

### Defer (follow-up PR)
- Centralized scheduler service instead of cron for richer retry/backoff/state.
- Queue-based orchestration worker with execution persistence and per-job retry policy.
- Per-job lock/expiry semantics and webhook-driven trigger mode.
- Migration from shell script glue to Python orchestrator service under `orchestration/`.

## Open-source scheduler options explored
- APScheduler (Python): cron-like scheduling + job stores + max runtime/retry hooks.
- Airflow (heavy): robust DAG management; likely overkill for current scope.
- Prefect (medium): strong orchestration primitives and visibility, higher stack weight.
- supercronic (containers): minimal cron replacement with better logs/restarts.

## Files likely touched
- `automation/install_cron_entries.sh`
- `automation/crontab.template`
- `automation/run_automation_cron_one_minute.sh`
- `automation/tests/test_install_cron_entries.sh`
- `automation/tests/test_crontab_restore_safety.sh`

## Evidence bundle references
- Live log evidence currently includes:
  - `/Users/jleechan/Library/Logs/worldarchitect-automation/jleechanorg_pr_monitor.log`
  - `/Users/jleechan/Library/Logs/worldarchitect-automation/codex_automation.log`
  - `/Users/jleechan/Library/Logs/worldarchitect-automation/codex_automation_api.log`
- Managed block currently observed with unstable `BASH_ENV` and `PATH` from temp `HOME` under `/var/folders/...`.
