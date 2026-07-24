# /super slash-command redirect — Local router → Cloud Build dispatch

**Date:** 2026-07-20 (~18:00 PT)
**Source:** Slack thread `C09GRLXF9GR/p1784573431` + `~/.claude/commands/super.md` (Mac + jeff-ubuntu, scp-synced)

## What changed

The `/super` slash command was redefined on 2026-07-20 13:10 as a transitional "thin GLM-5.2 router via `claudeg`" while the user's `claudeg`/`claudek` model-reachability thread was active. ~1 hour later the user redirected: *"`/super` shouldn't be using claudeg it should be using superpowers cloud"* — and a second redirect on the same day: *"Fix it on your machine and /linux"*.

`~/.claude/commands/super.md` now dispatches `$ARGUMENTS` to the Superpowers Cloud Build box end-to-end via `scripts/preflight-local.sh` + `scripts/lib-client.sh cloud_build_handoff` (one bounded replay) + the follow loop + `cloud_build_land_result`. Function name on the box is **`cloud_build_handoff`** (not `cloud_build_hand_off_run_plan` — fictitious name from a prior session).

`~/.claude/commands/superlight.md` (NEW) preserves the legacy `claudeg` router for one-liners where a full plan + handoff is overkill. Pinned at MD5 `03c1f591f0f8b29f48e409adcdad216b` on both machines.

## What was fixed in the same session

| Symptom | Root cause | Fix |
|---|---|---|
| `Host key verification failed.` on every `ssh cloud.superpowers.build` | Bastion rotated its `ssh-ed25519` host key since the last `last_enrollment_check: 2026-07-16T19:26:34Z`; bundled `assets/cloud-build-client-config-v0.json` has the new `host_key_fingerprint: SHA256:uIogunmqBg/yisJwDP3uHHzJ0ualJ9t2EucfrwjxzaQ` | Re-pinned `~/.ssh/cloud-build/known_hosts` from the bundled canonical config (Mac + jeff-ubuntu). Fingerprint matches `host_key_fingerprint` field — safe, since the script uses the bundled config as the trust anchor (not the live server). |
| `Permission denied (publickey)` after host-key fix | Bastion's authorized_keys no longer recognizes the local `id_ed25519` (public key fingerprint `8cZsH7MRG8TKU+DpmUzn02j1NioYGCii47bUeij6Mt4`) — enrollment database has been pruned since `2026-07-16T19:26:34Z` | NOT auto-fixed by this session. State.json retained (enrolled_fp_hash matches current local key, so `cb-client-setup.sh` won't auto-refresh). **User must supply a fresh enrollment code out-of-band** and pipe it to `printf %s "$code" | bash scripts/cb-client-setup.sh` (line 276 of that script reads it from stdin; bare run aborts with `FATAL: enrollment code cannot be empty`). |
| `/super` on jeff-ubuntu would crash with `state.json MISSING` | jeff-ubuntu was designed not to have the Cloud Build enrollment (the Mac is the only enrolled client; SSH identity + state.json live there) | Added a graceful auto-fallthrough on unenrolled hosts: step 2 of `/super` checks `state.json`, and if missing, prints a one-line `falling through to /superlight` notice and dispatches via `claudeg -p`. Mac keeps the strict `STOP and report` behavior. |

## Sync state (md5-verified identical on both hosts)

| File | Mac | jeff-ubuntu |
|---|---|---|
| `super.md` (8928 B) | md5 `f8ca1dd5350b20b682e05181d1405bcb` | md5 `f8ca1dd5350b20b682e05181d1405bcb` |
| `superlight.md` (3227 B) | md5 `03c1f591f0f8b29f48e409adcdad216b` | md5 `03c1f591f0f8b29f48e409adcdad216b` |
| `~/.ssh/cloud-build/known_hosts` | pinned from bundled config | pinned from bundled config (scp-synced) |
| `~/.config/cloud-build/state.json` | ✅ present | ❌ missing (by design) |

## What still needs the user

`Permission denied (publickey)` from the bastion despite the host-key fix. **Single fix point:** paste the new enrollment code into `printf %s "$code" | bash ~/superpowers-cloud-build-main/skills/cloud-build/scripts/cb-client-setup.sh` — without that, `/super` on the Mac will still abort at step 7 (`scripts/lib-client.sh cloud_build_handoff`) when the bastion rejects the SSH auth. The Linux fallback path (`/superlight`) does NOT have this problem — `claudeg` is fully wired there.

## Distinct from prior turns

This is a separate durable fact from the earlier `[[Cloud-Build-3rd-Execution-Mode]]` ingest (`superpowers-cloud-build-2026-07-20.md`). That source captured what Cloud Build IS; this captures the operational reality of running it from the slash-command layer.

## Entities

* [[Superpowers-Cloud-Build]] (the box, see `cloud-superpowers-build.md`)
* [[Prime-Radiant]] (plugin author)
* [[Slash-Command-Surface]] (cross-cuts: `/super`, `/superlight`, `/sudo`, `/er`, `/af`, etc.)
