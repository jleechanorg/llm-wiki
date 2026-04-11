---
title: "PR #1820: Fix Docker image to expose mvp_site package"
type: source
tags: [codex]
date: 2025-10-02
source_file: raw/prs-worldarchitect-ai/pr-1820.md
sources: []
last_updated: 2025-10-02
---

## Summary
- copy the application code into /app/mvp_site during image build so package imports resolve
- set PYTHONPATH and working directory to keep gunicorn entrypoint unchanged

## Metadata
- **PR**: #1820
- **Merged**: 2025-10-02
- **Author**: jleechan2015
- **Stats**: +14/-2 in 1 files
- **Labels**: codex

## Connections
