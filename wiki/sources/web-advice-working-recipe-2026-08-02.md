---
title: "/web-advice Working Recipe — real-website multi-model review (2026-08-02)"
type: source
tags: [browser-automation, aside, web-advice, evidence-review, playwright, cookies]
date: 2026-08-02
source_file: raw/reference_2026-08-02_web_advice_working_recipe.md
last_updated: 2026-08-02
---

## Summary
First fully-proven end-to-end run of `/web-advice` (multi-model adversarial review through real LLM websites) on 2026-08-02, reviewing worldai_claw iOS gameplay video evidence. Three of four model websites were driven for real — Gemini web (which watched an actual mp4 and found a new state-hydration bug), Grok, and Perplexity — after a user directive made the command hard-fail rather than accept API substitutions. The session produced a durable transport playbook: Aside without focus-stealing, a Chrome-headless cookie-injection lane, and the ChatGPT Cloudflare limitation.

## Key Claims
- `/web-advice` is defined as real browser sessions on the actual websites; provider-API or CLI-model substitutes are banned even with disclosure (user ruling 2026-08-02; HARD-FAIL CONTRACT now in the skill).
- Aside can be operated with zero focus stealing: launch windowless state with `open -g -a "/Applications/Aside.app"`, then open/drive every tab via repl `openTab` (CDP) — frontmost app verified unchanged via osascript.
- Chrome-profile sessions can be carried into a headless real-website session: `browserclaw cookies decrypt` (safe on the live Cookies DB) → Playwright `launch(channel="chrome", headless=True)` + `add_cookies`. Verified working for Gemini web including dynamic-file-input video upload.
- ChatGPT hard-blocks headless Chrome via Cloudflare ("Just a moment…"); the only fix is logging into chatgpt.com inside Aside.
- Long prompts in aside repl must be clipboard-pasted (`navigator.clipboard.writeText` + `Meta+V`), verified by innerText length before Enter — `keyboard.type` is minutes-slow at 2000+ chars.
- Review calibration: Gemini web (watched the video) returned PARTIALLY PROVEN and discovered the dice-mutation-on-scrollback bug (bead wc-0zxj); Grok and Perplexity judged video-alone evidence INSUFFICIENT without backend-trace triangulation.

## Key Quotes
> "lets make /web-advice hard fail and tell me and API path or substitutions are not acceptable" — user directive, 2026-08-02

> "Historical roll card re-renders, displaying mutated numerical outcomes compared to the initial turn execution." — Gemini web, watching US-032_captioned.mp4

## Connections
- [[AsideBrowser]] — primary transport; no-focus-steal operating mode established
- [[browserclaw]] — cookie decrypt/inject lane enabling headless real-website auth
- [[EvidenceStandards]] — video-alone insufficiency verdicts align with the /es triangulation requirement (API transcripts + backend logs)
- [[WorldaiClaw]] — the iOS evidence bundle under review; beads wc-cfdo (US-017 re-capture), wc-0zxj (dice mutation)
