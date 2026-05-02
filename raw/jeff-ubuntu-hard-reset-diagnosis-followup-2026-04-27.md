# Jeff-Ubuntu hard-reset diagnosis — Round 2 (corrections + research)

**Date:** 2026-04-27 (continues from `jeff-ubuntu-nvidia-input-switch-crash-2026-04-27.md`)
**Outcome:** Initial PCIe-degradation hypothesis ruled out; root cause for hard resets still unconfirmed; clear diagnostic plan and 12VHPWR safety check identified.

## Summary of corrections

The earlier wiki page treated two issues:
- **Issue A — bounce-to-greeter on monitor input switch** (clean GDM session restart on EDID change)
- **Issue B — recurring hard resets** (silent stop, no panic record)

Mid-session, hardware probes appeared to find a smoking gun: `LnkSta: 2.5GT/s (downgraded)` on the RTX 4090 PCIe link. This was promoted to "root cause of Issue B" prematurely. **A subsequent under-load test invalidated the finding** — the link reaches full Gen 4 (16 GT/s) when the GPU is loaded:

```
At deep idle (P8):    2.5 GT/s
At medium idle (P5):  5.0 GT/s
Under CUDA load (P0): 16.0 GT/s   ← healthy Gen 4
```

NVIDIA aggressively varies PCIe link speed by GPU power state. The "downgrade" was normal idle behavior, not hardware degradation. Reseating the GPU is NOT necessary on this evidence.

**Root cause of Issue B is back to UNKNOWN** with several plausible candidates remaining.

## What's confirmed real about Issue B

| Evidence | Source |
|---|---|
| Recurring hard resets since 2026-04-22 | `last reboot -F` shows "still running" for all 10 boots — no clean shutdown markers |
| 160 unsafe_shutdowns / 766 power_cycles = 20.9% chronic rate | `nvme smart-log /dev/nvme0n1` — drive has been observing this across 854 days |
| Silent stop, no panic record | pstore empty after each reset despite efi_pstore loaded |
| No software signature | journal has no segfault/oops/MCE/AER/thermal/OOM in any pre-death window |
| Box at idle is healthy now | sensors: CPU 56°C, NVMe 46°C, coolant 42.4°C, GPU 43°C — all well under thresholds |
| PCIe link is healthy under load | 16.0 GT/s Gen 4 reached when GPU active |

## Remaining root-cause candidates (per research + second opinion)

Ranked by evidence-fit and forum-frequency:

1. **12VHPWR sense-pin instability** (RTX 4090-specific)
   - Per Tom's Hardware and Wccftech: hundreds of 4090s exhibit melting / contact issues; sense-pin loss triggers instant OCP/SHDN that bypasses the OS — exact signature match for "silent stop, no panic, no AER, no pstore"
   - Safety-critical: visually inspect connector for browning, asymmetric seating, deformed pins, burnt smell, warm-to-touch
2. **PSU sag under transient load**
   - Test: `nvidia-smi -pl 250` to cap GPU at 250W for 24h. If hard resets stop, PSU/12VHPWR confirmed
3. **Non-ECC RAM bit-flip**
   - 64 GB non-ECC means DIMM bit-flips are invisible to EDAC
   - Marginal cell corrupting kernel memory wedges CPU exactly the same way, no log
   - Test: Memtest86+ overnight (8+ hours per pass)
4. **Bent CPU socket pins from cooler over-torque** (LGA1700)
   - Reproducibly drops PCIe x16 → x8 or Gen 4 → lower; could intermittently wedge bus
   - Diagnose-of-exclusion; requires pulling the cooler
5. **Motherboard PCIe retimer issue** (`LnkCap2: Retimer+ 2Retimers+`)
   - Less common, harder to fix, would manifest as link instability under stress

## Issue A status (separate from Issue B)

Bounce-to-greeter on monitor input switch — clean session restart on EDID change. Still treatable independently:
- **Fix:** pin EDID via `CustomEDID` xorg.conf option for DFP-0 (Samsung Odyssey G8)
- EDID was captured this session: `/tmp/edid-prep/hdmi-a-1.bin`, 256 bytes, valid checksums, monitor name "Odyssey G8"
- Install was prepared but not executed (waiting on box-stability work to finish first)

## Diagnostic plan — revised priority order

### Immediate (safety-critical)
1. **Visual 12VHPWR inspection** before next planned reboot. Look for: discoloration, asymmetric seating, smell, warm plug. If anything off — do not repower.

### Cheap experiments (run while box is up)
2. `nvidia-smi -pl 250` — cap GPU at 250W. Run for 24h or until next crash. Splits PSU vs not-PSU.
3. `setpci`-based PCIe AER unmask — only if we want noisier logs (research notes likely won't surface new info on a healthy link).

### Overnight tests
4. **Memtest86+** — 8+ hours, full pass. The single biggest blind spot in current evidence (no ECC, no log signature).
5. Continuous logging: write per-minute snapshots of PCIe link speed, GPU pstate, CPU temp, NVMe SMART → if next crash captures a degraded state right before death, root cause becomes visible.

### Hardware checks (require shutdown)
6. Reseat GPU + 12VHPWR cable
7. Update motherboard BIOS (multiple Z690/Z790 BIOS updates touched PCIe stability)
8. Inspect LGA1700 CPU socket pins for damage

## Research-cited evidence

Closest case match to this box:
- **NVIDIA Devforum 366619** — "Hard system hang Ubuntu 24.04, driver 580.126.09, no kernel log output" — exact OS + driver + symptom match
- **NVIDIA/open-gpu-kernel-modules issue #1010** — PCIe Gen 1 + system hangs (the false-positive that hooked us; still cited because it's a real failure pattern that LOOKS like our symptom)
- **Tom's Hardware — RTX 4090 16-pin connector melted after 1 year of usage**
- **Wccftech — Hundreds of RTX 4090 GPUs still prone to 12VHPWR connector issues**

## Process lessons captured (memory file references)

- `feedback_2026-04-27_validate_anomaly_under_load.md` — power-state-varying metrics (PCIe link, GPU clock, fan RPM, etc.) must be re-checked under load before declaring an anomaly
- `project_2026-04-27_pcie_downgrade_root_cause.md` (status: superseded) — record of the misdiagnosis + correction
- `feedback_2026-04-27_check_pcie_link_speed_first.md` (status: superseded) — original framing was wrong, see corrected version

## Conversation history note

User intuition "feel like we had a bunch of bad crashes before" was correct. NVMe SMART confirms it: 160 unsafe shutdowns over 854 days of drive uptime. The crash pattern predates this week's diagnostic effort by a long margin.

## Open question for next session

Whether the BIOS / motherboard makes any noise about PCIe / power events. Need: motherboard model + BIOS version (`sudo dmidecode -t baseboard -t bios`), and whether vendor exposes a UEFI event log accessible from Linux.
