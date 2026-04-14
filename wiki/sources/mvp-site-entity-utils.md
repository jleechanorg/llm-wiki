---
title: "mvp_site entity_utils"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/entity_utils.py
---

## Summary
Backward compatibility shim module. All functionality has been consolidated into entity_validator.py. Import from mvp_site.entity_validator for new code.

## Key Claims
- Re-exports filter_unknown_entities and is_unknown_entity from entity_validator
- Filters out 'Unknown' placeholder entity used when location is not found in world_data

## Connections
- [[mvpSiteEntityValidator]] — consolidated functionality now lives here