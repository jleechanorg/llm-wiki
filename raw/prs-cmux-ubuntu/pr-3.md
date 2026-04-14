# PR #3: chore: remove broken bd hooks shims

**Repo:** jleechanorg/cmux_ubuntu
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
> Low risk: changes are limited to local git hook scripts and only affect developer workflows during commit/push, not runtime behavior.
> 
> **Overview**
> Removes the `.beads` git hook shims (`post-checkout`, `post-merge`, `pre-push`, `prepare-commit-msg`) that delegated to the now-missing `bd hooks run` command.
> 
> Updates `.beads/hooks/pre-commit` to run a **gitleaks-only** staged secret scan (optionally using `.gitleaks.toml`), blocking commits on detection and warning when `gitleaks` is not installed.
> 
> <sup>Written by [Cursor Bugbot](https://cursor.com/dashboard?tab=bugbot) for commit 4dfaa8581cbdd75a39d91303c6118203f5de6b01. This will update automatically on new commits. Configure [here](https://cursor.com/dashboard?tab=bugbot).</sup>
<!-- /CURSOR_SUMMARY -->
