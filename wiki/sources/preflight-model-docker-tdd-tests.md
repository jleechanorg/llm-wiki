---
title: "TDD Tests for preflight_model_docker.py (CodeRabbit PR #5861)"
type: source
tags: [python, testing, tdd, preflight, gcs, tar, security]
source_file: "raw/test_preflight_model_docker.py"
sources: []
last_updated: 2026-04-08
---

## Summary
TDD tests validating fixes for CodeRabbit PR #5861 in scripts/preflight_model_docker.py. Tests cover four security and robustness issues: return value checking for GCS restore, tar archive extraction with dot-root entries, GCS URI validation, and symlink path traversal prevention.

## Key Claims
- **_restore_cache_from_gcs return value**: When FASTEMBED_GCS_REQUIRED=true, main() MUST check the return value and fail if it returns False. Without this fix, validation could pass incorrectly when a cached model exists from a prior layer.
- **_safe_extract_tar accepts tar -C archives**: Archives created with `tar -C dir -cf archive.tar .` produce member names like "./" and "./file.txt" — must be handled correctly.
- **_parse_gcs_uri rejects empty object_name**: gs://bucket/ yields empty object_name and must be rejected as invalid.
- **_safe_extract_tar blocks symlink path traversal**: Symlinks with linkname pointing outside dest (e.g., "../../../etc/passwd") must be blocked.

## Test Coverage
| Issue | Function | Test Method |
|-------|----------|-------------|
| #1 | _restore_cache_from_gcs | test_main_fails_when_gcs_required_and_restore_returns_false |
| #2 | _safe_extract_tar | test_accepts_tar_c_style_archive_with_dot_root |
| #3 | _parse_gcs_uri | test_rejects_gs_bucket_only_trailing_slash |
| #4 | _safe_extract_tar | test_rejects_symlink_escaping_via_linkname |

## Connections
- [[CodeRabbit]] — PR #5861 addressing these issues
- [[GCSUriParsing]] — URI validation concept
- [[TarExtractionSecurity]] — tar extraction with security checks
