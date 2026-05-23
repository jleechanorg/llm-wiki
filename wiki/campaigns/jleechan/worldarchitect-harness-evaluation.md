---
title: "worldarchitect.ai — 5-Layer Harness Evaluation"
type: concept
tags: [harness, worldarchitect.ai, evaluation, L1-L5]
sources: []
last_updated: 2026-04-13
---

# worldarchitect.ai — 5-Layer Harness Evaluation

## Executive Summary

The worldarchitect.ai harness has a documented 5-layer architecture (L1 Constraints through L5 Lifecycle). Seven GitHub issues (#6205–#6211) represent real gaps between documented infrastructure and enforced runtime behavior.

**Strongest layers:** L1 (file placement rules), L4 (skeptic-gate verification)
**Weakest layers:** L3 (MCP not wired), L5 (no crash recovery)

---

## Layer 1: Constraints (WEAK)

### Issue 6205 — No JSON Schema enforcement for rewards_box structure

**Finding:** No automated structural enforcement for nested field placement. Five fields drifted into the wrong nesting level during a checkpoint session merge, with no automated catch.

**Evidence:** `game_state` fields (`rewards_processed`, `level_up_in_progress`, etc.) were incorrectly nested inside `rewards_box` during checkpoint session merge without `world_logic.py` review. CLAUDE.md enforces file placement, but no automated check for field nesting correctness.

**Fix:** ArchUnit-style Python test or JSON Schema validator in presubmit verifying critical `game_state` fields are at documented paths.

**Priority: 4** (HIGH — causes real field nesting failures)

---

### Issue 6206 — No git hooks installed (only sample templates)

**Finding:** `.git/hooks/` contains only `.sample` template files. Claude Code PreToolUse/PostToolUse hooks fire before tool execution; git hooks fire after staging. Both enforcement points needed.

**Evidence:**
- `.claude/hooks/` — ~15 hook scripts (`pre_creation_blocker`, `detect_speculation`)
- `.git/hooks/` — only `.sample` files, no active hooks
- `.github/hooks/pre-commit-sha-check.sh` — exists but not installed as git hook

**Fix:** Hook installer (husky, pre-commit) to symlink `.claude/hooks/` as `.git/hooks/`.

**Priority: 3**

---

## Layer 2: Context (PARTIAL)

### Issue 6207 — No cross-session scratchpad or persistent memory

**Finding:** Each Claude Code session starts fresh. CLAUDE.md and AGENTS.md are comprehensive but static — no accumulation of agent learnings across sessions.

**Evidence:**
- `CLAUDE.md` (207 lines) and `AGENTS.md` (175 lines) — static operating protocol
- `.claude/skills/` (~50 skill files) — static procedures
- `scratchpad/` — transient files only
- `.beads/` — issue tracking, not cross-session memory

**Priority: 3**

---

## Layer 3: Execution (PARTIAL)

### Issue 6208 — settings.json MCP servers empty despite rich infrastructure

**Finding:** Claude Code MCP servers in `settings.json` are registered in the Claude Code config but not wired to actual server processes. The `mcp__worldai-tools__*` tools are available but not connected to running servers.

**Evidence:**
- `~/.claude/settings.json` MCP servers array lists `worldai-tools` and `slack` entries
- `worldai MCP server` tools confirmed functional via test calls
- But no startup script, no daemon manager, no `/etc/mcp/` config

**Priority: 2**

---

## Layer 4: Verification (STRONG)

### Issue 6209 — skeptic-cron SHA-only filter not cryptographically signed

**Finding:** skeptic-gate uses SHA of tool result as idempotency key. A SHA collision (theoretical) or a man-in-the-middle replacing the result could bypass the gate.

**Priority: 3** (HIGH theoretical, LOW practical)

---

### Issue 6210 — post_file_creation_validator has recursive hook + blocking risks

**Finding:** `post_file_creation_validator` uses a git hook that calls back into Claude Code (`claude --print`), creating a recursive invocation risk and potential deadlock.

**Priority: 2** (MEDIUM)

---

## Layer 5: Lifecycle (WEAK)

### Issue 6211 — No Claude Code session health monitoring or crash recovery

**Finding:** No watchdog monitoring Claude Code session health. Stale sessions accumulate when agents stall. Worktrees are created but never cleaned up on failure.

**Evidence:**
- 15+ stale worktrees in `~/.claude/worktrees/`
- No lifecycle event hooks for agent stall detection
- AO worker pool has no SLA monitoring

**Priority: 2**

---

## Fix Priority Order

1. **#6208** (MCP wiring) — enables testing infrastructure
2. **#6206** (git hooks) — foundational enforcement
3. **#6205** (schema enforcement) — structural correctness
4. **#6209** (cryptographic signing) — skeptic-gate integrity
5. **#6210** (recursive hook guard) — safety
6. **#6211** (session health monitoring) — lifecycle
7. **#6207** (cross-session scratchpad) — memory

---

## GitHub Issues
- [#6205](https://github.com/jleechanorg/worldarchitect.ai/issues/6205) — No JSON Schema enforcement for rewards_box
- [#6206](https://github.com/jleechanorg/worldarchitect.ai/issues/6206) — No git hooks installed
- [#6207](https://github.com/jleechanorg/worldarchitect.ai/issues/6207) — No cross-session scratchpad
- [#6208](https://github.com/jleechanorg/worldarchitect.ai/issues/6208) — MCP servers not wired
- [#6209](https://github.com/jleechanorg/worldarchitect.ai/issues/6209) — skeptic-gate SHA-only filter
- [#6210](https://github.com/jleechanorg/worldarchitect.ai/issues/6210) — post_file_creation_validator recursive risk
- [#6211](https://github.com/jleechanorg/worldarchitect.ai/issues/6211) — No session health monitoring
