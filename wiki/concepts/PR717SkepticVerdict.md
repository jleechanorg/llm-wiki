---
title: "PR #717 Skeptic Verdict"
type: concept
tags: [skeptic, gate-failure, bash-coverage, agent-orchestrator]
date: 2026-06-23
---

# PR #717 Skeptic Verdict

The Skeptic verdict on PR #717 (single-orchestrator + browser-open guards)
that identified three legitimate Gate 7 findings:

1. **No automated test coverage for the bash script migration** — the single-orchestrator
   migration in `scripts/ao-health.sh` was verified only by manual
   `bash scripts/ao-health.sh` output. No bats, no hand-rolled harness, no
   shell test.
2. **Orphan sweep uses brittle `pgrep -f "ao start"` literal** — the actual
   orchestrator cmdline is `node <dist>/index.js start <project>`, which
   doesn't contain the literal "ao start" string.
3. **Shell-quoting injection vector in `start-all.sh` line 130** — `$project`
   was interpolated unescaped into a `python3 -c "..."` argument.

## Resolution
All three followups landed in PR #718 ([#718](https://github.com/jleechanorg/agent-orchestrator/pull/718), commit `5ebd4cc2`):

1. [[PR718BashTestSuite]] — 33-check test harness
2. Hardened `pgrep -f` pattern to `start[[:space:]][a-zA-Z0-9_.-]+([[:space:]]|$)`
3. Replaced `python3 -c "..."` with `python3 - "$VAR" <<'PYEOF'` heredoc + argv

## See also
- [[ArgvHeredocFixPattern]]
- [[TestableBashPattern]]
