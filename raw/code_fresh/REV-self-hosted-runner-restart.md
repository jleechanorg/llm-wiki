# Self-Hosted Runner Restart Reliability

**Status:** IN_PROGRESS
**Priority:** P1
**Component:** self-hosted runner infrastructure
**Created:** 2026-02-21
**Type:** task
**Labels:** runner, ci, launchd, crontab

## GOAL
Ensure the self-hosted GitHub Actions runner (`claude-drift-runner`) auto-recovers and stays online after macOS restarts.

## MODIFICATION
- Define and keep the `launchd` configuration for `claude-drift-runner` as source-of-truth auto-start.
- Add crontab-based restart guard on reboot to enforce `~/actions-runner/svc.sh start` if needed.
- Confirm that all runner registrations are restarted/re-attributed correctly after reboot.
- Add/adjust monitoring notes/log checks so repeated session conflicts are handled as expected.

## NECESSITY
Runner was observed to come up offline after machine restart even after manual launchd setup, blocking PR CI checks until intervention.

## INTEGRATION PROOF
- Crontab reboot recovery path added via `self-hosted/scripts/restart-on-reboot.sh` and wired by `self-hosted/scripts/setup-github-runner-redundant.sh`.
- Monitor restart logic updated with lock, conflict cooldown, and explicit run-loop in `self-hosted/scripts/monitor.sh`.
- Documentation updated in `self-hosted/scripts/README-crontab.md` to include reboot recovery and updated redundancy layers.
- Next step: run the setup script on target macOS runner once to validate end-to-end boot recovery before closing.
