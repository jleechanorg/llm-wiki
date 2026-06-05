# macOS keychain popup multi-source fix + AO skeptic gate ops 2026-06-05

## macOS keychain popup root cause

macOS "A keychain cannot be found to store X" popups have at least 3 independent
headless sources, and ALL of them hit the same authorization right
`system.keychain.create.loginkc`:

1. AO agy workers (Agent Orchestrator / Antigravity)
2. GitHub Actions self-hosted runner CI git operations
3. cmux-codex-approve launchd worker

Because every source converges on the same authorization right, a single
blanket authorization change suppresses the prompt for all of them at once.

## Decisive blanket fix

```
sudo security authorizationdb write system.keychain.create.loginkc allow
```

- Back up the rule first (read the existing rule before overwriting).
- Reversible.
- Persists across reboot.
- Suppresses the prompt for every source simultaneously.

## Per-source fixes (both MERGED)

- AO agy worker: always symlink the session `Library/Keychains` to the real
  `~/Library/Keychains` — agent-orchestrator PR #653.
- CI runner: set `GIT_CONFIG_GLOBAL` to a `ci.gitconfig` that disables the
  osxkeychain credential helper, wired into the runner launchd plist —
  jleechanclaw PR #592. That same PR also added qdrant `--restart unless-stopped`.

## Diagnostic lesson

- `securityd` `-25294` is benign probe noise (observed 863 -> 0 popups); do not
  treat it as the real signal.
- Measure ACTUAL popups via:
  ```
  log show --predicate 'process == "SecurityAgent"'
  ```
- Find the requesting client via:
  ```
  log show --predicate 'process == "authd"' | grep keychain.create.loginkc
  ```

## AO ops

- Killing AO workers breaks the Skeptic Gate: with no verdict-poster, the gate
  hits a 20-minute timeout.
- Killing workers also regresses the agent-antigravity dist, because AO rebuilds
  from the checked-out branch. The durable fix is to MERGE to main.
- Skeptic verdicts can be posted manually:
  ```
  ao skeptic verify -n <PR> -m claude --trigger-sha <sha> --request-id <id>
  ```
  - `--dry-run` previews.
  - `--prompt` scopes evidence to the feasible class (a macOS-GUI fix cannot be
    CI-integration-tested).
- Do NOT commit evidence `.md` files — they trip CodeRabbit and the Evidence
  Gate. Use gists instead.

## mem0 / qdrant ops

- The qdrant container needed `docker update --restart unless-stopped` to survive
  reboots.
- "~/.hermes/hermes.json missing" was a FALSE alarm: the client reads
  `~/.hermes/config.yaml` with fallback defaults.
