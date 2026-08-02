---
title: QdrantLaunchdPlist
type: entity
tags: [launchd, plist, qdrant, hermes, native-binary]
sources: [sources/feedback-2026-07-27-mem0-qdrant-diagnosis-recipe.md]
last_updated: 2026-07-27
---

`~/Library/LaunchAgents/ai.hermes.qdrant.plist` — launchd-managed qdrant daemon
providing the `hermes_mem0` collection on `127.0.0.1:6333`. Replaced the docker-wait
launcher 2026-07-27 after 18 days of persistent failures.

## Current shape (post-fix)

```xml
<key>Label</key><string>ai.hermes.qdrant</string>
<key>ProgramArguments</key>
<array>
  <string>/Users/jleechan/.local/bin/qdrant</string>
  <string>--config-path</string>
  <string>/Users/jleechan/.local/share/qdrant/config/config.yaml</string>
  <string>--disable-telemetry</string>
</array>
<key>ProcessType</key><string>Background</string>
<key>RunAtLoad</key><true/>
<key>WorkingDirectory</key>
<string>/Users/jleechan/.local/share/qdrant/storage</string>
<key>StandardErrorPath</key><string>/Users/jleechan/.hermes/logs/qdrant.err.log</string>
<key>StandardOutPath</key><string>/Users/jleechan/.hermes/logs/qdrant.log</string>
```

## Why the `WorkingDirectory` key matters

macOS launchd Background jobs default to a cwd that can be read-only (no `WorkingDirectory`
explicit → `/var/empty` historically). qdrant falls back to `./snapshots/tmp` for
collection-init work, which crashes with `Read-only file system (os error 30)`. Without
this key the daemon panics on startup despite the binary running forever. The 18 failures
were this exact panic in different wrapping.

## Backups untouched

`ai.hermes.schedule.qdrant-backup.plist` (2am daily, `backup-qdrant-to-dropbox.sh`)
still treats the storage path as a stable dropbox snapshot source and works unchanged.

## See also

- [[Mem0QdrantDeployment]]
- [[Mem0Server]]
