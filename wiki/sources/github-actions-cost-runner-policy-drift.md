---
title: "GitHub Actions Cost Root-Caused to Runner Policy Drift"
type: source
tags: [github-actions, self-hosted-runner, launchd, subagents, graphql, rest-api]
date: 2026-05-24
source_file: https://github.com/jleechanorg/worldarchitect.ai/pull/7000
bead: rev-0qn8f
---

## Summary

A sudden metered billing charge and 100% budget consumption for the `jleechanorg` organization led to an investigation. While self-hosted runners are used extensively, standard paid GitHub-hosted standard Linux runners (`actions_linux` SKU) were still accumulating massive metered charges. The root cause was policy drift across four repositories that hardcoded standard GitHub runners (`ubuntu-latest`) instead of using the organization's private repo self-hosted default. This was concurrently resolved across all repositories using parallel subagents and parallel `/green` validation, and a daily `launchd` compliance scanner was established to prevent future policy drift.

This learning does not affect [[jeffrey-oracle]].

## Root Cause & Technical Details

1. **Metered Charges**: Analysis of the monthly Actions CSV report showed **144,197 minutes** of standard GitHub-hosted Linux runners (`actions_linux`) consumed in May 2026, creating $385.42 in billed charges. At the same time, **179,614 minutes** of self-hosted Linux and **5,230 minutes** of self-hosted macOS ran for exactly **$0.00**.
2. **Policy Drift**: The organization's private repo baseline mandates self-hosted runners by default:
   `runs-on: ${{ fromJson(vars.SELF_HOSTED_RUNNER_LABELS || '["self-hosted","self-hosted-mikey"]') }}`
   However, multiple workflow files had drifted from this policy and hardcoded standard GitHub runners (`ubuntu-latest`).
3. **Primary Drivers**:
   * **`worldarchitect.ai` @ `.github/workflows/test.yml`**: Alone responsible for **55.0% of the entire organization's bill** ($212.44) due to a conditional that explicitly forced standard runners for the heavy `core-tests` and `scripts` matrix groups.
   * **`worldarchitect.ai` @ `.github/workflows/design-doc-gate.yml`**: Responsible for **14.8%** of the bill ($57.26).
   * Gate/compliance workflows in `jleechanclaw` and `worldai_claw` were also hardcoded to `runs-on: ubuntu-latest`.

## Resolutions Applied

1. **Parallel Subagents**: Spawned four parallel `self` subagents concurrently to apply self-hosted runs-on updates across four separate git repositories:
   * **`worldarchitect.ai`**: [PR #7000](https://github.com/jleechanorg/worldarchitect.ai/pull/7000) (Merged)
   * **`agent-orchestrator`**: [PR #593](https://github.com/jleechanorg/agent-orchestrator/pull/593) (Merged)
   * **`worldai_claw`**: [PR #248](https://github.com/jleechanorg/worldai_claw/pull/248) (Merged)
   * **`jleechanclaw`**: [PR #590](https://github.com/jleechanorg/jleechanclaw/pull/590) (Merged)
2. **Parallel `/green` Verification**: Spawned four parallel green-validation subagents to monitor the active CI pipelines, address review feedback, bypass API rate limits using the REST API fallback, and successfully bring all four pull requests to verified green status concurrently.
3. **Human MERGE APPROVED Phase-Gate**: Once human authorization `MERGE APPROVED` was supplied, squash-merged all four PRs and deleted their remote branches.
4. **Daily launchd Compliance Scanner**:
   * Script: `/Users/jleechan/worldarchitect.ai/self-hosted-oss/scan_runner_violations.py`
   * Plist: `/Users/jleechan/worldarchitect.ai/self-hosted-oss/com.jleechanorg.runner_violations_scanner.plist` (Loaded to `~/Library/LaunchAgents/` scheduled daily at 9:00 AM).
   * **Approved Exceptions**: Supported selective exemptions of quick/lightweight workflows (e.g. `doc-size-check.yml`) by appending `# APPROVED_EXCEPTION` on the `runs-on:` line, keeping the compliance scanner clean.

## Key Learnings & Reusable Patterns

1. **Concurrency over Sequentiality**: Spawning specialized parallel subagents for independent repository work is highly efficient. Concurrently processing multiple repository optimizations and pipeline verifications reduces turnaround time significantly.
2. **git-header Stdin Blocking**: Running `git-header.sh` in non-interactive background tasks will hang indefinitely waiting for stdin `cat` unless stdin is explicitly redirected (e.g. `< /dev/null`). Always execute it with closed stdin inside automated or background runners.
3. **GraphQL REST API Fallback**: Always switch immediately to `gh api` REST endpoints when `GraphQL: API rate limit already exceeded` errors occur to avoid locking the validation pipeline.

## Connections

- [[SelfHostedRunnerCompliance]] — monitoring and enforcement patterns for private repositories.
- [[git-header-stdin-blocking]] — technical detail of closed-stdin execution.
- [[GraphQLRestFallback]] — GitHub API rate limit recovery.
