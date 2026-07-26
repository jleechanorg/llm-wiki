# Cloud Build (Superpowers /super) enrollment — how to verify it, and the trap

## The trap that wasted a whole debugging session (2026-07-21)

To check whether the Superpowers Cloud Build box (`cloud.superpowers.build`, used by
`/super` for remote coding) accepts this machine's key, you MUST ssh as the correct user.
The protocol has exactly TWO users, defined in
`~/superpowers-cloud-build-main/assets/cloud-build-client-config-v0.json`:

- `enrollment_user = "enroll"`  — one-time enrollment (single-use invite code)
- `git_proxy_user  = "cloud-bastion"` — the ACTUAL dispatch/git-proxy user

There is **NO `cloud-build@` user.** Testing `ssh cloud-build@cloud.superpowers.build`
always returns `Permission denied (publickey)` regardless of enrollment health, because
that account does not exist. Concluding "server-side de-enrollment / need a fresh code"
from that output is WRONG — it's the #1 false-diagnosis trap here.

## Correct verification (do this)

```bash
ssh -i ~/.ssh/cloud-build/id_ed25519 \
    -o UserKnownHostsFile=~/.ssh/cloud-build/known_hosts \
    -o BatchMode=yes -o StrictHostKeyChecking=accept-new \
    cloud-bastion@cloud.superpowers.build
```

- `cloud-bastion: interactive shell is not permitted`  → **SUCCESS.** The key is accepted;
  cloud-bastion is git-proxy-only and forbids interactive shells by design. Enrollment is healthy.
- `Permission denied (publickey)` → genuinely not enrolled / key not trusted.

## Enrollment facts

- The invite code is **single-use** ("This code is single-use") AND expiring — once
  consumed, re-testing it against `enroll@` returns `enroll: invalid or expired token`.
  That does NOT mean enrollment failed; a successful single-use consumption looks identical
  to a later re-test.
- `state.json` (`~/.config/cloud-build/state.json`) stores `enrolled_fp_hash` +
  `last_enrollment_check`. `cb-client-setup.sh` correctly SKIPS re-enroll when the local
  hash matches the current key — do NOT interpret an unchanged `last_enrollment_check` as
  "re-enrollment didn't work"; if `cloud-bastion@` accepts the key, you are enrolled.
- Enrollment is shared across machines (same key on Mac + jeff-ubuntu). If one is enrolled,
  both are. Both were confirmed working 2026-07-21.
- Recover a past invite code from Hermes history: it was pasted in a Slack/gateway message
  ("Cloud Build invite for … Enrollment code: <40-hex>"). Run /history before claiming a
  code was never provided.

## If /super dispatch fails despite auth being fine

`cloud-bastion@` accepting the key means AUTH is fine. A `/super` failure like
`Connection closed by <ip> port 22` / `Could not read from remote repository` during the
`cloud_build_handoff` git push is a SEPARATE problem (git-proxy / ProxyCommand / branch
push), not a de-enrollment — debug the dispatch path, never the enrollment.
