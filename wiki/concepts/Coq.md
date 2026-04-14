---
title: "Coq"
type: concept
tags: ["coq", "proof-assistant", "formal-verification", "compcert"]
sources: []
last_updated: 2026-04-14
---

Coq is a general-purpose proof assistant based on the Calculus of Inductive Constructions. It has been used to verify the CompCert verified C compiler and other critical software. Coq's significant contribution is the extraction mechanism: verified Coq programs can be extracted to executable code (OCaml, Haskell, Scheme).

## Key Properties
- **CIC foundation**: Very expressive type theory based on Calculus of Inductive Constructions
- **Verified compiler**: CompCert — a C compiler proven correct in Coq
- **Program extraction**: Verified Coq code can be extracted to executable languages
- **Long history**: Established tool with large user community and extensive libraries

## Connections
- [[ProofAssistant]] — Coq is a specific proof assistant
- [[FormalVerification]] — CompCert is a landmark formal verification project using Coq
- [[Lean]] — Lean's type system is inspired by Coq's

## See Also
- [[ProofAssistant]]
- [[FormalVerification]]
