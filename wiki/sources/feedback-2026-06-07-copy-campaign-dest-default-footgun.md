---
title: "copy_campaign.py dest default is source user, not jleechantest"
type: source
tags: [copy-campaign, dest-default, footgun, repro-tooling, worldarchitect-ai]
date: 2026-06-07
source_file: raw/feedback_2026-06-07_copy_campaign_dest_default_footgun.md
---

## Summary
scripts/copy_campaign.py does NOT default destination to jleechantest@gmail.com. When --dest-email/--dest-user-id are omitted, the copy lands under the SOURCE user (scripts/copy_campaign.py:310-311 — if dest_user_id is None: dest_user_id = source_user_id). --format json only early-exits (UID lookup, no copy) when paired with --dest-email — it is nested under if dest_email is None. Incident (2026-06-07, PR #7268 /repro): running copy_campaign.py --find-by-id fdpDipUzknuchYPIHtgA --format json (no --dest-email) created stray copy f8RBcMzaaIdSpyIYcLje under the prod source account jleechan@gmail.com (vnLp2G3m21PJL6kxcuAqmWSOtm73).

## Key Claims
- copy_campaign.py does NOT default destination to jleechantest — when --dest-email/--dest-user-id omitted, copy lands under source user (scripts/copy_campaign.py:310-311)
- --format json only early-exits when paired with --dest-email; bare --format json (no --dest-email) performs a real copy under source user
- Incident: stray copy f8RBcMzaaIdSpyIYcLje under prod source account jleechan@gmail.com from bare --format json run; correct test copy DhX4MreqJoxLHUlV59he came from later run WITH --dest-email jleechantest@gmail.com
- Always pass --dest-email jleechantest@gmail.com for any campaign copy / repro; never rely on a 'default test user'

## Connections
- [[project_2026-06-07_pr7268_cleanup_followups]]
- [[CopyCampaignDestDefault]]
- [[ReproToolingFootgun]]
