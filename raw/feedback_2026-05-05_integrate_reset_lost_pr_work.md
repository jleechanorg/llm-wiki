---
name: integrate reset lost PR work on expfix
description: /integrate git reset --hard origin/main on expfix lost unmerged PR #6790 work; recoverable via reflog cherry-pick
type: feedback
bead: none
originSessionId: ba84f1d8-9387-4e8c-90b0-3acad29d2529
---
## Context

On 2026-05-05, `/integrate` was invoked on a session whose `expfix` branch had unmerged PR #6790 work in commits:
- `4bbabed28` — fix(rewards_engine): correct progress_percent span in level-up path
- `5506e9b23` — fix(rewards_engine): restore current_level to committed level, keep progress span fix
- `22a4afafe` — test: cover server-derived rewards progress

The `/integrate` command internally ran `git reset --hard origin/main` on `expfix`, which moved the branch pointer to `origin/main` (SHA `733a44f18`), making the three commits above unreachable from the branch tip.

## Recovery

1. The commits were still in the local repo reflog and accessible by SHA
2. Cherry-picked onto a new `dev1777969762` branch (created by integrate from `origin/main` SHA `f22bc0ad0`)
3. `4bbabed28` and `5506e9b23` applied cleanly to `rewards_engine.py`
4. `22a4afafe` was empty on cherry-pick (test file change already in main) — skipped
5. Prompt schema removal (`level_up_available` from `provider_utils.py`) was already merged to main via `8fe3cf989` — no action needed

New PR [#6814](https://github.com/jleechanorg/worldarchitect.ai/pull/6814) created from `dev1777969762`.

## Rule

**Before `/integrate`, always check `git reflog` and `git log --oneline` on the target branch to confirm unmerged work is either committed to a PR or explicitly stashed/copied.** A hard reset on a branch with unmerged commits moves those commits into reflog history — recoverable but disruptive.

The `/integrate` reset is destructive to the local branch state. For branches with open PRs, the safer pattern is:
1. `git log --oneline <branch>` to identify unmerged commits
2. Cherry-pick or rebase them onto the new integration branch before resetting

## Verification

```bash
# Check target branch for unmerged commits before integrate
git log --oneline expfix | head -5

# If unmerged work exists, cherry-pick before integrate:
git cherry-pick <unmerged-sha1> <unmerged-sha2>

# After integrate reset, recover via reflog:
git reflog expfix  # find the pre-reset SHAs
git cherry-pick 4bbabed28 5506e9b23
```
