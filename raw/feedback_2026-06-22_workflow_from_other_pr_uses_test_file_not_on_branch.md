---
name: workflow-from-other-pr-uses-test-file-not-on-branch
description: "When a CI regression workflow was merged in a separate PR, older feature branches that touch its trigger paths fail with \"No such file\" until you rebase/merge main"
bead: rev-uvbcl
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 971c0ede-d782-4657-b676-352757cca104
---

# When a CI regression workflow was added in a separate PR, the older feature branch breaks the new check

**Symptom**: A PR that's been around for a while is now showing a new check FAIL that was just added to main in another PR. The failing run says "No such file or directory: testing_ui/some_dir/some_test.py". The check didn't exist before, but the new check fires because the older PR touches the workflow's `paths:` trigger (e.g., `mvp_site/main.py`).

**Root cause**: GitHub Actions `pull_request` events use the workflow file from the MERGE BASE (the target branch = main). When PR #X adds a workflow + its test file together and merges to main, the workflow starts running against ALL open PRs that touch its trigger paths — but those PRs were branched from before PR #X, so the test file from PR #X is not on their branch. The workflow's "Run the test" step fails with `No such file or directory`.

**Concrete example (2026-06-22)**: PR #7789 added `.github/workflows/mobile-auth-regression.yml` + `testing_ui/mobile_auth_same_origin/test_auth_same_origin.py`. The workflow's `pull_request.paths` includes `mvp_site/main.py`. PR #7786 (`feat-auth-browser-ci`, branched from main at 9eb33be37, BEFORE PR #7789 was merged) touches `mvp_site/main.py` (server-mint token helper). The Mobile Auth Same-Origin Regression check fires on PR #7786, fails with "No such file or directory: testing_ui/mobile_auth_same_origin/test_auth_same_origin.py".

**Fix**: Rebase or merge `origin/main` into the older branch. The merge picks up the test file (and the workflow, though the workflow already exists on main). In this case `git merge origin/main --no-edit` from the worktree produced a clean merge (35 files / 4487 insertions, but `mvp_site/main.py` had different hunks so git resolved it automatically — no manual conflict resolution needed).

**Why not just re-dispatch?** Re-dispatch doesn't change the workflow's checkout ref — it still pulls the same branch HEAD where the test file is missing. The only way to make the test file present is to actually add it to the branch.

**Why not skip with `if: false`?** You don't control the workflow file from your branch — it lives on main. Editing it requires a separate PR.

**Detection shortcut before rebase**:
```bash
# Find the missing file path from the failed run log
gh run view <run-id> --log 2>&1 | grep "No such file or directory"
# Check if the file exists on main
gh api 'repos/OWNER/REPO/contents/PATH?ref=main' | head -3
# If main has it but your branch doesn't, merge main
```

**Verify merge is conflict-free before pushing**:
```bash
git merge-tree $(git merge-base origin/<branch> origin/main) origin/<branch> origin/main | grep "changed in both"
# If only 0-1 files say "changed in both", merge is likely clean
```

**Related**: [[stale-local-head-false-7-green-claim]] (stale state before any claim); [[skeptic-cron-stale-sha-repost]] (other stale-state failure class). Also: GitHub `workflow_run` trigger uses main's copy of the file, not the PR's (per `workflow_run_default_branch_limitation`).

**Why**: This is a class of "your PR didn't add the failure, but a sibling PR's CI did" — easy to misdiagnose as a regression in your own change. The first instinct is to look at your code; the actual cause is the workflow's check ref pointing at your branch while the test file came from a sibling PR.
