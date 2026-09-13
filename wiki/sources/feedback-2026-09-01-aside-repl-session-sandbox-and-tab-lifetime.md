---
title: "aside repl session sandbox and tab lifetime (+ 2026-09-12 vendor-paste addendum)"
type: source
tags: [web-advice, aside, browser-automation, tooling]
date: 2026-09-01
source_file: raw/feedback_2026-09-01_aside_repl_session_sandbox_and_tab_lifetime.md
---

## Summary

Two independent findings about `aside repl` browser automation, gathered 2026-09-01 and extended 2026-09-12. Original: file paths outside the invocation's session directory are rejected, and browser tabs close when the `aside repl` process exits — so any multi-step vendor flow (open → attach files → prompt → submit → wait → capture) must run in a single invocation. Addendum: using the `aside` CLI directly (not the `mcp__aside-mcp__repl` tool, which stayed pinned to a signed-out account), `attachBrowserTab` to a tab from a *prior* invocation times out ~33s reliably; `~/.aside/uploads/<name>/` (unlike the stricter per-invocation session dir) does accept pre-staged host files; and the three reviewed vendors diverge sharply on how they accept large (50-70KB) pasted/injected text — Gemini works via clipboard paste, ChatGPT/Perplexity's composer paste silently no-ops and DOM-injection didn't reliably submit either, and typing that much text via synthetic keystrokes crashed the Aside daemon.

## Key Claims

- Tab lifetime = invocation lifetime for `aside repl`; do the entire flow in one script.
- `~/.aside/uploads/<subdir>/` accepts pre-staged files (contradicts the original 2026-09-01 finding that no host path works — likely a different, less-strict sandbox than `~/.aside/u/0/sessions/<random>`).
- `attachBrowserTab(targetId)` from a prior invocation → `CDP command timeout: Page.enable` (~33s), essentially always; use `openTab` fresh instead.
- Reading a vendor's true full response requires `page.evaluate(() => document.querySelectorAll('[data-message-author-role]')...)` (or the equivalent), not the accessibility `snapshot()` tree, which truncates long text nodes.
- Gemini accepts a Meta+V clipboard paste of large text reliably; ChatGPT and Perplexity do not, and neither a clipboard paste nor a DOM-injection workaround produced a real submitted response for those two vendors in this session.

## Key Quotes

> "budget one working seat (Gemini) as the realistic default for large-packet /wa reviews in this environment; treat ChatGPT/Perplexity as a bonus... disclose the coverage gap rather than burning more retries"

## Connections

- [[web-advice]] — the skill/workflow this constrains
- [[twodot-diff-pollutes-review-packets]] — same review session, different bug class
- [[rtk-diff-truncation]] — same review session, tooling-fragility theme
