---
id: feat-mcp-native-google-sso-auth
type: task
priority: 2
status: open
labels: [auth, mcp, future]
---

# feat(auth): MCP-native Google SSO auth flow (no browser required)

## Problem

Currently the "one-time setup" for MCP access still requires a browser:
1. User opens the web UI at the GCP URL
2. Signs in via Firebase/Google OAuth
3. Generates a `worldai_` personal API key
4. Pastes the key into their Claude Desktop config

Step 1–3 requires a browser session. Power users and CI agents can't bootstrap
auth without one.

## Goal

Allow a user to authenticate through MCP itself — no browser required.
Pattern: the `ai-universe-backend-dev` server does Google SSO via a device-flow
or PKCE redirect that can be initiated from a CLI/MCP session.

## Proposed Approach

Device Authorization Grant (RFC 8628 — "device flow"):
1. User calls an MCP tool: `authenticate` or `login`
2. Server returns a short-lived `device_code` + verification URL
3. User visits the URL in any browser, approves Google SSO once
4. MCP tool polls until approval → issues `worldai_` personal key
5. Key is returned to the MCP session; user stores it in config

This way the MCP session itself drives the auth flow.
The browser step is optional (just open the URL on any device, including phone).

## Acceptance Criteria

- `mcp__worldai__authenticate` tool triggers device flow
- Returns verification_url + expires_in
- Polls and returns `worldai_` token on approval
- Token stored in Firestore (same path as `POST /api/settings/personal-access-token`)
- Works from Claude Desktop MCP config with no prior web session

## Notes

- **Deferred** — current personal-key flow (web UI once) is acceptable for now
- Blocked on: deciding which OAuth provider handles device flow (Firebase doesn't
  natively; may need Google Identity Platform device flow or a lightweight PKCE proxy)
- Related: PR #5879 (personal API key system), ai-universe-backend-dev Google SSO impl

## References

- RFC 8628: OAuth 2.0 Device Authorization Grant
- ai-universe-backend-dev server Google SSO implementation (for pattern reference)
