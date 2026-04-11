---
title: "Firestore Service Inventory Deduplication Tests"
type: source
tags: [python, testing, firestore, inventory, deduplication, json-serialization]
source_file: "raw/test_firestore_inventory_dedup.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test coverage for firestore_service.py inventory deduplication logic. Addresses missing coverage identified in PR #3746 (lines 497-498, 506-507). Tests validate that the `_handle_inventory_safeguard` function correctly merges inventory items from different formats, handles duplicates, and gracefully manages unserializable objects.

## Key Claims
- **Non-dict items (strings)**: String-based inventory items are properly merged with dict-based inventory, removing duplicates
- **Complex dict items**: Complex dict items with JSON serialization are handled correctly, preserving additional fields like "gold"
- **Unserializable items**: Items that cannot be JSON serialized fall back to str() for deduplication comparison
- **Preserves existing duplicates**: Existing duplicate items in player inventory are intentionally preserved (not deduplicated away)

## Connections
- [[PR3746]] — PR that identified missing coverage for inventory safeguard logic
- [[FirestoreService]] — Service containing the tested `_handle_inventory_safeguard` function
- [[InventoryDeduplication]] — Concept of merging inventory items while avoiding duplicates
