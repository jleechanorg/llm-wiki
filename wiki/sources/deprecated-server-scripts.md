---
title: "Deprecated Server Scripts"
type: source
tags: [server-management, test-automation, deprecated, migration]
source_file: "raw/worldarchitect.ai-deprecated_servers.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Documentation of deprecated server scripts (run_test_server.sh, run_local_server.sh, tools/localserver.sh) that were replaced by the unified test_server_manager.sh and /testserver command. The new system provides multi-branch support, automatic port allocation, and integration with /push and /integrate commands.

## Key Claims
- **run_test_server.sh**: Replaced by test_server_manager.sh + /testserver command — had issues with single server only, no branch isolation, port conflicts
- **run_local_server.sh**: Replaced by test_server_manager.sh with port 5005 allocation — had hardcoded port and no multi-branch support
- **tools/localserver.sh**: Consolidated into test_server_manager.sh — duplicated functionality
- **New System Benefits**: Multi-branch support, automatic port allocation (8081-8090 range), PID tracking with proper cleanup, branch-specific logging
- **Integration Ready**: Works with /push and /integrate commands, status monitoring via /testserver list/status

## Key Commands

```bash
# OLD WAY
./run_test_server.sh start
./run_local_server.sh
./tools/localserver.sh start

# NEW WAY
./claude_command_scripts/commands/testserver.sh start
# or directly:
./test_server_manager.sh start
```

## New System Features

- `/testserver start [branch]` - Start server for branch
- `/testserver stop [branch]` - Stop server for branch  
- `/testserver list` - Show all running servers
- `/testserver status` - Show current branch status
- `/testserver cleanup` - Stop all servers

## Connections
- [[TestServerManager]] — the unified replacement system
- [[TestServerCommand]] — /testserver slash command
