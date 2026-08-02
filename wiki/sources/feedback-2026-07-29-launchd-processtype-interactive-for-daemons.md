---
title: "launchd user-scope daemons need ProcessType: Interactive (2026-07-29)"
type: source
tags: [disk_magician, launchd, plist, daemon, qdrant, processtype, keepalive, hermes]
date: 2026-07-29
source_file: /Users/jleechan/llm_wiki/raw/feedback_2026-07-29_launchd_processtype_interactive_for_daemons.md
---

## Summary

A wedged `ai.hermes.qdrant` launchd job was recovered via the `/sidekick`
mission `disk_magician-o5v`. The deeper fix that worked was changing
`ProcessType: Background` → `ProcessType: Interactive` in the plist. The
intuitive fix (KeepAlive + ThrottleInterval) was applied first but did not
work — launchd's `KeepAlive { SuccessfulExit: false }` does not prevent the
`ProcessType: Background` reaping that SIGTERM'd the qdrant child 36 s
after first bind. After ProcessType: Interactive, qdrant pid 30212 has
been continuously alive through the rest of the session.

## Key Claims

- For user-scope `~/Library/LaunchAgents/*.plist` daemons that must outlive
  the spawning shell, use `ProcessType: Interactive`. Apple's launchd
  classifies ProcessType by lifetime intent, not by what the binary does.
- KeepAlive governs respawn after clean exit; it does NOT prevent
  ProcessType: Background reaping on shell-exit.
- `SoftResourceLimits.NumberOfFiles: 65536` is needed for RocksDB-style
  processes that hold hundreds of fds; the kernel `ulimit -n` ceiling
  (typically 1048576) is fine, but launchd's `SoftResourceLimits` defaults
  to ~256 which is too low.
- Tests that verify a 5-second healthcheck miss this entire class of bug.
  The right test is "still alive 5 minutes later" + "port still bound".

## Key Quotes

> For any user-scope `~/Library/LaunchAgents/*.plist` whose ProgramArguments
> runs a daemon-like binary that must outlive the spawning shell: set
> `ProcessType: Interactive`. The intuitive "Background" label is a trap
> for session-anchored daemons.

> Two real defects hid the actual answer: KeepAlive is the loud,
> well-documented mechanism — so when qdrant died anyway, the fix felt
> "obviously" KeepAlive-related, and Background reaping was not even a
> candidate. Earlier sessions that "fixed qdrant" via KeepAlive +
> ThrottleInterval didn't actually exercise the post-30-second-time-window
> because they exited the session before launchd reaped the child. The
> bug was masked by the testing methodology, not by the docs.

## Connections

- [[QdrantLaunchdPlist]] — entity page (updated 2026-07-29 with the
  ProcessType lesson)
- [[Mem0QdrantDeployment]] — concept page (now needs a "ProcessType
  Interactive" footnote)
- [[Mem0HelperFiles]] — entity page (the migrated mem0 hooks)
- [[Mem0QdrantDiagnosisRecipe]] — sister source page; the 2026-07-27
  diagnosis recipe was about the qdrant binary launcher; this one is
  about the launchd job that holds the binary
- Beads: `disk_magician-37u` (RESOLVED 2026-07-29; backup-cron path
  follow-up still OPEN), `disk_magician-o5v` (CLOSED — sidekick mission
  complete)
