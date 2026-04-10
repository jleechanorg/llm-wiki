---
title: "AI Universe Frontend (Final)"
type: entity
tags: [frontend, react, vite, webapp]
sources: [ai-universe-frontend-testing-report]
last_updated: 2026-04-07
---

## Description
Live React-based single-page application for AI Universe, deployed on Render at https://ai-universe-frontend-final.onrender.com. Serves as the user interface for multi-model AI consultation.

## Technical Details
- **Framework**: React with TypeScript
- **Build Tool**: Vite 7.1.6
- **Build Command**: npm install && npm run build:prod
- **Start Command**: node proxy-server.cjs
- **Port**: 10000
- **Bundle Size**: ~547KB uncompressed (~151KB gzip)

## Assets
- `/assets/index-CZyTaIMc.js` — main bundle (360.22 KB)
- `/assets/vendor-D3F3s8fL.js` — vendor bundle (141.72 KB)
- `/assets/ui-Dd_g2LAA.js` — UI components (11.89 KB)
- `/assets/index-C0Gf0W3l.css` — styles (32.73 KB)

## Backend Connectivity
- **Backend URL**: https://ai-universe-backend-dev-114133832173.us-central1.run.app
- **CORS Handling**: proxy-server.cjs

## Connections
- [[Render]] — hosting platform
- [[Vite]] — build tool
- [[React]] — frontend framework
- [[AIUniverseBackendDev]] — backend API
- [[CORSProxy]] — proxy handling cross-origin requests

## Source
[[AI Universe Frontend Testing Report]]
