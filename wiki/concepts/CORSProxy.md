---
title: "CORS Proxy"
type: concept
tags: [web-development, security, networking]
sources: [ai-universe-frontend-testing-report]
last_updated: 2026-04-07
---

## Description
Server-side middleware that handles Cross-Origin Resource Sharing (CORS) by proxying requests between frontend and backend when they exist on different domains. The AI Universe uses proxy-server.cjs for this purpose.

## Purpose
- Bypass browser CORS restrictions
- Enable frontend (on Render) to call backend (on Cloud Run) safely
- Handle authentication headers and cookies across origins

## AI Universe Implementation
- **File**: proxy-server.cjs
- **Function**: Forwards API requests from frontend to backend
- **Backend URL**: https://ai-universe-backend-dev-114133832173.us-central1.run.app

## Source
[[AI Universe Frontend Testing Report]]
