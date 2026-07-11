---
type: implementation-plan
status: executing
date: 2026-07-10
design: roadmap/2026-07-10-agent-orchestrator-repository-cutover-design.md
bead: jleechan-lgm
---

# Agent Orchestrator Repository Cutover Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename the TypeScript and Go AO repositories and primary checkouts without interrupting any running AO, launchd, systemd, or factory workload.

**Architecture:** Use immutable GitHub repository IDs as identity, insert a TypeScript operational-reference gate between the two remote renames, and use temporary old-path symlinks during local directory moves. Keep TypeScript and Go launchers distinct until Go's fake-success PR action path is fail-closed.

**Tech Stack:** GitHub REST API through `gh api`, git/worktrees, macOS launchd, Ubuntu systemd user units, shell configuration, Go AO and TypeScript AO CLIs.

## Global Constraints

- Never force-push, reset, clean, stash, or overwrite unrelated dirty files.
- Never rename or substitute `jleechanorg/agent-orchestrator-golang`.
- Do not repoint generic `ao` to Go in this cutover.
- Keep services running; use temporary path bridges for restart safety.
- Update tracked launchd templates whenever installed plists change.
- Stop before a mutation if repository ID, checkout identity, or target path differs from the inventory.
- Record commands, exit codes, before/after SHAs, repository IDs, service health, and remaining-reference classifications.

---

### Task 1: Freeze identity and runtime inventory

**Files:**
- Modify: `roadmap/2026-07-10-agent-orchestrator-repository-cutover-implementation-plan.md`
- Modify: `.beads/issues.jsonl` through `br update jleechan-lgm`

**Interfaces:**
- Consumes: approved design and swarm audit.
- Produces: checksummed pre-cutover inventory and explicit go/no-go gates.

- [x] Record both GitHub repository IDs, current names, parents, open PRs, issues, releases, and default branches with `gh api`.
- [x] Record status, HEAD, remotes, worktrees, dirty-file hashes, and active cwd processes for primary Mac/Linux checkouts.
- [x] Record current launchd/systemd unit state and launcher resolution without restarting anything.
- [x] Confirm the launchd export worker has pushed a checkpoint and contains no production hardcode of the old Go source path.
- [x] Commit the inventory checkpoint and update bead `jleechan-lgm`.

### Task 2: Rename TypeScript GitHub repository

**Files:**
- Modify: live TypeScript slug references listed by the audit.
- Preserve: all repository content, issues, PRs, releases, and dirty local changes.

**Interfaces:**
- Consumes: original TypeScript repository ID.
- Produces: `jleechanorg/agent-orchestrator-ts` with the same ID.

- [x] PATCH `repos/jleechanorg/agent-orchestrator` with `name=agent-orchestrator-ts`.
- [x] Verify immutable ID, open PRs 752/755/756, representative issue, release, clone, fetch, and push URL.
- [x] Update critical Mac and Linux TypeScript slug references and independent clone remotes.
- [x] Run the operational-scope stale-reference gate; classify rather than rewrite historical records.
- [x] Stop if any executed reference still targets the old TypeScript namespace.

### Task 3: Rename Go GitHub repository

**Files:**
- Modify: Go clone origin remotes and current operational documentation.

**Interfaces:**
- Consumes: original mirror repository ID and a passing TypeScript reference gate.
- Produces: `jleechanorg/agent-orchestrator` with the mirror's original ID and unchanged upstream parent.

- [x] PATCH `repos/jleechanorg/agent-orchestrator-mirror` with `name=agent-orchestrator`.
- [x] Verify immutable ID, fork parent, open PRs, issues, clone/fetch, and default branch.
- [x] Verify the old TypeScript URL is no longer treated as a redirect and all live TypeScript consumers already use `-ts`.

### Task 4: Move Mac primary checkouts with temporary bridges

**Files:**
- Move: `/Users/jleechan/project_agento/agent-orchestrator` -> `/Users/jleechan/project_agento/agent-orchestrator-ts`
- Move: `/Users/jleechan/projects/agent-orchestrator-mirror` -> `/Users/jleechan/projects/agent-orchestrator`
- Modify: affected tracked launchd templates, installed plists, AO configuration, policies, and launcher paths.

**Interfaces:**
- Consumes: checkpointed dirty files and linked-worktree list.
- Produces: new canonical paths, repaired worktrees, and zero permanent bridges.

- [x] Confirm no active writer has cwd beneath a checkout; checkpoint or defer only the affected move if one does.
- [x] Atomically move one checkout, create its old-path symlink immediately, update its origin remote, and run `git worktree repair` for linked worktrees.
- [x] Update operational consumers to the new real path while services remain running.
- [x] Verify status, dirty-file hashes, launchd configuration/trigger/log evidence, and launcher identity.
- [ ] Remove that checkout's temporary symlink only after all operational checks pass; repeat for the other checkout.

### Task 5: Move Linux primary checkouts with temporary bridges

**Files:**
- Move: `/home/jleechan/project_agento/agent-orchestrator` -> `/home/jleechan/project_agento/agent-orchestrator-ts`
- Move: `/home/jleechan/projects/agent-orchestrator-mirror` -> `/home/jleechan/projects/agent-orchestrator`
- Modify: user systemd units, AO configuration, policies, launchers, and clone remotes.

**Interfaces:**
- Consumes: SSH access and recorded systemd baseline.
- Produces: new Linux canonical paths with active services preserved.

- [x] Confirm `agent-orchestrator-golang` identity and exclude it from every mutation.
- [x] Apply the one-checkout-at-a-time move, bridge, remote update, worktree repair, and verification protocol over `ssh jeff-ubuntu`.
- [ ] Remove the temporary bridge after a controlled supervisor handoff, then verify the bridge is absent and both services are healthy.
- [x] Run `systemctl --user daemon-reload` only after unit files are correct; do not restart healthy units unless required.
- [x] Verify unit active state, launcher identity, and recent service logs before removing bridges.

### Task 6: File capability and cleanup follow-ups

**Files:**
- Modify: `.beads/issues.jsonl` through `br`.
- Create: GitHub issues in the newly canonical Go repository.

**Interfaces:**
- Consumes: verified current-source findings.
- Produces: durable issue URLs and bead IDs.

- [x] File a P0/P1 Go issue to make merge and resolve-comments fail closed immediately, then implement real SCM behavior separately.
- [x] File config-migration/parity issues for YAML migration, generic-`ao` consumer classification, and stale `docs/STATUS.md` tracker text.
- [x] File cleanup for the separate `agent-orchestrator-golang` fork and divergent auxiliary checkouts; do not delete them in this cutover.
- [x] Update `jleechan-lgm` with all URLs and exact remaining actions.

### Task 7: End-to-end verification and evidence

**Files:**
- Modify: this plan's checkboxes and bead status.
- Create or modify: tracked next-steps artifact only if work remains.

**Interfaces:**
- Consumes: completed remote and local cutovers.
- Produces: exact proof or a fail-closed remaining-gap report.

- [ ] Re-query repository IDs/names, open PRs/issues, fork parent, clone/fetch, and remotes.
- [ ] Verify every primary and linked worktree, preserved dirty-file hashes, service active state, launchers, and absence of temporary symlinks.
- [ ] Run bounded operational stale-reference scans on both machines and classify every match.
- [ ] For each automatic job claim, capture configuration, trigger, and timestamped automatic log evidence.
- [ ] Verify the launchd export PR's current pushed SHA and Go AO binary resolution.
- [ ] Commit/push the evidence and report exact commit, issue, PR, bead, and remaining-gap URLs.
