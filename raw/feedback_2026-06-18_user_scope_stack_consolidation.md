---
name: user-scope-stack-consolidation-not-split
description: "User-scope infrastructure (daemon script + supervisor plist + wrappers) belongs in ONE repo, not split across 'where each file type traditionally lives' (e.g., daemon in user_scope, plist in hermes-agent/launchd/). Confirmed 2026-06-18 when user rejected parallel PRs in two repos."
type: feedback
bead: rev-gu8bi
metadata:
  node_type: memory
  type: feedback
---

# User-scope stack: consolidate, do not split

**When:** 2026-06-18 — after creating parallel PRs for the MCP daemon stack in two repos (daemon script + wrappers in `jleechanorg/user_scope` PR #20, plist template in `jleechanorg/hermes-agent` PR #30). User: *"That doesnt make sense. Code should only go in one place or the other they arent the same kind of repo"* → *"close the hermes agent PR lets just use user_scope and merge the user scope one"*.

**The mistake:** applied `launchd-plist-template` skill rule "Hermes gateway / scripts → `~/.hermes/launchd/`" literally, treating the MCP daemon's plist as a Hermes-managed service. The skill's mapping is about the *owning repo for the supervised service*. The MCP daemon is **user-scope infrastructure** — independent of Hermes — so its plist belongs with its daemon config in user_scope.

**The rule:**

| Question | Answer → Repo |
|---|---|
| Is the supervised service a Hermes-managed component (gateway / cron / scripts that the Hermes product owns)? | `~/.hermes/launchd/` → `jleechanorg/hermes-agent` |
| Is the supervised service user-scope infrastructure (MCP daemons, system utilities, anything that exists independently of any one product)? | wherever the service's config lives — typically `~/.config/<service>/` → `jleechanorg/user_scope` |
| Is it part of a third-party product (AO, OpenCode, Codex)? | the product's repo |

**Why "where each file type traditionally lives" fails:** launchd plist templates, env files, and `.gitignore` patterns all live in different ecosystems. If you split a single stack across repos "because each file type has its own home," you create implicit cross-repo coupling — the plist references the daemon's path, the README references both repos, the install script needs two `cp` commands. A new machine can't reproduce the stack from one `git clone`.

**Consolidation test (apply before creating a parallel repo PR):**

1. Does the new config supervise / configure / install something whose other parts already live in repo X?
2. Would a fresh `git clone` of repo X reproduce the entire stack with no cross-repo `cp` step?
3. If repo X is unavailable, would the new config still be meaningful (i.e., it doesn't depend on repo X being co-installed)?

If (1)=yes and (2)=no and (3)=no → put it in repo X, not in a separate "where it traditionally lives" repo.

**How to apply:**

- Before creating a plist template PR in `~/.hermes/launchd/` (or any other "template home" repo), ask: is the supervised service Hermes-owned, or is it user-scope infrastructure that happens to be supervised by launchd?
- User-scope infrastructure = a daemon / script / wrapper that exists independently of any one product. It is the *host* of multiple products (MCP daemons, system services), not a feature *of* a product.
- When in doubt, prefer the repo that already owns the daemon script and wrappers. A second home for the supervisor template creates drift, not safety.

**References:**

- Closed hermes-agent PR: [jleechanorg/hermes-agent#30](https://github.com/jleechanorg/hermes-agent/pull/30) (closed in favor of consolidation)
- Merged user_scope PR: `jleechanorg/user_scope` PR #20 — `config/mcp-daemon/com.jleechan.mcp-daemon.plist.template` now lives here, alongside the daemon script + wrappers it supervises
- Skill that almost misrouted me: `~/.claude/skills/launchd-plist-template/SKILL.md` — its "Hermes gateway → `~/.hermes/launchd/`" rule is about *Hermes-owned services*, not all launchd jobs on the machine
- Companion memory: `feedback_2026-06-17_mcp_daemon_diagnosis_fixes.md` (the two latent bugs that triggered this whole stack-tracking work)