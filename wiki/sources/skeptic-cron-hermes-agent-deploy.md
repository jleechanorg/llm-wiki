# Skeptic Cron Deployed to Hermes-Agent

Deployed skeptic-cron.yml and green-gate.yml to `jleechanorg/hermes-agent`. Verified E2E auto-merge on PR #11 at 00:23 UTC.

## Key behaviors
- Runs every 30 min on self-hosted runners
- SKEPTIC_NO_VERDICT: skeptic-cron IS the skeptic — evaluates gates 1-6, posts VERDICT: PASS, and merges in same run
- Gate 1 repo-agnostic: excludes "Green Gate", "Skeptic Gate", "Staging Canary Gate" by name
- Gate 3 CR fallback: matches verdict comment patterns for CR incremental stall
- Gate 4 Bugbot: only HIGH/CRITICAL severity where original_commit_id matches PR head SHA or is null
- GitHub mergeable field can be empty string (not just null) — Gate 2 treats as non-passing

## Related
- [[green-gate-ci-pattern]]
- [[ao-worker-idle-not-stuck]]
