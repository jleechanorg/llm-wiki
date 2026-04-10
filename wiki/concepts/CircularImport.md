---
title: "Circular Import"
type: concept
tags: [python, imports, architecture]
sources: [stream-event-type]
last_updated: 2026-04-08
---

A Python import cycle where module A imports B and B imports A. The StreamEvent type exists in a small "dependency leaf" module to break this cycle between [[StreamingOrchestrator]] and [[LlmService]].

**Solution Pattern:** Extract the shared dependency into a third module that both original modules import, without either importing the other.
