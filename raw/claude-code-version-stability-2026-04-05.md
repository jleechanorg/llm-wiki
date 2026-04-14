# Claude Code Version Stability Report: v2.1.77 through v2.1.92

**Date:** 2026-04-05
**Current version:** v2.1.77 (pinned)
**Purpose:** Decide whether to upgrade and to which version

---

## Per-Version Stability Ratings

| Version | Rating | Key Issues |
|---------|--------|------------|
| **2.1.77** | GREEN | Baseline. Stable. Known compaction threshold bug (fires at 150K regardless of 1M window) exists but is a platform-wide issue, not version-specific. |
| **2.1.78** | YELLOW | Permission regression: `.claude/` directory writes blocked in `bypassPermissions` and `dontAsk` modes (#35895, #35908 — fixed in later versions). `.claude/skills/` writes also prompted (#36396). VSCode memory regression (#35830). Good features: `StopFailure` hook, line-by-line streaming, plugin data persistence. |
| **2.1.79** | GREEN | Mostly fixes. Fixed `-p` hanging, Ctrl+C in print mode, rate limit retry for enterprise. Low risk. |
| **2.1.80** | YELLOW | `acceptEdits` mode stopped auto-approving `Write` (new file creation) — regression (#36593, fixed/closed). `--resume` fix for parallel tool results is valuable. |
| **2.1.81** | GREEN | Added `--bare` flag. Fixed OAuth token refresh race. Solid release. |
| **2.1.83** | GREEN | Major quality release. `CwdChanged`/`FileChanged` hooks, transcript search, fixed compaction-related UI issues (background agents invisible after compaction), many scroll/rendering fixes. |
| **2.1.84** | GREEN | PowerShell tool (Windows), `TaskCreated` hook, idle-return prompt. Solid. |
| **2.1.85** | GREEN | Conditional `if` field for hooks, fixed `/compact` failing on large conversations, fixed `--worktree` in non-git repos. Many good fixes. |
| **2.1.86** | RED | **Critical regression**: multiple reports of agent destroying user work (#40808 — detailed 20+ hour loss report). VSCode model switching broken (#40480). `Write`/`Edit`/`Read` failing on files outside project root (e.g., `~/.claude/CLAUDE.md`) — **directly relevant to the CLAUDE.md permission dialog issue**. Garbled characters (#40574). Changelog shows fix for the file-outside-root issue, but reports suggest instability. |
| **2.1.87** | RED | One-line fix release (Cowork Dispatch). BUT: spacebar stops working (#40814, Linux). 401 after login (#40473). Upgrade path from 2.1.86 broken on Windows (#41083). Effectively a hotfix that introduced new issues. |
| **2.1.88** | YELLOW | MCP tool results invisible — regression (#41361). Excessive token consumption reported (#42272). Custom commands in `.claude/commands/` not discovered (#41497). Discord plugin env var regression (#41768). |
| **2.1.89** | YELLOW | Massive feature release (50+ items). `PreToolUse` hook `defer` decision, `PermissionDenied` hook, autocompact thrash loop fix (important!). BUT: terminal content disappearing (#42244), SIGABRT crash on Debian (#42151), nested CLAUDE.md re-injection fix is valuable. Risk: large changeset means higher chance of latent bugs. |
| **2.1.90** | RED | **`--continue` regression**: silently drops conversation context when combined with `-p` (#43013, #42376 — **data loss**). Root cause: `sessionKind` filter added for `--resume` picker also filters `--continue`. Agent SDK `query()` timeout regression (#42884). Terminal scroll history removed (#42553). Resume after update broken (#42681). Plan mode editing files without permission (#42666). Workaround for `--continue`: `export CLAUDE_CODE_ENTRYPOINT=cli`. |
| **2.1.91** | YELLOW | Fixed `--resume` transcript chain breaks (important). BUT: `pgrep` ENOENT crash on macOS (#43336 — regression, crashes during normal Read tool use). Edit tool optimization (shorter `old_string` anchors). `--resume` cache invalidation still broken (#43657 — skill listing block migrates between messages, breaking prompt cache on every resumed turn). |
| **2.1.92** | YELLOW | Many fixes (tool input validation, thinking whitespace, seccomp). BUT: `remote-control` regression (#43609). Arrow keys output raw escape sequences in interactive menus (#43341 — regression). Intermittent freezes on Windows (#43753). `computer-use` MCP broken — native module path hardcoded to CI build machine (#43547). Insights command path building fails on Windows (#43979). `apply-seccomp` fails on Linux (#43454). |

---

## Focus Area Deep Dives

### Compaction Behavior

**Status: Platform-wide issue, no version fully fixes it.**

- The compaction threshold bug (fires at ~150K tokens regardless of 1M context window) is **not version-specific** — it persists across all versions tested.
- #42590: "Context compaction too aggressive on 1M context window (Opus 4.6)" — open, enhancement request. No configurable threshold exists yet.
- #40352: Compaction race condition during rate limit can destroy entire conversation transcript (data loss).
- #43685: `/compact [instructions]` does not actually trigger compaction (v2.1.92).
- #43886: Request to never interrupt a commit sequence with compaction.
- v2.1.89 added autocompact thrash loop detection (stops after 3 consecutive refill-to-limit cycles).
- **PreCompact/PostCompact hooks**: NOT YET IMPLEMENTED. Multiple feature requests open (#17237, #33088, #36749, #43733, #43946). All are enhancement/feature requests, none merged.

### --continue / --resume Bugs

**Status: Broken in v2.1.90, partially fixed in v2.1.91, still has cache issues.**

- v2.1.90 introduced a critical `--continue -p` regression (#43013): `sessionKind` filter silently discards sessions created by `claude -p`, so `--continue` starts a new empty session. **Workaround: `export CLAUDE_CODE_ENTRYPOINT=cli`**.
- v2.1.91 fixed `--resume` transcript chain breaks (async write failures losing history).
- v2.1.92 still has #43657: `--resume` cache invalidation — skill listing block migrates between messages on resume, invalidating prompt cache for every subsequent turn. Causes significantly higher token costs on resumed sessions.
- v2.1.89 fixed `-p --resume` hangs when deferred tool input exceeds 64KB.
- v2.1.89 fixed `-p --continue` not resuming deferred tools.

### Hook Support (PreCompact, PostCompact)

**Status: NOT AVAILABLE in any version through v2.1.92.**

Multiple open feature requests but no implementation:
- #17237 (oldest, from early 2026)
- #33088, #36749, #38018, #40492, #43733, #43946

The hook system supports: `PreToolUse`, `PostToolUse`, `StopFailure` (v2.1.78+), `SessionEnd`, `CwdChanged`/`FileChanged` (v2.1.83+), `TaskCreated` (v2.1.84+), `PermissionDenied` (v2.1.89+). But no compaction hooks.

### Permission Dialog Issues (CLAUDE.md edits)

**This is the user's specific pain point. Here is the root cause analysis:**

1. **v2.1.78 regression (#35895, #35908, #36396):** `.claude/` directory became "protected" — even `bypassPermissions` and `dontAsk` modes could not suppress the edit prompt. This was **fixed** in v2.1.80 (#36593 closed).

2. **v2.1.86 regression:** `Write`/`Edit`/`Read` failing on files outside the project root (e.g., `~/.claude/CLAUDE.md`). Changelog says "Fixed" in v2.1.86 itself, but the fix may be incomplete.

3. **Persistent issue (#37516):** `Edit` permission rules in allow list have **no effect** — `"Edit"`, `"Edit(*)"`, `"Edit(**)"`, `"Edit(/absolute/path)"` all fail to suppress the dialog. `defaultMode: "dontAsk"` also does not work for Edit. `"Read"` (bare) works, `"Edit"` does not. **This bug is still open** and affects all versions.

4. **v2.1.92 (#43384):** Empty `permission_suggestions` array for `.claude/` directory writes in `acceptEdits` mode — the permission dialog appears but offers no useful options.

5. **v2.1.84 (#210 in changelog):** "Fixed the 'allow Claude to edit its own settings for this session' permission option not sticking for users with `Edit(.claude)` allow rules."

6. **Related open issues:**
   - #37939: `--dangerously-skip-permissions` still prompts for `.claude/` directory writes
   - #41848: `--dangerously-skip-permissions` no longer bypasses permission dialogs at all
   - #43512: Request to allow disabling built-in `.claude/` path protection at project level

**Bottom line:** The `.claude/` directory has special built-in protection that overrides user permission settings. This is by design (security) but creates friction. No version fully resolves this. The Edit tool permission matching appears fundamentally broken for the `.claude/` protected directory (#37516 is still open).

---

## Upgrade Recommendation

### Best target: v2.1.85

**Rationale:**
- Includes all the good fixes from v2.1.78-v2.1.84 (hook `if` conditions, transcript search, `CwdChanged`/`FileChanged` hooks, `--resume` fixes)
- Adds conditional hook filtering (reduces hook overhead)
- Fixes `/compact` failing on large conversations
- Does NOT include the v2.1.86 destructive regression
- Does NOT include the v2.1.90 `--continue` regression
- Stable, no tagged regressions in issue tracker

### If you need v2.1.89+ features (autocompact thrash fix, `PermissionDenied` hook, `defer` decision):

**Use v2.1.89** but be aware:
- Large changeset (50+ items) means latent bugs are possible
- Terminal content disappearing reported on Linux (#42244)
- Do NOT upgrade past v2.1.89 unless the `--continue -p` fix lands (it has not as of v2.1.92)

### Versions to avoid:

| Version | Why |
|---------|-----|
| **v2.1.86** | Critical agent behavior regression, user work destruction |
| **v2.1.87** | Broken hotfix, spacebar/auth issues |
| **v2.1.90** | `--continue -p` data loss regression, still unfixed |

### CLAUDE.md permission dialog:

**No version fixes this.** The `.claude/` directory protection is architectural. Workarounds:
1. Use `--dangerously-skip-permissions` (but even this is reportedly broken in recent versions — #41848)
2. Accept the dialog as a security feature
3. Watch #37516 and #43512 for upstream resolution

---

## Summary Matrix

```
v2.1.77  [=====] GREEN   ← you are here (stable baseline)
v2.1.78  [===  ] YELLOW  ← .claude/ permission regression
v2.1.79  [=====] GREEN
v2.1.80  [===  ] YELLOW  ← acceptEdits Write regression (fixed)
v2.1.81  [=====] GREEN
v2.1.83  [=====] GREEN
v2.1.84  [=====] GREEN
v2.1.85  [=====] GREEN   ← RECOMMENDED upgrade target
v2.1.86  [=    ] RED     ← agent work destruction
v2.1.87  [=    ] RED     ← broken hotfix
v2.1.88  [===  ] YELLOW  ← MCP tool result regression
v2.1.89  [===  ] YELLOW  ← big release, good fixes, some risk
v2.1.90  [=    ] RED     ← --continue data loss
v2.1.91  [===  ] YELLOW  ← pgrep crash, cache invalidation
v2.1.92  [===  ] YELLOW  ← multiple regressions, active fixes
```
