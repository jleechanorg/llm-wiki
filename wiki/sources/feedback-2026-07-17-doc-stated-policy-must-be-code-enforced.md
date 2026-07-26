---
title: "Doc-stated safety policy ('fail-closed') must be code-enforced, not just written"
type: source
tags: [ezgha, watchdog, fail-closed, code-review, advice, git-safety]
date: 2026-07-17
source_file: feedback_2026-07-17_doc_stated_policy_must_be_code_enforced.md
---

## Summary
`.claude/skills/ezgha-watchdog/SKILL.md` declared restart-only remediation "UNAVAILABLE (fail-closed)" as policy, but the live launchd-installed `scripts/ezgha-fleet-watchdog.sh` restarted `ezgha serve` unconditionally with no code-level gate — the doc and the code had silently drifted apart for over a week. A real `/advice` pass caught the mismatch on PR worldarchitect.ai#8393. Fixed with an explicit opt-in env var, RED/GREEN tested, and deployed to a live, diverged operator checkout via a non-destructive file overlay rather than a git branch reconciliation.

## Key Claims
- A safety claim in a doc ("fail-closed", "read-only", "never auto-X") is a testable assertion about the code, not just prose — if nothing tests that the code matches the doc, they drift.
- This specific PR had originally shipped as **docs-only**, explicitly disclosing the gap rather than fixing it ("Known gap in this docs-only PR... tracked separately") — the fix only landed on a follow-up pass.
- The fix: `EZGHA_WATCHDOG_ALLOW_RESTART` env var, unset/0 = detect+log only (matches doc), explicit `=1` required to execute `launchctl kickstart` / `systemctl restart`.
- RED/GREEN verified via a new `scripts/test_restart_gate.sh` that mocks `launchctl`/`limactl`/`ezgha` and asserts no restart without opt-in, restart fires with opt-in, and `--dry-run` always suppresses restart regardless of opt-in.
- Deploying the fix to the operator's live daily-driver checkout hit a separate discovery: the local `main` branch there had diverged 465 commits ahead / 10 behind `origin/main` — stale drift from an old pre-history-rewrite snapshot, not real unpushed work. Rather than `git pull`/`git reset --hard` (destructive, needing separate authorization), the fix was deployed via `git show origin/main:<path> > <path>` — a single-file overlay with zero branch-history risk, verified live via a real `launchctl kickstart -k` trigger.

## Key Quotes
> "Restart-only remediation is UNAVAILABLE (fail-closed) pending jleechanorg/ez-gh-actions PR 67 (dual-Lima convergence) and PR 70/issue 60 (recovery controller) merging AND being proven live-deployed" — SKILL.md's stated policy, which the code did not enforce until this fix.

## Connections
- [[EzGhaDaemon]] — the daemon this watchdog supervises
- [[WorldArchitectAI]] — repo (worldarchitect.ai) where the watchdog skill and its SKILL.md live
- [[AO-Claim-Fail-Closed]] — related fail-closed-verification pattern in a different subsystem (AO claims), same underlying discipline: don't trust a status claim without execution proof
