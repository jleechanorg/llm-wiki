---
name: gcp-mxfp4-l4-incompatibility
description: GCP Cloud Run L4 cannot run gpt-oss MXFP4 models — Blackwell-only quantization
type: project
bead: jleechan-y39
---

Both `gpt-oss:20b` and `svjack/gpt-oss-20b-heretic` fail inference on Cloud Run NVIDIA L4 (Ada Lovelace, sm_89) with `CUDA error: device kernel image is invalid`. Root cause: both models use MXFP4 (Microscaling FP4) quantization which requires Blackwell (sm_100+). CPU fallback (`num_gpu=0`) OOM-kills at 32 GB. Models pull fine (28 GB); only inference blocked. Service deployed, tested, and torn down 2026-06-05 (commit 20951ab). Evidence: `results/2026-06-05_gcp-phase1-rerun/summary.json`.

**Why:** Phase 1 A/B re-run on GCP was blocked entirely. Decision pending on Q4_K_M alternatives vs Vertex AI A100 vs local-only.

**How to apply:** Before any GCP Cloud Run GPU experiment with `gpt-oss:*` models, verify the GPU tier is Blackwell (sm_100+). L4 and A100 (sm_80) are both incompatible with MXFP4. For L4 testing use Q4_K_M quantized models.
