---
title: "Default Limit 50"
type: concept
tags: [pagination, configuration, performance]
sources: []
last_updated: 2026-04-08
---

## Description
Default limit of 50 items per page is used for campaign list pagination. This balance allows displaying a full list while minimizing database query load.

## Rationale
- Enough to display most user's full campaign list
- Small enough to load quickly
- Minimal field selection keeps payload light

## Configuration
- Default: 50 campaigns
- Custom limit: Configurable via parameter
- Fields: title, last_played (minimal selection)
