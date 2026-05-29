---
name: API-driven lock release validation and stale check diagnostics
description: Implemented zero-trust API-driven verification to prevent incorrect manual and automated lock releases on open PRs
type: feedback
bead: none
---

# API-Driven Lock Release Validation and Stale Check Diagnostics

## Context
During concurrent agent sessions editing `mvp_site/world_logic.py` in `worldarchitect.ai` (PR #7142 and PR #7143), an agent falsely concluded that PR #7143 was not modifying `world_logic.py`. It manually executed a `domain_lock release` to clear the `mvp-core` whole-domain lock held by PR #7143, bypassing concurrency protections. In reality, PR #7143's remote HEAD *did* touch `world_logic.py` in commit `4482d30396`.

## The Root Cause (Divergence)
The agent fell victim to **local-remote git divergence**. By not executing `git fetch` or querying the live GitHub API before checking the files modified by PR #7143, it compared against an outdated local reference or a missing remote branch tracking state, incorrectly determining that the PR didn't modify `world_logic.py`. 

## The Solution
To prevent incorrect manual or automated overrides, we hardened the `domain_lock` CLI, hook scripts, and spawner integration to shift from local-only git comparisons to **live, API-driven zero-trust validation**:

1.  **Strict Release Validation (`domain_lock release`)**:
    *   By default, trying to release an active lock held by a PR now checks the PR state dynamically via `gh pr view <PR> --json state,files --repo <repo_name>`.
    *   If the PR state is `OPEN`, the CLI matches the PR's modified files list against the glob patterns of the domain being released (using the loaded registry).
    *   If any overlap is found, the command is **denied** with code `1` and prints a clear explanation showing the files responsible for the overlap:
        `DENIED: Refusing to release active lock for open PR #N because it still modifies files in the locked domain(s): [...]. Use --force to override.`
    *   To allow emergency overrides, a new `--force` CLI option was added to completely bypass this validation.

2.  **Diagnostics in the Hook (`hooks/domain-lock-pre-tool.sh`)**:
    *   Upgraded the stale-lock checking logic to output step-by-step diagnostic information to `stderr` (e.g. tracking PR numbers, querying repo paths, printing state evaluations).
    *   Enabled robust Python-based URL parsing to determine the GitHub repository path from the git remote.
    *   Appended `--force` to the GC auto-release command so that automated cleanup of merged/closed locks always succeeds without getting stuck.

3.  **Comprehensive Unit Tests**:
    *   Added 4 comprehensive test cases in `tests/test_conflict_override.py` covering successful releases with `--force`, denied release on open/overlapping PRs, allowed release on closed/merged PRs, and allowed release when no file overlap exists.

## Reusable Pattern / Rule
Never inspect or verify another branch's overlap based on stale local git history without a live fetch/API verification. Shift verification responsibility to the **live API (the single source of truth)** and require an explicit `--force` flag for lock overrides.

## References
*   **PR Reference:** [PR #7142](https://github.com/jleechanorg/worldarchitect.ai/pull/7142), [PR #7143](https://github.com/jleechanorg/worldarchitect.ai/pull/7143)
*   **Commit Reference:** [commit e5e44275f0a2d2fa95d63f10ef9e8f4abff4c81f](https://github.com/jleechanorg/merge_train/commit/e5e44275f0a2d2fa95d63f10ef9e8f4abff4c81f)
*   **Modified files:** `merge_train/domain_lock.py`, `hooks/domain-lock-pre-tool.sh`, `tests/test_conflict_override.py`
