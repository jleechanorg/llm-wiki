---
name: reboot_classification_and_concurrent_missions_2026-07-07
description: Four lessons from the 2026-07-07 crash-mission day — classify reboot cause before calling it a crash; check for concurrent agent missions before editing shared config; adversarial swarm verification catches missed evidence; verify observability is ARMED not just installed
metadata: 
  node_type: memory
  type: feedback
  bead: bd-p7m
  originSessionId: b63703c0-8c29-479d-a8a3-2e331de6f003
---

Four durable lessons from the 2026-07-07 Jeff-Ubuntu session (see [[watchdog_self_shutdowns_2026-07-07]] for the incident narrative).

## 1. A reboot is not a crash — classify termination cause first (Anti-Pattern fixed)

Both 2026-07-07 reboots were watchdog(8) load-average self-shutdowns (`error 253`), yet the user, soakctl, and initial triage all read them as "crashes." soakctl auto-FAILED a soak that had **zero panics in 4 days** (pstore 570→570).
**FIX (deployed 2026-07-07, bd-9ac closed):** `~/.local/bin/soakctl` now classifies every dead boot — watchdog (`journalctl -b <idx> -t watchdog | grep 'error 253'`, indexed so teardown spam can't hide it), clean (PID-1/journald markers ONLY — a *user-session* `Reached target shutdown.target` does NOT count; that false-matched the 12:52 mystery boot), else silent-stop. pstore delta stays authoritative for panics. Non-crash reboots → `INTERRUPTED` verdict, bead noted not closed-failed. Staged copy: `user_scope/scripts/soakctl`.
**Pattern:** triage order = pstore delta → `-t watchdog` grep → PID-1 shutdown markers → silent-stop.

## 2. Check for concurrent agent missions before editing shared machine config (Critical)

My `count = 16→10` edit to `~/.config/ezgha/config.toml` was byte-identically restored within 6 minutes — not a bug, but the user's OWN concurrent 12h "runner-truly-healthy" mission (goal dir `~/projects/ez-gh-actions/goals/2026-07-07-1920-runner-truly-healthy/`) whose user-stated invariant is 16 Linux runners, enforced by `ezgha-fleet-watchdog.sh`. Two authorized missions fought over one file; the revert looked like a ghost.
**How to apply:** before editing shared config, run `ps aux | grep 'codex exec'` and `ls ~/projects/*/goals/` for active missions; when two user directives conflict, the NEWER explicit one wins (June "≤10 runners" policy was superseded by the 07-07 "16 runners" goal); concede and coordinate via a note file in the other mission's goal dir instead of config ping-pong.

## 3. Adversarial swarm verification catches what confident diagnosis misses (Best Practice)

A 3-lens refute-by-default swarm (evidence / alternative-cause / plan-risk) on my "complete" diagnosis found: a third undocumented boot, the config revert, the live respawn-storm risk, and a better watchdog fix (repair-binary over threshold-raise — adopted). 2/3 lenses independently found the missed boot. This is [[use_secondo_against_confirmation_bias]] operationalized: verify the *diagnosis artifact*, not just the plan.

## 4. Observability must be verified ARMED, not installed (Critical — same class as [[verify_fix_actually_live_before_memorializing]])

kdump was installed in April (bd-uifreeze1) and never worked through 15 panics: boot log says `cannot allocate crashkernel low memory` — the `crashkernel=2G-4G:320M,...` range syntax silently fails on this box, `kexec_crash_loaded` was 0 the whole time. Every panic yielded only pstore fragments instead of full vmcores.
**FIX (staged 2026-07-07):** `/etc/default/grub.d/kdump-tools.cfg` → `crashkernel=512M,high`, arms on next reboot.
**Pattern:** after installing any crash/telemetry tooling, verify the armed-state file (`/sys/kernel/kexec_crash_loaded` = 1, `kdump-config status` = ready), not the package state. Also: guard thresholds must be derived from hardware — `max-load-1 = 24` on a 32-thread box is a self-DoS; prefer degrade-on-trip (repair-binary pausing the churn source) over reboot-on-trip.
