---
title: "Slow-CI Operator Directive (2026-08-16)"
type: concept
tags: [ci, operator-directive, escape-hatch, dark-factory, /green]
date: 2026-08-17
last_updated: 2026-08-17
sources:
  - /Users/jleechan/llm_wiki/raw/feedback_2026-08-17_factory_gh_token_and_poll_cadence.md
---

## Definition
An operator-issued directive (2026-08-16) that explicitly **reverses** the older "never a CI replacement" rule for the dark-factory repo. When any CI check has been queued or pending for **more than 10 minutes**, running the local equivalent is **MANDATORY and needs no authorization**.

## The rule
> "The moment any check has been queued/pending >10 minutes, running the local equivalent is MANDATORY and needs no authorization — never wait, never ask. It is a violation to report 'CI is queued/pending' in a status update unless local equivalents have already been run and their results are in that same update. 'Waiting on CI' is not a status."
>
> "Local results SATISFY `/green` Gate 1 when CI is backlogged — operator directive 2026-08-16, reversing the old 'never a CI replacement' wording, which was wrong."
>
> — `~/.claude/CLAUDE.md` "Slow/backlogged CI runners — run locally + post proof, don't just wait"

## How to apply
1. **Wait timer starts the moment a check enters queued/pending.** Don't sleep-then-check — set a 10-minute alarm.
2. **At 10 minutes**, run the local equivalent. Don't ask the user for permission — the directive authorizes this.
3. **Post the proof**: which checks were local vs CI, what passed/failed, what the local run's exit code was.
4. **Declare green and proceed**. Do not block on a queued runner.
5. **Report local failures immediately**, before finishing the sweep. Don't bury a local fail under "CI is still pending".

## What counts as a "local equivalent"
Mirror the workflow's actual commands. For example:
- `pytest tests/test_X.py` for the `test` job (mirror `Run tests` step).
- `cargo test --release` for `daemon-tests`.
- `bin/conformance validate` for `conformance`.
- For the Evidence Gate, the local equivalent is the dual-signal check (`**Evidence**: <gist-url>` marker present + gist content verification).
- For self-hosted runner selector drift, the local equivalent is comparing `vars.SELF_HOSTED_RUNNER_LABELS` against the live `gh api /orgs/.../runners`.

Don't run something cheaper than CI — match the workflow's actual scope, otherwise the local proof isn't comparable.

## When this fired in practice
[[PR #651]] (2026-08-17): self-hosted runners queued >10 min on a rebase from `a39572417f → 23edb52f`. Local proof:
- `test_conformance_validate_walker_skips_underscore_dot_libraries` — PASS (after the `pipelines/slim/ready.dot` `level5="true"` drop).
- `cargo test --release` — PASS (exit 0).
- Pre-existing flake: `test_ao_sandbox::test_codergen_ao_spawn_args_are_sandboxed` — FAIL on `origin/main` itself, NOT caused by the PR.

Declared green based on local proof, posted the diff, merged.

## Why this exists
The CI backlog was burning ~10-25 minutes per PR cycle, blocking all factory intake work. The older "never a CI replacement" rule was historically correct for catching CI infra drift, but in practice it just made sessions stall when runners were saturated. The operator directive inverts the default: trust local proof unless CI specifically shows a problem.

## Failure modes
- **Local equivalent diverges from CI**: if local passes but CI fails for a non-flake reason (e.g. CI uses a different Node version, different OS), the local proof is invalid — surface the discrepancy.
- **10-minute timer not respected**: if you start running local after only 2 minutes of CI queue, you're not following the directive.
- **Don't try to "fix" the CI backlog**: the directive is an escape hatch, not a license to investigate CI infra unless CI is failing on the user's machine.

## Related
- [[Dark Factory]] — the repo where this applies.
- [[Evidence Gate Dual-Signal Contract]] — the gate that, combined with this directive, makes `/green` achievable on a backlogged runner.
- [[PR #651]] — squash-merged using this directive.
- `~/.claude/CLAUDE.md` — source-of-truth policy.