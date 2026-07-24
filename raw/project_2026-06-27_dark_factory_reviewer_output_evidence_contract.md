---
name: Dark Factory reviewer/output/evidence contract and deterministic install smoke
description: Dark Factory nodes must pass rich artifacts forward, reviewer parallelization must preserve independent outputs, and install.sh smoke must test installation deterministically.
type: project
bead: jleechan-7f3
---

# Dark Factory Reviewer/Output/Evidence Contract

On 2026-06-27, dark-factory was updated and merged to `origin/main` at commit `9f854a8c238dfeafbf164904e8993236a2b61aed` (`https://github.com/jleechanorg/dark-factory/commit/9f854a8c238dfeafbf164904e8993236a2b61aed`).

The operator concern was that reviewer/evidence nodes could behave like status-token parsers instead of LLM-to-LLM communicators. The durable rule is: pipeline status is control flow only; the semantic handoff is the full free-form output plus artifact references.

Implemented changes:

- `/f`, `/fs`, and `/factory` require binary invocation proof blocks.
- Evidence envelopes are mandatory by default under `evidence/<run-id>/`.
- Full node outputs and transcript refs are handed downstream; previews are bounded only as previews.
- Shadow Codex review defaults on and remains opt-out.
- Redundant raw Codex reviewer tool nodes were replaced with `type="parallel_reviewer"` where appropriate.
- `install.sh` already used `uv`; its default smoke changed from sealed-holdout `pipelines/factory/hello.dot` to deterministic no-holdout `pipelines/parallel_demo.dot`.
- `requirements.lock` is committed and mandatory; `install.sh` fails closed if it is missing instead of falling back to mutable `requirements.txt`.

Verification:

- Merged-main focused pytest suite: `186 passed`.
- Independent Codex Spark reviews: no blockers.
- `origin/main` verified at `9f854a8c238dfeafbf164904e8993236a2b61aed`.
- `./install.sh --no-link --no-cmds` passed with `uv 0.9.13` and wrapper smoke `final_outcome: success`.
- Temp-copy negative test without `requirements.lock` failed with `RC=1` and `ERROR: requirements.lock not found.`

Reusable pattern: statuses route; rich outputs explain. Install smokes prove installation, not hidden product holdouts.
