# BD-oom

## GOAL
Make infra failure classification for memory-related installer/test failures deterministic and avoid false-positive matches that could hide real causes.

## MODIFICATION
- Tightened the OOM matcher in `scripts/ci/classify_infra_failure.sh` to remove broad token-only patterns.
- Kept explicit failure indicators for:
  - explicit memory exhaustion terms (`cannot allocate memory`, `MemoryError`, `OutOfMemoryError`)
  - process termination patterns tied to runners/tooling (`killed` patterns with `python/pip/npm/node/pytest/uv/poetry`)
  - kernel/exit-code OOM indicators (`Out of memory`, `exit code 137`)

## NECESSITY
The previous matcher was broad enough to classify non-infra text as infra, which could drive incorrect retry and quarantine behavior.

## INTEGRATION PROOF
- Updated regex branch for OOM classification in `scripts/ci/classify_infra_failure.sh`.
- Local validation:
  - `MemoryError: out of memory` → `oom_kill`
  - `Killed process 123 (python)` → `oom_kill`
  - non-memory noise → no class
