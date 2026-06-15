---
name: claw-slack-vs-gateway-dispatch
description: /claw must use Slack dispatch even when :8642 gateway HTTP is down — they are independent transports
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 9cb0a4f4-d2f7-4033-96aa-909ce5c4a2b2
---

The /claw skill defines Slack `#claw-dispatch` (channel `C0B9W8D609M`) as the primary async dispatch path. Hermes receives Slack messages via Socket Mode, which is **independent** of the HTTP gateway at `:8642`.

**Wrong behavior (2026-06-15):** When `:8642` health check failed, I exited the dispatch flow and went directly to `ao spawn` — bypassing Slack entirely.

**Correct behavior:** Gateway `:8642` being down should produce a warning, not an exit. The Slack dispatch step should still run. Only if Slack also fails should `ao spawn` be used as a last-resort fallback.

**Why:** The `:8642` HTTP endpoint and Hermes Socket Mode are separate processes. The gateway daemon can crash while Socket Mode remains alive. Hard-exiting on HTTP health-check failure silently breaks Slack dispatch even when Hermes is fully operational.

**How to apply:** When executing `/claw`, after a gateway health-check failure:
1. Print "⚠️ Hermes :8642 unreachable — attempting Slack dispatch anyway (Socket Mode may still be live)"
2. Proceed to post to `#claw-dispatch` via xoxp token
3. Only fall back to `ao spawn` if the Slack post also fails

**Skill to update:** `~/.claude/skills/claw-dispatch/SKILL.md` — change the hard `exit 1` on `:8642` failure to a warning + continue.

**References:** 2026-06-14/15 session — wa-2358 was spawned via direct `ao spawn` instead of Slack dispatch because gateway was down.
