---
title: "AuthContext"
type: entity
tags: [auth, authorization, security]
sources: [worldai-tools-mcp-proxy-tests]
last_updated: 2026-04-08
---

## Description
Authentication context class holding user identity and roles. Used by [[WorldAIToolsProxy]] to authorize tool access. Roles determine which tools a user can execute.

## Attributes
- actor_user_id: Unique user identifier
- actor_email: User email (may be None for service accounts)
- roles: Set of role names (support_admin, ops_admin, deploy_admin)
