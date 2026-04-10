---
title: "MVPSiteMain"
type: entity
tags: [flask, application, python]
sources: []
last_updated: 2026-04-08
---

## Description
Main Flask application module in the MVP site project. Contains the Flask app instance, create_app factory function, and all route handlers for the web application.

## In This Source
Referenced in test file as `mvp_site.main` module. Exports Flask app instance and create_app function.

## Connections
- [[FlaskAppImportEndpointTests]] — tested for import and initialization
- [[CacheBusting]] — exports CACHE_BUST_HASH_LENGTH through main module
- [[MCPClient]] — used for campaign management via MCP infrastructure
