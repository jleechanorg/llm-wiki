---
name: copy-campaign-dest-default-is-source-user-not-jleechantest-always-pass-dest-email
description: scripts/copy_campaign.py defaults destination to the source user; omitting --dest-email silently copies under the prod source account
metadata: 
  node_type: memory
  type: feedback
  originSessionId: c3c948a5-d372-4f31-88d7-1a9eb5a2f2d6
---

`scripts/copy_campaign.py` does NOT default the destination to `jleechantest@gmail.com`. When `--dest-email`/`--dest-user-id` are omitted, the copy lands under the **SOURCE user** (`scripts/copy_campaign.py:310-311` — `if dest_user_id is None: dest_user_id = source_user_id`). The only `jleechan@gmail.com` constant (`:43-44`) is the default **source** lookup for `--find-by-id`, not the destination.

`--format json` only early-exits (UID lookup, no copy) when **paired with `--dest-email`** — it is nested under `if dest_email is not None:` (`:525-538`). Bare `--format json` (no `--dest-email`) **performs a real copy** under the source user.

Incident (2026-06-07, PR #7268 /repro): running `copy_campaign.py --find-by-id fdpDipUzknuchYPIHtgA --format json` (no `--dest-email`) created stray copy `f8RBcMzaaIdSpyIYcLje` under the **prod source account jleechan@gmail.com** (vnLp2G3m21PJL6kxcuAqmWSOtm73). The correct test copy `DhX4MreqJoxLHUlV59he` came only from the later run WITH `--dest-email jleechantest@gmail.com` (uid 0wf6sCREyLcgynidU5LjyZEfm7D2).

**Why:** The repro skill convention is "copy to jleechantest@", but it realizes that by always passing the flag explicitly — the script has no jleechantest default. Assuming `--format json` would early-exit without the flag is the trap.

**How to apply:** For ANY campaign copy / repro, ALWAYS pass `--dest-email jleechantest@gmail.com`. Never rely on a "default test user." Cleanup tracked rev-akkq4 (delete stray copy); hardening rev-r8zkk (safe-dest default or same-user guard); skill doc fix rev-33enj. Related: [[project_2026-06-07_pr7268_cleanup_followups]].
