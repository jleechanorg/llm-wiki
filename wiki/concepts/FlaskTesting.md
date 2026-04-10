---
title: "Flask Testing"
type: concept
tags: [flask, testing, python, test-client]
sources: []
last_updated: 2026-04-08
---

## Description
Testing patterns for Flask applications using Flask's test client. Tests import Flask app, configure TESTING=True, and use app.test_client() for making requests.

## In This Source
Test file demonstrates Flask testing with test client fixture. Sets app.config["TESTING"] = True and uses app.test_client() for endpoint testing.

## Key Patterns
- `client()` fixture with app.test_client() and app.app_context()
- GET requests: client.get("/api/time")
- POST requests: client.post("/api/campaigns", json=data)
- Headers: {"X-Test-Bypass-Auth": "true"}

## Connections
- [[TestFixtures]] — client fixture pattern
- [[APIEndpointTesting]] — /api endpoints validation
