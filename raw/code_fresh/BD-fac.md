# BD-fac

## GOAL
Improve `scripts/venv_utils.sh` so self-hosted CI can create and reuse virtual environments reliably when path access is constrained, and avoid reusing corrupted venvs that cause unstable test runs.

## MODIFICATION
- Added writable-path resolution for venv creation before writing to disk.
- Added a venv health check to reject partially broken environments and recreate them automatically.
- Added fallback and directory checks so CI can recover to a safe cache location if the primary venv path is not writable.
- Preserved existing dependency install flow while tightening validation and path diagnostics.

## NECESSITY
Self-hosted runner environments can present transient workspace/path permission edge cases that produce flaky CI failures unrelated to product code. Reliable venv setup reduces avoidable infra-classified retries and lowers false-negative pipeline failures.

## INTEGRATION PROOF
- Updated implementation in `scripts/venv_utils.sh`.
- Local and CI call sites that use `setup_venv`/`ensure_venv` remain unchanged, so the hardening is transparent to existing consumers.
- Next action: rerun affected self-hosted jobs to confirm lower preflight/setup failure rates.
