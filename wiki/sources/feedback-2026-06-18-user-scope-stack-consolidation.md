---
title: "MCP daemon stack: consolidate user-scope infra in one repo, do not split"
type: source
tags: [feedback, mcp, launchd, infra-resilience, user-scope, anti-pattern, repo-organization]
date: 2026-06-18
source_file: ../../raw/feedback_2026-06-18_user_scope_stack_consolidation.md
bead: rev-gu8bi
---

## Summary

A near-mistake: applied the `launchd-plist-template` skill rule ("Hermes gateway / scripts → `~/.hermes/launchd/`") to a user-scope launchd plist (MCP daemon supervisor) and created parallel PRs in two repos — daemon script + wrappers in `jleechanorg/user_scope` PR #20, plist template in `jleechanorg/hermes-agent` PR #30. User pushback: *"Code should only go in one place or the other they arent the same kind of repo"*. The MCP daemon is **user-scope infrastructure**, not a Hermes-managed service, so its plist belongs with the daemon config it supervises. Closed hermes-agent PR #30 and merged user_scope PR #20 — single source of truth for the entire MCP daemon stack.

## Key Claims

- **`launchd-plist-template` skill rule is about *Hermes-owned services*, not all launchd jobs.** Reading "any new job → identify the owning repo" literally routed a user-scope plist to the wrong repo. The decision is whether the supervised service is a Hermes-managed component, not whether launchd supervises it.
- **User-scope infrastructure (daemon + supervisor + wrappers) belongs in ONE repo.** Splitting a single stack across "where each file type traditionally lives" creates implicit cross-repo coupling: the plist references the daemon's path, the README references both repos, the install script needs two `cp` commands. A fresh `git clone` of either repo alone cannot reproduce the stack.
- **Consolidation test (apply before opening a parallel-repo PR):** (1) Does the new config supervise / configure / install something whose other parts already live in repo X? (2) Would a fresh `git clone` of repo X reproduce the entire stack with no cross-repo step? (3) If repo X is unavailable, would the new config still be meaningful? If (1)=yes and (2)=no and (3)=no → put it in repo X.
- **The MCP daemon is user-scope infrastructure** — host of multiple products (Claude Code, Codex, OpenCode sessions all connect to its MCP endpoints), not a feature of Hermes. Its supervisor plist is a daemon config, not a Hermes launchd template.

## Key Quotes

> "Code should only go in one place or the other they arent the same kind of repo"

> "That doesnt make sense. Code should only go in one place or the other they arent the same kind of repo" — user feedback after I created parallel PRs.

> The MCP daemon is user-scope infrastructure, not a Hermes-managed service, so the plist belongs with the daemon config it supervises rather than in the Hermes agent's launchd/ directory.

## Connections

- [[LaunchdPlistTemplate]] — the skill whose mapping was misapplied; consolidation principle is a refinement of its decision tree
- [[MacOsLaunchd]] — broader launchd context; the consolidation rule applies regardless of macOS daemon specifics
- [[McpDaemonStack]] — the consolidated MCP daemon stack now lives at `jleechanorg/user_scope:config/mcp-daemon/`
- [[UserScopeInfra]] — concept page documenting the user-scope infrastructure category
- [[SkillRuleNarrowing]] — a reusable pattern: when a skill's mapping rule says "X goes in Y", confirm whether X is *owned* by Y's domain, not merely *related* to it
- [[Hermes-Agent]] — closed PR #30 shows the misroute; the canonical Hermes fork that the launchd skill references for Hermes-owned services
- [[Launchd]] — the launchd concept page; this source extends its "plist template" guidance with the consolidation principle

## Resolution Summary

| Action | Result |
|---|---|
| Close `jleechanorg/hermes-agent` PR #30 | done — plist template moved to user_scope |
| Merge `jleechanorg/user_scope` PR #20 | done — single source of truth (script + wrappers + plist template + README + .gitignore) |
| Update deployed plist | done — `KeepAlive=true` + `ThrottleInterval=60` applied via `plutil -replace` + `launchctl unload && load -w` |
| Verify daemon health | 11/11 MCP servers UP |
| Reframe `launchd-plist-template` skill | this learning is the prompt to add the "Hermes-owned vs user-scope" decision step |

## Pattern to Apply Forward

Before creating a plist template PR in `~/.hermes/launchd/` (or any other "template home" repo), ask: **is the supervised service Hermes-owned, or is it user-scope infrastructure that happens to be supervised by launchd?** User-scope infrastructure (a daemon / script / wrapper that exists independently of any one product) goes with the daemon config in user_scope — not split across "where each file type traditionally lives." When in doubt, prefer the repo that already owns the daemon script and wrappers; a second home for the supervisor template creates drift, not safety.