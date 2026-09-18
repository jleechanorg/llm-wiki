# Feedback: Automated Writes Must Never Mutate Primary Human Account

- **Source**: `/Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-09-17_automated_write_to_primary_account_policy_violation.md`
- **Date**: 2026-09-17
- **Category**: Safety Boundaries & Test Account Policies

## Key Invariant
Automated writes (campaigns, gameplay, sharing, settings, repairs) must NEVER authenticate as or mutate `jleechan@gmail.com` (UID `vnLp2G3m21PJL6kxcuAqmWSOtm73`).
Always use dedicated test accounts: `jleechantest@gmail.com` (UID `0wf6sCREyLcgynidU5LjyZEfm7D2`).
A benign or successful outcome (e.g. repairing corrupted database state) does NOT authorize bypassing this ironclad policy. All tools capable of state mutation must fail closed if targeted at the primary human account without explicit manual flags.
