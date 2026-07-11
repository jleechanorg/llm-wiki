---
type: design
status: approved
date: 2026-07-10
owner: jleechan
bead: jleechan-lgm
---

# Agent Orchestrator repository cutover

## Exit criteria

The cutover is complete only when every check below passes:

1. GitHub resolves `jleechanorg/agent-orchestrator-ts` to the original TypeScript repository ID and preserves its issues, releases, and open pull requests.
2. GitHub resolves `jleechanorg/agent-orchestrator` to the original `agent-orchestrator-mirror` repository ID and preserves its fork relationship to `AgentWrapper/agent-orchestrator`.
3. The primary Mac and Linux checkouts use these paths and remotes:
   - TypeScript: `~/project_agento/agent-orchestrator-ts` -> `jleechanorg/agent-orchestrator-ts.git`
   - Go: `~/projects/agent-orchestrator` -> `jleechanorg/agent-orchestrator.git`
4. Every linked worktree belonging to a moved primary checkout passes `git status` and appears under `git worktree list --porcelain` after repair.
5. Executed configuration, launchd/systemd units, install scripts, active skills, and current repository instructions contain no stale path or repository slug that changes the target program.
6. Historical logs, caches, generated evidence, and archived conversation records are reported separately and are not rewritten merely to make a global grep empty.
7. The installed TypeScript launcher remains available as `ao-ts`, while Go remains available as `ao-go`. The generic `ao` launcher is not repointed to Go until the fail-closed capability gates below pass.
8. A real smoke test on each machine proves both launchers report the expected implementation and can inspect their own configured projects.
9. The in-flight launchd export PR uses a stable installed Go AO binary or `AO_GO_BIN`; it contains no production dependency on the old `agent-orchestrator-mirror` source path.
10. Follow-up GitHub issues and beads exist for every confirmed capability or cleanup gap, with source paths and acceptance criteria.

## Decision

Perform a hard cutover without permanent local compatibility symlinks. Temporary cutover bridges are allowed only to keep running services restart-safe while paths are updated:

1. Rename `jleechanorg/agent-orchestrator` to `jleechanorg/agent-orchestrator-ts`.
2. Update critical TypeScript references before reusing the old namespace.
3. Rename `jleechanorg/agent-orchestrator-mirror` to `jleechanorg/agent-orchestrator`.
4. Rename the primary local checkout directories and repair linked worktrees.
5. Update operational references on the Mac and `jeff-ubuntu`, then run bounded stale-reference audits.

For each moved primary checkout, create the replacement path first, atomically move the directory, and immediately place a temporary symlink at the old path. Keep existing services running. Update and verify every operational consumer against the new real path, then remove the temporary symlink. A bridge that survives closeout is a failed exit criterion.

GitHub normally redirects repository URLs and Git transports after a rename, but reusing the old name destroys that redirect. GitHub Actions references do not follow repository renames. Therefore the two GitHub renames are separate gated steps, not one blind batch. Source: [GitHub repository rename behavior](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository).

`jleechanorg/agent-orchestrator-golang` is a separate older fork and is outside this rename. It must not be renamed or substituted for the explicitly selected `agent-orchestrator-mirror` repository.

## Ground truth

### TypeScript repository

- GitHub: `jleechanorg/agent-orchestrator`
- Primary Mac checkout: `/Users/jleechan/project_agento/agent-orchestrator`
- Primary Linux checkout: `/home/jleechan/project_agento/agent-orchestrator`
- Architecture: pnpm/TypeScript CLI, tmux orchestration, Next.js web UI, skeptic and autonomous-factory extensions.
- Open pull requests at design time: 752, 755, and 756.

### Go repository

- GitHub: `jleechanorg/agent-orchestrator-mirror`
- Upstream: `AgentWrapper/agent-orchestrator`
- Primary Mac checkout: `/Users/jleechan/projects/agent-orchestrator-mirror`
- Primary Linux checkout: `/home/jleechan/projects/agent-orchestrator-mirror`
- Architecture: Go daemon and CLI with SQLite/HTTP/SSE plus an Electron/React frontend.
- The Mac checkout has pre-existing local commits and a modified `frontend/pnpm-lock.yaml`; these must be preserved.

### Parallel work that must not be disrupted

- `jleechanclaw` draft PR 756 is implementing the daily launchd export through Go AO session `jleechanclaw-755-2`.
- The TypeScript checkout currently has an unrelated uncommitted edit in `packages/cli/src/commands/skeptic/gh-client.ts`.
- No local directory move may occur until the owning process has checkpointed and the exact dirty-file hashes are recorded.

## Cutover protocol

### Phase 0: immutable inventory and checkpoints

Record in the evidence bundle:

- GitHub repository IDs, names, fork parents, default branches, open PR URLs, issue counts, and release tags for both repositories.
- `git status --short --branch`, `git rev-parse HEAD`, remotes, and `git worktree list --porcelain` for every primary and auxiliary checkout.
- SHA-256 hashes of every pre-existing modified or untracked file.
- active tmux/AO sessions and processes whose cwd is under either checkout.
- current launchd/systemd unit definitions and installed launcher targets.

Abort the local move if an unrelated process is still writing inside a checkout. Preserve all dirty files; do not stash, reset, or clean them for this migration.

### Phase 1: TypeScript GitHub rename

Rename the repository through GitHub's repository API, then verify by immutable repository ID rather than name alone. Confirm the three open PRs and representative issues/releases now resolve beneath `jleechanorg/agent-orchestrator-ts`.

Before proceeding, update critical references that must continue targeting TypeScript:

- Mac `~/.hermes/agent-orchestrator.yaml` prompt and `gh` command slugs.
- Linux `~/.agent-orchestrator.yaml` project repository slug.
- current user policy and active operational skills on both machines.
- independent clone remotes that target the TypeScript repository.
- repository-owned executable commands and package metadata on an isolated TypeScript worktree/PR.

Do not rewrite audit logs, generated historical evidence, cached conversations, or old release prose during this gate.

### Phase 2: Go GitHub rename

Only after the TypeScript operational-reference gate passes, rename `jleechanorg/agent-orchestrator-mirror` to `jleechanorg/agent-orchestrator`. Verify its immutable repository ID, upstream fork relationship, default branch, open PRs, and Git transport.

Update Go clone remotes. Keep the upstream remote pointing to `AgentWrapper/agent-orchestrator`.

### Phase 3: local checkout moves

When all writers are checkpointed:

- Mac:
  - `/Users/jleechan/project_agento/agent-orchestrator` -> `/Users/jleechan/project_agento/agent-orchestrator-ts`
  - `/Users/jleechan/projects/agent-orchestrator-mirror` -> `/Users/jleechan/projects/agent-orchestrator`
- Linux:
  - `/home/jleechan/project_agento/agent-orchestrator` -> `/home/jleechan/project_agento/agent-orchestrator-ts`
  - `/home/jleechan/projects/agent-orchestrator-mirror` -> `/home/jleechan/projects/agent-orchestrator`

After moving any main checkout with linked worktrees, run `git -C <renamed-main> worktree repair <linked-worktree>...`, then verify every linked worktree. This sequence was reproduced on a disposable repository: the linked worktree failed before repair and passed afterward.

To preserve restartability during the move, create a temporary symlink from each old primary path to its new path immediately after the atomic rename. Do not reload a service merely because its source checkout moved. Remove each bridge only after all live consumers use the new path and automatic health evidence is captured.

Auxiliary clones under `projects_reference`, `projects_other`, and `.worktrees` are classified individually. Update their remotes immediately, but rename their directories only when no launchd/systemd unit or active process depends on the path. Directory names are not treated as proof of repository identity.

### Phase 4: operational references

Update only live references, including:

- Mac launchd plists whose executable or working-directory paths point at a moved checkout.
- Mac `AO_MAIN_REPO`, AO config entries, installer templates, and stable binary resolution.
- Linux `~/bin/ao`, user systemd units, AO project configuration, and policy files.
- Go/TypeScript build and install documentation.

Every installed launchd plist must continue to have a tracked `@HOME@` template in its owning repository. Reload only affected units, never unrelated jobs.

### Phase 5: verification and closeout

Run bounded audits over operational scopes first, then a broad report-only scan:

- live shell/config/skill/launchd/systemd references;
- all git remotes under known checkout roots;
- linked worktree health;
- GitHub repository identity and representative PR/issue URLs;
- `ao-ts` and `ao-go` smoke tests;
- the daily export job's configured Go AO binary path.

Classify remaining matches as operational, source documentation, historical evidence, generated/cache, or intentionally out of scope. A remaining historical match is not a cutover failure; a remaining executable stale reference is.

## Capability gates and follow-ups

Repository naming does not imply binary parity. Current-source verification found:

1. `backend/internal/service/pr/action_service.go` reports merge success without calling SCM, while resolve-comments always returns zero. Until fixed, generic automation must not trust or use these endpoints. The immediate correction should be fail-closed, followed by real SCM-backed behavior.
2. Go does not consume the TypeScript `agent-orchestrator.yaml` as live hot-reloaded configuration. Migration requires an explicit configuration bridge or documented project-by-project import, never silent substitution.
3. TypeScript-only commands and systems include skeptic, autonomous harness, verify, batch-spawn, init/update/config-help, and the web-dashboard CLI surface.
4. Go's current source does include tracker-intake daemon wiring; the contrary statement in `docs/STATUS.md` is stale documentation, not a runtime gap.
5. Go strengths include its daemon/API architecture, broad adapter set, Electron desktop UI, and cross-platform PTY support.

The repository rename may proceed while these are tracked, but the generic `ao` launcher must remain on the TypeScript implementation until the fake-success action path is fail-closed and every current generic-`ao` consumer is classified.

## Rollback

Rollback is identity-driven:

1. Stop only affected launchd/systemd units and AO sessions.
2. Restore operational config files from checksummed pre-cutover copies.
3. Move checkout directories back and run the same verified `git worktree repair` procedure.
4. Restore clone remote URLs.
5. Rename the Go repository back to `agent-orchestrator-mirror`, then rename TypeScript back to `agent-orchestrator` only after the namespace is free.
6. Verify repository IDs and representative PR/issue URLs after each reversal.

Rollback must not overwrite commits or dirty files, and it never uses force-push or reset.

## Evidence sources

- Swarm synthesis: `/tmp/llm_wiki/sidekick/rename-agent-orchestrator-repositories-update/AUDIT.md`
- Mac reference inventory: `/tmp/llm_wiki/sidekick/rename-agent-orchestrator-repositories-update/lane-mac-refs.md`
- Linux reference inventory: `/tmp/llm_wiki/sidekick/rename-agent-orchestrator-repositories-update/lane-linux-refs.md`
- History/memory inventory: `/tmp/llm_wiki/sidekick/rename-agent-orchestrator-repositories-update/lane-history-memory.md`
- Capability comparison: `/tmp/llm_wiki/sidekick/rename-agent-orchestrator-repositories-update/lane-capability-gap.md`
- Tracking bead: `jleechan-lgm`

The `/tmp` reports are working evidence; this tracked design and the bead are the durable recovery surfaces.
