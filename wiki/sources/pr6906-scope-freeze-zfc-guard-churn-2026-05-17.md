# PR6906 Scope Freeze Before ZFC Guard Churn

## Summary

PR https://github.com/jleechanorg/worldarchitect.ai/pull/6906 demonstrates a level-up/ZFC failure mode: a prompt-first cleanup can turn into a multi-day guard-retention and evidence-chasing branch unless scope is frozen early.

At fresh head `c7de608fcb4d8b7039dcaab43202c21bc64ce5b4`, the PR had 49 changed files and +4311/-767. The latest local guard-proof bundle inspected was still anchored at `853cca3261287cba866d75a1719204a24687aad9`, showing how quickly evidence became corroborating rather than exact-head proof.

## Rule

Freeze or split a level-up/ZFC PR when any of these appear:

- retained backend semantic correction guards;
- tests that assert retained guard behavior;
- repeated evidence reruns after head movement;
- opaque choice-ID migration work inside an originally narrow fix;
- CI/doc automation changes mixed with runtime behavior changes.

The narrow PR should carry only prompt/schema/root-cause fixes plus deletion of guards proven unnecessary. Migration, telemetry, harness enforcement, and CI/doc automation should move to follow-up PRs.

## Related Concepts

- [[ZFC-Level-Up-Architecture]]
- [[OpaqueChoiceIdContract]]
- [[AgentDrift]]

## References

- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/6906
- Fresh reviewed head: `c7de608fcb4d8b7039dcaab43202c21bc64ce5b4`
- Evidence path: `/tmp/worldarchitect.ai/worktree_level_choices/pr6906_guard_proof/iteration_001/metadata.json`
- Evidence SHA found there: `853cca3261287cba866d75a1719204a24687aad9`
- Bead: `rev-46450`

## Jeffrey Oracle

Does not affect `[[jeffrey-oracle]]`.
