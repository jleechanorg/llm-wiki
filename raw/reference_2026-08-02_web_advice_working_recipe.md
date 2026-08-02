---
name: web-advice-working-recipe
description: "Proven end-to-end recipe for running /web-advice for real (2026-08-02): aside no-focus-steal, chrome-headless cookie lane for Gemini video upload, clipboard-paste submission, VERDICT scraping, ChatGPT Cloudflare wall"
metadata: 
  node_type: memory
  bead: wc-1svg
  type: reference
  originSessionId: df047295-f9a7-421d-8a38-f5368d7969f5
  modified: 2026-08-02T19:59:40.175Z
---

Working /web-advice run proven 2026-08-02 (3-of-4 real websites; verdicts on iOS gameplay evidence). Companion rule: [[web-advice-hard-fail-no-substitution]] — none of this may be replaced by provider APIs.

**1. Transport bring-up (no focus steal):**
- `aside account list` (daemon probe) → `aside repl "console.log((await listBrowserTabs()).length)"` (window probe).
- `"No last-focused window"` = daemon alive, app windowless → `open -g -a "/Applications/Aside.app"` (`-g` mandatory; plain `open -a` and URL-via-`open` steal focus — user-flagged).
- All tab opens via repl `openTab(url)` (CLI or `mcp__aside-mcp__repl`); CDP opens never change macOS frontmost (verified via osascript before/after).
- Stale MCP session symptom: MCP repl sees 0 tabs / errors while CLI repl works → user runs `/mcp`, or just use `aside repl` in Bash (equivalent).

**2. Auth reality:** Aside = its own Chromium profile; Chrome logins do NOT carry over. 2026-08-02 state: Grok+Perplexity logged in in Aside; ChatGPT+Gemini not. Never log in for the user.

**3. Chrome-headless lane (for sites logged-in only in Chrome; user-approved transport):**
- `browserclaw cookies decrypt --db "$HOME/Library/Application Support/Google/Chrome/Default/Cookies" -o /tmp/ck_X.json --domain-filter '%google.com%'` — safe on the live DB (auto-copies). Merge chatgpt.com+openai.com sets for ChatGPT.
- Python Playwright: `launch(channel="chrome", headless=True)` + `ctx.add_cookies(...)` (coerce `sameSite` to Lax when missing) → real site with real session. **Gemini web: WORKS** (verified: avatar, Flash Extended picker, full chat).
- **ChatGPT: Cloudflare hard-walls headless** ("Just a moment..." even on channel=chrome, 20s+ waits). Do not retry — the fix is logging into chatgpt.com inside Aside.
- Delete `/tmp/ck_*.json` after the run.

**4. Gemini web VIDEO upload (the unique capability — only Gemini web watches mp4):** the file input is dynamic. Click `button[aria-label="Upload & tools"]`, then `input[type="file"]` appears → `set_input_files(video)`; fallback: `page.expect_file_chooser()` around the "Upload files" menu item. Then type prompt, poll the Send button enabled (upload processing gates it), submit, poll `message-content` innerText until stable ×3 (deadline ≥420s — video processing is slow). Working script pattern: `/tmp/gemini_web_review.py` (2026-08-02 session).

**5. Long-prompt submission in aside repl:** `keyboard.type()` at 2000+ chars is minutes-slow. Use clipboard: `await pg.evaluate(t => navigator.clipboard.writeText(t), prompt)` then `Meta+A, Backspace, Meta+V`; verify `innerText().length > 500` BEFORE pressing Enter. Worked on Grok and Perplexity (`[role="textbox"]`).

**6. Verdict scraping:** `snapshot(page)` → `tree.indexOf('VERDICT')` → slice forward. Gemini headless: poll last `message-content`. Screenshot the rendered response in the site UI (profile avatar visible) = the "really the website" proof artifact.

**7. Results calibration (same evidence, 3 models):** Gemini web (watched US-032 video): PARTIALLY PROVEN + found a real new bug (dice values mutate on scrollback → bead wc-0zxj). Grok/Perplexity (methodology): INSUFFICIENT — video alone needs backend-trace triangulation, which the /es bundle separately carries. 3-of-4 satisfies the skill; document the missing model honestly.
