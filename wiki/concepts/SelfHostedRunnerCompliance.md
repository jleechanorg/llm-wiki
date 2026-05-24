---
title: "Self-Hosted Runner Compliance"
type: concept
tags: [github-actions, billing, self-hosted-runner, launchd, compliance]
---

Enforcement mechanisms and patterns used to mandate free self-hosted runners by default for private repositories, preventing metered billing charges and resource policy drift.

## Compliance Pattern

In private GitHub organizations (e.g. `jleechanorg`), metered GitHub Actions billing charges can accumulate quickly when workflow files hardcode standard GitHub-hosted Linux or macOS runners (`ubuntu-latest`).

To prevent this policy drift:
1. **Dynamic Selector baseline**: Target the repository/organization shared self-hosted selector by default:
   ```yaml
   runs-on: ${{ fromJson(vars.SELF_HOSTED_RUNNER_LABELS || '["self-hosted","self-hosted-mikey"]') }}
   ```
2. **Selective Exemptions**: Quick/lightweight jobs that execute in seconds may run on standard runners only if explicitly annotated with `# APPROVED_EXCEPTION` on the `runs-on:` line:
   ```yaml
   runs-on: ubuntu-latest # APPROVED_EXCEPTION
   ```

## Daily Compliance Scanner Daemon

To prevent future policy drift, a daily compliance scanner is installed as a macOS `launchd` daemon.

* **Script**: `/Users/jleechan/worldarchitect.ai/self-hosted-oss/scan_runner_violations.py`
  This script scans specified repositories, parses `.github/workflows/*.yml` for `runs-on:` declarations, and checks for compliance with the self-hosted default or approved exceptions.
* **LaunchAgent Plist**: `/Users/jleechan/worldarchitect.ai/self-hosted-oss/com.jleechanorg.runner_violations_scanner.plist`
  Loaded into `~/Library/LaunchAgents/` and scheduled to trigger daily at 9:00 AM. It issues a native macOS notification on policy violation.

## Related

- [[SelfHostedRunnerNaming]] — name prefix matching Docker container names
- [[InstallScriptIdempotency]] — making installer scripts idempotent for `.env` files
- [[GitHubActionsMeteredCost]] — metered billing cost drivers
