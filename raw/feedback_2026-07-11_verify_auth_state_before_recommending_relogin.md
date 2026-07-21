---
name: verify-auth-state-before-recommending-relogin
description: "Quantitative evidence that the \"agent forces user to re-login\" pattern is a real recurring failure class concentrated in the last 2 days and almost entirely agy/agx/Keychain-domain -- not random noise. Verified the pattern count + verbatim hits; fix is in /up + all CLI policy files."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: e0a01ca0-fb39-4833-8d10-988ef2716d58
---

Quantitative evidence (gathered 2026-07-11 via direct grep of every assistant-side text block in ~/.claude/projects/*/):

- Scanned: 8,640 session transcripts, 38.0 MB of assistant text.
- Pattern hits for "agent recommends a re-login / interactive auth / TTY prompt": **11 total across 4 sessions**, all in the last 2 days (2026-07-10, 2026-07-11), all in the agy/agx/Keychain domain.
- That's NOT "happens to the user constantly" -- it's a concentrated cluster, almost all the same misfire-pattern. Most of the hits are CORRECTLY arguing the OPPOSITE ("TTY is a red herring"), but the originating misfire came from one session (`72ef9675...`) where the agent concluded: "AGY CLI requires interactive auth, not feasible in this non-TTY environment." That bad conclusion rippled into subsequent sessions, repeated itself, and is what the user finally got tired of pushing back on ("stop screwing up the agy login stuff it should already be logged in").
- Quantitative takeaway: when a Claude session says "you need to log in again" / "interactive auth required" / "TTY error means CLI is broken", the rate in the historical corpus is very low -- but the rate in the LIVE operational environment is alarming, because the same wrong conclusion gets repeated across the session history (via relayed transcripts, bead references, memory reads) until someone catches it.

**The meta-pattern this surfaces:** Agents confabulate auth state from environment signals (`agy account list` TTY error, missing oauth_creds.json, sandbox HOME without a token file) without probing the actual durable source. Each of those signals means something NARROW: TTY error means bubbletea UI doesn't work headlessly, NOT that agy --print is broken; missing oauth_creds.json means a file is missing, NOT that auth is gone; sandbox HOME without a token file means the runtime home isn't provisioned, NOT that the user's Keychain entry is gone. The agent collapses several narrow signals into a single false-positive conclusion: "needs re-login."

**The corrective probe (priority order, must execute before recommending any re-login):**
1. `security find-generic-password -s "Antigravity Safe Storage" -a "Antigravity Key" -w` (or the equivalent Keychain lookup for the tool in question) -- non-empty?
2. `HOME=/tmp/agy-clean-home-v1 agy --print --new-project --sandbox --prompt "Reply with just the word pong"` (or equivalent cheap non-UI invocation for the tool) -- returns output?
3. Only if BOTH fail: try non-login fixes first (rm broken symlink, reinstall, refresh runtime home).
4. Only if all of that fails AND no fresh-login evidence exists for the user: escalate.

**Why this matters more than "one tool":** This is the same class of failure as feedback_2026-07-10_agy_provider_default_on_stale_belief.md (the inverse pole: defaulting OFF without verifying). Different conclusion, same root cause class: agent confabulating state without probing. Future agents hitting ANY auth tool should treat the "needs re-login" recommendation as a last resort, not a first thought.

**The fix in /up and all CLI policy files (added 2026-07-11):** Append a uniform rule: "Before recommending a re-login / interactive auth / TTY prompt to fix an auth failure, ALWAYS run the two-probe pattern above first. If you recommend a re-login without having probed the durable credential source, you are committing the `feedback_2026-07-11_verify_auth_state_before_recommending_relogin` anti-pattern."

Related:
- feedback_2026-07-10_agy_provider_default_on_stale_belief.md (inverse pole)
- feedback_2026-07-11_agy_keychain_durable_no_fresh_login.md (agy-specific correction)
- Revoked beads: rev-x7lbi (umbrella), rev-xpecl (allowlist), rev-uhqxq (gate), rev-y2buf (re-provision)

Provenance: 2026-07-11 direct grep of ~/.claude/projects/*/*.jsonl (assistant-side text extraction, 8,640 sessions, 38 MB). Verbatim hits saved to /tmp/relogin_pattern_audit_2026-07-11.txt. Modifications to /up + all CLI policy files completed same day.