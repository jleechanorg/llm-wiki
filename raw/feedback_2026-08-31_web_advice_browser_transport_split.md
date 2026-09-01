---
name: web-advice browser transport split
description: Use the owning chat's browser in app runs and clean headless Chrome in CLI runs.
type: feedback
bead: none (Beads authority degraded)
---

# Web-advice browser transport split

## Context

An external review of WorldArchitect PR #9583 showed that an existing shared
Perplexity tab can contain another task's prompt and response. That output is
not attributable to the requested exact-head review, even when files appear
attached. The app Browser Chrome binding was unavailable, while direct
Playwright launching the installed Chrome headlessly was available.

## Rule

When `/web-advice` runs inside ChatGPT, Codex, Claude, or Aside with an owned
built-in browser, use that browser and an isolated, newly created chat. When
it runs from a coding CLI or Bash, launch an isolated Chrome process through
Playwright in strict headless mode, inject freshly decrypted local cookies,
and never reuse a shared chat tab.

## Required proof

- Authenticate the named vendor account and record the current plan when an
  upload capability is plan-gated.
- Start a clean chat; do not continue an existing conversation.
- Verify every exact packet filename is visibly rendered before sending.
- Accept a result only if it contains a response plus the requested exact head
  SHA and both attachment names.
- Treat mixed-chat state, missing attachment chips, an upgrade dialog, or a
  missing packet echo as a hard failure for that vendor seat.

## Technical direction

The headless runner needs vendor-specific upload strategies. ChatGPT can use
its unambiguous file input; Gemini and Perplexity must open their visible
upload menus, wait for the file chooser, and then verify the displayed chips.
The script report must make auth, plan, upload, send, and response failures
independently diagnosable.

## Verification

On 2026-08-31, a locally launched headless Chrome session showed the
Perplexity `jleechan77861 Pro` entitlement and visibly rendered both
`PR9583_224335_FULL_CODE_FILES.txt` and
`PR9583_224335_BASE_CODE_FILES_AND_DIFF.txt`. A fresh Perplexity chat in the
owning app browser then returned a completed PR #9583 response that echoed the
exact head SHA and both packet names. A shared Aside session later mixed
another PR's conversation, proving why new-chat isolation is mandatory.

## References

- `~/.claude/skills/web-advice/scripts/playwright_cookie_driver.py`
- `~/.claude/skills/web-advice/references/browser-transports.md`
- PR #9583 at head `224335e98a3a13a4ed04d3aa6ab66acfe40cf0b1`
