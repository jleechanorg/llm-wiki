---
title: Mem0 Environment Fix and PyPI Name Discrepancy
type: reference
date: 2026-05-24
bead: rev-4s58s
---

# Mem0 Environment Fix and PyPI Name Discrepancy

## Context
During Claude agent operations, the orchestrator utilizes git hooks and slash command handlers (such as `~/.claude/hooks/mem0_save.py`) to record persistent long-term memories. These hooks import the `mem0` Python package and store them in a shared Qdrant vector database collection (`openclaw_mem0`).

However, the hooks encountered:
`⚠️ mem0 unavailable (skipped) — mem0 module not installed in current Python env`

## Root Cause & Findings
1. **Missing Dependencies**: The python environment used by the orchestrator at `/Users/jleechan/.local/orch-venv/bin/python3` was missing `mem0ai` and `qdrant-client`.
2. **PyPI Package Name Discrepancy**: The official package name on the PyPI registry is `mem0ai` (no hyphens or underscores). Standard installation attempts using `pip install mem0` or `pip install mem0-ai` result in 404 / package not found errors because PyPI registers `mem0` as absent.
3. **Shared Qdrant Instance**: A shared Qdrant database collection (`openclaw_mem0`) runs locally on the machine, storing more than 31,000 memory points. Connecting successfully requires installing `qdrant-client` along with `mem0ai`.

## Resolution
1. **Targeted Python Environment**: Pinpoint the orchestrator's active python env: `/Users/jleechan/.local/orch-venv/bin/python3`.
2. **Pip Install**: Execute the install command targeting the correct PyPI package names:
   ```bash
   /Users/jleechan/.local/orch-venv/bin/pip install mem0ai qdrant-client
   ```
3. **Verification**:
   - `python3 -c "import mem0; print(mem0.__file__)"` resolves to `/Users/jleechan/.local/orch-venv/lib/python3.13/site-packages/mem0/__init__.py`.
   - `python3 ~/.hermes/scripts/mem0_shared_client.py stats` verifies connection to the collection successfully returning active points count.

## Reusable Patterns
- **Env Detection**: Always query the active python interpreter used by the runner environment before troubleshooting packages.
- **PyPI Name Check**: If `pip install <name>` returns a 404 / Package Not Found error, e.g. for `mem0`, check if the PyPI registry uses a suffix, prefix, or alias (like `mem0ai`).
