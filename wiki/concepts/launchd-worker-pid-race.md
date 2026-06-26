---
title: "Launchd Worker PID Race"
type: concept
tags: [launchd, pid-file, cli-integration, false-positive, service-management]
date: 2026-06-26
---

# Launchd Worker PID Race

**Definition**: When a launchd plist runs a worker process directly (e.g. `node dist/cli.js _proxy-worker`), the worker never goes through the parent CLI's `start` command, so the PID file is never written by the canonical path. A subsequent `cli start` from a shell session then **overwrites** the PID file with the parent CLI process PID — but the actual worker is a grandchild process with a different PID. Result: `cli status` reports STOPPED while the worker is answering requests on its port.

## Why it matters

This race makes `status` reports unreliable for users who don't distinguish between "started by launchd" and "started by me." Two failure modes:

1. User sees `status: STOPPED` even though the service is healthy → user runs `start` again → conflict or duplicate workers.
2. `stop` sends SIGTERM to the wrong PID (the parent CLI process) → worker keeps running orphaned → port stays bound.

## The pattern in code

```xml
<!-- ~/Library/LaunchAgents/com.example.worker.plist -->
<key>ProgramArguments</key>
<array>
  <string>node</string>
  <string>/path/to/dist/cli.js</string>
  <string>_proxy-worker</string>     <!-- bypasses `start` -->
  <string>--port</string>
  <string>9000</string>
</array>
<key>KeepAlive</key><true/>
<key>RunAtLoad</key><true/>
```

When the user later runs `cli start` from a shell:
- `cli start` writes `String(child.pid)` to the PID file — but `child.pid` is the `node _proxy-worker` process (grandchild of the launchd-spawned `cli`), not the launchd parent
- OR `cli start` sees `lsof -ti:PORT -sTCP:LISTEN` already has the launchd worker, decides "already running," and exits without writing the PID file
- Status then reads the (wrong or missing) PID file and reports STOPPED

## Fix pattern

`status` should fall back to the port listener when the PID-file check fails:

```typescript
if (!running) {
  try {
    const portOwner = execSync("lsof -ti:9000 -sTCP:LISTEN", {stdio: "pipe"})
      .toString().trim().split("\n")[0];
    if (portOwner) {
      pid = parseInt(portOwner, 10);
      running = true;
    }
  } catch { /* nothing on 9000 either */ }
}
```

Worst case: the displayed PID is the listener's actual PID (the worker, not its parent). Best case: the existing PID-file path works unchanged.

## When this class bites

- Any project where launchd plist runs a CLI subcommand directly (`_worker`, `_daemon`, `_serve`) instead of going through `cli start`
- Any project where `status` is the only way users know whether the service is healthy
- Any project where a different consumer of the same code (e.g. tmux pane, IDE plugin) might write to the same PID file

## Related concepts

- [[ServiceDiscrimination]] — same class of false-positive (trusting a derived signal instead of the actual mechanism)
- [[llm_inspector]] — the project where this was discovered and fixed (commit `72fbf44`)