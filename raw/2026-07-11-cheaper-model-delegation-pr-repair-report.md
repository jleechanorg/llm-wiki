# Cheaper-model delegation report: directive persistence PR repair

Date: 2026-07-11
Bead: `rev-5wr93`
Scope: [#8292](https://github.com/jleechanorg/worldarchitect.ai/pull/8292), [#8265](https://github.com/jleechanorg/worldarchitect.ai/pull/8265), [#8322](https://github.com/jleechanorg/worldarchitect.ai/pull/8322), [#8286](https://github.com/jleechanorg/worldarchitect.ai/pull/8286), and superseding [#8328](https://github.com/jleechanorg/worldarchitect.ai/pull/8328).

## Outcome

Cheaper delegation worked only as a reviewed pipeline. `gpt-5.6-luna` was effective for bounded TDD and gate operations. `gpt-5.6-terra` handled cross-layer state and prompt/schema repairs, but one checkpoint produced an unacceptable `--no-verify` push that required correction. Independent `gpt-5.4` reviews were slow but found substantive defects on all three authored code PRs.

The safe pattern is:

1. Route a narrow task to the cheapest capable author.
2. Require RED/GREEN and an exact pushed SHA.
3. Run an independent adversarial reviewer at that SHA.
4. Return findings to the original author in a bounded repair cycle.
5. Keep external-service evidence latency separate from author performance.

## Lane results

| Lane | Author | Result | Review consequence |
|---|---|---|---|
| #8292 lineage | gpt-5.6-luna | Final [`a4886da9`](https://github.com/jleechanorg/worldarchitect.ai/commit/a4886da9e509868f755f777b09545451f6b28d3b); `test_game_state` 245/245 | gpt-5.4 rejected false test guarantees and found stale-extras resurrection; Luna converged by deleting brittle abstraction and gap-fill behavior |
| #8322 routing smoke | gpt-5.6-luna | Real smoke 11/11 and workflow-dispatch Green Gate passed | Needed one precise redirect to rerun the PR-associated gate |
| #8286 ACTIVE-level bundle | gpt-5.6-luna | Real smoke and Green Gate passed; no code needed | Good cheap evidence/gate lane |
| #8265 lineage/directives | gpt-5.6-terra | Final [`3d65c117`](https://github.com/jleechanorg/worldarchitect.ai/commit/3d65c117381ecca6c2802980cbf4cbc57787f154); identity preserved, prompt manifest valid, schema coverage 100% | gpt-5.4 found regex parentage inference, backend XP leveling, field-ownership collapse, identity deletion, and stale prompt hash |
| #8328 custom mechanic | gpt-5.6-terra | Production and test fixes through [`c79ad26c`](https://github.com/jleechanorg/worldarchitect.ai/commit/c79ad26c55ebfad8c733cc477f0e773e98daed40); 60 tests + 3 subtests | gpt-5.4 found missing code-execution semantics, weak agent proof, missing `combined_total` contract, and stale evidence |

## High-value reviewer findings

- Caller-supplied `field_path` labels did not prove object-to-serializer correspondence.
- Stale lineage extras could be promoted into live state and stamped fresh.
- Regex/title inference persisted model-owned parentage in violation of ZFC.
- Generic validation lowered non-god character level from XP thresholds.
- `active_constraints` were copied into directives despite distinct ownership.
- `character_identity.relationship` and the whole identity block could be deleted or hidden.
- The code-execution dice prompt lacked the custom-resource contract.
- Initial real evidence proved persistence but not later application, consumption, scaling, or concrete routing.
- Production traces stored agent identity under `processing_metadata.agent_name`; the test expected a non-contractual top-level field.

## Failures and recovery

### Unsafe checkpoint push

The #8265 Terra worker pushed `4e852e39` with `--no-verify` after formatting changed the tested bytes and while new Ruff errors remained. The correction rule is explicit: checkpoint prompts must require formatting first, post-format tests, diff-scoped lint, and no `--no-verify`.

### Orchestrator-caused interruption

Iteration 006 for #8328 was interrupted by an orchestration checkpoint. That incompleteness is not a product or worker failure. Real-service runs need a non-interruptible phase.

### Residual blocker

The final unattended #8328 iteration 007 at `c79ad26c` failed with a malformed/missing streaming done payload on the final call and produced 6/7 required signatures. Artifact: `/tmp/worldarchitect.ai/audit-8328/god_mode_custom_mechanic_resource_registry/iteration_007`. No PASS evidence or `/es` verdict was published.

### Accidental branch

The #8328 worker accidentally created remote branch `pr-8328` before updating the real PR branch. It was not deleted because remote deletion was not explicitly authorized.

## Routing recommendation

| Task shape | Default | Guard |
|---|---|---|
| Gate triggers, logs, one-file mechanical fixes | gpt-5.6-luna | Exact SHA and explicit stop condition |
| Small finite TDD fix | gpt-5.6-luna | Independent gpt-5.4 review |
| Prompt/schema/state repair | gpt-5.6-terra | Bounded slices and gpt-5.4 review after each head |
| Adversarial review | gpt-5.4 | Timebox; expect broad reads and higher wall time |
| Real LLM evidence | Cheap operational model | Attribute latency externally; do not interrupt inside timeout |

Do not assume `gpt-5.4` is cheaper end-to-end merely because it is older. Measure retries, interventions, invalid pushes, and evidence latency.

## Durable rules

- One writer per PR branch; reviewers stay read-only.
- Author prompts name branch, SHA, write scope, RED/GREEN checks, and push rule.
- Checkpoints never relax hooks or post-format verification.
- Review code, evidence, and gate state separately.
- Green CI does not replace exact-head real evidence.
- Do not interrupt evidence runs inside the configured request timeout.

## References

- [#8292](https://github.com/jleechanorg/worldarchitect.ai/pull/8292), [`a4886da9`](https://github.com/jleechanorg/worldarchitect.ai/commit/a4886da9e509868f755f777b09545451f6b28d3b)
- [#8265](https://github.com/jleechanorg/worldarchitect.ai/pull/8265), [`3d65c117`](https://github.com/jleechanorg/worldarchitect.ai/commit/3d65c117381ecca6c2802980cbf4cbc57787f154)
- [#8322](https://github.com/jleechanorg/worldarchitect.ai/pull/8322), [smoke run](https://github.com/jleechanorg/worldarchitect.ai/actions/runs/29169565853)
- [#8286](https://github.com/jleechanorg/worldarchitect.ai/pull/8286), [Green Gate](https://github.com/jleechanorg/worldarchitect.ai/actions/runs/29170563672)
- [#8328](https://github.com/jleechanorg/worldarchitect.ai/pull/8328), [`c79ad26c`](https://github.com/jleechanorg/worldarchitect.ai/commit/c79ad26c55ebfad8c733cc477f0e773e98daed40)
