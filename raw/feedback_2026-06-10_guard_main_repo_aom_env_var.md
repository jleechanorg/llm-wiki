---
name: guardmainrepo-ao-main-repo-env-var-workaround-fork-policy-gap-not-upstream-pattern
description: AO_MAIN_REPO bypasses the fork-specific guardMainRepo safety check; upstream AgentWrapper/agent-orchestrator has no equivalent
metadata: 
  node_type: memory
  type: feedback
  bead: bd-cj5s
  originSessionId: 0b58c447-1542-4bd0-afac-baf29508bbb5
---

The `AO_MAIN_REPO` env var is the only way to bypass `guardMainRepo` in `packages/cli/src/commands/start.ts` when the user explicitly wants the coordinator to manage the main repo itself (the `agent-orchestrator` project). Setting `AO_MAIN_REPO=<some-worktree-path>` makes the guard check (`resolvedPath === mainRepoPath`) no longer match the project's registered `path: ~/project_agento/agent-orchestrator`, so the start proceeds.

**Why this matters:**
1. The env var is process-scoped — it must be set on every `ao start` invocation. Not in `~/.zshrc` by default. Forgetting it produces the cryptic "Refusing to operate on the main repo" error.
2. It effectively disables the guard firewall for the bypassed process. The guard still fires for subdirectory bypasses and URL-flow autoCreateConfig, but for the no-arg branch (the agent-orchestrator project's primary use case) it's a complete bypass.
3. **It is NOT an upstream pattern.** Upstream `ComposioHQ/agent-orchestrator` (now redirects to `AgentWrapper/agent-orchestrator`, same HEAD `5897b4e8d8cefc33f681ab73bf0e3ebc0b17b517`) has no `AO_MAIN_REPO`, no `guardMainRepo`, no worktree enforcement. The fork defined this policy; the env var is the workaround within that fork-only policy.

**How to apply:**
- When `ao start <projectId>` fails with "Refusing to operate on the main repo ... AO agents must run in git worktrees" for the `agent-orchestrator` project, use `AO_MAIN_REPO=/path/to/some/worktree ao start agent-orchestrator` as the workaround.
- The first-class fix is in flight: `bd-cj5s` calls for a `--allow-main-repo` CLI flag. Until that lands, persist the env var in `~/.zshrc` to avoid re-discovering the issue.
- If considering upstreaming `guardMainRepo` to `AgentWrapper/agent-orchestrator`: the right shape is opt-in (env var or flag), since changing upstream's "users can `ao start` from anywhere" behavior is a breaking change for existing users.

**References:**
- Source: `packages/cli/src/commands/start.ts` lines 327-334 (path-arg branch), 740-752 (registered-project branch), 996-1003 (URL-flow), 1096-1103 (no-arg cwd gap fix).
- 4 sites that fire: lines 334, 752, 1003, 1103.
- Introduced: PR #296 (`6577b7781`).
- Hardened: commit `199a56950` (cwd gap), `e8fca8795` (URL flow + comment).
- Recovery evidence: `~/roadmap/nextsteps-2026-06-10-coordinator-recovery-and-guardaudit.md` (Lane 1, Lane 2).
- Related memory: `project_2026-06-10_orphan_lifecycle_workers_reaped.md`, `feedback_2026-06-10_spurious_coordinator_project_removed.md`.
