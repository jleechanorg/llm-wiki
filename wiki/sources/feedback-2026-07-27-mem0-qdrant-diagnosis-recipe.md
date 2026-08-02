---
title: "Mem0/Qdrant broken ≠ API key — diagnosis recipe (2026-07-27)"
type: source
tags: [disk_magician, mem0, qdrant, fastembed, launchd, diagnosis-recipe]
date: 2026-07-27
source_file: /Users/jleechan/llm_wiki/raw/feedback_2026-07-27_mem0_qdrant_diagnosis_recipe.md
---

## Summary

On 2026-07-27 the user asked for help because mem0 was always breaking. Root cause was NOT
an API key, NOT Groq, and NOT the embedder switch. It was a launchd launcher problem on
top of a mem0 2.0 kwargs migration. Both fixed in place. This file is a diagnostic recipe
that survives across sessions so the next investigator doesn't mistake service-launch failure
for a client-API problem.

## Key Claims

- The launcher `~/.hermes/scripts/start-qdrant-container.sh` was waiting up to 60s for a
  Docker context that never came — **18 logged failures** between 2026-06-28 and 2026-07-26,
  then `exit 1` to launchd. Fix: swap to native binary path and add `WorkingDirectory`.
- mem0 2.0 silently broke `m.search()` and `m.get_all()` call sites that still used the
  `user_id=` kwarg. Three helpers (`mem0_shared_client.py`, `mem0_recall.py`, `mem0_dedup.py`)
  silently fail because `mem0_save.py` does `pass # Never block` on exceptions. Fixed in place.
- The mandatory 4-step diagnosis recipe (lsof + curl + launchctl print + canonical-error grep)
  must run before any `/learn` capture that mentions `mem0 unavailable`. Time saved: hours
  per failure.
- This is the **second** identical-pattern outage (the previous one was a SKILL.md probing
  OPENAI_API_KEY when mem0 had already switched to Ollama — feedback_2026-06-24-verify-harness-status-before-reporting.md, incident 2026-06-24).

## Key Quotes

> Anti-pattern: collapsing "service can't start" into "API key missing". The wrong fix path
> is to set GROQ_API_KEY or OPENAI_API_KEY, or to comment out the hook entirely.

> Whenever `m = Memory.from_config(MEM0_CONFIG); m.search(...)` raises a `Connection refused`,
> `Qdrant` exception, or any of these specifically mem0 raise types — DO NOT report "mem0
> unavailable" and stop.

## Connections

- [[Mem0Server]] — collection + LLM provider entity
- [[QdrantLaunchdPlist]] — new entity for `ai.hermes.qdrant.plist`
- [[Mem0HelperFiles]] — new entity for the 3 hook helpers
- [[Mem0QdrantDeployment]] — new concept page for the 5-stage recipe
- [[HarnessEngineering]] — parent concept
- [[ProbeTheBlockerBeforeDeclaringBlocked]] — anti-pattern ancestry
- [[DiskMagicianRepo]] — owning repo for the bead carrying this learning (disk_magician-8f4)
- WorldArchitectAi / WorldArchitectAI worktree job launchd layer (parallels the
  qdrant-launchd-vs-docker pattern)
