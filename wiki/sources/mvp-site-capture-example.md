---
title: "Capture Example"
type: source
tags: [capture, demo, testing, service-interactions]
sources: []
last_updated: 2026-04-14
---

## Summary

Demonstrates the capture framework for recording real service interactions during testing. Shows how to use capture mode, analyze captured data, compare with mocks, and generate baselines. Provides both real capture mode demo and mock data analysis for environments without service configuration.

## Key Claims

- **Capture Mode Setup**: Uses TEST_MODE=capture and TEST_CAPTURE_DIR environment variables
- **Service Provider Integration**: get_service_provider("capture") returns capture-enabled provider
- **Capture Summary**: provider.get_capture_summary() returns interaction statistics
- **Dual Demo Mode**: Tries real capture first, falls back to mock data analysis if services not configured
- **Sample Data Structure**: Demo uses firestore and gemini service interactions with success/error responses
- **Analysis Output**: Shows total interactions, services used, success rate, avg duration, errors

## Key Quotes

> "This demo requires real service configuration for full functionality"

> "Recording real service interactions during testing"

> "Generate mock baselines from real data"

## Connections

- [[CaptureAnalysis]] — analysis backend
- [[CaptureCLI]] — CLI interface
- [[APIMocking]] — mock comparison
- [[ServiceLayer]] — services being captured (Firestore, Gemini, Auth)

## Contradictions

- None identified