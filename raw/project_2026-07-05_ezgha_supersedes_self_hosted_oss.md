---
name: ez-gh-actions supersedes self-hosted-oss (delete legacy later)
description: ez-gh-actions is now the SOLE GitHub Actions runner daemon; self-hosted-oss/* in worldarchitect.ai is legacy and slated for deletion
metadata:
  type: project
bead: none
---

## Context

`ez-gh-actions` (`jleechanorg/ez-gh-actions`) is the new sole Rust-based
GitHub Actions runner daemon. It replaces `worldarchitect.ai/self-hosted-oss/*`
(shell-script-based: mac-runner-health.sh, ubuntu-runner-health.sh, heal-runners.sh,
runner-capacity-failover.sh, etc.). Per the user on 2026-07-05:

> "note that ez gh actiosn runner repo is the new sole gh actions and we should
> delete all hte self hosted oss code from this repo later lets /learn to
> remember this and someone else will do it"

## Evidence the migration is in progress

- `ezgha.service` is live on both hosts (jeff-ubuntu PID 627225, Mac PID ~44xxx)
- Mac fleet currently produces `ez-mac-runner-b-*` runners (5-6 active, handling
  real `jleechanorg/worldarchitect.ai` jobs as of 2026-07-05 ~18:00Z)
- Linux fleet currently produces `ez-org-runner-*` + `ez-runner-b-*` runners
  on jeff-ubuntu (15 active, all busy)
- Mac's old `org-runner-mac-*` (colima-managed) fleet is dead and being
  replaced by the ezgha-managed `ez-mac-runner-b-*` fleet
- worldarchitect.ai's `worldarchitect.ai/.claude/skills/runner-health/`
  was committed in PR #8140 (2026-07-03) but its scripts (check_docker.sh,
  check_api.sh, etc.) describe the LEGACY fleet, not the new ezgha one

## Why ez-gh-actions supersedes (not just supplements)

1. **Daemon-managed, not cron-managed.** ezgha serves continuously and
   recreates exited runners in a 30s loop. The legacy fleet relied on
   `launchd` calling `heal-runners.sh` once per tick — no in-process
   reconciliation, no slot-file lock.
2. **JIT registration.** No long-lived registration token (the
   memory `feedback_2026-06-28_ao_runner_token_expiry_404.md` failure class —
   ephemeral PAT tokens with 1-hour TTL). Each container registers itself
   with a JIT config, runs one job, deregisters. No `RUNNER_TOKEN=ADJS...`
   footgun.
3. **VM-within-VM isolation.** Linux containers in a Colima/Lima VM on the
   Mac; Linux host's qemu microVMs on jeff-ubuntu. Runner workload can't
   touch the host kernel. Legacy `myoung34/github-runner` containers
   were process-isolated only.
4. **Single source of truth.** Config at `~/.config/ezgha/config.toml`,
   state at `~/.config/ezgha/slot_assignments.toml`, registration via
   `gh api generate-jitconfig`. Legacy had three separate scripts all
   touching `~/.local/share/worldarchitect-runners/state/` with no lock.

## Why deletion is "later, someone else will do it"

- The legacy scripts are still load-bearing for at least one thing:
  the worldarchitect.ai repo's `.github/workflows/*.yml` files still
  reference `self-hosted,self-hosted-mikey` labels which are the
  LEGACY labels (ezgha adds `ezgha`, `Linux`/`macOS`, `X64`/`ARM64`).
- CI workflows that pin to `self-hosted-mikey` will continue to route to
  the legacy fleet (when it exists) and to the ezgha fleet (which
  inherits those labels).
- Full deletion requires: (a) verifying no worldarchitect.ai CI workflow
  depends on legacy scripts, (b) updating CLAUDE.md to drop references to
  `self-hosted-oss/`, (c) deleting the directory, (d) updating the
  `runtime-mirror-sync` install path.

## Action items (for the eventual deletion PR)

1. Audit all `.github/workflows/*.yml` for self-hosted-oss script deps.
2. Update worldarchitect.ai CLAUDE.md to remove self-hosted-oss/ sections.
3. Delete `self-hosted-oss/` directory.
4. Update `.claude/skills/runner-health/` — most of it is redundant with
   the new `ezgha-doctor` skill in ez-gh-actions.
5. Update `runtime-mirror-sync` install paths and any cross-repo beading.

## References

- ez-gh-actions repo: https://github.com/jleechanorg/ez-gh-actions
- worldarchitect.ai runner PRs merged 2026-07-03: #8138, #8140, #8141, #8142,
  #8143, #8144 — all rooted in self-hosted-oss (legacy)
- Mac ezgha fleet: `/Users/jleechan/projects/worktree_runnner_f23rgwe/ez-gh-actions`
  worktree on branch `worktree_runnner_f23rgwe`
- Mac fleet status: `gh api orgs/jleechanorg/actions/runners | jq '.runners[] |
  select(.name | startswith("ez-mac-runner"))'`
- Related memory entries:
  - `feedback_2026-06-28_ao_runner_token_expiry_404.md` (the failure class
    that motivated JIT registration)
  - `feedback_2026-06-23_lima_vm_watchdog_gap.md` (Lima VM reliability —
    now a layer in the VM-within-VM stack)
  - `feedback_2026-07-03-runner-health-skill-created.md` (legacy
    runner-health skill, slated for replacement)

## Why: memory anchors the migration intent

Without this entry, a future agent looking at `self-hosted-oss/` will treat
it as load-bearing. With it, the intent is explicit: legacy code, deletion
deferred, owner unspecified.

## How to apply: when reasoning about worldarchitect.ai runner infra

- Cite `jleechanorg/ez-gh-actions` as the new home for any runner logic
- Cite `~/.config/ezgha/config.toml` as the runtime config
- Treat `self-hosted-oss/*.sh` as legacy; do not add new scripts there
- New PRs against `self-hosted-oss/` should be reviewed against the
  question "should this live in ez-gh-actions instead?"