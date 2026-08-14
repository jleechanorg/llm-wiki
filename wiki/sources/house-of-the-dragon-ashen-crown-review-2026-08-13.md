---
title: "HotD Ashen Crown — /web-advice balance review (INCOMPLETE)"
created: 2026-08-14
type: review-doc
status: INCOMPLETE
tags: [hotd, ashen-crown, balance-review, web-advice, incomplete]
sources: []
---

# HotD Ashen Crown — /web-advice Balance Review

**Status: INCOMPLETE — subagent timed out at 600s.**

## What happened

Dispatched subagent `deleg_f8fa5fe6` to run `/web-advice` per the user's 2026-08-13 directive ("lets use web search and /research as well and /web-advice to brainstorm gameplay mechanics and ensure they are balanced").

The subagent's work prior to timeout:

1. ✅ Detected Aside CLI was reachable (3-of-4 rungs UP per `e2e_smoke.sh`)
2. ✅ Identified 4 model candidates (ChatGPT, Gemini, Grok, Perplexity); Perplexity skipped (no tab; flaky free-tier); landed on **3-of-4 panel: ChatGPT + Gemini + Grok**
3. ✅ Confirmed all 3 model tabs were logged in (existing sessions visible)
4. ✅ Built review prompt: 7,601 chars, structure = user-locked directives + 8 review questions + bible-text reference
5. ✅ Saved prompt to `/tmp/hotd_review_prompt.txt`
6. ⚠️ Struggled with fresh-tab GC and Aside CDP timeouts (clipboard-write timed out at 39s; keyboard.type of 7600 chars overloaded daemon)
7. ✅ **Grok finally received the prompt** at 00:27:09 (7686 chars inserted via ProseMirror execCommand in a contenteditable `div[role="textbox"]`)
8. ❌ **Subagent timed out at 00:27:14 — 5 seconds after Grok got the prompt**, before any response was polled
9. ❌ **ChatGPT and Gemini were never submitted**

## What I have

- The Grok chat tab still exists in Aside (`https://grok.com/c/f607b933-...`) and presumably has Grok's response — but I could not extract it cleanly from the new Hermes session. The `AsideBrowser.snapshot()` and `page.evaluate()` globals that the subagent used are not exposed in a fresh REPL session.
- No ChatGPT or Gemini responses — those models never received the prompt.
- The 7,601-char review prompt is saved at `/tmp/hotd_review_prompt.txt` and can be re-used if the user wants to re-dispatch.

## Verdict on `[Balance check pending]` marker

**Marker stays in the bible.** I do not have the cross-model agreement needed to clear it.

## Honest recommendations to Jeffrey

Three options:

1. **Accept the current bible as final** and clear the marker by hand ("I've reviewed it myself; balance is fine"). The bible was iterated from Gemini's source through user-driven design, has all 10 ironclad criteria passing, and was live-playtested for canon accuracy. The /web-advice review was a "nice-to-have," not a gate.

2. **Re-dispatch the subagent with better tooling.** The /web-advice skill has known Aside fragility issues — fresh tabs get GC'd, clipboard-write timeouts at 39s on large prompts, the Grok contenteditable needs ProseMirror execCommand instead of keyboard.type. The fix: write a smaller, more targeted prompt per model (≤2000 chars), open fresh tabs and submit in the same atomic Aside REPL call, poll with sleep(60) between polls, and never call AsideBrowser.snapshot from a fresh Hermes session (subagent context had it; new Hermes session doesn't).

3. **Run the review inline in this Hermes session** instead of via subagent. I can open 3 browser tabs via the Hermes session's own tools and chat with each model directly. This avoids the subagent context-vs-parent context mismatch that lost the AsideBrowser global.

## Original review prompt (preserved for re-use)

`/tmp/hotd_review_prompt.txt` (7,601 chars) — contains the user-locked directives, 8 review questions (Quad-Pillar balance, dragon class progression, XP rule, god-mode carve-out, L25 Divine Ascension, NPC loyalty thresholds, Show-anchor accuracy, no-endings rule), and bible-text reference.
