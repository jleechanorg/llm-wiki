---
title: "Self-Hosted Runners (jleechanorg)"
type: entity
tags: [self-hosted-runners, github-actions, infrastructure]
date: 2026-06-23
last_updated: 2026-06-23
---

## Self-Hosted Runners (jleechanorg/worldarchitect.ai)

GitHub Actions self-hosted runner fleet for the `jleechanorg/worldarchitect.ai` organization. Two physical hosts, 22 runners total.

### Fleet breakdown

| Host | Runner names | Count | Architecture | Container runtime |
|------|--------------|-------|--------------|-------------------|
| Mac (M-series) | `org-runner-mac-1..6` | 6 | ARM64 | Docker Desktop / Colima |
| Linux (jeff-ubuntu → Lima VM) | `org-runner-1..16` | 16 | X64 | Docker in Lima QEMU guest |

### Disk management (post PR #7851)

**Linux fleet:**
- Lima disk threshold: 75% (alert), 85% (auto-prune), 85% (hard-cleanup trigger via daily cron at 04:00)
- Pre-job hook runs `/_work` cleanup in-container
- Host-level `monitor.sh` runs every 15 min via cron
- Hard-cleanup (stop+prune+start) runs **daily** at 04:00 (changed from weekly in PR #7851)
- Watchdog (Lima QEMU hang detection) runs every 5 min via cron

**Mac fleet:**
- Pre-job hook runs `/_work` + pip cache cleanup in-container at 10 GB free threshold (was 5 GB; PR #7851)
- `mac-runner-disk-cleanup.sh` runs every 30 min via launchd
- Host-level `docker image prune -f` runs unconditionally on each cycle (PR #7851)
- `ubuntu-runner-health.sh` (Linux-side monitor) checks Lima from Mac every 15 min via launchd

### Critical bugs fixed in PR #7851

1. `monitor.sh:189` had `docker system prune -f --volumes` at 90% disk — would destroy all 16 named runner workdir volumes. **Removed `--volumes`**, lowered trigger 90→85%.
2. Hard-cleanup cron was weekly (`0 4 * * 0`) — 7 days of uncleaned layers. **Changed to daily** (`0 4 * * *`).
3. Hard-cleanup skip threshold 70% (would skip at 78%) — **lowered to 50%**.
4. Mac cleanup only cleaned inside containers — **added host-level image prune**.
5. Lima SSH port randomized on restart — **pinned `ssh.localPort: 40257`** in install.sh lima.yaml template.

### References

- [[LimaVM]]
- [[LimaWatchdog]]
- [[LimaVMSSHCommunication]]
- [[RuntimeMirror]] (stable-path install convention)
- PR #7843 (Lima watchdog + mac health monitor Lima probe)
- PR #7851 (systematic disk cleanup)
