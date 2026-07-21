---
name: feedback_2026-07-17_doc_stated_policy_must_be_code_enforced
description: "A SKILL.md/doc declaring a safety policy (e.g. \"fail-closed\") does not make it true — verify the live code actually enforces it"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d3cfc352-9d05-44f7-a2b8-13ee0b08732e
---

`.claude/skills/ezgha-watchdog/SKILL.md` declared "Restart-only remediation is
UNAVAILABLE (fail-closed)" as policy, but the live launchd/systemd-installed
script (`scripts/ezgha-fleet-watchdog.sh`, ticking every 120s) restarted the
`ezgha serve` supervisor unconditionally once past a hysteresis threshold —
`launchctl kickstart` / `systemctl restart` ran with no way to disable it
short of `--dry-run` (which also suppressed unrelated colima auto-start
logic). The doc and the code disagreed, and nobody had checked.

A real `/advice` pass (Opus + web research + 4-model secondo panel) caught
this on PR jleechanorg/worldarchitect.ai#8393, which had originally shipped
as a **docs-only** change disclosing the gap ("Known gap in this docs-only
PR... tracked separately") rather than fixing it. On follow-up the actual
code fix was made in the same PR: added `EZGHA_WATCHDOG_ALLOW_RESTART`
(unset/0 = detect+log only; explicit `=1` required to execute the restart
command), RED/GREEN-verified with a new `scripts/test_restart_gate.sh` that
mocks `launchctl`/`limactl`/`ezgha` and asserts no restart fires without
opt-in, plus a restart does fire with it. shellcheck clean.

**Why:** Any skill/doc that makes a safety claim ("fail-closed", "read-only",
"never auto-X") is a testable assertion about the code, not just prose. If
nobody wrote a test asserting the code matches the doc, the two silently
drift — exactly what happened here for over a week (doc updated 2026-07-13,
code gap not closed until 2026-07-17).

**How to apply:** When a SKILL.md/README/CLAUDE.md makes a safety-relevant
policy claim about a script or service, grep the actual implementation for
the corresponding gate before trusting the doc. If the gate doesn't exist,
that's a real bug, not a "docs-only, tracked separately" deferral — fix the
code in the same PR when it's small (this fix was ~50 lines + one test file),
per the fix-on-discovery rule.

**Second pattern from the same session — deploying a fix to a stale/diverged
checkout without destructive git ops:** the operator's live daily-driver
checkout (`/Users/jleechan/worldarchitect.ai`) had a local `main` branch
465 commits ahead / 10 behind `origin/main` (stale drift from an old
pre-history-rewrite snapshot, not real unpushed work) and a separate checked
-out branch (`worktree_llm_ignore`) with similar drift. Reconciling either
via `git pull`/`git reset --hard` would have required a destructive
operation needing separate explicit authorization. Instead: left both
branches untouched, ran `git show origin/main:<path> > <path>` to overlay
just the one file the live launchd job actually executes, verified with
`bash -n` + a real `launchctl kickstart -k` trigger showing the updated
script ran cleanly. Zero branch-history risk, fully reversible
(`git checkout -- <file>`), and the live process was provably updated (not
just "the file changed on disk").

Related: [[feedback_2026-07-16_coderabbit_rate_limit_account_wide_and_approve_config]]
(same session — verify-before-trust discipline). Bead `rev-ft3i8` updated
with this fix's provenance (2026-07-17); full acceptance still blocked on
ez-gh-actions PR #67/#70 landing.
