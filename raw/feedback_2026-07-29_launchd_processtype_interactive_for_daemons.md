---
name: launchd-user-scope-daemon-jobs-need-processtype-interactive
description: "A launchd LaunchAgent marked `ProcessType: Background` is reaped when the spawning shell exits, even with `KeepAlive { SuccessfulExit: false }`. For local daemons (qdrant, mem0 hooks, etc.) use `ProcessType: Interactive`."
metadata: 
  node_type: memory
  type: feedback
  bead: disk_magician-37u (resolved 2026-07-29; backup-cron path still OPEN as follow-up)
  originSessionId: d1c16e37-c03b-4f8d-bf7d-57d09005a2a4
  modified: 2026-07-29T09:16:30.285Z
---

Context: on 2026-07-29 a `/sidekick` mission (`disk_magician-o5v`) recovered
the wedged `ai.hermes.qdrant` launchd job. After (a) `KeepAlive {
SuccessfulExit: false } + ThrottleInterval: 5` was added, qdrant bound 6333
correctly but launchd `SIGTERM`'d the qdrant child 36 s later. `last exit
code = (never exited)` and `immediate reason = speculative` again. The
launchd print had `successful exit => 0` — launchd counted it as a
successful exit even though we said "false".

Root cause: `ProcessType: Background` causes launchd to treat the job as
a transient background helper of the spawning session. When the spawning
shell exits (typical at end-of-session / end-of-script), launchd reaps the
child. **KeepAlive's `SuccessfulExit: false` does not prevent this** — it
only governs respawn after a clean exit code. ProcessType governs the
sibling lifecycle question "should this outlive the session?"

The fix that worked (verified live 2026-07-29 02:01 PDT): change
`ProcessType: Background` to `ProcessType: Interactive` in the plist.
After `launchctl bootout && launchctl bootstrap`, qdrant pid 30212 has
been alive continuously through this write. `/healthz` green,
`/collections` returning both `hermes_mem0` and `mem0migrations`,
`Memory.add()` returns `event: ADD`, `m.search()` returns 20 hits — full
end-to-end mem0 chain recovered.

## Rule (general)

For any user-scope `~/Library/LaunchAgents/*.plist` whose ProgramArguments
runs a daemon-like binary that must outlive the spawning shell:

```
<key>ProcessType</key>
<string>Interactive</string>
```

Apply this even if the daemon would *intuitively* be a "background" job.
Apple's launchd semantics classify ProcessType based on lifetime intent,
not on what the binary does. The intuitive "Background" label is a trap
for session-anchored daemons.

## What KeepAlive actually does (and doesn't)

- `KeepAlive { SuccessfulExit: false }` → launchd will respawn after a
  *clean* exit (code 0). It does NOT prevent SIGTERM from session reaping.
- `KeepAlive { Crashed: true }` → launchd will respawn after abnormal
  exit. Doesn't help if launchd itself is sending the SIGTERM.
- `KeepAlive { AfterInitialDemand: true }` → only respawn if the job
  received any demand since boot. Wrong shape for daemons.
- `ThrottleInterval: N` → minimum seconds between respawns. Useful
  pairing with KeepAlive to avoid respawn storms.
- `SoftResourceLimits.NumberOfFiles: 65536` → raises fd ceiling for
  RocksDB-style processes that hold hundreds of file handles.

What **none of these do** is prevent `ProcessType: Background` reaping.
For that you need `ProcessType: Interactive` (or omit ProcessType
entirely; the default for LaunchAgents is `Interactive` since macOS
Sequoia 15.4 — see changelog).

## Related bead

`disk_magician-37u` was the original incident report. Resolved
2026-07-29 via this fix. The same bead carries an outstanding
follow-up: `ai.hermes.schedule.qdrant-backup.plist` reads from
`~/.hermes/qdrant_storage/` (old path) — its backups will be empty
until the cron path is updated. Sidekick's hard bound forbade the
side-effect fix without explicit human approval; this is the next
caller's note to handle.

## Diagnostic recipe (3-step, fast)

If a user-scope `~/Library/LaunchAgents/*.plist` daemon appears to
launch then exit silently within ~60 s:

1. `launchctl print gui/$UID/<label> | grep -E "ProcessType|KeepAlive|execs|runs|last exit"` — confirm Background + no KeepAlive.
2. `tail ~/.hermes/logs/<label>.log` — look for a SIGTERM line ~30 s after bind or for the actix graceful-shutdown pattern.
3. **Edit the plist: change `ProcessType: Background` to `ProcessType: Interactive`, then `launchctl bootout && launchctl bootstrap`.** If `/healthz` returns 200 within 10 s and the child pid stays alive past 5 min, you're done.

## Why this knowledge was previously missing

Two real defects hid the actual answer:
- KeepAlive is the loud, well-documented mechanism — so when qdrant died
  anyway, the fix felt "obviously" KeepAlive-related, and Background
  reaping was not even a candidate.
- Earlier sessions that "fixed qdrant" via KeepAlive + ThrottleInterval
  didn't actually exercise the post-30-second-time-window because they
  exited the session before launchd reaped the child. The bug was
  masked by the testing methodology, not by the docs.

**Lesson (this is the durable lesson, beyond launchd): when a fix
"works" via a 5-second healthcheck but the service was supposed to be
permanent, the test is not adequate.** Use a 5-minute wait + a probe for
both `process still alive` and `port still bound`.

## See also

- [[QdrantLaunchdPlist]] — entity page (updated 2026-07-29 with the
  ProcessType lesson)
- [[Mem0QdrantDeployment]] — concept page (now needs a "ProcessType
  Interactive" footnote)
- Bead `disk_magician-37u` — original incident report
- Bead `disk_magician-3je` — earlier closed `[DRY-RUN]` log bug
- Bead `disk_magician-yua` — ezgha deploy drift (different scope)
- Memory `feedback_2026-07-29_root_cause_disk_full.md` — same-session
  root-cause taxonomy for disk-full (the 5-producer analysis)
