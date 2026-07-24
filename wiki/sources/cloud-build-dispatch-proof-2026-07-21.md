---
title: "Superpowers Cloud Build — /super dispatch end-to-end proof + v0.8.1 cd drift fix"
type: source
tags: [cloud-build, superpowers, dispatch, proof, bug-fix, glm-5.2]
date: 2026-07-21
source_file: raw/cloud-build-install-instructions.md
gist: https://gist.github.com/jleechan2015/9d0471c668ecac922cd58026f3e430d3
bug_report_gist: https://gist.github.com/jleechan2015/286f0b03b75d5036ae490ccd6073abd8
---

## Summary

Verified end-to-end that **both** the Mac and jeff-ubuntu can dispatch `/super` → Cloud Build box → GLM-5.2 → box-authored commit → land on `private/*` branch, by running parallel dummy PRs on 2026-07-21. **Mac dispatch worked out of the box; jeff-ubuntu was broken by a one-line `cd` drift in `cloud-build-super-dispatch.sh` v0.8.1** — applied the one-line patch locally and verified the same dispatch chain succeeds on both machines.

## End-to-end proof (2026-07-21)

Built two orphan-snapshot repos with a trivial plan (`create .cloud-build-e2e-marker.txt`), pushed to GitHub, dispatched via `cloud-build-super-dispatch.sh`, polled until `state=done`, called `cloud_build_land_result`, verified the box authored the commit.

### jeff-ubuntu (after cd fix)

- Repo: https://github.com/jleechan2015/cb-e2e-jeff-ubuntu-20260721-172109
- Branch: `private/cb-e2e-jeff-172109`
- Run ID: `cb-e2e-jeff-ubuntu-20260721-172109-20260722002148-2001e7`
- Box commit: `e17cfb8 Cloud Build <supervisor@cloud-build.local> cloud-build-e2e: jeff-ubuntu dispatch proof`
- Marker: `Cloud Build E2E test: jeff-ubuntu, dispatch worked end-to-end, 2026-07-22T00:24:01Z`
- Status: `state: done, tasks_completed: 1, harness: serf-3, runner: exec`

### Mac

- Repo: https://github.com/jleechan2015/cb-e2e-macbook-20260721-172109
- Branch: `private/cb-e2e-mac-172110`
- Run ID: `cb-e2e-macbook-20260721-172109-20260722003813-1aba7a`
- Box commit: `8a12c52 Cloud Build <supervisor@cloud-build.local> cloud-build-e2e: macbook dispatch proof`
- Marker: `Cloud Build E2E test: macbook, dispatch worked end-to-end, 2026-07-22T00:21:09Z`
- Status: `state: done, tasks_completed: 1, harness: serf-3, runner: exec`

## The v0.8.1 cd drift bug (Linux only)

`cloud-build-super-dispatch.sh` ships with `cd "$SCRIPT_DIR"` on the Linux copy — wrong. The Mac copy has the correct `cd "$SCRIPT_DIR/.."` with an explanatory comment. After the broken `cd`, the subsequent `bash scripts/preflight-local.sh "$PROJECT" "$PLAN_REL"` fails with "No such file or directory" because cwd is `<skill-root>/scripts/` and the relative path resolves to `<skill-root>/scripts/scripts/preflight-local.sh` (does not exist).

### Diff

```diff
--- a/skills/cloud-build/scripts/cloud-build-super-dispatch.sh (jeff-ubuntu, BROKEN)
+++ b/skills/cloud-build/scripts/cloud-build-super-dispatch.sh (Mac, CORRECT)
@@ -27,7 +27,8 @@ WORK_BRANCH="${4:?run_sha not provided}"
   *) printf 'FATAL: work_branch must start with private/ (got %s); server will refuse\n' "$WORK_BRANCH" >&2; exit 1 ;;
 esac

-cd "$SCRIPT_DIR"
+# SCRIPT_DIR is scripts/ itself; the scripts/... references below expect the skill root.
+cd "$SCRIPT_DIR/.."

 # Preflight — refuses projects with external secrets/services unless CLOUD_HERMETIC_CONFIRMED=1
 bash scripts/preflight-local.sh "$PROJECT" "$PLAN_REL"
```

### One-line local fix (applied on jeff-ubuntu 2026-07-21)

```bash
sed -i 's|^cd "$SCRIPT_DIR"$|# SCRIPT_DIR is scripts/ itself; the scripts/... references below expect the skill root.\ncd "$SCRIPT_DIR/.."|' \
    ~/superpowers-cloud-build-main/skills/cloud-build/scripts/cloud-build-super-dispatch.sh
```

After fix: `preflight OK` and dispatch proceeds; box accepted the run.

## Install instructions (canonical)

Full instructions: https://gist.github.com/jleechan2015/9d0471c668ecac922cd58026f3e430d3

Quick recap:

```bash
# Download + extract (one-time)
cd ~
curl -LO "https://pub-347cd78fe2db440ab5f46aa1c1307d59.r2.dev/4684e636b84511ba0cdca7a18d9b172e/superpowers-cloud-build.tgz"
tar xzf superpowers-cloud-build.tgz

# Claude Code install
/plugin marketplace add ~/superpowers-cloud-build-main
/plugin install cloud-build@superpowers-cloud-build

# Codex install
codex plugin marketplace add ~/superpowers-cloud-build-main
codex plugin add cloud-build@superpowers-cloud-build

# Enroll (single-use enrollment code, 24h expiry)
printf %s "$CODE" | bash ~/superpowers-cloud-build-main/skills/cloud-build/scripts/cb-client-setup.sh

# Verify
ssh -i ~/.ssh/cloud-build/id_ed25519 cloud-bastion@cloud.superpowers.build
# → "cloud-bastion: interactive shell is not permitted" (exit 0)  ✓ key accepted
```

Trigger the box from a Claude Code or Codex session by saying: **"run this plan on the cloud"**

## Key Claims

- The Mac's `cloud-build-super-dispatch.sh` has been working all along (17 prior successful runs: cb-wa-8353, cb-wa-levelup, cb-lineage-fix, cb-mrtr-e2e, cb-wa-pr8429, etc.). Box author always `Cloud Build <supervisor@cloud-build.local>`.
- jeff-ubuntu's dispatch was silently broken from 2026-07-20 enrollment onward; the bug caused "still no luck" reports every time `/super` was invoked from Linux.
- One-line patch + verified working on 2026-07-21.
- Box uses GLM-5.2 via its OWN internal proxy (`10.0.100.1:65500`), NOT OpenRouter. Local `claudeg`/OpenRouter 402 does NOT affect the box.
- Heartbeat stale ≥240s during long LLM ops is NORMAL (see [[feedback-2026-07-20-cloud-build-heartbeat-stale-during-llm]]); do NOT abort on heartbeat-stale alone.
- Orphan-snapshot handoff is REQUIRED when main has secret-bearing history (box's git-secret guard scans full ancestry).

## Key Quotes

> "bastion: starting box for cb-e2e-jeff-ubuntu-20260721-172109" — jeff-ubuntu dispatch after cd fix, 2026-07-21

> "git secret guard: scanning outgoing range d7c43c21...de7f726..3b7a3022..." — Mac dispatch on 2-commit orphan snapshot history, passed

> "/super dispatch OK: run_id=cb-e2e-jeff-ubuntu-20260721-172109-20260722002148-2001e7 plan=.claude/plans/plan.md branch=private/cb-e2e-jeff-172109 sha=db9678d..." — dispatch success after cd fix

## Connections

- [[SuperpowersCloudBuild]] — the box service itself (Prime Radiant, Inc.)
- [[CloudBuildBastionHost]] — Mac + jeff-ubuntu enrolled dispatch machines sharing one SSH key
- [[CloudBuildOrphanSnapshotHandoff]] — git-secret-guard workaround used in today's E2E test
- [[SuperCommand]] — `/super` slash entry that calls the now-fixed dispatch script
- [[SuperlightCommand]] — legacy `claudeg`/OpenRouter router, NOT the box
- [[CloudBuildInstallEnrollment]] — earlier 2026-07-20 install/enrollment source page (now superseded by this one for the cd fix)
