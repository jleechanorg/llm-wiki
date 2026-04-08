# Wiki Index

This file is maintained by the LLM. Updated on every ingest.

## Overview
- [Overview](overview.md) — living synthesis across all sources

## Sources
- [MCP Server Installation Guide](sources/worldarchitect.ai-scripts-mcp_setup.md-d8bf98ae.md) — global installation for Claude/Codex with 15+ servers, copy to new repo workflow
- [Ubuntu Dual Boot System Information](sources/worldarchitect.ai-docs-ubuntu-dual-boot-pc-specs.md-a5e54cc2.md) — Intel i9-13900K + 64GB RAM + RTX 4090
- [Beads CLI Command Reference](sources/beads-docs-cli_reference.md-b47a2629.md) — comprehensive command reference for bd CLI v0.21.0+ covering issue management, atomic operations, and state management
- [Error Handling Guidelines](sources/beads-docs-error_handling.md-8a5959dc.md) — three patterns for Go error handling: Exit Immediately, Warn and Continue, Silent Ignore
- [/contexte Command Universal Composition Fix](sources/worldarchitect.ai-docs-contexte-universal-composition-fix.md-c1fdb0c3.md) — fixed /contexte to use direct implementation instead of attempting to invoke built-in /context
- [PATTERNS.md - Living Document of Observed Preferences](sources/worldarchitect.ai-docs-patterns.md-135aa57f.md) — implicit patterns from GitHub history analysis with confidence levels (60-100%)
- [Core Application Code Breakdown](sources/worldarchitect.ai-docs-core_application_code_breakdown.md-40b3cdff.md) — 29,994 production lines across 9 runtime areas: API gateway, gameplay orchestration, AI pipeline, validation, persistence, diagnostics, mocks, testing, frontend
- [Orchestration System Test Summary](sources/worldarchitect.ai-docs-orchestration_test_summary.md-be980261.md) — dynamic agent creation working, 8 agents created in isolated git worktrees with Gemini integration
- [CLAUDE.md Compression Analysis - Proof of Content Preservation](sources/worldarchitect.ai-docs-compression_proof.md-6a418499.md) — 74% compression (811→213 lines) with zero content loss proof
- [Differentiated Linting Workflows](sources/worldarchitect.ai-docs-workflow_differentiation.md-9945d804.md) — `/push` quality gate (lint before push, blocking) vs `/pushl` fast iteration (push first, non-blocking)
- [Timeline Log Budgeting Claim Review](sources/worldarchitect.ai-docs-timeline_log_claims.md-b993975c.md) — debunks TIMELINE_LOG_DUPLICATION_FACTOR 2.05 claim; timeline log not serialized in LLMRequest
- [Command Usage — Last 30 Days](sources/worldarchitect.ai-docs-command-usage.md-a82ab449.md) — 27,305 files scanned, /copilot leads with 552 invocations, 131 commands at zero usage
- [V1/V2 Architectural Differences Reference](sources/worldarchitect.ai-docs-v1_v2_architectural_differences.md-95e43944.md) — technical reference for V1 Flask vs V2 React architectures, data format conversion, and debugging patterns
- [V2 Campaign Creation Performance Improvements](sources/worldarchitect.ai-docs-v2-performance-improvements.md-8c4b66ed.md) — animated progress bar, optimistic UI, error recovery with retry, and power-user skip animation for 10-11 second campaign creation
- [LLM-First State Management Plan](sources/worldarchitect.ai-docs-llm_state_management_plan.md-2909e4cb.md) — PR #2778: LLM-first approach to campaign coherence replacing server-side validation with prompt engineering
- [PR #3746: Session Header Fix - Before/After Evidence](sources/worldarchitect.ai-docs-pr-3746-evidence.md-4081a17a.md) — 0%→100% pass rate via fallback generation + CURRENT/MAX format
- [ChatGPT Pulse Comprehensive Repository Analysis Prompt](sources/worldarchitect.ai-docs-chatgpt_pulse_comprehensive_repo_analysis_prompt.md-ef699bfd.md) — comprehensive analysis template for WorldArchitect.AI covering MCP architecture, frontend, backend, and AI systems
- [Banned Names Reference](sources/worldarchitect.ai-world_reference-banned_names_reference.md-f4da76ec.md) — 60 names overused by LLMs (Alaric, Corvus, Elara, Lyra, Phoenix, Raven, etc.) with replacement history
- [Slash Commands Documentation](sources/worldarchitect.ai-docs-slash_commands.md-b15590ca.md) — comprehensive documentation for /timeout, /cerebras, /header, /deploy and command composition
- [Streaming Refactoring Plan - Task to Bead Mapping](sources/worldarchitect.ai-docs-streaming-refactoring-plan.md-1de3fd3e.md) — PR #2541: consolidate streaming/non-streaming paths, add JSON mode, two-phase tool execution, response validation
- [WorldAI Faction Management Mini-Game Tests](sources/worldarchitect.ai-testing_mcp-readme_faction_minigame.md-bc6daff3.md) — 21 tests validating faction minigame state structure and persistence via GOD_MODE_UPDATE_STATE
- [Visual Content Validation - E2E Data Flow](sources/worldarchitect.ai-testing_llm-test_visual_content_validation.md-4f89f34e.md) — test validates React V2 displays user content, not hardcoded templates
- [Enhanced Screenshot Validation Protocol](sources/worldarchitect.ai-docs-enhanced_screenshot_validation_protocol.md-a72a15e6.md) — multi-method UI verification combining Claude Vision, accessibility trees, and progressive baselines
- [Schema Prompt Regression Test - PR#5584](sources/worldarchitect.ai-testing_llm-test_schema_prompt_regression.md-9023136d.md) — branch comparison validating dynamic prompts remain equivalent
- [LLM Schema Non-Compliance Investigation](sources/worldarchitect.ai-docs-llm-schema-noncompliance-2026-02-17.md-d859ddcc.md) — 50% raw failure rate in JSON schema output traced to `[Mode: STORY MODE]` prefix parsing bug
- [Backup Script Enhancement: Added Codex Conversations Support](sources/worldarchitect.ai-docs-backup-script-updates.md-37063997.md) — dual backup of Claude and Codex conversations to Dropbox, 14,978 files total
- [Genesis vs Ralph Orchestrator Benchmark Report](sources/worldarchitect.ai-docs-benchmark-genesis-vs-ralph-2025-09-28.md-41fc5338.md) — Genesis 92.75 vs Ralph 81.75: Genesis 3-4x faster with ~9 vs 300 iterations
- [Detailed Agent Instructions for Beads Development](sources/agent_instructions.md-e0854e51.md) — Go 1.24+ development guidelines, test isolation with BEADS_DB, Dolt database, mandatory "landing the plane" push workflow
- [Genesis vs Ralph Orchestrator Benchmark Results (Sept 2025)](sources/worldarchitect.ai-docs-benchmark-results.md-0ecfb7b2.md) — Sept 27 test: 3/3 Genesis with Codex, 2/3 Ralph with Claude fallback due to codex KeyError
- [Testing MCP Agent Instructions](sources/worldarchitect.ai-testing_mcp-agents.md-1da0d001.md) — mandatory testing standards: no mocks, MCPTestBase required, loud failure signals
- [Testing MCP - Server-Level Tests with Real LLMs](sources/worldarchitect.ai-testing_mcp-readme.md-b84b04bf.md) — real LLM E2E testing framework with strict no-mocks policy
- [Testing Design Document](sources/worldarchitect.ai-docs-testing_design.md-49ee62ef.md) — 3-layer test architecture: MCP, HTTP, and UI (Playwright) with base test classes and core user flow coverage
- [Milestone 2: AI Content Integration Test - Execution Summary](sources/worldarchitect.ai-docs-milestone2-test-execution-summary.md-b08e741b.md) — execution infrastructure for testing AI content uses user campaign data, not hardcoded "Shadowheart"
- [Browser Automation Workflows](sources/worldarchitect.ai-docs-browser_automation_workflows.md-e1ff129a.md) — practical workflows combining Playwright and Superpowers Chrome for testing
- [Browser Automation Comparison: Playwright vs Superpowers Chrome](sources/worldarchitect.ai-docs-browser_automation_comparison.md-cf793872.md) — complete guide choosing between Playwright (~200 deps) and Superpowers Chrome (zero deps)
- [Combat Ally Turns & Resource Visibility Test](sources/worldarchitect.ai-testing_mcp-test_combat_ally_turns_readme.md-63e2824c.md) — E2E test validating automatic ally turns and combat resource display (HP/AC/status)
- [React V2 Settings Button Discovery](sources/worldarchitect.ai-docs-react_v2_settings_discovery.md-8c0ec4a2.md) — CORRECTION: settings button already exists, visibility issue not missing feature
- [React V2 - Next Priority Fixes](sources/worldarchitect.ai-docs-react_v2_next_steps.md-41427184.md) — 4 critical fixes: settings button, sign-out, URL routing, per-campaign buttons
- [Homepage Latency Optimization Report](sources/worldarchitect-ai-docs-homepage_latency_report.md-135bcd7c.md) — field selection (99% size reduction) and parallel I/O (26% latency improvement) for WorldArchitect.AI
- [Character Creation Flow Paths](sources/worldarchitect-ai-testing_mcp-character_creation_flows.md-199b12e2.md) — D&D 5e character creation/level-up paths with TIME FREEZE principle for lifecycle testing
- [Animal Movement Web Game - Technical Design](sources/worldarchitect-ai-docs-animal_game_design_document.md-fea42926.md) — browser-based animal game with HTML5 Canvas, sprite animation, and tile-based physics
- [LLM Capability Mapping](sources/worldarchitect-ai-testing_llm-test_llm_capability_mapping.md-b6517719.md) — systematic LLM boundary discovery via D&D scenarios
- [Blueplane Telemetry Core](sources/blueplane-telemetry-core.md) — local privacy-first telemetry for AI coding assistants
- [WorldArchitect.AI Context Components Reference](sources/worldarchitect.ai-docs-context_components_reference.md-4e3d3055.md) — token budget allocation for LLM context: scaffold (15-20%), entity tracking (10,500 fixed), story budget (50-60%)
- [WorldArchitect.AI](sources/worldarchitect-ai.md) — AI-powered D&D 5e platform with MCP architecture, 700K+ LOC
- [AI Usage Tracker](sources/ai-usage-tracker.md) — unified token usage and cost tracking for Claude and Codex
- [Beads - AI-Native Issue Tracking](sources/.beads-readme.md-749dcadc.md) — CLI-first issue tracking that lives in your repo, git-native and AI-friendly
- [Beads Attribution — beads-merge](sources/beads-docs-attribution.md-70975eb9.md) — 3-way merge algorithm vendored from @neongreen with MIT license
- [Beads](sources/bd-beads.md) — distributed git-backed graph issue tracker for AI agents
- [Beads Development Container](sources/beads-devcontainer-readme.md) — Go 1.23 devcontainer with bd CLI built from source, supports Codespaces and VS Code Remote Containers
- [Beads Build and Version Infrastructure](sources/beads-build-infrastructure.md-6f30884a.md) — coordinated build system ensuring all installation methods produce binaries with complete version info
- [Beads Agent Instructions](sources/beads-agents.md-df02cf0a.md) — comprehensive agent instructions for Beads issue tracking with visual design standards and session completion workflow
- [BD (Beads) Guide for AI Agents](sources/bd-beads_guide.md-6fd48096.md) — Git-backed issue tracker with MCP integration, dependency tracking, and auto-sync to JSONL
- [Beads Community Tools](sources/beads-docs-community_tools.md-43bea8d0.md) — curated list of 24 community UIs, extensions, and integrations for Beads issue tracking
- [Deletion Tracking](sources/beads-docs-deletions.md-3c5b1006.md) — inline tombstones with audit trail, TTL-based expiration, and 3-way merge conflict resolution for cross-clone sync
- [MVP Site Prompts - Character Template & Game State Protocols](sources/worldarchitect.ai-world_reference-mvp_site_prompts_merged.md-4eaaf864.md) — character profile template with internal MBTI/alignment, D&D 5E SRD authority, and critical dice-unknowable game state protocol
- [AI Universe Living Blog](sources/ai-universe-living-blog.md) — living blog MCP server + novel engine for PR lifecycle fiction
- [AI Universe Daily User Activity Reports](sources/ai-universe-daily-reports.md) — DAU/WAU analytics from WorldArchitect.AI
- [WorldArchitect.AI Deployment Log](sources/worldarchitect-ai-deployments.md) — GCP Cloud Run deployment history
- [WorldArchitect.AI 20-Turn Test Improvement](sources/worldarchitect-ai-20turn-test-improvement.md) — E2E test iteration 004 vs 005 analysis showing timestamp and level progression fixes
- [Game State Logical Consistency Validation Test](sources/worldarchitect-ai-testing_llm-test_game_state_logical_consistency.md-d5dce451.md) — multi-LLM validation protocol for D&D game state consistency
- [Streaming Full Journey with Network Proof](sources/worldarchitect.ai-testing_llm-test_streaming_full_journey_with_network_proof.md-8d8e92c0.md) — E2E streaming validation with screenshots, OCR, and SSE network proof
- [Sanctuary Mode Autonomy Analysis](sources/worldarchitect.ai-testing_mcp-sanctuary_autonomy_analysis.md-bd149cb6.md) — activation requires explicit completion language, expiration is autonomous
- [Full User Journey Test Spec](sources/worldarchitect-ai-full-user-journey-test-streaming.md) — E2E test spec for campaign→character→story workflow with streaming
- [GitHub Development Statistics](sources/worldarchitect-ai-github-stats.md-92dcfa3a.md) — elite DORA metrics with 12.5/day deployment frequency
- [Adding Anthropic API Key to GitHub Secrets](sources/worldarchitect-ai-docs-github-secret-setup.md) — tutorial for setting up Claude Code in GitHub Actions
- [GitHub Actions Auto-Deployment](sources/worldarchitect-ai-github-actions-auto-deployment.md) — auto-deploy to dev on main push, manual approval for production

- [Immediate Subagent Implementations for Context Optimization](sources/immediate-subagent-converge-context-optimization.md) — implementation-ready subagent tasks for 60-75% context reduction in /converge
- [PR #1410 Context Optimization - Validation Report](sources/worldarchitect.ai-docs-pr-1410-context-optimization-validation.md-188f1b47.md) — 20-30% context savings validated via A/B testing, 85.4% compression

- [Import Optimization Analysis Report](sources/worldarchitect.ai-docs-import-optimization-analysis.md-3bf88938.md) — 167 inline imports across 64 files, organized by severity

- [Implementation vs Orchestration Decision Framework](sources/worldarchitect.ai-docs-implementation-decision-framework.md-ffa9728e.md) — systematic framework preventing fake code through "Can I implement this fully right now?" gate
- [Team Guide: Fake Code Prevention](sources/worldarchitect.ai-docs-team-fake-code-prevention-guide.md-77b17e6f.md) — adoption guide for enhanced fake code prevention with mandatory /fake3 and zero-tolerance policies
- [Preventing Scene Backtracking and Missed God-Mode Corrections](sources/worldarchitect.ai-docs-backtracking_prevention_plan.md-62338d56.md) — proactive prevention, auto state repair, and continuity locks to prevent scene rewinding
- [Improved Research Test Prompt - Red-Green Methodology](sources/worldarchitect.ai-docs-improved_research_test_prompt.md-79587c15.md) — RED test with fake command, GREEN test with real /help command for research methodology validation
- [Review Command Retest Prompt](sources/worldarchitect.ai-docs-review_command_retest_prompt.md-8e26e7f4.md) — test prompt validating `/research` finds built-in `/review` with source authority hierarchy
- [jleechanclaw GitHub Statistics](sources/repos-jleechanclaw-github-stats.md-f99b8330.md) — elite DORA metrics: 11.8/day deployment freq, 1.7h median PR merge time, 47.6 commits/day
- [XSS Security Fix - Frontend Error Handling](sources/worldarchitect-ai-docs-xss-fix-summary.md-31263d85.md) — critical XSS vulnerability fixed with sanitizeForDisplay() function and safe DOM manipulation
- [Security Fixes for orchestration/agent_monitor.py](sources/worldarchitect.ai-docs-security_fixes_agent_monitor.md-40cae6cd.md) — critical command injection and path traversal vulnerabilities fixed with input validation

- [Screenshot Cleanup Summary - 2025-08-06](sources/worldarchitect.ai-docs-screenshot_cleanup_summary_20250806_220105.md-55b62779.md) — organized test evidence structure: archived 24 files, created v1/v2 evidence directories, established file naming standards

- [iOS MCP Client Implementation Analysis](sources/worldarchitect.ai-docs-ios_mcp_implementation_analysis.md-e1047eed.md) — Swift MCP SDK, Streamable HTTP, OAuth 2.1 PKCE, MVVM+SwiftUI for D&D/RPG apps

- [Behavioral Automation System - Executive Summary](sources/worldarchitect.ai-docs-roadmap_summary.md-f161f89a.md) — 6-phase roadmap transforming ~20% compliance to 95% using Memory MCP
- [Iteration 005 Detailed Campaign Analysis](sources/worldarchitect.ai-docs-iteration_005_detailed_analysis.md-918736ff.md) — 20-turn E2E analysis after 5 prompt clarifications
- [Iteration 007 Campaign Analysis](sources/worldarchitect.ai-docs-iteration_007_analysis.md-0f81426d.md) — all 25 turns pass, critical economic (upkeep 10x too high) and ranking (stuck at #201) issues identified
- [Local Disk Cleanup Process](sources/worldarchitect.ai-docs-local_disk_cleanup_process.md-b30f137c.md) — script for reclaiming disk space from AI tooling artifacts (Cursor, Claude, Playwright, pip caches)

- [MacBook Dev Environment Setup Guide](sources/worldarchitect.ai-docs-macbook-dev-setup.md-292386a1.md) — comprehensive setup script for replicating WorldArchitect.AI dev environment on new MacBook
- [CLI Provider Test Results](sources/worldarchitect.ai-docs-cli_provider_test_results.md-08b5d2a4.md) — 4 LLM providers tested: Claude opus (✅), sonnet (⚠️ rate limited), MiniMax (✅), Codex (✅)
- [Claude Code Learning & Mistakes Analysis Report](sources/worldarchitect.ai-docs-claude_code_learning_mistakes_analysis_2025.md-21eb9606.md) — 2,188 learning opportunities across 2,620 sessions; top mistakes: orchestration failures, testing breakdowns, context loss
- [JSON Parsing Changes - PR #3458](sources/worldarchitect.ai-docs-json_parsing_changes.md-cd5aa29e.md) — removed regex-based JSON recovery, now uses json.loads() only — fail-fast behavior
- [MCP Server Red-Green Analysis - PR #1551](sources/worldarchitect.ai-docs-mcp_server_redgreen_analysis.md-b0eb466e.md) — Red-Green analysis showing MCP server warnings are cosmetic only, 98.8% test pass rate, system production ready
- [External Memory Backup System Debug Summary](sources/worldarchitect.ai-docs-memory-backup-debug-summary.md-a39b1aee.md) — fixed 4/5 failing health checks to 0/5 passing
- [TASK-074 Unit Test Coverage Review](sources/worldarchitect.ai-docs-task_074_progress_summary.md-e1559df6.md) — fixed coverage.sh vpython path, PR #394 ready for merge
- [System Prompt Test Scenarios](sources/worldarchitect.ai-docs-system_prompt_test_scenarios.md-10ff2e08.md) — 5 test scenarios validating system prompt generates action-first Claude Code commands
- [Claude Code System Prompt Capture - Method Comparison](sources/worldarchitect.ai-docs-claude_code_system_prompt_comparison.md-8ee34429.md) — compares debug method vs HTTP proxy method for system prompt capture
- [CLAUDE.md - Directory Documentation Standards](sources/worldarchitect.ai-docs-claude.md-012e4860.md) — comprehensive documentation standards covering ADRs, feature evidence, and lifecycle management
- [Claude Code Session Analysis Report - July/August 2025](sources/worldarchitect.ai-docs-claude_session_analysis_2025_july_august.md-e3f2c767.md) — 2,620 conversations over 30 days: 15.6 PRs/day, 96% orchestration command usage, 85% first-time-right accuracy
- [Temperature Analysis for Faction Tool Calling](sources/worldarchitect.ai-docs-temperature_analysis_faction_tool_calling.md-d3e6428c.md) — higher temperature (0.9) performs better for tool calling (56% vs 4-20% at lower temps) due to exploration breaking "skip tools" patterns
- [Comment Reply Workflow](sources/worldarchitect.ai-docs-commentreply-workflow.md-bd564723.md) — 3-step PR comment processing: fetch → Claude analyze/fix → post via GitHub API with threaded replies
- [Copilot Command Family Development Guidelines](sources/worldarchitect.ai-docs-copilot-command-family-guidelines.md-e167e767.md) — guidelines for implementing /copilot, /copilot_lite, and /copilot_expanded commands as explicitly requested by user
- [Cache-Busting Guide](sources/worldarchitect.ai-scripts-cache_busting.md-9a54b261.md) — content-based hashes for aggressive browser caching with perfect cache invalidation
- [JSON Display Bugs Analysis Report](sources/worldarchitect.ai-scripts-json_display_bug_fixes.md-ff16df26.md) — two JSON display bugs from PR #278 verified as FIXED
- [MCP Server Migration Guide](sources/worldarchitect.ai-scripts-migration.md-4418a621.md) — unified installer replaces old launchers, user scope default, better error handling
- [Faction Tool Invocation Investigation - Next Steps](sources/worldarchitect.ai-docs-faction_investigation_next_steps.md-e3fcd5bf.md) — 6-phase investigation into 4% regression, restoring tool invocation to 56%+ baseline
- [Faction Tool Invocation - Next Steps Investigation](sources/worldarchitect.ai-docs-faction_next_steps_investigation.md-7d9aafc8.md) — 28% vs 56% gap analysis: semantic classifier interference, agent selection timing, tool availability
- [Copilot PR Review Summary](sources/worldarchitect.ai-scripts-copilot_review_summary.md-1de67376.md) — missing imports fixed, PR ready for merge after functional issues addressed
- [PR #4534 Comment Resolution Summary](sources/worldarchitect.ai-docs-pr-4534-comment-resolution.md-d713dca3.md) — 312 comments analyzed via 6 parallel agents: 63 critical/high issues (20%), 78 medium (25%), GameState serialization bugs + schema mismatches
- [Code Reviewer Agent Definition](sources/code-reviewer-agent-definition.md) — expert code reviewer agent with confidence-based filtering (≥80) for bugs, security, and quality issues
- [Claude Code Source Leak Analysis](sources/claude-code-source-leak.md) — Anthropic Claude Code .map sourcemap leak: KAIROS proactive agent mode, 44 hidden feature flags, model codenames, DRM, 3-layer memory
- [Simon Willison Agentic Engineering Podcast](sources/simon-willison-agentic-engineering-podcast.md) — Simon Willison's podcast highlights on agentic engineering
- [Claude Dispatch Interfaces](sources/claude-dispatch-interfaces.md) — Ethan Mollick on Claude Dispatch and AI agent interface design
- [Google Calendar Oct 2025 - Mar 2026](sources/google-calendar-oct2025-mar2026.md) — 100 calendar events: graduate courses, therapy, wedding planning, business meetings
- [Tax 1099 Emails 2026](sources/tax-1099-emails-2026.md) — 1099 tax correspondence with attorney Jorge Martins, Chase Sapphire, Venmo, GitHub Copilot
- [MCP Mail Fork](sources/repos-mcp-mail-agents.md) — MCP Agent Mail fork by jleechanorg: lazy loading (65% token reduction), global architecture, 9 enhancements
- [jleechanclaw README](sources/repos-jleechanclaw-readme.md) — Harness analyzer (9am launchd), smoke test bead, fresh machine setup
- [jleechanclaw CLAUDE.md](sources/repos-jleechanclaw-claude.md) — Rule #1: never delete files, GITHUB_TOKEN env var, uv/Python 3.11+ policy
- [jleechanclaw SOUL.md](sources/repos-jleechanclaw-soul.md) — Identity: genuinely helpful, agento skill routing, PR Work Protocol, CodeRabbit rules
- [jleechanclaw AGENTS.md](sources/repos-jleechanclaw-agents.md) — Session startup protocol, memory system, upstream-first, PR Green Criteria
- [jleechanclaw Audit Report](sources/repos-jleechanclaw-audit-report.md) — Harness engineering practices, security posture
- [smartclaw README](sources/repos-smartclaw-readme.md) — smartclaw repo: setup, heartbeat, auto-start, slack, backup
- [MCP Mailbox Sharing Plan](sources/mcp-mailbox-sharing-plan.md) — Sharing MCP Agent Mail as static bundle: SQLite WASM, Ed25519 signing, age encryption
- [OpenClaw Setup Guide](sources/openclaw-setup-guide.md) — OpenClaw setup: automated backup (launchd, 4h interval, API key redaction)
- [Character Creation Instructions](sources/character-creation-instructions.md) — D&D 5e character creation: mandatory planning_block JSON choices, God Mode
- [E2E Test Status](sources/e2e-test-status.md) — E2E test status tracking
- [MCP Mail Codebase Analysis](sources/mcp-mail-codebase-analysis.md) — 16,561 LOC Python, 27 MCP tools, 57 test files, SQLite + Git archive
- [MCP Mail Cross-Project Coordination](sources/mcp-mail-cross-project-coordination.md) — Projects isolated namespaces; monorepo pattern recommended
- [MCP Mail Test Coverage](sources/mcp-mail-test-coverage.md) — Build slots (10 tests) and pre-push guard (9 tests) coverage
- [MCP Mail Agent Onboarding](sources/mcp-mail-agent-onboarding.md) — Step-by-step agent coordination workflow: ensure_project → register → discover → message
- [MCP Mail Tier 2 Upstream Analysis](sources/mcp-mail-tier2-upstream-analysis.md) — Pre-push guards (4f403be): blocks conflicting pushes, diagnostics CLI
- [Smartclaw Orchestration System Design](sources/smartclaw-orchestration-system-design.md) — OpenClaw + AO orchestration: replace yourself, 4 memory tiers, deterministic first
- [Smartclaw Harness Engineering](sources/smartclaw-harness-engineering.md) — 4-layer harness: agent env, deterministic AO, OpenClaw judgment, entropy management
- [Smartclaw Genesis Design](sources/smartclaw-genesis-design.md) — Genesis: config layer on top of OpenClaw — fills existing files, tunes config
- [Smartclaw Zero-Touch Definition](sources/smartclaw-zero-touch-definition.md) — Zero-touch: AO spawned + worker drove to N-green + skeptic merged; GitHub actor audit
- [Smartclaw ws-stream Incident 2026-03-28](sources/smartclaw-2026-03-28-ws-stream-incident.md) — P0: protocol version mismatch → 367 WS failures/day → Slack reply drops → downgrade to 2026.3.24
- [Smartclaw Staging Pipeline](sources/smartclaw-staging-pipeline.md) — 3-stage pipeline: staging branch → canary (6/6) → CI gate (2/6) → production
- [Smartclaw Context Window Comparison](sources/smartclaw-context-window-comparison.md) — OpenClaw (business context) vs AO workers (delivery context)
- [Smartclaw Postmortem 2026-03-19](sources/smartclaw-postmortem-2026-03-19-routing.md) — Wrong repo context delegation; SOURCE/TARGET contract enforced
- [Smartclaw Orchestration Research 2026](sources/smartclaw-orchestration-research-2026.md) — Spotify Honk, Composio AO: 30 agents, 60% PR success, LLM-as-Judge veto
- [Smartclaw Cron Migration](sources/smartclaw-cron-migration.md) — Git-tracked launchd plists (20+ templates) vs live-only gateway cron jobs
- [Smartclaw ZOE Agent Swarm](sources/smartclaw-zoe-agent-swarm-reference.md) — OpenClaw as orchestrator (Zoe): 94 commits/day, tmux mid-task redirect
- [Smartclaw Human Channel Bridge](sources/smartclaw-human-channel-bridge.md) — AO lifecycle → Slack channel C0ANK6HFW66 mirroring
- [Smartclaw HEARTBEAT.md](sources/smartclaw-heartbeat.md) — Heartbeat task file: empty = no heartbeat API calls
- [Smartclaw TOOLS.md](sources/smartclaw-tools.md) — MCP servers, project-specific handling, cron guardrail
- [Smartclaw SOUL.md](sources/smartclaw-soul.md) — Smartclaw identity: genuinely helpful, agento routing, tmux-based coding
- [Smartclaw AO Exhaustive Audit](sources/smartclaw-ao-exhaustive-audit.md) — AO vs current stack: AO better at plugin registry/session archive; stack better at review depth
- [Smartclaw mem0 Purge Runbook](sources/smartclaw-mem0-purge-runbook.md) — Qdrant vector store purge: dry-run default, ID allowlist, hash confirmation
- [jcc-19-fix CLAUDE.md](sources/jcc-19-fix-claude.md) — This repo IS ~/.openclaw/: harness structure, deprecated openclaw_config repo
- [jcc-19-fix BOOTSTRAP.md](sources/jcc-19-fix-bootstrap.md) — Fresh workspace bootstrap: establish identity, update IDENTITY/USER/SOUL files
- [jcc-19-fix Audit Report](sources/jcc-19-fix-audit-report.md) — Token scrub policy, AGENTS.md workspace version, migration bundle scrub strategy
- [Discord Eng Bot SOUL.md](sources/discord-eng-bot-soul.md) — Consensus: Discord-first answer bot, second-opinion-tool, citation rules, hard output gate
- [JSON Display Bugs Analysis Report](sources/json-display-bugs-analysis-report-2026-04-07.md) — Analysis of two JSON display bugs in PR #278 verified as FIXED

## Entities

## Concepts

- [Research Test Report: Default /review Command in Claude Code CLI](sources/worldarchitect.ai-docs-research_review_command_test_report.md-895e5636.md) — confirms `/review` is a built-in slash command in Claude Code CLI

- [Research Reproducibility Test Report](sources/worldarchitect.ai-docs-research_reproducibility_test_report.md-762c9ac3.md) — confirms `/review` is a built-in slash command in Claude Code CLI

- [Qwen vs Sonnet Benchmark Index](sources/qwen-vs-sonnet-benchmark-index.md-800b5891.md) — 20-30x faster responses (559ms avg) with quality parity across 12 coding tasks

## Syntheses