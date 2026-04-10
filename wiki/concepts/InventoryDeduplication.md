---
title: "Inventory Deduplication"
type: concept
tags: [gaming, inventory, deduplication, merging]
sources: [firestore-service-inventory-deduplication-tests]
last_updated: 2026-04-08
---

The process of merging inventory items from multiple sources while avoiding duplicate entries. In the WorldArchitect system, inventory can exist as either a simple list of strings or a more complex dict with an "items" array and additional metadata.

## Implementation Details
The `_handle_inventory_safeguard` function in firestore_service.py handles:
- Converting between string and dict inventory formats
- Merging items while removing duplicates (case-sensitive string comparison)
- Falling back to str() comparison when JSON serialization fails
- Preserving intentional duplicates in existing player inventory

## Related Pages
- [[FirestoreServiceInventoryDeduplicationTests]]
- [[PR3746]]
