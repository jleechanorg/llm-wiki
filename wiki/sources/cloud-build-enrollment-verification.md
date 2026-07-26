---
title: "Cloud Build (/super) enrollment verification — the cloud-bastion@ trap"
type: source
tags: [cloud-build, superpowers, super, ssh, enrollment, verification, debugging-trap]
date: 2026-07-21
source_file: ../raw/cloud-build-enrollment-verification.md
---

## Summary
Verifying whether the Superpowers Cloud Build box (`cloud.superpowers.build`, used by
`/super` for remote coding) trusts this machine's key MUST be done by ssh-ing as
`cloud-bastion@` (the git-proxy user) — NOT `cloud-build@`, which does not exist and always
returns `Permission denied (publickey)`. Testing the nonexistent user is the #1
false-diagnosis trap: it looks like "server-side de-enrollment / need a fresh invite code"
when enrollment is actually healthy. A whole 2026-07-21 debugging session was lost to this.

## Key Claims
- The protocol has exactly two users (`cloud-build-client-config-v0.json`):
  `enrollment_user = "enroll"` (one-time, single-use code) and
  `git_proxy_user = "cloud-bastion"` (actual dispatch). There is NO `cloud-build@` user.
- Correct health check: `ssh cloud-bastion@cloud.superpowers.build` →
  `cloud-bastion: interactive shell is not permitted` = **SUCCESS** (key accepted,
  git-proxy-only user forbids shells by design). `Permission denied (publickey)` = genuinely
  not enrolled.
- Invite codes are single-use AND expiring; a consumed code re-tested against `enroll@`
  returns `invalid or expired token` — this does NOT mean enrollment failed.
- `cb-client-setup.sh` correctly skips re-enroll when local `state.json` `enrolled_fp_hash`
  matches the current key; an unchanged `last_enrollment_check` is NOT evidence of failure.
- Enrollment is shared across Mac + jeff-ubuntu (same key); if one is enrolled, both are.
- A `/super` dispatch failure (`Connection closed by <ip> port 22` during the git-proxy
  push) when `cloud-bastion@` accepts the key is a SEPARATE dispatch-path bug, not
  de-enrollment.

## Key Quotes
> "cloud-bastion: interactive shell is not permitted" — the SUCCESS response; means the key is accepted.
> "This code is single-use." — Cloud Build invite codes; consumption looks like later expiry.

## Connections
- [[disk_magician]] — the /super work this session was landing (state-repo PRs) before the enrollment misdiagnosis.
- [[jeffrey-oracle]] — operational verification discipline: test the right endpoint/user before concluding an auth failure.

## Dispatch discipline (from gist 4df2938c "Cloud Build box confusion", 2026-07-20)
- The box runs **GLM-5.2 via its own internal proxy (10.0.100.1:65500)** — NOT OpenRouter. A local `claudeg`/`/superlight` `402 credit_exhausted` says NOTHING about the box.
- The **heartbeat goes stale (>240s) DURING long LLM operations** — the box keeps working. NEVER abort a run on heartbeat-stale.
- Correct follow-loop: poll `cloud_build_fetch_status` (not heartbeat) → read `tasks_completed`/`head_sha` from the `cloud/status` ref → when `head_sha` advances, call `cloud_build_land_result` to fetch the box's commit from the run-scoped git URL (the box's push-back doesn't always self-complete).
- "run identity conflict" / git-push failures during handoff = the **git-secret guard** rejecting a repo whose history has secret-bearing commits, NOT a bastion bug. Fix = orphan-snapshot handoff (git archive → fresh 2-commit repo → push a throwaway `private/*` branch → guard scans only the clean range → PASS).
- `/super` ALWAYS dispatches to the real box; local-subagent / claudeg / OpenRouter fallbacks were REMOVED from `~/.claude/commands/super.md` (both machines, 2026-07-20). Falling back is a silent-substitution method-fidelity violation.
- Proven working runs: cb-wa-8353 (2026-07-19), cb-wa-lu3-20260721011459-e71e87 (2026-07-20).
