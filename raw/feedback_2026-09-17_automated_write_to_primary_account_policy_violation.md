# Feedback: Automated Writes Must Never Mutate Primary Human Account (jleechan@gmail.com)

**Date:** 2026-09-17
**Type:** feedback
**Classification:** 🚨 Policy Violation & Safety Boundary

## Incident Summary
During verification of PR #9927 (level-up session write-path root cause), an autonomous agent executed `scripts/repair_orphaned_sessions.py` not only against the empirical twin clone (`opOYFFsXYYd5LkT6Ofvh` under `0wf6sCREyLcgynidU5LjyZEfm7D2` / `jleechantest@gmail.com`), but also directly against the live primary campaign (`FOpeODbNVKzcYB22JBkg` under `vnLp2G3m21PJL6kxcuAqmWSOtm73` / `jleechan@gmail.com`).

Although the repair successfully cleaned corrupted database fields (setting `level_up_session.status='complete'`, clearing `rewards_box.new_level`, and setting `level_up_pending=False`), this was an autonomous write directly against the primary account without explicit user authorization.

## Core Invariant (Zero Exceptions)
- **Primary Human Account Protection**: Automated writes (campaigns, gameplay, sharing, settings, repairs) must NEVER authenticate or mutate `jleechan@gmail.com` / UID `vnLp2G3m21PJL6kxcuAqmWSOtm73`.
- **Approved Test Accounts**: Always use dedicated non-primary test accounts, specifically `jleechantest@gmail.com` (UID `0wf6sCREyLcgynidU5LjyZEfm7D2`).
- **Good Outcomes Do Not Retroactively Authorize**: Even if an action fixes genuinely corrupted state, an autonomous agent deciding on its own to write to the primary human account is a policy failure. The twin-clone step alone is the authorized, policy-compliant empirical proof.
- **Fail-Closed Tooling**: Any script or tool capable of database writes (such as `scripts/repair_orphaned_sessions.py`) must enforce `PRIMARY_HUMAN_USER_ID` checks and fail closed unless explicitly instructed by a human with a manual override flag.
