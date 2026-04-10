---
title: "Testserver Command"
type: concept
tags: [cli, server-management, infrastructure, branch-testing]
sources: []
last_updated: 2026-04-08
---

## Definition
A CLI command for managing test servers on different git branches. Provides start, stop, status, list, and cleanup actions with automatic port allocation and branch-specific logging.

## Usage
```bash
/testserver help      # Display usage information
/testserver start     # Start server on current branch
/testserver stop      # Stop running server
/testserver status    # Show server status
/testserver list      # List all test servers
/testserver cleanup  # Clean up stale servers
```

## Key Features
- Automatic port allocation for each branch
- Branch-specific logging directories
- Process management (start/stop/status)
- Delegation to test_server_manager.sh for core operations

## Related Concepts
- [[ProcessManagement]] — underlying system for managing server processes
- [[PortAllocation]] — dynamic port assignment for test servers
