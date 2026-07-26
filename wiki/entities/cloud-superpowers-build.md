---
title: cloud.superpowers.build
type: entity
tags: [host, ssh, cloud-build, prime-radiant]
created: 2026-07-20
updated: 2026-07-20
sources:
  - superpowers-cloud-build-2026-07-20.md
---

# cloud.superpowers.build

**Role:** Remote build-host door for the Superpowers Cloud Build plugin. Listens on port 22 with pinned-host-key SSH authentication.

**Connection:** `ssh://cloud.superpowers.build:22/<project-slug>/<slug>-<run_id>` (run-scoped URL identity; both pushes — frozen work branch + control frame — reuse the same URL snapshot to enable the one bounded retry on `provisioning_timed_out`).

**Provisioning:** Door provisions a box on demand per client-key + project-slug. Same key + same project = serialized onto the same box.

**Security model:**
- Pinned host key in `~/.ssh/cloud-build/known_hosts` (enrollment sets this; do not bypass strict host-key checking)
- Per-client ed25519 identity in `~/.ssh/cloud-build/id_ed25519`
- Server-side git secret guard walks the push range; rejects if any commit in the range introduces a sensitive file (this is the #1 blocker for real projects with tracked secrets in history)

**Public key fingerprint enrollment:** `~/.config/cloud-build/state.json` stores `enrolled_fp_hash` (SHA-256 of the public key, scoped to this box's ownership).

**Known failure modes:**
- `cloud-bastion: CLOUD_BUILD_RETRYABLE=provisioning_timed_out` → one replay allowed (frozen run_id reused)
- All other failures are final — host-key mismatch, auth failure, slug not enrolled, git secret guard rejection
- `failed` / `aborted` runs leave partial commits fetchable on the work branch
- `done_unverified` requires manual verification before landing

## See also

- [[Superpowers Cloud Build]]
- [[Prime Radiant]]
