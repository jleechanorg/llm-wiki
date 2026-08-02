---
name: verify-server-worktree-identity-via-lsof
description: "a running local server on a known port is not proof it serves the tree under test — verify its process cwd with lsof before capturing evidence, not just that the port answers"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bc3b0c3b-7695-40fc-916d-e83f512181b9
  modified: 2026-07-26T06:45:10.275Z
---

During /es evidence capture for PR #8602 (worldarchitect.ai, fix/waitlist-failclosed-misleading-ui), a lane pointed at `localhost:8081` assuming that was "the rig" — the port answered, so it was treated as the fix under test. `lsof -p <pid> | grep cwd` revealed that process was actually rooted in `/Users/jleechan/projects/wa_worktree_ratelimit`, a different branch with none of the fix present. Its first "GREEN" run reproduced the same broken behavior as RED.

Instead of rationalizing the contradiction, the lane investigated, discarded the tainted recordings, started an isolated server on `:8092` rooted in the correct worktree (`wa_worktree_waitlistui`), and verified `cwd` via `lsof -p <pid> | grep cwd` before every subsequent capture. Confirmed in the final evidence manifest at `/Users/jleechan/projects/wa_capture_staging/es_8602/MANIFEST.md:1-12,53,221` — every capture line states the verified worktree and port.

**Rule:** On any machine with multiple git worktrees of the same repo (this one routinely has several), a listening port is not evidence of which branch's code is running. Before capturing evidence against a local server:
1. Find the PID bound to the port (`lsof -i :<port>`).
2. Confirm its cwd (`lsof -p <pid> | grep cwd`) matches the worktree/branch under test.
3. Re-verify before every capture session, not just once at startup — a stale server from an earlier lane can still be listening.

This is the same family as [[feedback_2026-07-25_verify_different_layer_than_claim_layer]] (verify a different layer than the claim's own layer) but specific to process/tree identity rather than data layer. Also related: [[project_2026-07-25_waitlist_fabricated_deny_and_ip_ratelimit_lockout]] (same PR #8602 evidence effort).
