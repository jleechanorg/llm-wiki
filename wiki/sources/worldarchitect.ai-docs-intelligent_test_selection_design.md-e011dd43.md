---
title: "Intelligent Test Selection Design"
type: source
tags: [worldarchitect-ai, testing, ci-cd, performance, intelligent-selection]
sources: []
date: 2026-04-07
source_file: raw/intelligent_test_selection_design.md
last_updated: 2026-04-07
---

## Summary
Design document for intelligent test selection in WorldArchitect.AI PRs. The system analyzes git diff to identify changed files and runs only relevant tests, achieving 60-80% test reduction while maintaining safety through mandatory integration test coverage.

## Key Claims
- **Default behavior change**: Intelligent selection becomes default (not opt-in), with `--full` flag to override
- **60-80% test reduction**: For focused changes, skipping irrelevant tests significantly speeds up feedback
- **Safety net requirements**: Always run hook tests, critical integration tests, and directly modified test files
- **CI-robust change detection**: Uses GitHub env vars or fallback to `origin/main...HEAD` diff

## Key Findings

### File Change Detection
- Detects changes in production code, test code, configuration, CI/workflows, and documentation
- Uses `git fetch --no-tags --prune --depth=1` for reliable CI detection
- Falls back to `origin/main...HEAD` when CI env vars unavailable

### Dependency Mapping
| Source File | Related Tests |
|-------------|---------------|
| `main.py` | All `test_main_*.py`, `test_api_*.py`, `test_end2end/*` |
| `llm_service.py` | `test_llm_*.py`, `test_json_*.py`, integration tests |
| `firestore_service.py` | `test_firestore_*.py`, `test_main_*.py` (auth tests) |
| `world_logic.py` | `test_world_*.py`, most integration tests |
| `frontend_v2/*` | `test_v2_*.py`, React-specific tests |

### Critical Files Triggering Full Suite
- `constants.py`, `main.py`, `requirements*.txt`, `requirements*.in`
- `pyproject.toml`, `poetry.lock`, `Pipfile`, `Pipfile.lock`
- `.github/workflows/*.yml`, `Dockerfile`, `Makefile`

## Implementation Strategy

The enhanced `run_tests.sh`:
1. Parses `--full` flag to force complete suite
2. Analyzes changed files via git diff
3. Runs dependency analyzer to select tests
4. Falls back to full suite on selection failure

## Connections
- [[WorldArchitect.AI]] — the platform this test optimization targets
- [[GitHub Actions Auto-Deployment]] — related CI/CD infrastructure
- [[Homepage Latency Optimization Report]] — another performance optimization effort