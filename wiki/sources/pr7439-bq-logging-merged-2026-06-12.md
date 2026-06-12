# PR #7439 BQ Forensic Logging Merged

**Date**: 2026-06-12 | **Bead**: rev-lb0ao

PR [#7439](https://github.com/jleechanorg/worldarchitect.ai/pull/7439) merged to main (commit 2cca3481dc): BQ forensic logging for 4 streaming paths.

4 paths → `worldarchitecture-ai.llm_forensics.llm_payloads`: gemini_provider, llm_parser, world_logic, llm_service.

**Local dev**: `USE_ADC=true` required (Firebase SA key lacks BQ roles).
**Local test env**: Set `PORT=8080` when running mvp_site tests to avoid contamination from a running dev server.
