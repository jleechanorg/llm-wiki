---
name: self-hosted-mikey-label-routing-not-environment-2026-06-13
description: "self-hosted-mikey is a GitHub Actions routing label, NOT an environment marker. Both self-hosted-oss/ (Docker+Ubuntu) and self-hosted-bare/ (no Docker, host OS) use the same label"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 73be4e82-d635-4fd2-96b7-639072ec7448
---

# `self-hosted-mikey` is a routing label, not an environment

**Anti-pattern:** assuming `runs-on: [self-hosted, self-hosted-mikey]` means "this job runs in Docker on Ubuntu."

**Reality:** the label is just a GitHub Actions routing tag. It tells the GitHub Actions controller which runner fleet to dispatch to. The execution environment is determined by:

- `self-hosted-oss/` runners → `myoung34/github-runner:ubuntu-noble` Docker container (Ubuntu Noble in Colima/Docker)
- `self-hosted-bare/` runners → host OS directly (Linux x64 on Linux, macOS ARM64 on Mac)

Both fleets register under the same `self-hosted-mikey` label, so workflows can land on either. The `mikey` in the label is a nod to Michael Young (`myoung34`), the maintainer of the original container image — but it's reused as a label by the bare runner for routing compatibility.

**Why this matters:** explaining "bare runner on Mac" to a reviewer familiar with `self-hosted-oss/` requires calling this out explicitly, because the label name suggests Docker wrapping that no longer exists. The naming is preserved for label stability, not for technical accuracy.

**How to apply:** When asked "can we use the bare runner on Mac?" or "what does this runner image look like," clarify: the `self-hosted-mikey` label is shared; the underlying execution is `myoung34` container (OSS) vs host OS (bare). Don't conflate label with environment.
