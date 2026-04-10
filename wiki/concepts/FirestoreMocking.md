---
title: "Firestore Mocking"
type: concept
tags: [python, testing, firestore, firebase, mocking]
sources: []
last_updated: 2026-04-08
---

## Definition
Firestore mocking is a testing pattern where the Firestore client is replaced with a MagicMock that simulates database operations. Tests patch the get_db() function to return a controlled mock client instead of connecting to actual Firebase services.

## Pattern
```python
@patch("firestore_service.get_db")
def test_firestore_operations(self, mock_get_db):
    mock_client = MagicMock()
    mock_get_db.return_value = mock_client
    # test code that uses get_db()
```

## Related
- [[MagicMock]]
- [[FirestoreService]]
- [[UnitTesting]]
