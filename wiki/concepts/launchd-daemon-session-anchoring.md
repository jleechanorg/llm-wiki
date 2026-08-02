---
title: LaunchdDaemonSessionAnchoring
type: concept
tags: [launchd, plist, daemon, hermes, keepalive, processtype, testing-methodology]
sources: [sources/feedback-2026-07-29-launchd-processtype-interactive-for-daemons.md]
last_updated: 2026-07-29
---

For any user-scope `~/Library/LaunchAgents/*.plist` job whose
ProgramArguments runs a daemon-like binary (qdrant, mem0 hooks, an
ollama wrapper, etc.) that must outlive the spawning shell, the launchd
job must be anchored to the user session.

## Rule

```xml
<key>ProcessType</key>
<string>Interactive</string>
```

Pair with:

```xml
<key>KeepAlive</key>
<dict>
  <key>SuccessfulExit</key>
  <false/>
</dict>
<key>ThrottleInterval</key>
<integer>5</integer>
<key>SoftResourceLimits</key>
<dict>
  <key>NumberOfFiles</key>
  <integer>65536</integer>
</dict>
```

## Why "Interactive" and not "Background"

Apple's launchd classifies `ProcessType` based on lifetime intent, not on
what the binary does. The intuitive "Background" label is a trap for
session-anchored daemons: when the spawning shell exits, launchd reaps
Background jobs even when `KeepAlive { SuccessfulExit: false }` is set.
The 2026-07-29 qdrant wedge showed this empirically — qdrant bound 6333
correctly, served 4 PUT/GET requests, then was SIGTERM'd 36 s in by
launchd despite KeepAlive.

## Testing methodology — the real lesson

When verifying a launchd daemon fix, the test is not "healthcheck
returned 200 within 10 seconds." That test passes for both the failing
config (qdrant binds briefly before Background reaping kills it) and
the working config. The correct test is:

1. Boot the daemon under launchd.
2. **Wait 5 minutes** (longer than any plausible Background reaping
   timeout — launchd reaps Background on shell-exit, which on macOS is
   tied to the user session and can take 1–2 minutes in some configs).
3. Re-check: process still alive, port still bound, /healthz still green.
4. If only step 2 was performed, the test is inadequate.

This methodology is the load-bearing piece of the learning — the plist
fix without the methodology would not catch this bug class next time.

## How KeepAlive, ThrottleInterval, and SoftResourceLimits differ

| Key | What it governs | What it does NOT govern |
| --- | --- | --- |
| `KeepAlive { SuccessfulExit: false }` | respawn after a clean exit | does NOT prevent SIGTERM from session reaping |
| `KeepAlive { Crashed: true }` | respawn after abnormal exit | doesn't help if launchd itself sends the SIGTERM |
| `ThrottleInterval: N` | minimum seconds between respawns | nothing about lifetime |
| `SoftResourceLimits.NumberOfFiles: 65536` | raises fd ceiling for RocksDB-style processes | nothing about lifetime |

## Diagnostic recipe (3-step, fast)

If a user-scope `~/Library/LaunchAgents/*.plist` daemon appears to
launch then exit silently within ~60 s:

1. `launchctl print gui/$UID/<label> | grep -E "ProcessType|KeepAlive|execs|runs|last exit"` — confirm Background + no KeepAlive.
2. `tail ~/.hermes/logs/<label>.log` — look for a SIGTERM line ~30 s after bind or for the actix graceful-shutdown pattern.
3. **Edit the plist: change `ProcessType: Background` to `ProcessType: Interactive`, then `launchctl bootout && launchctl bootstrap`.** If `/healthz` returns 200 within 10 s and the child pid stays alive past 5 min, you're done.

## Sister rules (not this concept)

- [[Mem0QdrantDeployment]] — full mem0+qdrant deployment recipe
- [[QdrantLaunchdPlist]] — entity page for `ai.hermes.qdrant.plist` (current shape post-fix)

## See also

- Bead `disk_magician-37u` (RESOLVED 2026-07-29) — original incident
  report with full reasoning chain
- Bead `disk_magician-o5v` (CLOSED) — sidekick mission that produced
  this learning
- Memory `feedback_2026-07-29_launchd_processtype_interactive_for_daemons.md` — load-bearing
  memory entry; the durability layer for the next investigator
