---
title: "GCP Cloud Run L4 Cannot Run gpt-oss MXFP4 Models (Blackwell-only)"
type: source
tags: ["gcp", "cloud-run", "mxfp4", "blackwell", "l4-incompatibility", "spicy-llm"]
date: 2026-06-05
source_file: project_2026-06-05_gcp_mxfp4_finding.md
---

## Summary
Both `gpt-oss:20b` and `svjack/gpt-oss-20b-heretic` fail inference on Cloud Run NVIDIA L4 (Ada Lovelace, sm_89) with `CUDA error: device kernel image is invalid`. MXFP4 quantization requires Blackwell (sm_100+).

## Key Claims
- Root cause: MXFP4 requires Blackwell (sm_100+); L4 and A100 (sm_80) are both incompatible
- Models pull fine (28 GB); only inference blocked. CPU fallback OOM-kills at 32 GB
- Service deployed, tested, torn down 2026-06-05 (commit 20951ab)
- Decision pending: Q4_K_M alternatives vs Vertex AI A100 vs local-only
- Bead jleechan-y39

## Key Quotes
> Before any GCP Cloud Run GPU experiment with `gpt-oss:*` models, verify the GPU tier is Blackwell (sm_100+)

## Connections
- [[SpicyLLM]] — heretic repo state
- [[MXFP4Quantization]] — concept
