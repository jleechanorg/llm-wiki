---
title: "self-hosted-mikey label is routing, not environment (2026-06-13)"
type: source
tags: [self-hosted-runners, github-actions, routing, label, feedback, 2026-06-13]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_self_hosted_mikey_label_means_routing_not_environment.md
---

## Summary
The `self-hosted-mikey` GitHub Actions label is a **routing tag**, not an environment marker. Both `self-hosted-oss/` (Docker + Ubuntu via `myoung34/github-runner:ubuntu-noble` container) and `self-hosted-bare/` (no Docker, host OS) register runners under the same label, so workflows can land on either fleet. The `mikey` in the label is a nod to Michael Young (`myoung34`), preserved for label stability rather than technical accuracy.

## Key Claims
- `runs-on: [self-hosted, self-hosted-mikey]` does NOT imply Docker-on-Ubuntu execution
- `self-hosted-oss/` runners run in `myoung34/github-runner:ubuntu-noble` Docker containers (Colima/Docker)
- `self-hosted-bare/` runners execute on the host OS directly (Linux x64 on Linux, macOS ARM64 on Mac)
- Both fleets register under the same `self-hosted-mikey` label
- The label name is preserved for routing compatibility, not technical accuracy
- Explaining "bare runner on Mac" to a reviewer familiar with `self-hosted-oss/` requires calling this out explicitly

## Key Quotes
> "The label is just a GitHub Actions routing tag. It tells the GitHub Actions controller which runner fleet to dispatch to."

> "The `mikey` in the label is a nod to Michael Young (`myoung34`), the maintainer of the original container image — but it's reused as a label by the bare runner for routing compatibility."

## Connections
- [[ColimaMigration]] — same 2026-06-13 session; OSS runners now on Colima
- [[self-hosted-oss]] — Docker+Ubuntu fleet
- [[self-hosted-bare]] — host-OS fleet (PR #7491)
- [[myoung34-github-runner]] — origin of the `mikey` label
- [[GitHubActionsRoutingLabels]] — general label-vs-environment distinction
