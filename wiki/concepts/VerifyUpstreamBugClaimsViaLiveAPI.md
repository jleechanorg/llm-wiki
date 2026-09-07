---
title: "Verify Upstream Bug Claims via Live API, Not Search Summaries"
type: concept
tags: [verification, evidence, github, websearch]
date: 2026-09-06
---

## Definition
When a WebSearch tool returns a prose summary claiming specific GitHub issue
numbers, titles, and quoted bodies exist, that summary text can itself contain
model-generated restatement or error — it is not proof the issues exist as
described. Before telling a user "this is a known upstream bug," re-fetch each
cited issue directly (`gh api repos/<owner>/<repo>/issues/<n>`) and confirm the
title, state, body, and comments actually match what the search summary claimed.

## Why it matters
A search-result summary is itself an LLM-generated synthesis layered on top of
raw search snippets. It can hallucinate plausible-sounding issue numbers, invert
a fix's status (open vs. closed-by-fix vs. closed-by-inactivity-bot), or
misattribute a quote. Only the raw API response is ground truth.

## Procedure
1. WebSearch for the claim (e.g. "`<tool>` `<feature>` not working github issue").
2. Extract every cited issue/PR number and repo from the results.
3. Fetch each one directly: `gh api repos/<owner>/<repo>/issues/<n> --jq '{number,title,state,created_at}'`.
4. For the most load-bearing 2–3 issues, also fetch `.body` and `/comments` to
   confirm the quoted evidence is real and not paraphrased/invented, and to
   check whether the issue was actually *fixed* or merely closed by a stale-bot.
5. Only then present the finding as "confirmed via gh api" rather than "search
   results suggest."

## Applied in
- [[feedback-2026-09-06-fable-model-picker-upstream-bug|Fable /model picker investigation, 2026-09-06]] —
  8 issues cited by WebSearch, all verified to exist with matching titles via
  `gh api`; 3 had full body/comments pulled to confirm the server-side root
  cause and that none were actually fixed (all closed by inactivity-bot).

## Related
- [[ClaudeCodeModelPickerEntitlementGap]]
