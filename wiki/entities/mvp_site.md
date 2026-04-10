---
title: "mvp_site"
type: entity
tags: [project, backend, module]
sources: [pydantic-validation-entity-tracking-tests]
last_updated: 2026-04-08
---

## Description
MVP backend site module containing the entity_tracking subsystem. Houses Pydantic-based validation for game state entity extraction.

## Key Components
- [[entity_tracking]] — entity extraction and validation module
- SceneManifest — Pydantic model for scene data
- DefensiveNumericConverter — type coercion utilities

## Connections
- Used by: campaign UI, story context system
- Related: [[Pydantic]] validation framework
