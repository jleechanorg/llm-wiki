---
title: "[agento] docs: add WIP README + install bootstrap script"
type: source
tags: [github, pr, jleechanorg-smartclaw]
sources: []
date: 2026-03-29
pr_url: https://github.com/jleechanorg/smartclaw/pull/1
pr_number: 1
pr_repo: jleechanorg/smartclaw
---

## Summary
## Summary
- Main documentation is now README.md with WIP/prototype warning
- Files copied from jleechanorg/jleechanclaw (sanitized):
  - docs/HARNESS_ENGINEERING.md
  - roadmap/ORCHESTRATION_DESIGN.md
  - openclaw.json (runtime config template)
  - agent-orchestrator.yaml (orchestrator config template)
- install.sh kept for dependency bootstrap
- All files include source citations

## Background
Adapting content from private jleechanorg/jleechanclaw harness for public smartclaw repo. Content sa...

## Key Changes
- 35 commit(s) in this PR
- 100 file(s) changed
- Large diff (20+ files)
- Merged: 2026-03-29

## Commit Messages
1. docs: add WIP README + install bootstrap script
  
  - Add README_SMARTCLAW.md with WIP warning, dependency list,
    setup prerequisites, and architecture boundaries section
  - Add install.sh for safe/idempotent dependency bootstrap
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
2. Fix: Ensure script exits when Python detection fails in command substitution
  
  The detect_python function's exit 1 only exited the subshell when called
  via command substitution, allowing the script to continue with an empty
  PYTHON_BIN. Added explicit check to exit parent script if PYTHON_BIN is empty.
3. docs: update README with sourced content from jleechanclaw
  
  Add content sourced from private jleechanorg/jleechanclaw:
  - Architecture diagram from ORCHESTRATION_DESIGN.md
  - Harness engineering philosophy from docs/HARNESS_ENGINEERING.md
  - Deterministic first principle
  - Configuration examples from agent-orchestrator.yaml (sanitized)
  - Agent rules examples (sanitized)
  - Maturity model from NxCode framework
  
  Include explicit "Source from jleechanclaw" citations throughout.
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
4. docs: add smartclaw package with sourced content from jleechanclaw
  
  Main documentation (README.md):
  - Updated as primary doc with WIP/prototype warning
  - Includes architecture, harness engineering principles
  - Comparison table: smartclaw vs Agent-Orchestrator
  - Dependencies, setup prerequisites, quickstart
  
  Files copied from jleechanorg/jleechanclaw (sanitized):
  - docs/HARNESS_ENGINEERING.md - Harness engineering philosophy
  - roadmap/ORCHESTRATION_DESIGN.md - Orchestration design document
  - openclaw.json - Runtime config template (sanitized)
  - agent-orchestrator.yaml - Agent orchestrator config template
  
  All files include "Source: Adapted from jleechanclaw" citations.
  
  Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
5. fix: secure config template defaults - enable sandbox, disable elevated tools, require exec confirmation
6. Make portability defaults env-driven and close sweep beads
7. Fix: Move Phase 2 recheck block to execute after Phase 2 completes
  
  The recheck block was testing PHASE2_RC before Phase 2's background
  job completed, causing it to always execute against pre-Phase-2 state.
  Moved the recheck (re-probing services) to after wait collects Phase 2
  results, so it properly validates whether Phase 2 fixes worked.
8. Fix GitHub API head parameter to include owner prefix
  
  The GitHub API head parameter requires format 'owner:branch' but was only passing the branch name. This caused the API to always return empty results, leading to sessions with open PRs being incorrectly reaped after 4 hours.
9. Fix: Replace hardcoded private repo name with empty string in LEGACY_DEFAULT_PROJECT_KEY
  
  Changed LEGACY_DEFAULT_PROJECT_KEY from 'jleechanclaw' to empty string in both mcp_mail.py and dispatch_task.py. This prevents MCP mail operations from silently defaulting to a private project when environment variables are unset, causing them to fail visibly instead of misrouting.
10. feat: add orchestration source, tests, and repo infrastructure from jleechanclaw
  
  Adds the full implementation layer copied from jleechanorg/jleechanclaw:
  
  - src/orchestration/: 60+ modules (webhook pipeline, escalation router,
    failure budget, parallel retry, PR reviewer, outcome recorder, etc.)
  - src/tests/: unit test suite (429 tests covering all orchestration modules)
  - tests/: integration and hardening tests
  - scripts/: install, doctor, backup, and automation helpers
  - launchd/: macOS LaunchAgent plist templates for managed services
  - pyproject.toml, Makefile: package metadata and dev workflow shortcuts
  - .github/: CI workflow definitions
  - .beads/: issue-tracking artifacts (.gitignore, config, metadata)
  - .env.example: environment variable template (no secrets)
  - .gitleaks.toml, .gitleaksignore: secret scanning config
  - .coderabbit.yaml: CodeRabbit review config
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
11. docs: add remaining docs, skills, and .claude commands from jleechanclaw
  
  - SOUL.md, TOOLS.md, HEARTBEAT.md: operating guidance and liveness docs
  - .claude/commands/, .claude/skills/: custom agent commands and skill definitions
  - skills/: agent skill implementations (agento, dispatch-task, etc.)
  - docs/: additional engineering docs (GENESIS_DESIGN, ORCHESTRATION_RESEARCH,
    ZOE_AGENT_SWARM_REFERENCE, webhook_runbook, coderabbit-ping-workflow, etc.)
  - roadmap/: additional design docs (AGENTO_GREEN_LOOP_GAPS, AGENT_REVIEWER_LOOP,
    MVP_OPENCLAW_AIORCH_MULTI_AGENT, NATURAL_LANGUAGE_DISPATCH, VALUE_ROUTER_DESIGN,
    MEMORY_UPGRADE_PLAN, EVIDENCE_REVIEW_SCHEMA)
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
12. docs: expand README with ToC and repository map
  
  - Add Table of Contents (13 sections)
  - Add "What's in this repository?" section mapping all major dirs/files
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
13. fix: harden openclaw.json template security defaults (CodeRabbit Major)
  
  - OPENCLAW_RAW_STREAM: "1" → "0" — disable raw traffic logging by default
    to avoid persisting prompts/secrets to disk (opt-in for debugging)
  - allowRequestSessionKey: false + remove broad "hook:" prefix — prevents
    callers with hooks token from targeting arbitrary namespaces
  - channels.slack.allowFrom: [] + dmPolicy: "allowlist" — explicit allowlist
    rather than wildcard that bypasses groupPolicy enforcement
  - dispatch_task.py: replace hardcoded private repo name with generic label
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
14. fix: address CodeRabbit Major issues - hardening, identifiers, security
  
  - pyproject.toml: rename package from jleechanclaw → smartclaw
  - bead_lifecycle_validator.py: treat unparseable timestamps as stale
    instead of silently skipping (prevents stuck beads hiding forever)
  - monitor-agent.sh: remove hardcoded node v22.22.0 from PATH;
    clear hardcoded Slack channel IDs (C0AKYEY48GM → empty default)
  - scripts/doctor.sh: clear hardcoded Slack channel ID default
  - scripts/run_tests_with_coverage.sh: replace eval with bash -c
  - scripts/install-qdrant-container.sh: pin image to v1.13.6 (via
    QDRANT_IMAGE env var), bind to 127.0.0.1 instead of 0.0.0.0
  - launchd/*.template: replace hardcoded node v22.22.0 with current
    across all 4 templates; webhook daemon binds to 127.0.0.1
  - .github/workflows/coderabbit-ping-on-push.yml: add 10-minute
    dedup window to prevent re-pinging CR on rapid successive pushes
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
15. fix: further address CodeRabbit Major issues - logs, eval, identifiers
  
  - launchd/ai.agento-manager: move logs from /tmp to ~/.openclaw/logs;
    remove hardcoded /opt/homebrew/bin/python3 → use python3 from PATH
  - launchd/ai.openclaw.lifecycle-manager: move logs from /tmp to ~/.openclaw/logs
  - scripts/run_tests_with_coverage.sh: replace bash -c with direct argv
    execution ("$@") — callers updated to pass cmd as positional args
  - src/orchestration/auto_resolve_threads.py: update docstring example
  - src/orchestration/dispatch_task.py: update docstring example
  - src/orchestration/session_reaper.py: update docstring example
  - src/orchestration/webhook_worker.py: update comment example
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
16. fix: use push SHAs for accurate file change detection in auto_resolve_threads
  
  Use GitHub compare endpoint (before...after SHAs) when push SHAs are
  available, falling back to single-commit endpoint, then PR-level file
  list. Eliminates the ambiguity of branch-name-only resolution.
  
  Also updates auto_resolve_threads_for_pr signature to accept before_sha
  and after_sha params, passing them through to get_files_changed_in_push.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
17. Fix install script to install local smartclaw package instead of private jleechanorg-orchestration package
18. fix: address CodeRabbit nitpick comments across 4 files
  
  - workflow: add tags-ignore to prevent tag push triggers
  - lifecycle-manager plist: source .bash_profile (login shell safe), create log dir
  - run_tests_with_coverage.sh: split fast/unit modes, cross-platform open hint,
    remove UUOC pipe for jq
  - dispatch_task.py: import get_default_project_key from mcp_mail (dedup), remove
    inline re import, use Path.name for project extraction, log retry exceptions
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
19. fix: remove redundant subprocess import and fix listComments dedupe window
  
  - dispatch_task.py: remove inline subprocess import (module-level import exists)
  - coderabbit-ping workflow: paginate comments and reverse to check most recent
    first within dedupe window, fixing per_page: 20 returning oldest not newest
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
20. fix: hunk-level thread resolution and paginated PR files in auto_resolve_threads
  
  Critical fix: resolve threads only when their line falls within a changed hunk,
  not just any file-level change. Adds get_changed_file_hunks() which parses
  unified diff patches from the compare endpoint into (start, end) ranges, and
  _line_in_hunks() for intersection. Threads on untouched lines are now skipped.
  
  Also:
  - _get_pr_files_gh: add --paginate to handle large PRs (>100 files)
  - get_files_changed_in_push: propagate first exception instead of silently
    swallowing errors (callers can now detect auth/rate-limit failures)
  - get_review_threads: fail closed when comment page is truncated (comment_total
    > len(comments)) to avoid misclassifying threads as bot-only
  - CLI: add --before-sha / --after-sha args; dry-run uses hunk-level display
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
21. fix: harden security defaults and install robustness
  
  - openclaw.json: zero out elevated.allowFrom wildcards
  - install.sh: add --user flag for PEP 668 managed-env compatibility
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
22. fix: ensure worktree_base dir exists before use; use node from PATH in plist
  
  - dispatch_task.py: os.makedirs(worktree_base, exist_ok=True) before
    resolve_worktree_for_branch to prevent mkdtemp failures on missing dir
  - lifecycle-manager plist: use 'node' from PATH instead of hardcoded nvm path
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
23. fix: add --branch to CLI and UUID suffix to prevent session/worktree collisions
  
  - dispatch_task.py main(): add --branch arg forwarded to dispatch()
  - _make_async_session_name: append uuid4 hex suffix to prevent collisions
    when multiple agents dispatch to same repo concurrently
  - _create_new_worktree: include uuid4 suffix in branch and worktree path
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
24. fix: fail-closed for missing patch, branch param in hunk lookup, signal handling
  
  auto_resolve_threads.py:
  - get_changed_file_hunks: add branch param for branch...HEAD diff fallback
  - Fail closed when patch is absent (no hunks) — skip thread instead of resolving
  - Pass branch through in auto_resolve_threads_for_pr and dry-run path
  - Fix dry-run display to use fail-closed logic (hunks required)
  
  lifecycle-manager plist:
  - Add signal handling (SIGTERM/SIGINT trap) to clean up worker PIDs on stop
  - KeepAlive: use dict form with SuccessfulExit=false to prevent restart loops
  - Project list defaults to placeholder; empty/placeholder exits 0 not 1
  
  install.sh:
  - Make tmux and gh hard requirements (exit 1 with clear error + install URL)
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
25. fix: use %-style logging and clarify worktree_path docstring
  
  - register_agent_mcp_mail: use %s-style log formatting for lazy evaluation
  - _resolve_target_repo: clarify docstring (worktree_path always empty)
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
26. Fix: Conditionally use --user flag to avoid venv conflicts
  
  Detects virtual environment via VIRTUAL_ENV and omits --user flag when
  inside a venv to prevent 'Can not perform a --user install' errors.
  Retains --user for non-venv installations to avoid PEP 668 errors.
27. fix: resolve all 6 Critical/Major PR#1 blockers
  
  evidence_review_gate.py (PRRT_kwDORrCs9c51pktt):
    Add TRUSTED_EVIDENCE_AUTHORS allowlist; only verdicts from coderabbitai,
    codex, openclaw, or github-actions bots are accepted. Arbitrary commenters
    (PR authors, external contributors) no longer satisfy the gate.
  
  action_executor.py (PRRT_kwDORrCs9c51qa2_):
    Guard MergeAction.pr_url being None before calling .rstrip(); return a
    clear failure result instead of raising AttributeError.
    Remove the incorrect mapping of "pull request is not mergeable" to success
    -- only "already merged" is treated as an idempotent success.
  
  escalation.py (PRRT_kwDORrCs9c51qa3D):
    Remove the locally-redefined action dataclasses (RetryAction,
    KillAndRespawnAction, NotifyJeffreyAction, NeedsJudgmentAction,
    ParallelRetryAction, EscalationAction, JudgmentResult). Import all of them
    directly from escalation_router so that action_executor.execute_action()
    isinstance() dispatch resolves to the single canonical type hierarchy.
  
  failure_budget.py (PRRT_kwDORrCs9c51qa3F):
    Replace the broken cached-snapshot save() approach with a proper
    read-modify-write pattern inside the exclusive file lock. New helpers
    _load_from_disk_locked() and _write_locked() are always called under the
    lock. record_escalation() and record_strategy_change() now take the lock,
    read fresh disk state, apply the increment, and write atomically so
    concurrent processes cannot silently overwrite each other updates.
  
  auto_resolve_threads.py (PRRT_kwDORrCs9c51qL5d):
    Fix _parse_hunk_ranges() to emit a single (n, n) range per added (+) line
    instead of the full +start,count hunk span. Context lines are explicitly
    excluded, so a review thread on an unchanged context line inside a large
    hunk is no longer wrongly auto-resolved.
  
  scripts/run_tests_with_coverage.sh (PRRT_kwDORrCs9c51pxWz):
    Enforce COVERAGE_THRESHOLD after coverage collection in the "coverage"
    mode. Use jq to extract .total.lines.pct and awk for floating-point
    comparison; set overall_status=1 (failing the build) when actual coverage
    falls below the threshold.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
28. fix: address Major inline blockers in monitor-agent.sh, doctor.sh, auto_resolve_threads.py
  
  monitor-agent.sh:
    - Use HTTP_GATEWAY_URL for gateway token subprobe (PRRT_kwDORrCs9c51pxWq)
    - Guard Phase 1 launchctl with Darwin check for Linux compat (PRRT_kwDORrCs9c51pxWu)
    - Skip doctor.sh inference only when monitor probe is enabled (PRRT_kwDORrCs9c51pxWn)
  
  doctor.sh:
    - Timezone FAIL -> WARN on non-macOS hosts (PRRT_kwDORrCs9c51pxWv)
    - Use plist_token fallback for gateway CLI probes (PRRT_kwDORrCs9c51pxWw)
  
  auto_resolve_threads.py:
    - Fix paginate+jq to use NDJSON output for multi-page PR files (PRRT_kwDORrCs9c51qL5g)
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
29. fix: address remaining Critical blockers in pyproject.toml, run_tests_with_coverage.sh, decomposition_dispatcher.py
  
  pyproject.toml (PRRT_kwDORrCs9c51pktc):
    Upgrade setuptools build requirement from >=68.0 to >=78.1.1 to remediate
    CVE-2024-6345 (RCE via command injection) and CVE-2025-47273 (path traversal /
    arbitrary file write) which affect all versions prior to 70.0 and 78.1.1
    respectively.
  
  scripts/run_tests_with_coverage.sh (PRRT_kwDORrCs9c51pxW1):
    Replace non-existent pnpm build/test/test:coverage commands in 'all' mode
    with Python-native pytest invocation with --cov coverage collection. The
    repo is Python-based with no package.json; pnpm commands would always fail.
    Coverage threshold enforcement uses the same jq/awk pattern as the
    'coverage' mode.
  
  src/orchestration/decomposition_dispatcher.py (PRRT_kwDORrCs9c51pktr):
    Restrict spawn() retry to known transient exception types (TimeoutError,
    ConnectionError, OSError). Non-transient failures (configuration errors,
    permission denied, bad arguments) now propagate immediately instead of being
    silently downgraded to blocked=True, which could mask bugs. This also
    reduces the risk of duplicate session creation on non-idempotent failures.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
30. fix: infer branch from worktree path in list_jc_sessions (PRRT_kwDORrCs9c51ozE6)
  
  Previously list_jc_sessions always set branch=None, so is_safe_to_kill
  always entered Case 2 (no-PR / 4h threshold) and never checked PR state
  in Case 3. Sessions backing an active open PR were incorrectly eligible
  for reaping after 4 hours.
  
  Fix: derive branch name from os.path.basename(worktree_path) -- dispatch
  creates the worktree at <worktree_base>/<branch>, so the directory name
  equals the branch name. When worktree_path is None the branch stays None
  and existing Case 1 (orphaned) logic applies unchanged.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
31. fix: address CR analysis findings - context manager, allowBots, SOUL.md sanitization
  
  action_executor.py (PRRT_kwDORrCs9c51ouwm):
    Replace bare open(freeze_path) with context manager to ensure file handle is
    always closed, even if an exception occurs.
  
  openclaw.json:
    Set allowBots:false to prevent bot message loops; operators who need bot
    routing can explicitly enable it per-channel.
  
  SOUL.md:
    Replace hardcoded 'jleechanclaw' project_key with env-var reference
    '${SMARTCLAW_PROJECT_KEY:-YOUR_PROJECT_KEY}' so the public template does
    not expose a private project identifier.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
32. fix: address new CR Major issues from incremental review
  
  openclaw.json:
    Update MiniMax-M2.5 cost config from zeroed placeholders to actual pricing
    (input: $0.15/M, output: $1.20/M per MiniMax platform docs).
  
  SOUL.md:
    Fix stage label mismatch: step 1 incorrectly used --stage2 flag; corrected
    to --stage1 for the first-stage bundle generation command.
  
  action_executor.py:
    - Move log_guidance_sent() call to after successful delivery so failed sends
      are not recorded as delivered (guidance tracking was skew-prone).
    - Wrap check_merge_ready() in try/except with action logging and Jeffrey DM
      on failure; exceptions previously bubbled silently past the log/notify path.
    - Wrap generate_fix_strategies() in try/except with action logging and
      Jeffrey DM on failure; strategy failures now propagate through proper
      channels instead of crashing the execute_parallel_retry path.
    - Switch remaining f-string logger calls to %-style lazy formatting.
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
33. fix: address remaining CR Major issues (8 threads across 5 files)
  
  - monitor-agent.sh: use $SLACK_API_BASE for auth.test and apps.connections.open
  - scripts/doctor.sh: TIMEOUT_CMD resolution before MCP/inference/memory probes; WARN when unavailable
  - scripts/run_tests_with_coverage.sh: replace pnpm with Python pytest equivalents
  - decomposition_dispatcher.py: ThreadPoolExecutor for real max_parallel; write blocked subtask status back
  - test_decomposition.py: update tests for new retry semantics and parallel execution
  - scripts/sym-dispatch.sh + related: create stub scripts referenced in skills/sym/SKILL.md
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
34. fix: address CR CHANGES_REQUESTED - Critical and Major issues
  
  - action_executor.py: fix ActionResult TypeError (lines 570, 685) - was passing error= kwarg that does not exist in dataclass; use details= instead
  - action_executor.py: make _log_action writes best-effort (wrap in try/except)
  - action_executor.py: distinguish kill errors in KillAndRespawnAction - only spawn after confirmed kill or benign already-gone markers; escalate on unexpected kill failures to prevent duplicate sessions
  - decomposition_dispatcher.py: use SubtaskStatus.FAILED enum instead of hardcoded failed string; add explicit import
  - doctor.sh: warn (not fail) on env-backed Slack token references since resolve_secret_ref handles them in the next block
  - doctor.sh: fix wrong OPENCLAW_* env var names in roundtrip fallback; template uses SLACK_BOT_TOKEN, SLACK_APP_TOKEN, HOOKS_TOKEN etc.
  - monitor-agent.sh: read MiniMax baseUrl from config instead of hardcoding the endpoint URL
  - sym-dispatch.sh: escape all dynamic fields via json.dumps before building JSON payloads
  
  Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
35. Resolve merge conflict with main for PR #1

## Files Changed
- `.beads/.gitignore`
- `.beads/config.yaml`
- `.beads/issues.jsonl`
- `.beads/metadata.json`
- `.claude/commands/coderabbit.md`
- `.claude/commands/cr.md`
- `.claude/commands/er.md`
- `.claude/commands/evidence_review.md`
- `.gitleaks.toml`
- `.gitleaksignore`
- `HEARTBEAT.md`
- `Makefile`
- `SOUL.md`
- `TOOLS.md`
- `agent-orchestrator.yaml`
- `docs/GENESIS_DESIGN.md`
- `docs/ORCHESTRATION_RESEARCH_2026.md`
- `docs/ORCHESTRATION_SYSTEM_DESIGN.html`
- `docs/ORCHESTRATION_SYSTEM_DESIGN.md`
- `docs/ZOE_AGENT_SWARM_REFERENCE.md`
- `docs/coderabbit-ping-workflow.md`
- `docs/orchestration-system-justification.md`
- `docs/symphony-runtime-dedupe.md`
- `docs/webhook_runbook.md`
- `enqueue-symphony-tasks.sh`
- `health-check.sh`
- `launchd/ai.agento-manager.plist.template`
- `launchd/ai.ao-pr-poller.plist.template`
- `launchd/ai.openclaw.lifecycle-manager.plist.template`
- `launchd/ai.openclaw.mem0-extract.plist.template`
- `launchd/ai.openclaw.qdrant.plist.template`
- `launchd/ai.openclaw.scheduler.plist.template`
- `launchd/ai.openclaw.webhook.plist.template`
- `monitor-agent.sh`
- `openclaw.json`
- `pyproject.toml`
- `roadmap/AGENTO_GREEN_LOOP_GAPS.md`
- `roadmap/AGENT_REVIEWER_LOOP.md`
- `roadmap/EVIDENCE_REVIEW_SCHEMA.md`
- `roadmap/MEMORY_UPGRADE_PLAN.md`
- `roadmap/MVP_OPENCLAW_AIORCH_MULTI_AGENT.md`
- `roadmap/NATURAL_LANGUAGE_DISPATCH.md`
- `roadmap/ORCHESTRATION_DESIGN.md`
- `roadmap/VALUE_ROUTER_DESIGN.md`
- `run-scheduled-job.sh`
- `scripts/doctor.sh`
- `scripts/install-agento.sh`
- `scripts/install-all.sh`
- `scripts/install-ao-pr-poller.sh`
- `scripts/install-launchagents.sh`
- `scripts/install-mctrl-supervisor.sh`
- `scripts/install-qdrant-container.sh`
- `scripts/install-symphony-daemon.sh`
- `scripts/run_tests_with_coverage.sh`
- `scripts/start-qdrant-container.sh`
- `scripts/sym-dispatch.sh`
- `scripts/sym-send-5-leetcode-hard.sh`
- `scripts/sym-send-5-swebench-verified.sh`
- `scripts/sync-check.sh`
- `skills/agento/SKILL.md`
- `skills/agento_report/SKILL.md`
- `skills/sym/SKILL.md`
- `src/orchestration/__init__.py`
- `src/orchestration/action_executor.py`
- `src/orchestration/anomaly_detector.py`
- `src/orchestration/ao_cli.py`
- `src/orchestration/ao_events.py`
- `src/orchestration/auto_resolve_threads.py`
- `src/orchestration/auto_review_trigger.py`
- `src/orchestration/auto_triage.py`
- `src/orchestration/backup_redaction.py`
- `src/orchestration/bead_lifecycle_validator.py`
- `src/orchestration/code_path_classifier.py`
- `src/orchestration/coderabbit_gate.py`
- `src/orchestration/datetime_util.py`
- `src/orchestration/decomposition_dispatcher.py`
- `src/orchestration/dispatch_task.py`
- `src/orchestration/escalation.py`
- `src/orchestration/escalation_handler.py`
- `src/orchestration/escalation_router.py`
- `src/orchestration/event_util.py`
- `src/orchestration/evidence.py`
- `src/orchestration/evidence_bundle.py`
- `src/orchestration/evidence_review_gate.py`
- `src/orchestration/failure_budget.py`
- `src/orchestration/gh_integration.py`
- `src/orchestration/guidance_tracker.py`
- `src/orchestration/jsonfile_util.py`
- `src/orchestration/lifecycle_reactions.py`
- `src/orchestration/mcp_http.py`
- `src/orchestration/mcp_mail.py`
- `src/orchestration/mctrl_status.py`
- `src/orchestration/merge_gate.py`
- `src/orchestration/openclaw_notifier.py`
- `src/orchestration/outcome_recorder.py`
- `src/orchestration/parallel_retry.py`
- `src/orchestration/path_util.py`
- `src/orchestration/pattern_synthesizer.py`
- `src/orchestration/pr_lifecycle.py`
- `src/orchestration/pr_review_decision.py`

## Review Notes
1. @coderabbitai review

2. @coderabbitai all good?

3. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

4. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 1 --repo jleechanorg/smartclaw --json state,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup,headRefOid

echo ""
ech...

5. @coderabbitai full review

6. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Full review triggered.

</details>

7. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

8. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 1 --repo jleechanorg/smartclaw --json state,mergeable...

9. @coderabbitai all good?

10. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 1 --repo jleechanorg/smartclaw --json state,mergeable...

11. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

12. @coderabbitai review

13. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

14. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 1 --repo jleechanorg/smartclaw --json state,mergeable...

15. @coderabbitai review

16. @coderabbitai all good?

17. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

18. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 1 --repo jleechanorg/smartclaw --json state,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup,headRefOid

echo ""
ech...

19. @coderabbitai all good?

20. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 1 --repo jleechanorg/smartclaw --json state,mergeable...

21. @coderabbitai all good?

22. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 1 --repo jleechanorg/smartclaw --json state,mergeable...

23. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

24. @coderabbitai review

25. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

26. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 1 --repo jleechanorg/smartclaw --json state,mergeable...

27. @coderabbitai all good?

28. @coderabbitai review

29. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

30. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 1 --repo jleechanorg/smartclaw --json state,mergeable...

31. @coderabbitai review

32. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

33. @coderabbitai full review

34. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Full review triggered.

</details>

35. @coderabbitai all good?

36. @coderabbitai review

37. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

38. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 1 --repo jleechanorg/smartclaw --json state,mergeable...

39. @coderabbitai review

40. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

41. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

42. @coderabbitai review

43. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

44. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 1 --repo jleechanorg/smartclaw --json state,mergeable...

45. @coderabbitai review

46. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

47. @coderabbitai approve

48. @coderabbitai all good?

49. @coderabbitai all good?

50. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 1 --repo jleechanorg/smartclaw --json state,mergeable...

51. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
echo "=== PR STATUS ==="
gh pr view 1 --repo jleechanorg/smartclaw --json state,mergeable...

52. @coderabbitai review

53. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

54. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Comments resolved and changes approved.

</details>

55. @coderabbitai all good?

56. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

REPO="jleechanorg/smartclaw"
PR=1

echo "=== PR STATUS JSON ==="
gh pr...

57. @coderabbitai all good?

58. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot]

## ✅ AUTOMATION COMPLETE — [STATUS: NEEDS WORK]

**Verified at commit `c3e17f10` (c3e17f10)**

---

## 📊 Current Status: **ISSUES FOUND** ⚠️

| Cat...

59. @coderabbitai review

60. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

61. @coderabbitai all good?

62. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

63. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

REPO="jleechanorg/smartclaw"
PR=1

summ() {
  echo "---- $1 ----"
}

#...

64. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

REPO="jleechanorg/smartclaw"
PR=1
HEAD_COMMIT="e631db36"

# Ensure we'...

65. @coderabbitai all good?

66. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

`@coderabbit-user`

## ✅ AUTOMATION COMPLETE — [STATUS: NEEDS WORK]

Verified against the latest head of PR `#1`; see script...

67. @coderabbitai full review

68. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Full review triggered.

</details>

69. @coderabbitai all good?

70. @coderabbitai review

71. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

72. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

REPO="jleechanorg/smartclaw"
PR=1

echo "=== PR_STATUS ==="
gh pr view...

73. @coderabbitai all good?

74. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot]

## ✅ AUTOMATION COMPLETE — STATUS: NEEDS WORK

**Verified at commit `e631db36` (e631db366e77471c1e9ae44824dc7b5bd735602d)**

---

## 📊 Current Stat...

75. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

76. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

REPO="jleechanorg/smartclaw"
PR=1
TARGET_COMMIT="004f6153009fe8a55192b...

77. @coderabbitai all good?

78. @coderabbitai review

79. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

80. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

`@coderabbit-user`

## ✅ AUTOMATION COMPLETE — STATUS: NEEDS WORK

**Verified at commit `<current HEAD>` (latest on PR `#1` ...

81. @coderabbit all good?

82. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

REPO="jleechanorg/smartclaw"
PR=1

# PR status
gh pr view "$PR" --repo...

83. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

84. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

REPO="jleechanorg/smartclaw"
PR=1
TARGET_COMMIT="1097f0f021bda14ec012d...

85. @coderabbitai all good?

86. @coderabbit all good?

87. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@github-actions`[bot]

## ✅ AUTOMATION COMPLETE — [STATUS: NEEDS WORK]

**Verified at commit `1097f0f0` (1097f0f021bda14ec012da84531e47912be760b6)**

---

## 📊 Current St...

88. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

REPO="jleechanorg/smartclaw"
PR=1

echo "=== PR_STATUS ==="
gh pr view...

89. @coderabbit-ai @greptileai @bugbot @copilot

**Summary (Review Flow):**
1. Review every outstanding PR comment to understand required fixes and clarifications.
2. Verify that the author has addressed each comment in code or via consolidated response summary.
3. Check for any new bugs, security vulne...

90. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

REPO="jleechanorg/smartclaw"
PR=1
TARGET_COMMIT="622e8aa56d1e87007e16b...

91. @coderabbitai all good?

92. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

`@jleechan2015`

## ✅ AUTOMATION COMPLETE — [STATUS: NEEDS WORK]

**Verified at commit `622e8aa5` (622e8aa56d1e87007e16ba78605d44433071b154)**

---

## 📊 Current Status: *...

93. @coderabbitai all good?

94. @coderabbitai review

95. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

96. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

REPO="jleechanorg/smartclaw"
PR=1
TARGET_COMMIT="622e8aa56d1e87007e16b...

97. @coderabbitai review

98. <!-- This is an auto-generated reply by CodeRabbit -->
<details>
<summary>✅ Actions performed</summary>

Review triggered.

> Note: CodeRabbit is an incremental review system and does not re-review already reviewed commits. This command is applicable only when automatic reviews are paused.

</detail...

99. @coderabbitai all good?

100. <!-- This is an auto-generated reply by CodeRabbit -->
> [!TIP]
> For best results, initiate chat on the files or code changes.

<details>
<summary>🧩 Analysis chain</summary>

🏁 Script executed:
```
#!/bin/bash
set -euo pipefail

REPO="jleechanorg/smartclaw"
PR=1

# 1) PR status
if gh pr view "$PR" ...

