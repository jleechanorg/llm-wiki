---
title: "PR #5519: Genesis v10-v11: Intent classifier pipeline + dual-head architecture design"
type: source
tags: []
date: 2026-02-15
source_file: raw/prs-worldarchitect-ai/pr-5519.md
sources: []
last_updated: 2026-02-15
---

## Summary
- Built end-to-end Genesis intent classification pipeline (v10.x series) with MLX LoRA fine-tuning
- Iterated through v10.1→v10.11→v11 with LLM re-labeling (+42.4pt improvement)
- **Critical finding**: v11 (56.7% accuracy) is a failed iteration -- predicts ACTION for everything, 0% recall on CONTINUE and OTHER classes
- **v10.11 (37.8%) is the best production candidate** with balanced multi-class detection (K: 66.7%, O: 41.2%)
- Designed research-validated dual-head architecture (REV-586w6) as n

## Metadata
- **PR**: #5519
- **Merged**: 2026-02-15
- **Author**: jleechan2015
- **Stats**: +49391/-35 in 91 files
- **Labels**: none

## Connections
