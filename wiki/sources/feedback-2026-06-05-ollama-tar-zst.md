---
title: "Ollama ≥0.30.x Ships .tar.zst Not .tgz"
type: source
tags: ["ollama", "dockerfile", "zstd", "feedback"]
date: 2026-06-05
source_file: feedback_2026-06-05_ollama_tar_zst.md
---

## Summary
Ollama releases from v0.30.x use `.tar.zst` (zstandard) format instead of `.tgz`. Docker builds targeting these versions must `apt-get install zstd` and extract with `zstd -d` first.

## Key Claims
- Ollama ≥0.30.x uses .tar.zst format
- Dockerfile needs `apt-get install zstd` + `zstd -d /tmp/ollama.tar.zst -o /tmp/ollama.tar`
- Don't use install.sh approach (requires sudo, container env issues)

## Key Quotes
> Cloud Build failed silently with a `.tgz`-named binary that was actually `.tar.zst` until we identified the release format change for v0.30.5

## Connections
- [[Ollama]] — installation concept
