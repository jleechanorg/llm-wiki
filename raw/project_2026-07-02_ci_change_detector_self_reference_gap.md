---
name: ci-change-detector-self-reference-gap
description: scripts/ci-detect-changes.sh unconditionally skipped .github/workflows/test.yml changes, so a fix to that workflow could never self-verify via its own PR's CI
type: feedback
bead: rev-zaqr4 (parent), fixed in PR #8133 (jleechanorg/worldarchitect.ai)
---

**Rule:** Any CI change-detector/gate script that decides which tests to run based on which files changed MUST include itself and the workflow file(s) it configures in its own "trigger everything" watch set. Otherwise a fix to the detector or its workflow can never self-verify — the PR that fixes it will show the test job as SKIPPED (not passing, not failing) on every trigger type, including manual `workflow_dispatch`.

**Why:** `scripts/ci-detect-changes.sh` mapped `.github/**` diffs to "no test groups selected" unconditionally (comment: "changes should not trigger core-tests"). PR #8133 fixed a self-hosted-runner exec-bit bug in `.github/workflows/test.yml` — this diff only ever touched `.github/workflows/test.yml`, so `has-changes` stayed `false` and the `Directory tests` matrix was SKIPPED on the normal `pull_request` trigger AND on a manual `workflow_dispatch` of the exact same commit. The manual dispatch didn't help because `detect-changes` still runs first and computes the same (false) has-changes result regardless of trigger type.

**Fix pattern:** add a targeted exception — if the changed file is the workflow file itself or the change-detector script itself, select ALL test groups (can't know in advance what a shared-template change affects) instead of skipping. Verify locally before pushing: `source scripts/ci-detect-changes.sh; main pull_request <base> <head> simple` and confirm `has-changes=true`.

**How to apply:** Before shipping a CI-infra-only PR, ask "will my own change's job even run on this PR?" — check the change-detector's exclusion rules for the specific file(s) being edited, not just whether the target job's `on:` triggers include the event type.

**Evidence-citation pitfall discovered in the same PR:** when citing a `workflow_dispatch` run as proof a fix works, verify which COMMIT that dispatch actually ran against — a dispatch triggered before the fix commit landed will show the pre-fix (broken) behavior and silently invalidate the citation. An independent `/er` evidence-reviewer caught this exact mistake (citing run 28618115295, dispatched against the first of two commits, as "proof" when it actually showed the still-skipped pre-fix state). Always cross-check the cited run's head SHA against the PR's current head SHA before using it as evidence.
