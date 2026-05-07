# Ambiguous local branch origin/main blocks integrate.sh

**Date**: 2026-05-05
**Type**: Anti-Pattern / Feedback
**Classification**: Best Practice

## Summary

A local git branch literally named `origin/main` shadows the remote tracking ref `refs/remotes/origin/main`. When `integrate.sh` calls `git rev-list origin/main..HEAD`, git resolves `origin/main` to the local branch (stale, older SHA) rather than the remote tracking ref, producing a false "570 unmerged commits" hard-stop.

## Symptoms

- `warning: refname 'origin/main' is ambiguous.` in git output
- `integrate.sh` reports large number of "unmerged" commits that are actually already in remote main
- `--force` flag does not bypass this check (it only overrides uncommitted-changes and squash-merge checks)

## Diagnosis

```bash
git for-each-ref --format='%(refname)' | grep "refs/heads/origin/"
```

If this returns any results (e.g., `refs/heads/origin/main`), those local branches shadow remote tracking refs.

## Fix

```bash
git branch -d "origin/main"
```

Safe when the local branch has no unique commits (verify with `git log refs/remotes/origin/main..refs/heads/origin/main`).

## References

- Memory: `~/.claude/projects/-Users-jleechan-worldarchitect-ai/memory/feedback_2026-05-05_ambiguous_origin_main_local_branch.md`
- Branch affected: `dev1777969762`
- Deleted SHA: `733a44f18`
