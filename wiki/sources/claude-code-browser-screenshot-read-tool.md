---
title: "Claude Code Browser Screenshot + Read Tool for UI Verification"
type: source
tags: [claude-code, browser-automation, chrome-superpowers, evidence, ui-testing]
date: 2026-05-02
source_file: ~/llm_wiki/raw/consulting-page-browser-screenshot-20260502.png
---

## Summary

Claude Code can view PNG screenshots directly in conversation via the Read tool, enabling visual verification of browser-rendered pages without leaving the terminal. This works through the `chrome-superpowers` MCP browser tool which saves screenshots to a session cache directory, and the Read tool which renders PNGs as images in the conversation output.

## Key Claims

- The Read tool can display PNG/JPG images when given an absolute file path
- `chrome-superpowers` MCP browser automatically saves screenshots to `~/Library/Caches/superpowers/browser/<date>/session-<id>/<N>-<action>.png` on every browser action (navigate, screenshot, etc.)
- The PNG path is returned in the tool result — no manual capture needed
- Claude Code's Read tool renders images inline when reading a PNG file path
- This enables real-time visual verification of deployed pages, PR preview URLs, or any browser-rendered content

## Browser Workflow

1. **Open browser** — `chrome-superpowers` MCP tool: `show_browser` action
2. **Navigate** — `navigate` action with URL, timeout, viewport settings
3. **Capture** — `screenshot` action saves PNG to session cache, returns path
4. **View** — Read tool with the PNG path renders the image inline in the conversation

## Relevant Commands

```bash
# Chrome-superpowers browser session directory pattern
~/Library/Caches/superpowers/browser/<YYYY-MM-DD>/session-<session_id>/

# Files created per action:
#   <N>-navigate.html   — rendered DOM snapshot
#   <N>-navigate.md     — structured DOM text
#   <N>-navigate.png    — full-page screenshot
#   <N>-navigate-console.txt — browser console log
```

## Connections

- [[chrome-superpowers MCP]] — the browser automation tool providing the screenshot capability
- [[Claude Code MCP Tools]] — list of MCP tools available to Claude Code
- [[PR Preview URL Verification]] — using this technique to verify GCP preview deployments

## Related Source Artifacts

- PNG: `~/llm_wiki/raw/consulting-page-browser-screenshot-20260502.png` — verified consulting page on GCP preview (ai-universe-frontend PR #443)
- Test URL: https://ai-universe-frontend-s2-114133832173.us-central1.run.app/consulting
