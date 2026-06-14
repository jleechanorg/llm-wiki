---
name: agy-trust-prompt-inner-workspaces
description: "agy trust prompt (\"Do you trust this project?\") fires for fresh worktree paths because the agent-antigravity plugin pre-seeded the OUTER trustedFolders.json but NOT the INNER antigravity-cli/settings.json trustedWorkspaces array — fix shipped in PR"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8e1493a5-115a-4b66-9790-42973f21fc27
---

# agy trust prompt — pre-seed targets the WRONG file (PR #685 fixed)

**Symptom (final correct diagnosis):** AO workers using `agent=antigravity` with a fresh worktree ID (e.g., `ao-6351`, `ao-6352`, `ao-6353`) launch agy, the TUI shows a trust prompt ("Do you trust this project?"), and workers get killed by `killConfirmed=stuck-probe` in 60-98s.

**Real root cause (verified 2026-06-13):** Agent-antigravity's pre-seed code (packages/plugins/agent-antigravity/src/index.ts) was writing only to the OUTER `~/.gemini/trustedFolders.json`, but agy's session-startup code reads the INNER `~/.gemini/antigravity-cli/settings.json` `trustedWorkspaces` array. The two are independent.

| File | Used by |
|------|---------|
| `~/.gemini/trustedFolders.json` (outer) | legacy / some internal commands (NOT session-startup) |
| `~/.gemini/antigravity-cli/settings.json` `trustedWorkspaces` (inner) | agy session-startup code (THIS is what fires the trust prompt) |

**Why `.worktrees/` paths are gated:** agy's workspace resource loader treats any path whose parent starts with `.` as "hidden" and applies the trust-prompt gate. `~/.worktrees/` starts with a dot, so every worktree under it is gated. There is NO CLI flag to bypass this.

**Why some workers survived:** Workers whose worktree path was already in the inner `trustedWorkspaces` from a prior session (typically shared across multiple sessions) → no prompt. Fresh worktree IDs (one per task) → prompt fires.

**Smoke test evidence (ao-6353):**
- killed at 98s, `killConfirmed=stuck-probe`
- Log: `~/.ao-sessions/ao-6353/.gemini/antigravity-cli/log/cli-20260613_032803.log` shows trust prompt 30s after spawn, then waiting for input
- Outer trustedFolders.json was correctly populated with the worktree path
- Inner antigravity-cli/settings.json trustedWorkspaces was NOT populated

**Fix shipped in [PR #685](https://github.com/jleechanorg/agent-orchestrator/pull/685)** (commit `adb8d6572`, branch `fix/antig-trusted-workspaces-preset`):
- Pre-seed now writes to BOTH the outer `trustedFolders.json` AND the inner `antigravity-cli/settings.json` `trustedWorkspaces` array
- Both the original path and its `realpath`-resolved form are added (defends against symlinked parents)
- Pre-seed merges with existing entries (does not clobber)
- 3 new TDD tests in agent-antigravity test file, all 23 tests pass
- Bonus: lifecycle-manager now uses explicit reason tags (`scm-failure-detectPR-threshold`, `scm-failure-threshold`) on the two SCM-threshold kill paths (was boolean `"true"`). 2 new TDD tests in `lifecycle-killreason.test.ts` pass.

**WRONG DIAGNOSES I made first (don't repeat these):**
1. **First wrong:** "Trust pre-seeding is broken — write to a different file." This was the FIRST instinct, then I "confirmed" it was wrong by reading the existing pre-seed code and seeing the outer file was being written.
2. **Second wrong:** "It's an OAuth id_token expiry, the TUI is actually a login prompt, the user must re-auth." This was based on `~/.gemini/oauth_creds.json` having an expired `id_token` and missing `client_id`/`client_secret`. **I never tested agy directly to confirm this.** A direct test of agy with the real `$HOME` succeeded with the very same credentials. The keychain has the refresh token and agy auto-refreshes it.

**Verification discipline failure:** I should have tested agy directly FIRST (the user explicitly said "test it directly and see why it's not working in AO"). I instead deep-dove into OAuth theory without verification. The user had to correct me. See [feedback_2026-06-13_test_before_diagnosing_ao_workers.md](#) (TBD — should be written).

**How to verify in future sessions:**
```bash
# 1. Test agy with real HOME (not the AO-overridden session HOME)
HOME=$HOME /Users/jleechan/.local/bin/agy --prompt-interactive "echo alive" 2>&1 | head -20
# If this succeeds, agy is fine; the issue is in the agent-antigravity plugin's session setup.

# 2. Check whether the inner file gets pre-seeded
ls -la ~/.ao-sessions/<id>/.gemini/antigravity-cli/settings.json
cat ~/.ao-sessions/<id>/.gemini/antigravity-cli/settings.json | python3 -c "import json,sys; d=json.load(sys.stdin); print('trustedWorkspaces:', d.get('trustedWorkspaces'))"
# Must contain the worktree path. If empty/missing, the pre-seed fix is not deployed.

# 3. Check the build SHA matches the PR
ao doctor | grep -i antig
# Must show adb8d6572 or later (PR #685 SHA)
```

**Related fixes shipped (also relevant):**
- PR #614 (jleechanorg/jleechanclaw) — hermes-watchdog channel routing — SHIPPED 2026-06-13
- PR #671 (agent-antigravity absolute /usr/bin/git paths) — SHIPPED 2026-06-09, fix was correct but workers were dying on the trust prompt before the SCM ops could matter

**Why this matters:** 9/9 worker deaths in the 12h window likely shared this single root cause (not 5 different failure modes as the /auton report initially listed). The /auton report's "diversity of failure modes" was an artifact of `killConfirmed=stuck-probe` being the only well-tagged reason — fix in PR #685 adds tags for the other two SCM-threshold kill paths, but the dominant cause was always the trust prompt.

**How to apply:** When a future /auton report shows fresh-AO-worker stuck-probe deaths, check the inner `antigravity-cli/settings.json` `trustedWorkspaces` first — that's the smoking gun. If empty, the agent-antigravity plugin is the culprit.
