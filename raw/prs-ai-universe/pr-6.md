# PR #6: Extend model timeouts to three minutes

**Repo:** jleechanorg/ai_universe
**Merged:** 2025-09-19
**Author:** jleechan2015
**Stats:** +235/-212 in 10 files
**Labels:** codex

## Summary
- raise the default LLM runtime timeouts to three minutes
- ensure the second opinion agent uses the runtime-configured three-minute limit for every model call
- update integration tests and docs/testing guides to reflect the longer timeout window

## Raw Body
## Summary
- raise the default LLM runtime timeouts to three minutes
- ensure the second opinion agent uses the runtime-configured three-minute limit for every model call
- update integration tests and docs/testing guides to reflect the longer timeout window

## Testing
- npm --prefix backend run lint
- npm --prefix backend run type-check

------
https://chatgpt.com/codex/tasks/task_e_68ccaf65136c832fa2eb52933b9596d9

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->
## Summary by CodeRabbit

- **New Features**
  - Default model timeouts increased to 3 minutes with unified, graceful timeout fallbacks and standardized timeout signaling.
  - Plan-based, staggered secondary-opinion requests (1–4) for faster, more reliable responses; primary/secondary responses report per-model status, tokens, cost, and errors.
  - Added centralized input sanitization and optional delayed model invocation; streaming/tool outputs adapted to new timeout/response semantics.
  - Support for cancelling in-flight model requests.

- **Documentation**
  - Endpoint and testing docs updated to reflect 3-minute timeouts and behavior.

- **Tests**
  - Integration tests and test cases extended to 3-minute limits and adjusted success thresholds.
<!-- end of auto-generated comment: release notes by coderabbit.ai -->
