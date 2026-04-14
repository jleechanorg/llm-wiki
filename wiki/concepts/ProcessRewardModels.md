---
title: "Process Reward Models"
type: concept
tags: [PRM, process-reward, step-level-feedback, reasoning, LLM-training, outcome-supervised]
sources: [extended-reasoning-frontier, formal-verification-frontier]
last_updated: 2026-04-14
---

## Summary

Process Reward Models (PRM) train a reward signal at the level of individual reasoning steps rather than on the final outcome. Where [[ExtendedThinking]] allocates a reasoning budget to think longer, PRM actively discriminates between good and bad reasoning steps, guiding the model toward correct intermediate states. This is the key enabling technology behind OpenAI's <o1/o3/o4> "草莓" (strawberry) reasoning pattern.

## Key Claims

### Why Outcome Supervision Is Insufficient
- Final-answer supervision cannot teach the model to "think step-by-step correctly"
- A model can reach a correct answer via flawed reasoning and still get rewarded
- Step-level errors compound: wrong intermediate state → wrong final answer

### How PRM Works
1. Train a discriminator to rate each step in a reasoning chain
2. Use step-level scores to penalize reasoning paths that go wrong early
3. The reward signal propagates backward: bad early steps reduce probability of good entire paths
4. At inference time, beam search over reasoning steps guided by PRM scores

### PRM vs Outcome Reward Models (ORM)

| Aspect | ORM (Outcome) | PRM (Process) |
|--------|--------------|--------------|
| Signal | Final answer correct/incorrect | Each step rated |
| Training signal | Sparse (only at end) | Dense (every step) |
| Handles early errors | No — wrong path can still reach correct answer | Yes — penalize at first bad step |
| Sample efficiency | Lower | Higher |

### Connection to Extended Thinking

PRM provides the step-level grounding that makes [[ExtendedThinking]] more efficient:
- Without PRM: model explores reasoning paths uniformly
- With PRM: model prunes bad reasoning paths early, focusing compute where it matters
- o1/o3/o4 reportedly use PRM-style signals to allocate their extended thinking budget

### Key Papers
- **Process Reward Model (Lightman et al., 2023)** — shows PRM outperforms ORM on math reasoning
- **GRM (Generalist Reward Model)** — scales PRM to general domains

## Connections

- [[ExtendedThinking]] — PRM is what makes extended thinking efficient
- [[ReasoningBudget]] — PRM helps allocate reasoning budget to the right paths
- [[SelfCritique]] — PRM can be viewed as automated step-level critique
- [[VerificationLoop]] — PRM provides the internal verification signal before external tests
- [[TestTimeCompute]] — PRM enables smarter allocation of test-time compute

## See Also

- [[SelfCritique]] — manual step-level critique (human or LLM)
- [[ExtendedThinking]] — where PRM signals are consumed at inference time
- [[DeterministicFeedbackLoops]] — PRM as an automated feedback signal
