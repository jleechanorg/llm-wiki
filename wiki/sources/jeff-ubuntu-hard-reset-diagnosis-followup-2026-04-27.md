---
title: "Jeff-Ubuntu hard-reset diagnosis follow-up — PCIe misdiagnosis correction (2026-04-27 R2)"
type: source
tags: [linux, nvidia, hardware, pcie, rtx-4090, 12vhpwr, debugging-methodology, diagnostic-error, memory-correction]
date: 2026-04-27
source_file: ../../raw/jeff-ubuntu-hard-reset-diagnosis-followup-2026-04-27.md
---

## Summary
Round 2 of the Jeff-Ubuntu hard-reset investigation. Mid-session, an apparent smoking gun (RTX 4090 PCIe link at 2.5 GT/s) was promoted to "root cause" before validation. A skeptical second opinion (Gemini) prompted an under-load test that disproved the diagnosis: the link correctly reaches Gen 4 (16 GT/s) when the GPU is active. The Gen 1 reading was normal NVIDIA P8 idle behavior, not hardware degradation. Root cause for hard resets remains unconfirmed; remaining candidates are 12VHPWR sense-pin instability (RTX 4090-specific safety-critical risk), PSU sag, non-ECC RAM bit-flip, and bent CPU socket pins. NVMe SMART confirms 160 historical unsafe_shutdowns — chronic, not new.

## Key Claims
- **PCIe Gen 1 reading was a misread**, not a real downgrade. NVIDIA driver puts the link at 2.5 GT/s in P8, 5.0 GT/s in P5, 16.0 GT/s in P0. Validated by under-load test (CUDA context create + 256 MB alloc → link goes Gen 4).
- **Hard reset root cause still unknown.** Software signatures all negative (no panic, no pstore, no AER, no MCE, no thermal). Hardware candidates: 12VHPWR (highest fit), PSU sag, RAM (non-ECC blind spot), CPU socket pins.
- **NVMe SMART confirms chronic pattern**: 160 unsafe_shutdowns / 766 power_cycles = 20.9% over 854 days drive uptime.
- **12VHPWR melt risk on RTX 4090 is the highest-priority hardware safety check** before next reboot — Tom's Hardware and Wccftech document hundreds of cases; Linux silent-stop signature matches sense-pin loss / OCP/SHDN behavior exactly.
- **Gemini's "split the diagnostic tree" test**: `nvidia-smi -pl 250` to cap GPU at 250W for 24h. Hard resets stopping confirms PSU/12VHPWR; continuing rules them out.
- **Issue A (bounce-to-greeter on input switch) is unrelated and still tractable** via EDID pinning. EDID was captured this session.

## Key Quotes
> "Gen 1 / 2.5GT/s is the normal idle state for NVIDIA GPUs (ASPM downshift). If a flaky link were really wedging the bus, you would expect Xid 79 ('GPU has fallen off the bus'), driver timeouts, or hangs — not a clean power cycle with no logs at all." — Gemini second opinion, 2026-04-27

> "Hard resets with zero logs are almost always power delivery or thermal, not PCIe signaling." — Gemini

> "12VHPWR melt risk is the #1 hazard. Silent hard-reset + PCIe Gen 1 stuck + RTX 4090 = high prior for connector contact failure. Power off NOW and inspect the 12VHPWR plug for: brown/black discoloration, asymmetric seating (one side higher than the other), deformed pins, smell of burnt plastic, warm-to-touch plug after light use." — Research agent finding from Tom's Hardware / Wccftech / Overclock.net

## Connections
- [[Jeff-Ubuntu NVIDIA input-switch GUI crash|sources/jeff-ubuntu-nvidia-input-switch-crash-2026-04-27]] — Round 1 source doc
- [[12VHPWR connector]] — primary hardware risk identified
- [[NVIDIA RTX 4090]] — model with documented power-connector issues
- [[PCIe link power management]] — concept that explains the misread (P8/P5/P0 different speeds)
- [[non-ECC RAM observability gap]] — the diagnostic blind spot for silent-stop class
- [[adversarial second opinion]] — validation method that caught the error
- [[validate-under-load methodology]] — the meta-lesson; see feedback memory
