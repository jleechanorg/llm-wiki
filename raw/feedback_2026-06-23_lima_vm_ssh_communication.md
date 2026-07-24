---
name: lima-vm-ssh-communication
description: Two-stage SSH hop from Mac to Lima QEMU VM (self-hosted Linux runners) — port 40257 fixed via lima.yaml ssh.localPort
type: feedback
bead: none
---

## Context

The 16 Linux self-hosted runners (`org-runner-1..16`) run inside a Lima/QEMU VM called `colima` that lives on the Ubuntu host `jeff-ubuntu`. To run any command inside the Lima guest (the actual runner VM), Claude on the Mac must chain two SSH connections.

## The pattern (one bash invocation)

```bash
ssh jeff-ubuntu "
  # Inside jeff-ubuntu's shell — now SSH INTO the Lima VM
  ssh -p 40257 \
      -i ~/.lima/_config/user \
      -o ConnectTimeout=5 \
      -o BatchMode=yes \
      -o StrictHostKeyChecking=no \
      127.0.0.1 \
      'uname -a; uptime; df -h /' 2>/dev/null
"
```

Or use `limactl shell` as a one-hop alternative (no SSH config needed):

```bash
ssh jeff-ubuntu "~/.local/bin/limactl shell colima -- df -h /" 2>/dev/null
```

## Why port 40257 specifically

Lima normally picks a random ephemeral port on each `limactl start`. That breaks any hardcoded probe script (lima-watchdog.sh, ubuntu-runner-health.sh, monitor.sh). Fix: pin the port in the Lima config:

```yaml
# self-hosted-colima/install.sh writes this into lima.yaml on install
ssh:
  localPort: 40257
  loadDotSSHPubKeys: false
  forwardAgent: false
```

If you find Lima coming up on a different port (e.g. 46447) after a restart, the localPort entry is missing. Patch manually:

```bash
ssh jeff-ubuntu "~/.local/bin/limactl stop colima && sed -i 's/^ssh:$/ssh:\n  localPort: 40257/' ~/.lima/colima/lima.yaml && ~/.local/bin/limactl start colima"
```

## Why the SSH key path matters

`~/.lima/_config/user` is the SSH private key Lima generates on first boot for the `jleechan` user inside the VM. It is NOT the user's normal SSH key — using `~/.ssh/id_rsa` or any other key will be silently rejected because Lima's sshd only accepts the key it generated.

## Verification probe (the canonical "is Lima healthy" check)

```bash
ssh jeff-ubuntu "ssh -p 40257 -i ~/.lima/_config/user \
    -o ConnectTimeout=5 -o BatchMode=yes -o StrictHostKeyChecking=no \
    127.0.0.1 echo LIVE 2>/dev/null && echo Lima=LIVE || echo Lima=DEAD"
```

If `Lima=DEAD` → VM is hung or limactl port randomized. First action: `limactl list` to see actual port; if port differs from 40257, restart Lima with the pinned config.

## Why this is two stages (not one)

- `ssh jeff-ubuntu` is a normal SSH connection the Mac makes to the Ubuntu host over the network.
- The Lima VM is QEMU running inside jeff-ubuntu. Its QEMU process exposes a forwarded port on jeff-ubuntu's loopback (127.0.0.1:40257). The Lima hostagent on jeff-ubuntu handles the port forward to sshd inside the guest.

The Mac CANNOT directly SSH to the Lima guest's port 22 — the QEMU network is internal to jeff-ubuntu. Only jeff-ubuntu can reach the Lima guest's loopback port forward.

## Related memories

- [[verify-lima-vm-before-runner-ops]] — always SSH-probe Lima BEFORE diagnosing offline runners; stale docker.sock looks plausible but VM may be hung
- [[lima-vm-watchdog-gap]] — root cause of the June 18-23 5-day outage (QEMU hang with no detection); lima-watchdog.sh now auto-restarts

## References

- PR #7843 (`fix/runner-watchdog-hardening`): added lima-watchdog.sh and Lima probe to ubuntu-runner-health.sh
- PR #7851 (`fix/runner-disk-cleanup-systematic`): pinned ssh.localPort=40257 in install.sh lima.yaml template
- File: `self-hosted-colima/scripts/lima-watchdog.sh` — uses this exact pattern
- File: `self-hosted-oss/ubuntu-runner-health.sh` check_lima_vm() — uses this exact pattern with mac→jeff-ubuntu→Lima hop
