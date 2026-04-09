"""
Regression tests for rotate_personal_api_key and revoke_personal_api_key.

Verifies that these functions use dot-notation transaction.update() (not
transaction.set() with a nested dict) when the user doc already exists, so
that existing settings fields (gemini_api_key, openclaw_gateway_url, etc.)
are preserved on generate/revoke.

See: fix commit eea7c67cba — "use dot-notation update to preserve settings
on API key rotate/revoke"
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("FIRESTORE_EMULATOR_HOST", "localhost:8080")
os.environ.setdefault("TESTING_AUTH_BYPASS", "true")

from google.cloud import firestore

from mvp_site import firestore_service


def _make_db_mock(user_exists: bool, existing_hash: str | None = None):
    """Build a fake Firestore client whose transaction records all calls.

    The critical wiring: user_ref.get.return_value = user_snap so that the
    production code's `user_ref.get(transaction=transaction)` returns our
    controlled snapshot with the correct .exists value.
    """
    # Stable ref objects for identity checks
    user_ref = MagicMock(name="user_ref")
    new_key_ref = MagicMock(name="new_key_ref")
    old_key_ref = MagicMock(name="old_key_ref")

    # user_snap controls the branching logic
    user_snap = MagicMock(name="user_snap")
    user_snap.exists = user_exists
    if user_exists:
        settings = {}
        if existing_hash:
            settings["personal_api_key_hash"] = existing_hash
        user_snap.to_dict.return_value = {"settings": settings}
    else:
        user_snap.to_dict.return_value = None

    # Wire user_ref.get() → user_snap so production code sees the right snapshot
    user_ref.get.return_value = user_snap

    # transaction mock — records set/update/delete calls
    txn = MagicMock(name="txn")

    # db wiring
    db = MagicMock(name="db")
    db.transaction.return_value = txn

    users_coll = MagicMock(name="coll:users")
    users_coll.document.return_value = user_ref

    api_keys_coll = MagicMock(name="coll:api_keys")
    # First call to api_keys.document() → new_key_ref; second → old_key_ref
    api_keys_coll.document.side_effect = [new_key_ref, old_key_ref]

    def _collection(name):
        if name == "users":
            return users_coll
        return api_keys_coll

    db.collection.side_effect = _collection

    return db, txn, user_ref, new_key_ref, old_key_ref, user_snap


class TestRotatePersonalApiKeyTransactionBehavior(unittest.TestCase):
    """Verify rotate_personal_api_key uses update() not set() for existing users."""

    def _call_rotate(self, db, new_hash="newhash123"):
        with patch("mvp_site.firestore_service.get_db", return_value=db):
            return firestore_service.rotate_personal_api_key("user-abc", new_hash)

    def test_existing_user_calls_transaction_update_with_dot_notation(self):
        """When user doc exists, must call transaction.update() with dot-notation key."""
        db, txn, user_ref, new_key_ref, _, _ = _make_db_mock(
            user_exists=True, existing_hash=None
        )
        result = self._call_rotate(db, "newhash456")
        self.assertTrue(result)

        # Collect all transaction.update calls
        update_calls = [c for c in txn.method_calls if c[0] == "update"]
        self.assertTrue(
            update_calls,
            "transaction.update() was never called — did the fix get reverted?",
        )
        # The update must use dot-notation key, not a nested dict
        update_kwargs = update_calls[0].args[1] if update_calls[0].args else {}
        self.assertIn(
            "settings.personal_api_key_hash",
            update_kwargs,
            f"Expected dot-notation key 'settings.personal_api_key_hash' in update() "
            f"but got: {list(update_kwargs.keys())}",
        )
        self.assertEqual(update_kwargs["settings.personal_api_key_hash"], "newhash456")

    def test_existing_user_does_not_call_set_for_user_doc(self):
        """When user doc exists, must NOT call transaction.set() for the user doc."""
        db, txn, user_ref, new_key_ref, _, _ = _make_db_mock(
            user_exists=True, existing_hash=None
        )
        self._call_rotate(db, "newhash456")

        # Any set() calls should be for the new api_keys doc, not user_ref
        set_calls_on_user = [
            c
            for c in txn.method_calls
            if c[0] == "set" and c.args and c.args[0] is user_ref
        ]
        self.assertFalse(
            set_calls_on_user,
            f"transaction.set() was called on the user_ref for an existing user — "
            f"this would overwrite all settings: {set_calls_on_user}",
        )

    def test_new_user_calls_set_merge_true(self):
        """When user doc does not exist, must use set(merge=True) — safe for new docs."""
        db, txn, user_ref, new_key_ref, _, _ = _make_db_mock(user_exists=False)
        result = self._call_rotate(db, "firsthash")
        self.assertTrue(result)

        set_calls_on_user = [
            c
            for c in txn.method_calls
            if c[0] == "set" and c.args and c.args[0] is user_ref
        ]
        self.assertTrue(
            set_calls_on_user,
            "Expected transaction.set() for new user doc but it was not called",
        )
        # Verify merge=True is set
        call_kwargs = set_calls_on_user[0].kwargs if set_calls_on_user else {}
        self.assertTrue(
            call_kwargs.get("merge"),
            "Expected set(..., merge=True) for new user doc",
        )

    def test_new_user_does_not_call_update(self):
        """When user doc does not exist, must NOT call transaction.update()."""
        db, txn, user_ref, new_key_ref, _, _ = _make_db_mock(user_exists=False)
        self._call_rotate(db, "firsthash")

        update_calls = [c for c in txn.method_calls if c[0] == "update"]
        self.assertFalse(
            update_calls,
            "transaction.update() should not be called for a new user (doc doesn't exist)",
        )


class TestRevokePersonalApiKeyTransactionBehavior(unittest.TestCase):
    """Verify revoke_personal_api_key uses update() with DELETE_FIELD."""

    def _call_revoke(self, db):
        with patch("mvp_site.firestore_service.get_db", return_value=db):
            return firestore_service.revoke_personal_api_key("user-abc")

    def test_existing_user_calls_update_with_delete_field(self):
        """Revoke must call transaction.update() with DELETE_FIELD, not set()."""
        db, txn, user_ref, _, _, _ = _make_db_mock(
            user_exists=True, existing_hash="oldhash"
        )
        result = self._call_revoke(db)
        self.assertTrue(result)

        update_calls = [c for c in txn.method_calls if c[0] == "update"]
        self.assertTrue(
            update_calls,
            "transaction.update() was never called in revoke — fix may be missing",
        )
        update_data = update_calls[0].args[1] if update_calls[0].args else {}
        self.assertIn("settings.personal_api_key_hash", update_data)
        self.assertEqual(
            update_data["settings.personal_api_key_hash"],
            firestore.DELETE_FIELD,
            "Expected firestore.DELETE_FIELD to remove the hash field atomically",
        )

    def test_existing_user_does_not_call_set_on_user_doc(self):
        """Revoke must NOT call transaction.set() on the user doc (would wipe settings)."""
        db, txn, user_ref, _, _, _ = _make_db_mock(
            user_exists=True, existing_hash="oldhash"
        )
        self._call_revoke(db)

        set_calls_on_user = [
            c
            for c in txn.method_calls
            if c[0] == "set" and c.args and c.args[0] is user_ref
        ]
        self.assertFalse(
            set_calls_on_user,
            "transaction.set() on user_ref would overwrite all settings — must not be called",
        )

    def test_nonexistent_user_returns_true_without_update(self):
        """Revoke with no user doc is a no-op and returns True."""
        db, txn, user_ref, _, _, _ = _make_db_mock(user_exists=False)
        result = self._call_revoke(db)
        self.assertTrue(result)
        update_calls = [c for c in txn.method_calls if c[0] == "update"]
        self.assertFalse(
            update_calls,
            "No update should occur when user doc does not exist",
        )


if __name__ == "__main__":
    unittest.main()
