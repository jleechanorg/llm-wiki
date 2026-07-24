---
title: InstallScriptIdempotency
type: concept
tags: [bash, install-script, idempotency, env-file, launchd]
date: 2026-05-04
---

## Definition

`install.sh` scripts that modify `.env` or config files must be idempotent — running them multiple times must produce the same result as running them once.

## Pattern

Use `grep -q` to check if a key exists, then `sed -i ''` to update it in-place:

```bash
_ensure_env() {
  local key="$1" value="$2" env_file="$3"
  if ! grep -q "^${key}=" "$env_file" 2>/dev/null; then
    printf '\n%s\n' "$key=$value" >> "$env_file"
  else
    sed -i '' "s|^${key}=.*|${key}=${value}|" "$env_file"
  fi
}
_ensure_env "RUNNER_NAME_PREFIX" "${RUNNER_NAME_PREFIX:-org-runner}" "$INSTALL_DIR/.env"
```

**Never** use `echo >> "$env_file"` unconditionally — that appends on every run and corrupts the file.

## Bootout Error Handling

```bash
# WRONG — || true silences failures
launchctl bootout "gui/$(id -u)/${OLD_LABEL}" 2>/dev/null || true

# RIGHT — explicit success/failure messaging
if launchctl bootout "gui/$(id -u)/${OLD_LABEL}" 2>/dev/null; then
  echo "  Booted out: ${label}"
else
  echo "  WARN: bootout failed for ${label} (may not be loaded)"
fi
```

## Connected Concepts

- [SelfHostedRunnerNaming](SelfHostedRunnerNaming.md) — naming must stay consistent across re-runs
- [Launchd](Launchd.md) — launchd plist installation

## Update 2026-06-27 — deterministic installer smoke

An installer smoke test must prove installation mechanics, not product correctness. In dark-factory, `install.sh` already used `uv` for `uv python install`, `uv venv`, and `uv pip install`, but its default smoke used `pipelines/factory/hello.dot`, which can fail on sealed holdout evaluation even when installation is correct.

Fix pattern: use a deterministic no-LLM/no-holdout graph for installer smoke. The dark-factory installer now uses `pipelines/parallel_demo.dot` with `--backend echo`, and `./install.sh --no-link --no-cmds` verified `final_outcome: success`.

Source: [Dark Factory reviewer/output/evidence contract and deterministic install smoke](../sources/project-2026-06-27-dark-factory-reviewer-output-evidence-contract.md).
