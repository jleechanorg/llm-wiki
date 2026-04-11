---
title: "WorldArchitect.AI Frontend Base Template"
type: source
tags: [worldarchitect, frontend, bootstrap, firebase, template, html, css, javascript]
source_file: "raw/worldarchitect-ai-frontend-base-template.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Base HTML template establishing the frontend structure for WorldArchitect.AI. Integrates Bootstrap 5.1.3 for responsive layout, Firebase Authentication SDK for user auth, and custom theming system with default/fantasy/base themes. Provides consistent navbar, container structure, and script loading order.

## Key Claims
- **Bootstrap 5.1.3 Integration**: Full Bootstrap CSS and JS bundle for responsive grid, components, and utility classes
- **Firebase Authentication**: Firebase Auth SDK loaded via gstatic CDN (9.6.1) for authentication functionality
- **Custom Theming System**: Three theme CSS files (default.css, fantasy.css, base.css) providing visual styling variations
- **Theme Bootstrap JS**: Custom theme-bootstrap.js loaded before other scripts for theme initialization
- **Modular Template Structure**: Jinja2-style block system (title, head, content, scripts) for page-level customization
- **Bootstrap Icons**: Icon library 1.7.2 integrated via CDN for UI iconography
- **Container Fluid Layout**: Main content uses container-fluid for full-width responsive layouts

## Key Quotes
> "<nav class=\"navbar navbar-expand-lg\">" — Bootstrap navbar component for main site navigation

> "<script src=\"https://www.gstatic.com/firebasejs/9.6.1/firebase-auth-compat.js\"></script>" — Firebase Auth SDK for user authentication

## Connections
- [[WorldArchitect.AI]] — the main project this template serves
- [[Bootstrap]] — CSS framework providing responsive layout and components
- [[Firebase]] — authentication backend service
- [[Bootstrap Icons]] — icon library for UI elements

## Contradictions
- None identified
