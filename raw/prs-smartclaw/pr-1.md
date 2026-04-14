# PR #1: [agento] docs: add WIP README + install bootstrap script

**Repo:** jleechanorg/smartclaw
**Merged:** 2026-03-29
**Author:** jleechan2015
**Stats:** +55306/-0 in 186 files

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
Adapting content from private jleechanorg/jleechanclaw harness for public smartclaw repo. Content sanitized to remove secrets/IDs.

## Test Plan
- [x] All files committed
- [x] Branch pushed to smartclaw
- [x] PR updated

🤖 Generated with Claude Code

<!-- This is an auto-generated comment: release notes by coderabbit.ai -->

## Raw Body
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
Adapting content from private jleechanorg/jleechanclaw harness for public smartclaw repo. Content sanitized to remove secrets/IDs.

## Source References
- jleechanclaw docs/HARNESS_ENGINEERING.md - Harness engineering philosophy
- jleechanclaw roadmap/ORCHESTRATION_DESIGN.md - Orchestration architecture
- jleechanclaw openclaw.json.redacted - Config template
- jleechanclaw agent-orchestrator.yaml - Orchestrator config

## Changes

### README.md (updated - now main doc)
- Explicit WIP/prototype warning
- Architecture diagram from ORCHESTRATION_DESIGN.md
- Harness engineering principles from HARNESS_ENGINEERING.md
- Comparison: smartclaw vs Agent-Orchestrator
- Dependencies, prerequisites, quickstart, security notes
- Links to all template files

### docs/HARNESS_ENGINEERING.md (new)
- Full harness engineering philosophy
- Four layers: Agent Environment, Feedback Loops, LLM Judgment, Entropy Management
- Five key principles
- Maturity model from NxCode framework

### roadmap/ORCHESTRATION_DESIGN.md (new)
- The Stack architecture
- Deterministic First, LLM for Judgment principle
- Webhook ingress pipeline
- Escalation routing
- Parallel retries
- Failure budgets
- Autonomous PR review
- Memory integration

### openclaw.json (new template)
- Runtime configuration template
- Sanitized from jleechanclaw version
- Uses environment variables for secrets

### agent-orchestrator.yaml (new template)
- Agent orchestrator config template
- Sanitized from jleechanclaw version
- Includes example agent rules

### install.sh (kept)
- Safe, idempotent bootstrap script

## Test plan
- [x] All
