---
name: hermes-ecosystem-breaks-from-launchd-plist-drift-scripts-moved-deleted
description: "Systemic root cause for /history, /ms, mem0 \"always keeps breaking\" — plists reference scripts that get moved to worktrees/deleted, exit 127 silently"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a7986b04-4bf6-4480-8eab-c42621bf3503
---

**Pattern (observed 2026-06-18, recurring):** Hermes ecosystem services keep breaking because of **launchd plist drift** — plists reference scripts at hardcoded paths that get moved/deleted/refactored, but the plists never get updated. Exit code 127 (command not found) silently accumulates.

**Concrete instances seen in one audit (2026-06-18):**

| Service | Plist | Referenced script | FIX on 2026-06-18 |
|---|---|---|---|
| Hermes gateway | `ai.hermes.prod` | `~/.hermes/scripts/launchd-env-wrapper.sh` | FIX: restored from `~/.hermes/.claude/worktrees/nudge-rate-limit/scripts/launchd-env-wrapper.sh` (worktree backup); `launchctl kickstart -k gui/$(id -u)/ai.hermes.prod` → PID 20746, `/health` 200 OK |
| Claude memory sync | `ai.hermes.claude-memory-sync` | `~/.hermes/scripts/sync-claude-memory.sh` | FIX: restored from same worktree |
| Qdrant plist | `~/Library/LaunchAgents/ai.hermes.qdrant-docker.plist` | `docker start hermes-qdrant` (wrong container name) | FIX: broken plist renamed `*.broken-2026-06-18`; rendered canonical plist from `~/.hermes/launchd/ai.hermes.qdrant.plist.template` (substituting `@HOME@`) and installed as `~/Library/LaunchAgents/ai.hermes.qdrant.plist` |
| Qdrant container | n/a | `hermes-mem0-qdrant` (deleted) | FIX: `bash ~/.hermes/scripts/install-qdrant-container.sh` recreated container with `--restart unless-stopped`; mem0 write test confirmed point count 144→145 |
| 11 other launchd jobs | various | various | NOT YET FIXED — track via [jleechan-vuh](https://github.com/jleechanorg/agent-orchestrator/issues/709) (nightly audit cron) |

**How to recognize this pattern (diagnostic order):**

1. `launchctl list | awk '$1=="-" && $2=="127" {print $3}'` — exit 127 = missing script. List plists with broken references.
2. `ls -la /Users/jleechan/.hermes/scripts/<script-name-from-plist>` — confirm file is gone.
3. `find ~/.hermes/.claude/worktrees ~/.hermes/.worktrees -name "<script>"` — most "missing" scripts live in old worktrees from prior refactors. They were moved out of `scripts/` but the plist wasn't updated.
4. Check `~/Library/LaunchAgents/` vs `~/.hermes/launchd/*.template` — drift between installed plist and template is the policy violation.

**Why it keeps recurring:**
- Scripts get moved during refactors (script → worktree → different repo).
- `launchd-plist-template` rule exists (`~/.claude/skills/launchd-plist-template/SKILL.md`) but isn't enforced on every plist install.
- `KeepAlive SuccessfulExit: false` makes launchd restart the broken job every 10s (ThrottleInterval), creating log noise but never fixing itself.
- Each crash → restart cycle compounds with other drift (e.g., qdrant container deleted, gateway crash leaves mem0-server orphaned).

**Fix order (when this pattern appears):**

1. Identify exit-127 plists: `launchctl list | awk '$2==127 {print $3}'`
2. For each: find the script in `~/.hermes/.claude/worktrees/*/scripts/` or `~/.hermes/.worktrees/*/scripts/`
3. Restore the script: `cp ~/.hermes/.claude/worktrees/<branch>/scripts/<script> ~/.hermes/scripts/ && chmod +x`
4. If the script is wrong/outdated: regenerate plist from template per `launchd-plist-template` rule.
5. Kickstart the plist: `launchctl kickstart -k gui/$(id -u)/<label>`
6. Verify: `launchctl list | grep <label>` should show PID + exit 0 within a few seconds.

**Permanent structural fix (not yet implemented — would prevent recurrence):**

A nightly audit cron that runs:
```bash
launchctl list | awk '$2=="127" {print $3}' | while read label; do
  plist=~/Library/LaunchAgents/${label}.plist
  [ -f "$plist" ] && plutil -p "$plist" | grep -A0 "ProgramArguments" || echo "$label"
done | tee ~/.hermes/logs/launchd-drift-$(date +%F).log
```
Alert via `HERMES_OPS_SLACK_CHANNEL` if non-empty. This would have caught all 13 broken jobs at once.

**Why /history and /ms "always keep breaking" (the user's actual complaint):**

- /history and /ms skills run sqlite/grep reads against backends managed by these launchd services.
- When gateway or qdrant is down, dependent services (mem0-server, hermes memory.db writers) silently fail.
- The /ms skill explicitly skips mem0 (`# Mem0 (Qdrant at localhost:6333) not directly searchable — skip`), so a mem0 outage doesn't break /ms directly — but the user's perception is that "everything is broken."
- **Once the launchd drift is fixed (13 jobs at exit 127), the entire hermes ecosystem becomes reliable.** /history and /ms will work consistently.

**Related memory:** [[reference_hermes_mem0_qdrant_setup]] (mem0-specific qdrant container setup)

**Why `/launchd` skill is the structural defense (not yet applied to all plists):**

The `~/.claude/skills/launchd/SKILL.md` skill encodes the canonical 6-step protocol. The drift today happened because **steps 4 and 6 were skipped for several plists**:

1. Write target script ✓
2. Write sourced wrapper script (`launchd-env-wrapper.sh`) — this is what was missing for gateway + sync ✓ FIXED
3. Write plist template file using `@HOME@` placeholders ✓ for qdrant (template at `~/.hermes/launchd/ai.hermes.qdrant.plist.template`); ✗ for many other plists
4. **Commit template to owning repo** — this is the structural defense. `~/.hermes/launchd/<label>.plist.template` MUST exist; install scripts can detect missing templates and refuse to install orphan plists. **The broken qdrant plist was hand-authored — no template existed when it was installed, so no drift detection was possible.** ✓ FIXED for qdrant (broken plist quarantined, template version installed); ✗ NOT FIXED for the other 11 plists.
5. `launchctl bootout` on existing registration (idempotent)
6. Bootstrap rendered plist + verify

**The structural fix that prevents recurrence:** every plist install MUST verify `~/.hermes/launchd/<label>.plist.template` exists in the repo before bootstrapping. If absent, refuse and demand template first. This is what `install-launchagents.sh` does — but it only fires if invoked. The [jleechan-vuh](https://github.com/jleechanorg/agent-orchestrator/issues/709) nightly audit cron is the missing backstop that catches drift for any plist installed outside the canonical path.

**Apply this rule (not just for AO repo, for any plist):**

- Before `launchctl bootstrap` for a new plist, verify a `.plist.template` exists in the owning repo (e.g. `~/.hermes/launchd/` for Hermes, `~/.config/mcp-daemon/` for MCP daemons per `mcp-installation` skill).
- Never install a hand-authored plist. If the template doesn't exist, write it first.
- After every `ao-update.sh`, run `launchctl list | awk '$2=="127" {print $3}'` — exit 127 within 24h of an update is drift evidence.
- The user's "X keeps breaking again" complaint, when X is a launchd-managed service, is this pattern until proven otherwise.