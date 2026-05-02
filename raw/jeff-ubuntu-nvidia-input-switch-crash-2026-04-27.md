# Jeff-Ubuntu: GUI bounce / hard-reset on monitor input switch

**Date:** 2026-04-27
**Box:** Jeff-Ubuntu (jleechan workstation)
**User-reported symptom:** "UI seems to crash whenever I switch inputs (e.g., I switched to input 2 for my laptop)."

## System stack

| Component | Value |
|---|---|
| OS | Ubuntu 24.04.4 LTS |
| Kernel | 6.17.0-22-generic |
| GPU | NVIDIA RTX 4090 (HDA NVidia HDMI/DP, 4 audio outputs visible) |
| Driver | **nvidia-driver-580 580.126.09-0ubuntu0.24.04.2** |
| Display server | X11 (`XDG_SESSION_TYPE=x11`, `/usr/libexec/gdm-x-session`) |
| DM | GDM3 |
| Active connector | **HDMI-A-1 only** (DP-1, DP-2, DP-3 all disconnected) |
| Monitor | Samsung (EDID manufacturer code `4c2d`) |
| RAM | 64 GB, **non-ECC** |
| Swap | 16 GiB (added 2026-04-25) |
| Existing modprobe | `nvidia_drm modeset=1`, `NVreg_PreserveVideoMemoryAllocations=1`. Missing: `nvidia_drm fbdev=1` |

## Two distinct issues, originally conflated

### Issue A — Input-switch bounce-to-greeter (frequent, every input switch)
**Mechanism:** clean GDM session restart on EDID change.
**Evidence (2026-04-27 boot at 14:08):**
- 14:13:51 first `gdm-x-session` PID 28666 = greeter
- 14:18:38 new `gdm-x-session` PID 32540 = post-event session
- 14:18:39 user `gdm-x-session` PID 32835
- 14:18:40 OLD process exits with `(II) Server terminated successfully (0). Closing log file.`
- Preceded by `(II) NVIDIA(GPU-0): Deleting GPU-0` — orderly teardown, **not** a segfault
- No RANDR errors, no NVIDIA crash messages
**Trigger:** EDID change when monitor flips input. NVIDIA + X11 GDM treats this as a display reconfiguration and restarts the session. User experiences: "UI gone, bounced to login."

### Issue B — Hard reset (recurring; mechanism unconfirmed)
**Pattern:** every boot since 2026-04-22 ended without clean shutdown markers (`last reboot -F` shows "still running" for all 8+ boots).
**Most recent:** 2026-04-27 boot ended 13:35:46 mid-cron with no precursor in journald or kernel ring.
**Ruled out (this boot):**
- Runner storm livelock — log volume 1,597 lines / 26h (~61/hr) vs confirmed-storm baseline 51,813/3h (~17,000/hr). 280× quieter.
- OOM-killer — no events
- Kernel panic — no panic markers, pstore empty (and pstore IS mounted/capable)
- NVIDIA XID / DRM / GPU fault — no events
- Thermal throttle — CPU 28°C at boot, no throttle
- MCE / EDAC — non-ECC RAM means silent DIMM errors are invisible
- NVMe / ATA / PCIe AER errors — none
**Consistent with:**
- NVIDIA mode-(b) HPD crash (page-allocation failure inside `nvidia_modeset` that wedges before journald flushes and before the panic path runs — leaves exactly this silent-stop signature)
- Or hardware: PSU sag, DRAM bit-flip (invisible without ECC), VRM glitch
- Cannot distinguish from logs alone; both produce identical signatures

## Driver version is a known-broken HPD-recovery branch

`580.126.09` matches the version called out in [Wayland: DP hotplug failure with HDR — display permanently lost (RTX 4070, 580.126.09)](https://forums.developer.nvidia.com/t/wayland-dp-hotplug-failure-with-hdr-display-permanently-lost-rtx-4070-580-126-09/362206).

Sister regression in 570.x branch (also Ubuntu 24.04 default pool): [Driver 570.86.15 Breaks Wayland Display Restoration on RTX 4070 SUPER w/ Samsung G95SC — Fixed by Downgrading to 550](https://forums.developer.nvidia.com/t/nvidia-driver-570-86-15-breaks-wayland-display-restoration-on-rtx-4070-super-with-samsung-g95sc-fixed-by-downgrading-to-550/327977).

## Failure-mode taxonomy (per public bug research)

Two failure modes from the **same trigger** (HPD edge from monitor input switch on NVIDIA + X11):

| Mode | Signature | Observed on this box? |
|---|---|---|
| (a) Xorg segfault → bounce to GDM | X server SIGSEGV, NVIDIA error in Xorg log | **No** — exit code 0, orderly teardown |
| (b) Kernel hang → hard reset | log truncated mid-write, no `Stopping`/`Reached target shutdown`, no panic record | **Possibly** — matches yesterday's signature exactly, but no direct timestamp evidence of an input switch at 13:35:46 |

What this box **does** show is a **third path** not in the published taxonomy: clean GDM session restart on EDID change (Issue A above). Annoying, not crashy.

## Recommended fixes (in order)

1. **Pin EDID via `CustomEDID` for HDMI-A-1** — eliminates the EDID change event from the GPU's POV entirely. Lowest blast radius, highest success rate. Survives any input switch.
2. **Add `nvidia_drm fbdev=1`** to existing modprobe config — incremental, pairs with the modeset/PreserveVRAM options already in place.
3. **Downgrade NVIDIA to 550.x branch** — only if (1)+(2) don't resolve the bounce, AND if hard-reset recurs after EDID pinning. 550 is the published-stable target.
4. **Enable hardware watchdog + persistent SysRq** (Tier-2 work from 2026-04-25 freeze diagnosis, never implemented) — would force a panic dump on the next hang instead of silent stop, giving us direct evidence for Issue B.
5. **Run memtest86+** at next reboot — non-ECC RAM means we cannot rule out DIMM faults from logs alone.

**Avoid:** switching GDM to Wayland on this exact driver — 580.126.09 has documented Wayland HPD bugs too (it's not a free fix here).

## Source documents / forum links

- [NVidia GPU + KVM Switch = X11 Crash](https://forums.developer.nvidia.com/t/nvidia-gpu-kvm-switch-x11-crash/107065)
- [X doesn't return after I turn off monitor — Fedora](https://discussion.fedoraproject.org/t/x-doesnt-return-after-i-turn-off-monitor/73435)
- [Linux 1050ti monitor layout screwed up on DisplayPort disconnect/reconnect](https://forums.developer.nvidia.com/t/linux-1050ti-monitor-layout-screwed-up-on-displayport-disconnect-reconnect/117446)
- [Wayland: DP hotplug failure with HDR — RTX 4070, 580.126.09](https://forums.developer.nvidia.com/t/wayland-dp-hotplug-failure-with-hdr-display-permanently-lost-rtx-4070-580-126-09/362206)
- [Driver 570.86.15 Breaks Wayland Display Restoration — Fixed by Downgrading to 550](https://forums.developer.nvidia.com/t/nvidia-driver-570-86-15-breaks-wayland-display-restoration-on-rtx-4070-super-with-samsung-g95sc-fixed-by-downgrading-to-550/327977)
- [Managing a Display EDID on Linux — NVIDIA KB](https://nvidia.custhelp.com/app/answers/detail/a_id/3571/~/managing-a-display-edid-on-linux)
- [NVIDIA X Config Options — Appendix B](https://download.nvidia.com/XFree86/Linux-x86_64/435.17/README/xconfigoptions.html)
- Internal: prior memory `project_2026-04-25_ui_freeze_diagnosis.md` (runner-storm/journald-livelock — separate root cause, now mitigated by PR #6681/#6692 merged 2026-04-27 04:54 UTC)

## Misdiagnosis log (lessons)

1. **Initial claim "today's crash was a runner storm"** — wrong. Verified by log-volume comparison. Runner storm signature is *log volume*, not "containers exist."
2. **Initial claim "14:18:38 was an input-switch crash"** — wrong. It was the greeter→user-session login handoff (clean exit code 0, orderly NVIDIA GPU-0 teardown). Need to read X exit codes before calling something a crash.
3. **Memory item `project_2026-04-25_ui_freeze_diagnosis.md` is partially stale** — runner-storm risk mitigated by 04-27 PR merge; future diagnostic flows should not default to "runner storm" for fresh freezes on this box.
