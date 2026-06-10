---
name: Optional Registry and Self-Invocation Fix in merge_train hooks
description: Fix silent hook skips due to missing file_domains.yaml and recursive self-invocation loops in per-repo predict-spawn-check.sh.
type: feedback
bead: none
---

# Optional Registry and Self-Invocation Fix in merge_train hooks

## Context
After migrating from domain-level locks (Phase B) to symbol-level conflicts (Phase C), the `file_domains.yaml` registry file became optional. However, the hook scripts (`pre-commit.sh`, `predict-spawn-check.sh`, and `gemini-conflict-warn.sh`) still exited 0 silently if `file_domains.yaml` was not present in the target repository. Additionally, when `gemini-conflict-warn.sh` was installed as `<repo>/.gemini/predict-spawn-check.sh`, it resolved its target to itself and exited immediately due to the session sentinel file.

## Technical Detail & Cause
1. **Silent Fail-Fast**: The registry file was hard-gated:
   ```bash
   if [[ ! -f "$REGISTRY" ]]; then exit 0; fi
   ```
   Since `install.sh` no longer generated `file_domains.yaml` by default, hooks exited silently in repositories without it.
2. **Recursive Call**: `gemini-conflict-warn.sh` was copied to `predict-spawn-check.sh` inside target `.gemini/` directories. It had:
   ```bash
   SPAWN_CHECK="$SCRIPT_DIR/predict-spawn-check.sh"
   bash "$SPAWN_CHECK"
   ```
   This ran itself again, hit the per-session sentinel, and exited 0 without ever executing the real global `predict-spawn-check.sh`.

## Solution
1. **Optional Registry**: Made the registry file argument optional in `pre-commit.sh` and `predict-spawn-check.sh`:
   ```bash
   REGISTRY_ARG=()
   if [[ -f "$REGISTRY" ]]; then
     REGISTRY_ARG=(--registry "$REGISTRY")
   fi
   ```
2. **Global Script Resolution**: Changed `gemini-conflict-warn.sh` to look for the global script first and verify it is not calling itself:
   ```bash
   SPAWN_CHECK="$HOME/.local/bin/predict-spawn-check.sh"
   if [[ -f "$SPAWN_CHECK" ]] && [[ "$(realpath "$SPAWN_CHECK")" == "$(realpath "${BASH_SOURCE[0]}")" ]]; then
     exit 0
   fi
   ```
3. **Diagnostic logs**: Added checking and concluding log messages to stderr in `conflict_check_helper.py`.

## Verification
- Verified via `merge_train test-hooks --agent all` that outputs checking and concluding stderr logs successfully.
- Verified pre-commit hook runs on git commit.

## References
- Pull Request: [PR #25](https://github.com/jleechanorg/merge_train/pull/25)
- Commit: [Commit #5bb7527](https://github.com/jleechanorg/merge_train/commit/5bb7527c7d42cf38a06f3661ee2d3345d4eefd20)
