---
name: agy-keychain-durable-no-fresh-login
description: agy CLI auth is durable in macOS Keychain; never recommend an interactive TTY login before verifying Keychain + a clean HOME actually fails -- live verified 2026-07-11
metadata: 
  node_type: memory
  type: feedback
  related: feedback_2026-07-10_agy_provider_default_on_stale_belief.md
  originSessionId: e0a01ca0-fb39-4833-8d10-988ef2716d58
---

Do NOT recommend "run interactive agy login" or treat a TTY error as proof of broken agy auth before verifying both (1) the live Keychain credential AND (2) a clean-HOME agy --print probe. The user's mental model is correct: their agy login is durable (Keychain-backed) and should not need re-auth. Verified live on this machine 2026-07-11:
- `security find-generic-password -s "Antigravity Safe Storage" -a "Antigravity Key" -w` returns a non-empty token string (prefix `tUMw343RdbqsSwC3EYPlmQ==`).
- `HOME=/tmp/agy-clean-home-v1 agy --print --new-project --sandbox --prompt "Reply with just the word pong"` returned the model output `pong` -- real LLM response, no TTY, no login, no security dialog. This is the load-bearing test: same invocation that failed earlier today with "Authentication required" returned model text after the file-side cleanup (rm + install.sh).
- The earlier failure (`agy_provider: agy authentication required or timed out`) was caused by a **broken self-referential symlink at `~/.gemini/oauth_creds.json`** (file: -> same path; "Too many levels of symbolic links"). The CLI's `agy --print` path does NOT consult that file -- it reads from Keychain -- so the broken symlink alone cannot break `agy --print`. The CLI failure earlier today was from a *different* code path (the worldarchitect provider's dispatch) that was looking for a valid `oauth_creds.json` in the runtime HOME; once the file was removed, `_has_headless_agy_auth` fell through to ANTIGRAVITY_TOKEN (env) and Keychain (priority order per `mvp_site/llm_providers/provider_gateway.py:43-65`).

**Why this matters / the persistent agent mistake:** This is the OPPOSITE pole of the related note feedback_2026-07-10_agy_provider_default_on_stale_belief.md. That note captured an over-correction in the "default OFF" direction (agent set `AGY_PROVIDER_ENABLED=false` on every run, never verified, based on a stale TTY/auth belief). THIS note captures the over-correction in the "needs login" direction (agent assumes the fix for any agy auth failure is "run an interactive `agy` login", never verifies Keychain first). Both are the same class: **confabulating auth state instead of probing it**. Both have happened in this exact session. The 2026-07-11 UPDATE on the related note (saying "TTY/auth IS a real blocker") is itself now superseded by this live verification.

**The two specific TTY traps to avoid:**
1. `agy account list` (or any other bubbletea UI command) DOES trigger SecurityAgent/`/dev/tty` failures headlessly -- but that is unrelated to whether `agy --print` works. Treating a `agy account list` TTY error as proof that `agy --print` is broken is the confabulation.
2. A long-lived interactive login creates a **new** Keychain entry that overwrites the durable one. Pointing the user at "do another `agy` login" can in the worst case reset their Keychain credential -- always check Keychain first and ONLY recommend the manual OAuth flow if the Keychain entry is genuinely missing or `agy --print` returns no output AND a clean-HOME probe also returns no output.

**Corrective rule for future agents (the operational test, in priority order):**
1. `security find-generic-password -s "Antigravity Safe Storage" -a "Antigravity Key" -w` -- non-empty? If yes, Keychain is healthy.
2. `HOME=/tmp/agy-clean-home-v1 agy --print --new-project --sandbox --prompt "Reply with just the word pong"` -- returns a model response? If yes, agy CLI is fully functional headlessly.
3. Only if BOTH fail should the agent propose an interactive re-login, AND should first try the cheap non-login fixes: `rm ~/.gemini/oauth_creds.json` (the dangling-symlink class), `mvp_site/install.sh --runtime-home <durable>` (re-provisions with the 9585553a58 symlink guard, now part of PR #8334), `source <runtime-home>/worldai-agy.env`. Re-probe. Only if all of those still fail, escalate to "needs interactive login".
4. The user's interactive auth state is durable. The fix for broken install.sh / broken runtime symlinks is `rm + install.sh`, not a fresh login.

**How to apply:** any future session that frames agy auth as "needs a fresh TTY login" should re-read this note and verify the two probes above before recommending that path. Any future session that frames agy auth as "Keychain-prompt is the failure mode" should re-read feedback_2026-07-10_agy_provider_default_on_stale_belief.md (the inverse trap) AND THIS NOTE -- the failure class is "agent confabulated state without probing", regardless of which direction the confabulation goes.

**Related:**
- feedback_2026-07-10_agy_provider_default_on_stale_belief.md (inverse trap -- defaulting agy OFF without verifying)
- bead rev-y2buf (this session's "interactive agy login" framing, closed after this evidence)
- bead rev-9ce1b (the install.sh symlink guard landing via PR #8334 prevents the symptom class that triggered the false login claim)
- bead rev-an94i (root cause of the broken symlink in the first place)

**Provenance:** /Users/jleechan/Documents/agy.txt (user-provided notes); live verification on the user's Mac 2026-07-11; parallel-agent investigation dispatched same day; the user explicitly told this session "stop screwing up the agy login stuff it should already be logged in" and "I shouldnt need to login again for hte millionth time" -- these statements are correct, not cranky.