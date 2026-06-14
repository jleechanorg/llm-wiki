---
name: feedback_2026-06-13_claw_always_show_attach_urls
description: "After every /claw dispatch always show ao attach, dashboard, log monitor lines"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7d4e40ac-8020-4acd-887e-3066371819ae
---

After every `/claw` invocation, always output monitoring lines in the reply — never omit them.

**Why:** User explicitly requested this so they always know how to attach, monitor, or kill a worker without asking.

**How to apply:**

- **AO spawn path:**
  ```
  ✅ AO worker spawned: <session-name>
     Attach:    ao attach <session-name>
     Dashboard: ao session ls --project <project>
     Status:    ao status <session-name>
  ```
  Run `ao session ls --project <project>` immediately after spawn to get the session name.

- **Hermes chat fallback (nohup):**
  ```
  ✅ Hermes worker dispatched (PID: <pid>)
     Log:     <logfile>
     Monitor: tail -f <logfile>
     Kill:    kill <pid>
  ```

- **Slack path:**
  ```
  ✅ Dispatched via Slack #claw-dispatch
     Thread: <thread_url>
  ```

These lines are mandatory after every /claw dispatch regardless of path taken.
