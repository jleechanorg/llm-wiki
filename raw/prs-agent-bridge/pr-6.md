# PR #6: chore: remove broken bd hooks shims

**Repo:** jleechanorg/agent_bridge
**Merged:** 2026-03-14
**Author:** jleechan2015
**Stats:** +14/-96 in 5 files

## Summary
(none)

## Raw Body
bd hooks subcommand no longer exists in br v0.1.24. Removes post-checkout, post-merge, pre-push, prepare-commit-msg shims. Simplifies pre-commit to gitleaks-only scan.

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Hook changes are limited to local developer workflow and add a straightforward secret-scan gate; main risk is unexpected commit blocking or skipped scanning if `gitleaks` isn’t installed.
> 
> **Overview**
> Removes the Beads (`bd hooks run ...`) git-hook shim scripts (`post-checkout`, `post-merge`, `pre-push`, `prepare-commit-msg`) that no longer work with the current `bd` version.
> 
> Replaces the `pre-commit` hook with a standalone `gitleaks protect --staged` scan (optionally using `.gitleaks.toml`) that blocks commits on detected secrets and warns when `gitleaks` is not installed.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 81ad777c05cd7e90daf0be959139b48b1104acb2. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Summary by CodeRabbit

* **Chores**
  * Streamlined git hooks infrastructure for improved development workflows.
  * Enhanced pre-commit security with automatic secret leak detection to prevent accidental credential exposure during commits.

<!-- end of auto-generated comment: release notes by coderabbit.ai -->
