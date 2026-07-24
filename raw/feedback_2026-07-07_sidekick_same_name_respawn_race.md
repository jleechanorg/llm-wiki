---
name: sidekick-same-name-respawn-race
description: "sending a shutdown_request to a sidekick then immediately spawning a new mission under the SAME teammate name can race with the pending shutdown, producing two concurrent workers that clobber shared scratch files"
metadata: 
  node_type: memory
  type: feedback
  bead: "rev-3vv8h, rev-ux16z"
  originSessionId: ed376cb6-f347-4237-a510-b404c88d46f0
---

**What happened:** closed out a sidekick mission (MCP overhead fix) by sending it a `shutdown_request`. Shortly after, spawned a brand-new, unrelated mission (2-week token usage audit) reusing the literal teammate `name: "sidekick"`. The spawn tool returned the SAME underlying `agent_id`/session as the just-shut-down teammate (`sidekick@session-739ab145`), meaning the name is tied to a reusable slot/pane, not a fresh isolated process per spawn. The shutdown approval arrived asynchronously later, well after the new mission's STATE.md had already been written — creating a race where it was genuinely ambiguous whether the "old" or "new" work was actually running.

**Symptom:** STATE.md for the new mission showed no progress for a while (suspicious), so respawned again under a distinct name (`token-audit-sidekick`) out of caution. It turned out BOTH the original "sidekick" (which had NOT actually died — it kept working the old mission's leftover mailbox and picked up the new task too) and the new `token-audit-sidekick` ran the SAME mining mission concurrently, both writing to the same shared scratch files (`mac_mining.json`, `jeffubuntu_mining.json` under `/tmp/claude-harness/sidekick/token-usage-2wk-audit/`).

**Why it didn't cause silent data corruption this time:** `token-audit-sidekick`'s synthesis step happened to run its own careful in-window filtering (deriving 32.59B from `per_day` buckets) rather than trusting a single pre-computed grand-total field, so when it read whatever was on disk at synthesis time, the derived number was verifiably reproducible after the fact (independently re-summed `per_day` >= 2026-06-24 → matched exactly, 32,593,744,507). Also, the duplicate "sidekick" instance self-detected the collision (via interleaved Progress Log entries in the shared STATE.md) and voluntarily stood down rather than also writing a competing REPORT.md. This was lucky self-correction, not a structural guarantee — a less careful duplicate write easily could have silently clobbered a partially-written JSON mid-append.

**Root cause:** no live-lock or namespaced output path for concurrent sidekick spawns. Two sidekicks working the same STATE.md/scratch-dir path have no mechanism to detect each other except by chance (both happened to append distinguishable Progress Log entries with different names).

**Fix needed (not yet implemented, tracked in beads):**
- `rev-3vv8h` — the collision itself as a discovered gap
- `rev-ux16z` — filed by the duplicate "sidekick" instance itself: needs a live-lock (e.g. a PID/name lockfile checked before a sidekick writes to a shared mining-output path) + namespaced output paths per spawn attempt (e.g. suffix scratch files with the teammate name, merge results in a final synthesis step) so concurrent spawns under retry/caution scenarios fail safe instead of racing.

**How to apply:** when a `shutdown_request` is sent to a named teammate and you need to start genuinely new work soon after, default to a DISTINCT teammate name for the new mission rather than reusing the old one, until the shutdown is confirmed via an explicit `shutdown_approved` message — reusing the name before confirmation risks exactly this race. If forced to reuse a name (e.g. mission continuity), verify liveness first (`SendMessage` and wait for a reply, or check for STATE.md progress) before assuming the old instance is gone.
