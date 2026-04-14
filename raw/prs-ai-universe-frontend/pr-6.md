# PR #6: feat: Add comprehensive development and deployment scripts from backend

**Repo:** jleechanorg/ai_universe_frontend
**Merged:** 2025-09-19
**Author:** jleechan2015
**Stats:** +6693/-0 in 29 files

## Summary
Import all utility scripts from the AI Universe backend repository to provide comprehensive development, testing, deployment, and maintenance capabilities for the frontend project.

## Raw Body
## Summary

Import all utility scripts from the AI Universe backend repository to provide comprehensive development, testing, deployment, and maintenance capabilities for the frontend project.

## 🛠 **Script Categories**

### **Core Development Scripts** (5 scripts)
- `claude_mcp.sh` - MCP protocol development utilities (72KB)
- `claude_start.sh` - Claude CLI integration and startup (77KB) 
- `run_local_server.sh` - Local development server management
- `integrate.sh` - Branch integration and conflict resolution (28KB)
- `push.sh` - Git push utilities with branch management

### **Testing & Quality Assurance** (4 scripts)
- `coverage.sh` - Code coverage analysis and reporting (8KB)
- `run_tests_with_coverage.sh` - Comprehensive test execution (9KB)
- `run_lint.sh` - Code quality and linting checks
- `loc.sh` / `loc_simple.sh` - Lines of code analysis

### **Deployment & Infrastructure** (4 scripts)
- `deploy.sh` - Production deployment automation (6KB)
- `setup-github-runner.sh` - CI/CD runner configuration (8KB)
- `setup-secrets.sh` - Secret management for deployments
- `setup-custom-domain.sh` - Custom domain configuration

### **MCP Integration Tools** (4 scripts)
- `aiuniverse-http.sh` - HTTP MCP server utilities
- `aiuniverse-stdio.sh` - STDIO MCP server utilities
- `mcp_stdio_wrapper.js` - MCP protocol wrapper
- `search_ai_universe_mcp.py` - MCP search functionality (10KB)

### **Development Utilities** (6 scripts)
- `add-to-claude.sh` - Claude CLI integration helpers
- `clear-rate-limits.sh` - Rate limit management
- `kill_ai_servers.sh` - AI server process management
- `create_snapshot.sh` - Development snapshot utilities
- `create_worktree.sh` - Git worktree management
- `setup_email.sh` - Email configuration

### **Configuration & Debugging** (5 scripts)
- `demo-config-management.sh` - Configuration management demos
- `debug-unicode.mjs` - Unicode debugging utilities
- `force-config-refresh.mjs` - Configuration refresh tools
- `reset-rate-limits.mjs` - Rat
