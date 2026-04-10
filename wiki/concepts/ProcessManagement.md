---
title: "Process Management"
type: concept
tags: [infrastructure, testing, subprocess, process-lifecycle]
sources: []
last_updated: 2026-04-08
---

## Definition
The system for controlling lifecycle operations (start, stop, status) of server processes running on different git branches. Uses subprocess execution and shell scripts to manage background server processes.

## Implementation
- Scripts located in `claude_command_scripts/commands/`
- testserver.sh as primary entry point
- test_server_manager.sh handles actual process operations
- Environment variables for configuration (ports, paths)

## Key Operations
- **start**: Launch server process in background
- **stop**: Terminate running server process
- **status**: Check if server is running, get PID/port
- **list**: Show all active test servers
- **cleanup**: Remove stale processes and port allocations

## Related Concepts
- [[TestserverCommand]] — CLI interface for process management
- [[SubprocessTesting]] — testing approach using mock for process execution
