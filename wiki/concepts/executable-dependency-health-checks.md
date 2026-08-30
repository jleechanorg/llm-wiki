---
title: "Executable dependency health checks"
type: concept
tags: [health-check, integration, sdk-drift, mem0, observability]
sources: [sources/feedback-2026-08-30-cloud-run-and-mem0-drift-guardrails.md]
last_updated: 2026-08-30
---

## Definition

A dependency is healthy only when a safe probe executes the capability the application actually relies on. Imports, constructors, open ports, and downstream service readiness prove prerequisite layers, not end-to-end compatibility at the client boundary.

## Mem0 Contract

Mem0 recall health requires one real, read-only semantic search using the installed SDK's current signature. For Mem0 2.0.14, that means `search(query, filters={"user_id": ...}, top_k=...)`; a stale `user_id=` and `limit=` call can fail even when Qdrant, Ollama, Groq, package import, and `Memory.from_config()` all succeed.

Every client boundary should have a compatibility test that asserts the SDK call shape. Fail-open hooks may preserve the parent operation, but must emit the exception type and message to stderr or a bounded diagnostic log.

Credential presence is also only a prerequisite. On 2026-08-30, a configured Groq key returned `401 invalid_api_key`; presence-only enablement treated extraction as available while inferred writes disappeared. jleechanclaw PR #841 (`e614e005d2ad9fe640f31a21881739a452799aab`) added a bounded direct-memory fallback with `infer=False` through the verified local embedder and Qdrant path, while reporting the authentication error. Two tests passed, and a real fallback add followed by search returned the saved canary first at score `0.929`.

## Connections

- [[Mem0HelperFiles]] — duplicated client boundaries must share tested call semantics.
- [[Mem0QdrantDeployment]] — service readiness remains a prerequisite, not sufficient proof.
- [[SilentFailurePathPattern]] — swallowed SDK errors make partial health look like success.
- [[RepositoryDefaultsDoNotRemediateLiveState]] — both concepts require verification at the actual end-state boundary.
