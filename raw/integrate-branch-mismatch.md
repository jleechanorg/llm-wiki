---
name: integrate-branch-name-mismatch
description: "integrate.sh may report a different branch name than what git actually creates; verify with git branch --show-current"
metadata:
  type: feedback
  bead: none
  originSessionId: 3dc1a846-12b5-462e-80b4-5f73dfdf1172
---

`integrate.sh` output branch name may not match the actual git branch. Script reported `dev1778804652` but actual branch was `dev1778804655`.

**Why:** The script computes the branch name from a timestamp, but the timestamp may differ between computation and actual `git checkout -b` execution (or there may be a race in the script). Setting upstream with the reported name fails: `git branch --set-upstream-to=origin/main dev1778804652` → "branch does not exist."

**How to apply:** After `integrate.sh` completes, always verify the actual branch name with `git branch --show-current` before setting upstream or running any branch-specific commands. Never trust the script's reported name.
