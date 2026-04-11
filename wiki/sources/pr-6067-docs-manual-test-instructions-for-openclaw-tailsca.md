---
title: "PR #6067: docs: manual test instructions for OpenClaw + Tailscale integration"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-worldarchitect-ai/pr-6067.md
sources: []
last_updated: 2026-04-02
---

## Summary
- Adds comprehensive manual test instructions for OpenClaw gateway + Tailscale tunnel integration
- Documents 6 test scenarios: gateway health, local inference, Tailscale tunnel, WorldArchitect settings, proof-prompt hash, Grok API key
- Includes architecture diagram for GCP → Tailscale → local inference path
- Documents known issues (gateway scope regression in v2026.3.28, blocked Grok API key, deploy.sh secrets gap)
- Migrates Beads issue-tracking from legacy bd (Dolt-backed) to beads_rust (br

## Metadata
- **PR**: #6067
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +987/-764 in 5 files
- **Labels**: none

## Connections
