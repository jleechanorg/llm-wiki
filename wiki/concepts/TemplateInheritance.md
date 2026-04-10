---
title: "Template Inheritance"
type: concept
tags: [template, inheritance, jinja2, frontend, html]
sources: []
last_updated: 2026-04-08
---

## Description
Template pattern where base template defines structure and child templates override specific sections. Common in Jinja2/Django templates.

## WorldArchitect.AI Usage
The base template defines blocks (title, head, content, scripts) that child pages can override:
- `{% block title %}` — page title
- `{% block head %}` — additional head elements
- `{% block content %}` — main content area
- `{% block scripts %}` — additional scripts

## Benefits
- Single base template ensures consistent structure
- Child pages only define unique content
- Easy to make global changes
