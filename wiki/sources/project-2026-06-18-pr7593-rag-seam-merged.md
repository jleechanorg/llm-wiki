---
title: "PR #7593 RAG Prompt Seam MERGED — original/rag/shadow modes live"
type: source
tags: [rag, worldarchitect, pr-merged, gemini, token-savings, ci-gates]
date: 2026-06-18
source_file: raw/project_2026-06-18_pr7593_rag_seam_merged.md
---

## Summary

PR #7593 `feat(rag): production RAG prompt seam — original/rag/shadow (combined)` was merged on 2026-06-18T18:17:17Z (merge commit `bfb88e1f`). It introduces three selectable RAG modes per user via Firestore `settings.rag_mode`: `original` (full 333,169-char system instruction), `rag` (chunked ~137K, 0.411× ratio, `\n\n[...]\n\n` separator, skips Gemini cache), and `shadow` (serves full prompt, fires parallel RAG build on daemon thread, logs to BQ). Token savings at level-up turn confirmed in BQ `llm_payloads`: 59,545 vs 106,130 prompt tokens = 43.9% reduction. Two CI gate bugs were discovered and documented during the merge process.

## Key Claims

- RAG mode reduces system instruction from 333,169 → 137,010 chars (0.411×) and prompt tokens from 106,130 → 59,545 (43.9% savings) at the level-up turn, confirmed in BQ `llm_payloads` table
- `MEDIA_URL_RE` in `pr_description_gate.py` (line 106) is missing `re.MULTILINE` — GitHub Releases `.gif`/`.mp4` URLs in middle of section content don't match due to `$` anchor; gist URL workaround for Gate 6b
- Skeptic-smoke timing race: if Skeptic runs while MCP Smoke is in-progress, VERDICT has Gate 8=WAIT; fix = dispatch second Skeptic after smoke completes
- New modules `prompt_rag.py` (BM25+embedding rerank, 323L) and `rag_mode.py` (mode resolver, 84L) added — did not inflate `llm_service.py`

## Key Quotes

> "43.9% token savings at level-up turn (59,545 vs 106,130 prompt tokens), confirmed in BQ llm_payloads" — project memory

## Connections

- [[WorldArchitect]] — RAG seam is live on main for this project
- [[RAG]] — three-mode production implementation via BM25+embedding rerank
- [[GreenGate]] — documented two gate bugs: MEDIA_URL_RE regex and Skeptic-smoke race
- [[BQLogging]] — llm_payloads table confirmed token reduction; 98 rows from 3-mode test run
</content>
