---
title: "PR #5760: Complete: /fixpr 5755 - Cache corruption detection for LocalIntentClassifier"
type: source
tags: []
date: 2026-03-04
source_file: raw/prs-worldarchitect-ai/pr-5760.md
sources: []
last_updated: 2026-03-04
---

## Summary
- Add cache corruption detection and repair helpers to LocalIntentClassifier
- Detect dangling ONNX symlink targets and truncated blob directories before model load
- Remove corrupted cache dirs to allow clean re-download
- Add focused unit test for cache repair behavior

## Metadata
- **PR**: #5760
- **Merged**: 2026-03-04
- **Author**: jleechan2015
- **Stats**: +286/-0 in 3 files
- **Labels**: none

## Connections
