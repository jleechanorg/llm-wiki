---
title: "Compiler Verification"
type: concept
tags: [compiler-verification, verified-compilers, Coq, Isabelle, CakeML, CompCert]
sources: []
last_updated: 2026-04-14
---

## Summary

Compiler Verification is the application of formal verification techniques to prove that a compiler correctly translates source programs to semantically equivalent target programs. It is a mature subdomain of formal verification where compilers like CompCert (Coq-verified C compiler) and CakeML (Verifiable ML compiler framework) have achieved production use. Compiler verification serves as the inspiration for verifying the entire software toolchain — if the compiler is proven correct, bugs in compiled code can only come from the source.

## Key Claims

- **Semantic preservation**: A verified compiler guarantees that the compiled output has exactly the same behavior as the source program for all inputs in the specified semantics
- **Proof burden**: Verified compilers require significant proof effort but eliminate an entire class of bugs (compiler-induced incorrectness)
- **Production use**: CompCert is used by Airbus for safety-critical embedded C code compilation
- **CakeML**: A complete compiler stack from parsed source to machine code, all with formal guarantees
- **Connection to AI coding**: Verified compilers could provide end-to-end guarantees for AI-generated code when combined with autoformalization

## Connections

- [[FormalVerification]] — compiler verification is a specific application domain of formal verification
- [[ProofAssistant]] — Coq and Isabelle are the primary tools for compiler verification
- [[Coq]] — CompCert is built in Coq
- [[Lean]] — emerging compiler verification work in Lean 4
- [[Autoformalization]] — autoformalization could enable AI-assisted proof generation for compiler verification
- [[SelfDebugging]] — verified compilation means debugging can focus on source-level issues

## Key Verified Compilers

| Compiler | Language | Tool | Status |
|----------|----------|------|--------|
| CompCert | C | Coq | Production use at Airbus |
| CakeML | ML | HOL4 | Research + production |
| Isabelle/Refinement | Various | Isabelle | Research |

## See Also
- [[FormalVerification]]
- [[ProofAssistant]]
- [[Coq]]
- [[Lean]]
