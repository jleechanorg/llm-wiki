---
title: "2026-06-13 Learn Skill Bypasses Wiki Ingest"
type: source
tags: ["feedback"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_learn_skill_bypasses_wiki_ingest.md
---

## Summary
/learn skill step 6 caused agents to direct-Write wiki files instead of calling Skill(\

## Key Claims
- `/learn` step 6 instructed the agent to "follow the wiki-ingest workflow"
- with a 6-step manual procedure (copy to raw, create source page, update
- index, append log, update concept/entity, oracle impact). The agent
- treated this as license to write files directly via `Write` / `Edit` /
- When called from `/integrate` in non-llm_wiki worktrees, the agent knew
- the global rule "Never write files directly to wiki/sources/" but

## Connections
- [[karpathy-wiki-pattern-enforcement]]
- [[wiki-ingest-must-be-skill-invocation]]
- [[wikilinks]]
