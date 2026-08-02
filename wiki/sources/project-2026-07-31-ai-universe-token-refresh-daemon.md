---
title: "AI Universe token refresh daemon (launchd)"
type: source
tags: [auth, mcp, launchd, daemon, firebase, refresh-token, ai-universe, secondo]
date: 2026-07-31
source_file: project_2026-07-31_ai_universe_token_refresh_daemon.md
---

## Summary

Deployed `org.jleechanorg.auth-aiuniverse-token-refresh` launchd agent (2026-07-31) that fires `auth-cli.mjs refresh` every 30 minutes. Keeps the Firebase refreshToken inside its sliding 30-day window so `/secondo` never prompts for browser re-login unless the user changes their Google password — exactly the user's stated requirement.

## Key Claims

- Firebase user-auth tokens cannot be made literally "never expire"; the only viable approach is to keep the refreshToken sliding via a daemon.
- Identity Platform session cookies max at 14 days and have no console override above that.
- Service-account auth is dead-end for AI Universe: live probe with a Google OAuth access token minted from `firebase-adminsdk-fbsvc@ai-universe-b3551.iam.gserviceaccount.com` returned HTTP 401 because the MCP backend uses Firebase Admin SDK `verifyIdToken` (rejects Google OAuth access tokens).
- Wrapper script must source `~/.bashrc` with `set +u` / `set -u` wrap and explicitly guard the `VITE_AI_UNIVERSE_FIREBASE_API_KEY` env var — non-interactive launchd shells can skip bashrc exports.
- Use modern `launchctl bootout` / `bootstrap`, not the deprecated `load` / `unload`.

## Key Quotes

> "Firebase user-auth tokens cannot be made literally 'never expire': idToken: 1 hour (hard security policy, not configurable); refreshToken: ~30 days sliding (rotated on every use, invalidated on password change / sign-out-everywhere / account disable)."

> "The only way the chain breaks is: Mac off for 30+ days, or user changes Google password, or admin revokes sessions — all of which require explicit human action and match the user's 'never expire unless I change Google password' requirement."

## Connections

- [[AIUniverseMCP]] — the service whose auth this daemon manages
- [[FirebaseAuthPolicy]] — idToken 1h / refreshToken 30d sliding limits
- [[IdentityPlatform]] — session cookies max 14 days (no longer option)
- [[LaunchDSkillProtocol]] — clean re-install via `bootout` + `bootstrap`
- [[AuthCLI]] — the script the daemon invokes
- [[MemoryEntry feedback_2026-07-31_ai_universe_mcp_render_to_cloudrun_migration]] — same session, same auth-cli.mjs, same root-cause-first probe pattern
- [[Bead rev-eboni]] — closed as completed for AI Universe daemon; WorldAI follow-up remains