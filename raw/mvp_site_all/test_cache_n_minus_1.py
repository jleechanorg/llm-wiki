"""
TDD tests for N-1 cache promotion logic.

When a cache rebuild happens, the NEW cache has Gemini propagation delay
(cached_tokens=0 for ~30-60s). The N-1 logic defers switching to the new
cache: the current request uses the OLD cache, and the new cache is
promoted on the NEXT request.

Layer 1 unit test — no server required.
"""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock

from google.genai import types

from mvp_site.gemini_cache_manager import CampaignCacheManager


def _make_mock_client(cache_name: str = "cachedContents/test-cache-1") -> MagicMock:
    """Create a mock Gemini client whose caches.create returns a named cache."""
    client = MagicMock()
    mock_cache = MagicMock()
    mock_cache.name = cache_name
    client.caches.create.return_value = mock_cache
    return client


class TestCacheNMinus1(unittest.TestCase):
    """Test N-1 cache promotion logic in CampaignCacheManager."""

    def test_first_cache_deferred_no_old_cache(self):
        """First-ever cache: N-1 applied, caller gets None (no old cache to use)."""
        mgr = CampaignCacheManager("test-campaign")
        client = _make_mock_client("cachedContents/first-cache")

        result = mgr.create_cache(
            client=client,
            system_instruction="You are a DM.",
            story_entries=["entry1", "entry2"],
            actual_story_count=2,
        )

        # N-1 deferral: cache_name=None (caller makes uncached request this turn)
        self.assertIsNone(result.cache_name)
        self.assertTrue(result.deferred)
        # Cache is staged as pending — not yet promoted to active
        self.assertIsNone(mgr.cache_name)
        self.assertTrue(mgr.has_pending_cache())

    def test_rebuild_returns_old_cache_name(self):
        """On rebuild, create_cache returns the OLD cache name (N-1 logic)."""
        mgr = CampaignCacheManager("test-campaign")

        # First cache — deferred, so promote before next request
        client1 = _make_mock_client("cachedContents/cache-v1")
        mgr.create_cache(
            client=client1,
            system_instruction="You are a DM.",
            story_entries=["e1", "e2"],
            actual_story_count=2,
        )
        # Simulate next request: promote first cache to active
        mgr.promote_pending_cache(client=client1)
        self.assertEqual(mgr.cache_name, "cachedContents/cache-v1")

        # Rebuild — should return OLD name, not new
        client2 = _make_mock_client("cachedContents/cache-v2")
        result = mgr.create_cache(
            client=client2,
            system_instruction="You are a DM.",
            story_entries=["e1", "e2", "e3", "e4", "e5", "e6", "e7"],
            actual_story_count=7,
        )

        # N-1: returns old cache name for THIS request, deferred=True
        self.assertEqual(result.cache_name, "cachedContents/cache-v1")
        self.assertTrue(result.deferred)
        # Active cache is still v1
        self.assertEqual(mgr.cache_name, "cachedContents/cache-v1")
        self.assertEqual(mgr.cached_entry_count, 2)
        # New cache is pending
        self.assertTrue(mgr.has_pending_cache())

    def test_promote_switches_to_new_cache(self):
        """promote_pending_cache() switches active cache to the new one."""
        mgr = CampaignCacheManager("test-campaign")

        # First cache — deferred, promote before rebuild
        client1 = _make_mock_client("cachedContents/cache-v1")
        mgr.create_cache(
            client=client1,
            system_instruction="You are a DM.",
            story_entries=["e1", "e2"],
            actual_story_count=2,
        )
        mgr.promote_pending_cache(client=client1)

        # Rebuild (deferred)
        client2 = _make_mock_client("cachedContents/cache-v2")
        mgr.create_cache(
            client=client2,
            system_instruction="You are a DM.",
            story_entries=["e1", "e2", "e3", "e4", "e5", "e6", "e7"],
            actual_story_count=7,
        )
        self.assertTrue(mgr.has_pending_cache())

        # Promote on next request
        client3 = _make_mock_client()
        promoted = mgr.promote_pending_cache(client=client3)

        self.assertTrue(promoted)
        self.assertEqual(mgr.cache_name, "cachedContents/cache-v2")
        self.assertEqual(mgr.cached_entry_count, 7)
        self.assertFalse(mgr.has_pending_cache())
        # Old cache was deleted
        client3.caches.delete.assert_called_once_with(name="cachedContents/cache-v1")

    def test_should_rebuild_false_when_pending(self):
        """should_rebuild() returns False when a pending cache exists."""
        mgr = CampaignCacheManager("test-campaign")

        # First cache at 2 entries — promote before rebuild
        client1 = _make_mock_client("cachedContents/cache-v1")
        mgr.create_cache(
            client=client1,
            system_instruction="You are a DM.",
            story_entries=["e1", "e2"],
            actual_story_count=2,
        )
        mgr.promote_pending_cache(client=client1)

        # Rebuild triggers at 7 entries (5 since last cache)
        client2 = _make_mock_client("cachedContents/cache-v2")
        mgr.create_cache(
            client=client2,
            system_instruction="You are a DM.",
            story_entries=["e1", "e2", "e3", "e4", "e5", "e6", "e7"],
            actual_story_count=7,
        )

        # With pending cache, should_rebuild must be False (even though
        # entries_since_cache would exceed threshold based on old count)
        self.assertFalse(mgr.should_rebuild(9))
        self.assertFalse(mgr.should_rebuild(20))

    def test_promote_then_rebuild_works(self):
        """After promotion, normal rebuild logic resumes."""
        mgr = CampaignCacheManager("test-campaign")

        # First cache — promote before rebuild
        client1 = _make_mock_client("cachedContents/cache-v1")
        mgr.create_cache(
            client=client1,
            system_instruction="You are a DM.",
            story_entries=["e1", "e2"],
            actual_story_count=2,
        )
        mgr.promote_pending_cache(client=client1)

        # Rebuild (deferred)
        client2 = _make_mock_client("cachedContents/cache-v2")
        mgr.create_cache(
            client=client2,
            system_instruction="You are a DM.",
            story_entries=list(range(7)),
            actual_story_count=7,
        )

        # Promote
        client3 = _make_mock_client()
        mgr.promote_pending_cache(client=client3)
        self.assertEqual(mgr.cached_entry_count, 7)

        # Now should_rebuild works normally again
        self.assertFalse(mgr.should_rebuild(11))  # 4 since cache, < 5
        self.assertTrue(mgr.should_rebuild(12))  # 5 since cache, >= 5

    def test_reset_clears_pending(self):
        """reset_cache() clears both active and pending state."""
        mgr = CampaignCacheManager("test-campaign")

        # First cache — promote, then rebuild so there's an active + pending state
        client1 = _make_mock_client("cachedContents/cache-v1")
        mgr.create_cache(
            client=client1,
            system_instruction="",
            story_entries=["e1"],
            actual_story_count=1,
        )
        mgr.promote_pending_cache(client=client1)
        client2 = _make_mock_client("cachedContents/cache-v2")
        mgr.create_cache(
            client=client2,
            system_instruction="",
            story_entries=["e1", "e2"],
            actual_story_count=2,
        )

        self.assertTrue(mgr.has_pending_cache())

        mgr.reset_cache()

        self.assertIsNone(mgr.cache_name)
        self.assertEqual(mgr.cached_entry_count, 0)
        self.assertFalse(mgr.has_pending_cache())

    def test_no_promote_when_nothing_pending(self):
        """promote_pending_cache() returns False when nothing is pending."""
        mgr = CampaignCacheManager("test-campaign")
        client = _make_mock_client("cachedContents/cache-v1")
        mgr.create_cache(
            client=client,
            system_instruction="",
            story_entries=["e1"],
            actual_story_count=1,
        )

        # First create stages as pending — promote it
        first_promote = mgr.promote_pending_cache(client=client)
        self.assertTrue(first_promote)

        # Now nothing is pending
        result = mgr.promote_pending_cache(client=client)
        self.assertFalse(result)

    def test_tool_upgrade_skips_n_minus_1_deferral(self):
        """If old cache lacks code_execution, switch to tool-capable cache immediately."""
        mgr = CampaignCacheManager("test-campaign")

        # Old cache without code_execution support — promote before rebuild
        client1 = _make_mock_client("cachedContents/cache-v1")
        mgr.create_cache(
            client=client1,
            system_instruction="You are a DM.",
            story_entries=["e1", "e2"],
            actual_story_count=2,
            tools=None,
        )
        mgr.promote_pending_cache(client=client1)
        self.assertFalse(mgr.has_code_execution)

        # Rebuild with code_execution must not defer to the old incompatible cache.
        client2 = _make_mock_client("cachedContents/cache-v2")
        result = mgr.create_cache(
            client=client2,
            system_instruction="You are a DM.",
            story_entries=["e1", "e2", "e3"],
            actual_story_count=3,
            tools=[types.Tool(code_execution={})],
        )

        # Tool upgrade: immediate switch, no deferral (deferred=False)
        self.assertEqual(result.cache_name, "cachedContents/cache-v2")
        self.assertFalse(result.deferred)
        self.assertEqual(mgr.cache_name, "cachedContents/cache-v2")
        self.assertEqual(mgr.cached_entry_count, 3)
        self.assertTrue(mgr.has_code_execution)
        self.assertFalse(mgr.has_pending_cache())
        client2.caches.delete.assert_called_once_with(name="cachedContents/cache-v1")


if __name__ == "__main__":
    unittest.main()
