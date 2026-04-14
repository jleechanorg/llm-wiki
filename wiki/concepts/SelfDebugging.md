---
title: "Self Debugging"
type: concept
tags: [self-debugging, self-repair, self-fix, autonomous-fix]
sources: [formal-verification-frontier]
last_updated: 2026-04-14
---

## Summary

Self Debugging is the capability of an AI model to autonomously diagnose and fix bugs in its own code. It combines self-critique (identifying that something is wrong), error detection (localizing the problem), and code repair (producing and validating the fix) into a single closed-loop process. Self-debugging goes beyond self-critique in that it does not merely identify problems but actively generates, tests, and validates corrections. This is the mechanism that enables truly autonomous code repair in advanced coding harnesses.

## Key Claims

- Self-debugging requires three sub-capabilities: error localization (identifying which part of the code is faulty), root cause analysis (understanding why it is faulty), and fix generation (producing corrected code)
- Compared to self-critique, self-debugging adds the active fix-and-validate loop — it does not stop at identifying problems
- Self-debugging systems can be built as multi-turn agent loops where the model is the executor, critic, and debugger simultaneously
- Verified codebases (see [[FormalVerification]]) provide a reliable ground truth that makes self-debugging more reliable: the model can use the specification as a target for its fixes
- Research on self-debugging in code generation (Chen et al., 2023; Ding et al., 2024) shows measurable improvement in bug fix success rates, particularly for stack-trace-driven debugging

## Connections

- [[SelfCritique]] — self-debugging subsumes self-critique: critique identifies problems, debugging fixes them
- [[AdversarialTesting]] — adversarial testing finds the bugs that self-debugging then fixes
- [[VerificationLoop]] — self-debugging is the "fix" stage in a verification loop, preceded by verification and adversarial attack
- [[SkepticGate]] — skeptic gates can trigger self-debugging passes when verification fails
- [[AgenticCoding]] — self-debugging is the natural extension of agentic coding for post-generation refinement
- [[HarnessEngineering]] — a harness implementing self-debugging requires robust error capture and re-execution infrastructure

## Relationships to Other Concepts

Self-debugging is the most sophisticated member of the self-repair family. A [[HarnessEngineering]] effort implementing self-debugging would typically layer it on top of [[ExtendedThinking]] (for root cause analysis) and [[ReasoningBudget]] (to allow sufficient compute for complex debugging sessions).

## See Also
- [[ErrorDetection]]
- [[CodeRepair]]
- [[Reflexion]]
