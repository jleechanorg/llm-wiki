# PR #7: feat(proxy): add cerebras provider mode

**Repo:** jleechanorg/codex_plus
**Merged:** 2025-09-26
**Author:** jleechan2015
**Stats:** +69/-1 in 1 files
**Labels:** codex

## Summary
(none)

## Raw Body
## Goal
- allow the proxy control script to run using Cerebras credentials when requested

## Modifications
- added global `--cerebras` flag parsing and provider-mode bookkeeping in `proxy.sh`
- ensured Cerebras environment variables are validated and exported to the proxy runtime
- surfaced the active provider in status output and documented the new option in the help text

## Necessity
- the proxy needs a Cerebras launch mode so it can be pointed at Qwen Coder via Cerebras without rewriting environment variables manually

## Integration Proof
- `bash -n proxy.sh`
- `./proxy.sh --help`


------
https://chatgpt.com/codex/tasks/task_e_68d4f50783c0832f87b4162b86975c1d
