---
title: "Reboot-cause classification, concurrent-mission config conflicts, swarm verification, kdump arming (2026-07-07)"
type: source
tags: [crash-investigation, jeff-ubuntu, watchdog, soakctl, kdump, multi-agent, adversarial-verification]
date: 2026-07-07
source_file: raw/feedback_2026-07-07_reboot_classification_and_concurrent_missions.md
---

## Summary

Four lessons from the 2026-07-07 Jeff-Ubuntu crash-mission day. Both of the day's "crashes" were actually watchdog(8) load-average self-shutdowns (max-load-1=24 on a 32-thread i9-13900K) — soakctl and initial triage misread them as kernel crashes, auto-failing a soak that had zero panics in four days. A config edit was ghost-reverted by the user's own concurrent "runner-truly-healthy" agent mission enforcing 16 runners. A 3-lens refute-by-default swarm found a missed third boot and a better watchdog fix. kdump turned out never to have been armed through all 15 panics since April.

## Key Claims

- A reboot is not a crash: triage order is pstore delta → `journalctl -b <idx> -t watchdog` (error 253) → PID-1 shutdown markers → silent-stop. A *user-session* `Reached target shutdown.target` is NOT a clean-shutdown marker (false-matched the 12:52 mystery boot).
- soakctl now emits `INTERRUPTED` (clock invalid, config NOT falsified) for non-crash reboots instead of `FAILED`; pstore fingerprint stays authoritative for panics (bead bd-9ac, deployed `~/.local/bin/soakctl`).
- Before editing shared machine config, check for concurrent agent missions (`ps aux | grep 'codex exec'`, `ls ~/projects/*/goals/`). When two user directives conflict, the newer explicit one wins; concede and coordinate via a note file, not config ping-pong.
- Adversarial refute-by-default verification of a *confident diagnosis* (not just a plan) caught: a missed 3rd boot, the config revert, a live respawn-storm risk, and a superior mitigation (watchdog repair-binary that pauses the runner fleet instead of rebooting).
- Observability must be verified ARMED, not installed: kdump was present since April but `kexec_crash_loaded=0` the whole time ("cannot allocate crashkernel low memory" — range syntax fails on this box); fixed with `crashkernel=512M,high`. Guard thresholds must derive from hardware — a load threshold below `nproc` is a self-DoS.

## Key Quotes

> "loadavg 28 16 10 is higher than the given threshold 24 18 12! ... shutting down the system because of error 253 = 'load average too high'" — the "crash" that wasn't (journal, 2026-07-07 12:51)

> "cannot allocate crashkernel low memory (size:0x10000000)" — why kdump never armed through 15 panics

## Connections

- [[RebootCauseClassification]] — the reusable triage method this incident produced
- [[WatchdogOfWatchdogsArchitecture]] — the fleet watchdog (enforce-16) vs system watchdog (load) interaction that caused the self-DoS loop
- [[AdversarialEvaluation]] — refute-by-default lenses applied to a diagnosis artifact
- [[JeffLeeChan]] — machine owner; concurrent runner-truly-healthy mission was his newer directive
