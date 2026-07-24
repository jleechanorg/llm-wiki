# Direct Firestore User Lookup by Email

When checking settings (e.g., RAG settings) for a specific user, scanning the entire users collection or using unindexed queries creates latency and fails to scale. 

## Technical Detail & Pattern
1. Retrieve the UID via Firebase Authentication:
   ```python
   from firebase_admin import auth
   user_record = auth.get_user_by_email(email)
   uid = user_record.uid
   ```
2. Query Firestore directly by document ID (UID):
   ```python
   user_ref = db.collection("users").document(uid)
   user_doc = user_ref.get()
   ```
This avoids scanning all user documents and requires no extra indexing.
