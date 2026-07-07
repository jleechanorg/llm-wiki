---
name: jeff-ubuntu-oom-runner-starvation-2026-07-07
description: "A 12GB colima VM plus desktop apps on jeff-ubuntu's 62Gi host starved 13 self-hosted runner containers via OOM; staged container restart recovered 15/16"
metadata: 
  node_type: memory
  type: project
  bead: "none (see rev-gxv98, rev-88wm6, rev-ih7n6 for adjacent open beads)"
  originSessionId: cfee38e7-2623-45d6-b7e1-87ba5e3a8d31
---

On the night of 2026-07-06/07, jeff-ubuntu's self-hosted GitHub Actions runner fleet (16 containers) largely went dark. Root cause: the colima VM was sized at 12GB while desktop applications running on the same 62Gi host consumed enough additional memory that the combined pressure triggered OOM kills, starving 13 of the 16 runner containers (the containers run inside the colima/Lima VM per [[reference-jeff-ubuntu-docker-lima]], so host-level `docker ps` alone would not have shown the failure).
- **Why this matters:** this is a distinct failure mode from the previously-documented Lima VM silent hang ([[project_2026-06-23_lima_vm_watchdog_gap]]) — that was the VM itself becoming unresponsive; this is the VM staying up but being memory-starved by co-resident desktop load, so `limactl` status and even a live SSH session can look fine while runner containers inside are being OOM-killed one by one.
- **Recovery:** a staged (not all-at-once) container restart recovered 15 of 16 runners. Staging avoided re-triggering the same OOM condition that a simultaneous mass restart would likely reproduce (all 16 containers cold-starting at once spikes memory demand higher than steady-state).
- **Adjacent open beads found during this session** (not closed — still need root-cause follow-up): `rev-gxv98` (Colima VM state=Stopped at 2026-07-07T01:11:04Z, auto-started by watchdog — possibly the same memory-pressure event triggering a full VM stop rather than just container OOM), `rev-88wm6` (jeff-ubuntu monitor.sh/lima-watchdog.sh cron jobs silently stopped logging since last reboot — means this whole incident window had reduced observability), `rev-ih7n6` (runner host disk exhaustion, separate resource axis).

**How to apply:** when jeff-ubuntu runners show mass-offline or mass-busy-stuck symptoms, check colima/Lima VM memory allocation vs actual host free memory (`free -h` on the VM, not just the host) before assuming a code/registration-token problem ([[feedback_2026-06-28_ao_runner_token_expiry_404]] and [[feedback_2026-06-28_runner_alert_hysteresis_noise]] cover other causes of the same "runners look dead" symptom). If restarting a starved fleet, stage the restart in small batches rather than restarting all containers simultaneously. Consider raising the colima VM memory allocation above 12GB, or moving desktop-app load off the runner host, as the durable fix — tracked loosely under `rev-runn001` (host freeze / cgroup binding) but no dedicated memory-sizing bead exists yet; create one if this recurs.
