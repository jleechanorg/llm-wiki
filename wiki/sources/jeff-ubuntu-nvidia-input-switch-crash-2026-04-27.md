---
title: "Jeff-Ubuntu NVIDIA input-switch GUI crash (2026-04-27 diagnosis)"
type: source
tags: [linux, nvidia, x11, gdm, hardware, edid, display, ubuntu-24.04]
date: 2026-04-27
source_file: ../../raw/jeff-ubuntu-nvidia-input-switch-crash-2026-04-27.md
---

## Summary
On 2026-04-27 the user reported "UI crashes whenever I switch monitor inputs." Diagnosis split the symptom into two distinct issues: (A) clean GDM session restart on EDID change — annoying bounce-to-greeter, NOT a crash — and (B) a separate recurring hard-reset pattern across every boot since 2026-04-22 with no software fingerprint. Driver `580.126.09` matches a published-broken HPD-recovery branch on NVIDIA forums. Recommended fix: pin EDID via `CustomEDID` for HDMI-A-1 (eliminates the trigger entirely), with driver downgrade to 550.x as a fallback if (B) recurs.

## Key Claims
- Issue A and Issue B are different problems that were initially conflated. A is a clean session restart (Server terminated successfully exit code 0, orderly `Deleting GPU-0` teardown). B is a hard reset with no panic, no pstore record, no DRM/NVIDIA error in journal — silent stop signature consistent with NVIDIA mode-(b) HPD failure or with hardware (PSU/RAM) but indistinguishable from logs alone.
- The previously suspected runner-storm livelock is **not** the cause for the current crash pattern: log volume on the prev boot was 1,597 lines / 26h vs storm baseline 51,813 / 3h (~280× quieter). PR #6681 + #6692 merged 04:54 UTC further reduce that risk going forward.
- Box is on the **NVIDIA 580.126.09** branch, named in NVIDIA developer-forum bug reports as having broken HPD recovery (link: forums.developer.nvidia.com/t/wayland-dp-hotplug-failure-with-hdr-display-permanently-lost-rtx-4070-580-126-09/362206).
- `nvidia_drm modeset=1` and `NVreg_PreserveVideoMemoryAllocations=1` are already set; `nvidia_drm fbdev=1` is missing.
- Active connector is HDMI-A-1 only; DP-1/2/3 disconnected. Monitor manufacturer code 4c2d (Samsung).
- Switching GDM to Wayland is **not** a free fix on this driver — 580.126.09 has documented Wayland HPD bugs too.
- Non-ECC RAM means DIMM bit-flips would be invisible. Cannot rule out hardware as the root of Issue B.

## Key Quotes
> "(II) Server terminated successfully (0). Closing log file." — gdm-x-session PID 28666, 14:18:40 — proves Issue A is a clean exit, not a segfault.

> "every boot since Apr 22 shows 'still running' in utmp" — `last reboot -F` output, proving the hard-reset pattern is recurring (Issue B), not a single event.

> "Driver 570.86.15 Breaks Wayland Display Restoration on RTX 4070 SUPER — Fixed by Downgrading to 550" — title of NVIDIA forum thread that establishes the 5x0/580 regression line and 550 as the safe target.

## Connections
- [[NVIDIA proprietary driver]] — failure source, both Issue A trigger and Issue B mechanism (mode b)
- [[GDM]] — implements the EDID-change → session-restart behavior driving Issue A
- [[X11 RANDR / hotplug]] — protocol layer where the EDID change propagates
- [[CustomEDID xorg.conf option]] — primary mitigation; pins EDID so GPU never sees the HPD edge
- [[journald livelock]] — earlier (2026-04-25) freeze cause on same box; ruled out for this incident
- [[GitHub Actions runner storm (myoung34/github-runner)]] — earlier root cause, mitigated by PR #6681/#6692 (jleechanorg/worldarchitect.ai)
- [[ECC vs non-ECC RAM observability]] — concept gap; without ECC, hardware DIMM faults leave no log trace
- [[hardware watchdog + persistent SysRq + kdump]] — Tier-2 observability work that would force a panic dump on hang
