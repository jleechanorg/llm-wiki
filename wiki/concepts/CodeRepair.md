---
title: "CodeRepair"
type: concept
tags: ["code-repair", "bug-fixing", "self-correction", "debugging"]
sources: []
last_updated: 2026-04-14
---

Code Repair is the application of fixes after [[ErrorDetection]] has identified a bug. It is step 2 of the [[SelfDebugging]] pipeline (Detect → Diagnose → Repair).

## Key Properties
- **Root cause focused**: Good repairs fix the root cause, not just the symptom
- **Requires understanding**: Model must understand why the error occurred, not just what the error was
- **Test-driven repair**: After repair, re-running tests validates the fix
- **Part of [[VerificationLoop]]**: Repair + verification is the core loop

## Connections
- [[SelfDebugging]] — code repair is the repair step in self-debugging
- [[ErrorDetection]] — error detection feeds the repair process
- [[VerificationLoop]] — code repair is followed by verification
- [[Reflexion]] — Reflexion memory helps avoid repeating the same repairs

## See Also
- [[SelfDebugging]]
- [[ErrorDetection]]
