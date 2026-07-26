---
title: "Usage-signal substring count is invalid — only exact command-tag match works"
type: source
tags: [claude-code, usage-measurement, methodology]
date: 2026-07-12
source_file: raw/feedback_2026-07-12_usage-signal-substring-count-invalid.md
---

## Summary

While prioritizing which of ~60 Claude Code slash commands were worth migrating to the thin-skill pattern, a raw substring count of command names across session history returned 10,000–184,000 "hits" for every command, including ones with zero real usage. The false signal came from Claude Code's own skill-catalog system-reminder, which repeats every registered command/skill name+description in nearly every turn's tool-result. Only the exact `<command-name>/X</command-name>` invocation tag is a reliable usage-frequency proxy.

## Key Claims

- Exact tag match (`<command-name>/X</command-name>`) correctly identified real usage: `harness`(54), `sidekick`(48), `es`(24), `research`(18), `learn`(14).
- Raw substring counting (`content.count("name")`) is dominated by skill-catalog boilerplate, not real invocations — verified by tracing a sample hit back to catalog text.
- One legitimate exception: independent prose evidence (a roadmap doc describing real automation usage of `/fixpr` via the `copilot-fixpr` subagent) can override a 0-hit tag-match result. A raw substring count cannot.

## Connections

- [[FatCommandToThinSkillMigration]] — this measurement fed the migration priority decision.
- [[ClaudeCodeSkillCatalogBoilerplate]] — the noise source responsible for the false signal.
