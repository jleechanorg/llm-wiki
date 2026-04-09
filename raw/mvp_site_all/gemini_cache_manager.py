"""
Gemini Explicit Cache Manager

Manages explicit caching for WorldArchitect.AI campaigns to take advantage
of unchanging story entries and system prompts.

Key Strategy:
- Cache: System prompts + old story entries (1-N) that never change
- Uncached: Recent entries (N+1 to current) + dynamic game state
- Rebuild: Every 5 new entries (~1s overhead amortized to 200ms/request)

Expected Savings: 70-80% cost reduction with 100% cache hit frequency
"""

import json
import time
from typing import Any, NamedTuple

from google import genai
from google.genai import types

from mvp_site import logging_util


class CacheCreateResult(NamedTuple):
    """Result from create_cache() - includes deferred signal for N-1 logic."""

    cache_name: str | None
    deferred: (
        bool  # True if cache was created but shouldn't be used yet (propagation delay)
    )


class CampaignCacheManager:
    """Manages explicit caching for a single campaign."""

    # Rebuild cache every N new entries
    # Trade-off: Lower = more story cached but more rebuild overhead
    # At 5 entries: ~1s rebuild cost / 5 requests = 200ms amortized overhead
    REBUILD_THRESHOLD = 5

    # Cache TTL (1 hour)
    CACHE_TTL = "3600s"
    CACHE_TTL_SECONDS = 3600  # TTL in seconds for internal use
    CACHE_EXPIRY_BUFFER = 300  # 5 minute buffer before TTL to trigger proactive rebuild

    def __init__(self, campaign_id: str):
        """
        Initialize cache manager for a campaign.

        Args:
            campaign_id: Unique campaign identifier
        """
        self.campaign_id = campaign_id
        self.cache_name: str | None = None
        self.cached_entry_count: int = 0
        self.has_code_execution: bool = False
        self._cached_model: str | None = None  # Model the active cache was built for
        self._cache_created_at: float | None = None  # Timestamp when cache was created
        # N-1 logic: after a rebuild, keep the old cache name for the first
        # request so we don't hit propagation delay on the brand-new cache.
        # The old cache is deleted on the next request when we promote the new one.
        self._pending_cache_name: str | None = None
        self._pending_entry_count: int = 0
        self._pending_has_code_execution: bool = False
        self._pending_model: str | None = None  # Model the pending cache was built for

    def should_rebuild(
        self,
        current_entry_count: int,
        *,
        requires_code_execution: bool = False,
        model_name: str | None = None,
    ) -> bool:
        """
        Check if cache should be rebuilt.

        Args:
            current_entry_count: Total number of story entries
            requires_code_execution: Whether the request needs code execution
            model_name: Current model being used for this request

        Returns:
            True if cache should be rebuilt
        """
        if self.cache_name is None:
            return True  # No cache exists
        if requires_code_execution and not self.has_code_execution:
            return True
        # Model mismatch: cache was built for a different model — must rebuild
        # or we'll get FAILED_PRECONDITION from Gemini API
        if model_name and self._cached_model and model_name != self._cached_model:
            logging_util.info(
                f"📦 CACHE_MODEL_MISMATCH: campaign={self.campaign_id}, "
                f"cached_model={self._cached_model}, request_model={model_name}. "
                f"Forcing rebuild."
            )
            return True
        # Check if cache is approaching TTL expiry - proactive rebuild before
        # FAILED_PRECONDITION from expired cache
        if self._cache_created_at is not None:
            cache_age = time.time() - self._cache_created_at
            ttl_threshold = self.CACHE_TTL_SECONDS - self.CACHE_EXPIRY_BUFFER
            if cache_age > ttl_threshold:
                logging_util.info(
                    f"📦 CACHE_TTL_EXPIRY: campaign={self.campaign_id}, "
                    f"cache_age={cache_age:.0f}s, threshold={ttl_threshold}s. "
                    f"Proactive rebuild to avoid FAILED_PRECONDITION."
                )
                return True
        # If a pending cache exists, don't rebuild again — promote first
        if self._pending_cache_name is not None:
            return False

        entries_since_cache = current_entry_count - self.cached_entry_count
        return entries_since_cache >= self.REBUILD_THRESHOLD

    def create_cache(
        self,
        client: genai.Client,
        system_instruction: str,
        story_entries: list[Any],
        model_name: str = "gemini-2.0-flash",
        actual_story_count: int | None = None,
        tools: list[types.Tool] | None = None,
    ) -> "CacheCreateResult":
        """
        Create new cache with system instruction, tools, and story entries.

        The Gemini API requires system_instruction and tools to be in CachedContentConfig,
        NOT in the GenerateContent config. This allows GenerateContent to use the cache
        without re-specifying these elements. Critical for code_execution support.

        IMPORTANT (DICE-s8u): If code_execution tool is needed, it MUST be included in
        the tools parameter here. When using cached_content, Gemini API rejects any
        attempt to add tools in GenerateContent config.

        Args:
            client: Gemini API client
            system_instruction: System instruction text (goes in CachedContentConfig.system_instruction)
            story_entries: List of story entries (dicts or strings) to cache
            model_name: Model to use for cache
            actual_story_count: Actual number of story entries in the cache
                (may differ from len(story_entries) if entries are bundled as JSON)
            tools: List of Tool objects to include in cache (e.g., code_execution)

        Returns:
            CacheCreateResult with cache_name and deferred flag.
            deferred=True means cache was created but has propagation delay (N-1 logic).
        """
        start_time = time.time()

        # Build cache content parts (story entries only - system_instruction goes in config)
        cache_parts = []
        for entry in story_entries:
            # Serialize structured entries to stable JSON before caching.
            if isinstance(entry, (dict, list)):
                entry_text = json.dumps(entry)
            else:
                entry_text = str(entry)
            cache_parts.append(types.Part(text=entry_text))

        # Create cache with system_instruction and tools in config (NOT in GenerateContent)
        # This is required by Gemini API - see error:
        # "CachedContent can not be used with GenerateContent request setting
        # system_instruction, tools or tool_config"
        # CRITICAL FIX (DICE-s8u): Include tools (especially code_execution) in cache
        # so that continue_story can use code_execution for dice rolls.
        try:
            cache_config_kwargs: dict[str, Any] = {
                "display_name": (
                    f"worldarchitect_campaign_{self.campaign_id}_{len(story_entries)}"
                ),
                "system_instruction": system_instruction,
                "ttl": self.CACHE_TTL,
            }
            if cache_parts:
                cache_config_kwargs["contents"] = [
                    types.Content(
                        role="user",
                        parts=cache_parts,
                    )
                ]

            # Add tools to cache if provided (required for code_execution support)
            if tools:
                cache_config_kwargs["tools"] = tools
                logging_util.info(
                    f"📦 CACHE_WITH_TOOLS: campaign={self.campaign_id}, "
                    f"tool_count={len(tools)}"
                )

            cache = client.caches.create(
                model=model_name,
                config=types.CreateCachedContentConfig(**cache_config_kwargs),
            )

            # Log token count from cache creation response for diagnostics
            cache_token_count = getattr(
                getattr(cache, "usage_metadata", None), "total_token_count", None
            )
            logging_util.info(
                f"📦 CACHE_TOKEN_COUNT: campaign={self.campaign_id}, "
                f"total_token_count={cache_token_count}, "
                f"entries={len(story_entries)}, "
                f"cache_name={cache.name}"
            )

            new_has_code_execution = any(
                getattr(tool, "code_execution", None) is not None
                for tool in tools or []
            )
            new_entry_count = (
                actual_story_count
                if actual_story_count is not None
                else len(story_entries)
            )
            duration = time.time() - start_time

            # N-1 logic: Don't switch to the new cache immediately.
            # Gemini has a propagation delay after cache creation — the first
            # request against a brand-new cache returns cached_tokens=0.
            # Instead, stage the new cache as "pending" and keep using the
            # old cache for this request. promote_pending_cache() switches
            # to the new cache on the NEXT request.
            #
            # Exception: if this rebuild upgrades tool capability (old cache
            # lacked code_execution but new cache includes it), OR if the model
            # changed, we must switch immediately because the old cache is
            # not functionally valid (wrong tools or wrong model → FAILED_PRECONDITION).
            _is_model_mismatch = bool(
                model_name and self._cached_model and model_name != self._cached_model
            )
            if self.cache_name is not None:
                if (
                    new_has_code_execution and not self.has_code_execution
                ) or _is_model_mismatch:
                    old_cache_name = self.cache_name
                    self.cache_name = cache.name
                    self.cached_entry_count = new_entry_count
                    self.has_code_execution = new_has_code_execution
                    self._cached_model = model_name
                    self._cache_created_at = time.time()
                    switch_reason = (
                        "model_mismatch" if _is_model_mismatch else "tool_upgrade"
                    )
                    logging_util.info(
                        f"📦 CACHE_CREATED ({switch_reason} immediate switch): "
                        f"campaign={self.campaign_id}, "
                        f"entries={len(story_entries)}, duration={duration:.2f}s, "
                        f"old_cache={old_cache_name}, new_cache={cache.name}"
                    )
                    if old_cache_name:
                        try:
                            client.caches.delete(name=old_cache_name)
                        except Exception as e:
                            logging_util.warning(
                                f"Failed to delete old cache after tool upgrade "
                                f"for campaign {self.campaign_id}: {e}"
                            )
                    return CacheCreateResult(cache_name=cache.name, deferred=False)

                # Old cache exists — defer the switch
                _active_age = (
                    time.time() - self._cache_created_at
                    if self._cache_created_at is not None
                    else 0
                )
                self._pending_cache_name = cache.name
                self._pending_entry_count = new_entry_count
                self._pending_has_code_execution = new_has_code_execution
                self._pending_model = model_name
                self._cache_created_at = (
                    time.time()
                )  # Track when pending cache was created
                # If active cache already expired while we were rebuilding, return None
                # so callers skip the stale reference rather than hitting FAILED_PRECONDITION
                if _active_age >= self.CACHE_TTL_SECONDS:
                    logging_util.warning(
                        f"📦 CACHE_DEFERRED_SKIP: campaign={self.campaign_id}, "
                        f"active_age={_active_age:.0f}s >= TTL={self.CACHE_TTL_SECONDS}s. "
                        "Returning None to avoid FAILED_PRECONDITION on expired cache."
                    )
                    return CacheCreateResult(cache_name=None, deferred=True)
                logging_util.info(
                    f"📦 CACHE_CREATED (N-1 deferred): campaign={self.campaign_id}, "
                    f"entries={len(story_entries)}, duration={duration:.2f}s, "
                    f"new_cache={cache.name}, still_using={self.cache_name}"
                )
                # Return the OLD cache name — use it for this request, but signal deferred
                return CacheCreateResult(cache_name=self.cache_name, deferred=True)
            else:
                # First cache ever — apply N-1 deferral (propagation delay applies to new caches too).
                # Store internally so promote_pending_cache() can switch to it next request.
                # Return cache_name=None so callers don't try to use it this request.
                self._pending_cache_name = cache.name
                self._pending_entry_count = new_entry_count
                self._pending_has_code_execution = new_has_code_execution
                self._pending_model = model_name
                self._cache_created_at = time.time()
                logging_util.info(
                    f"📦 CACHE_CREATED (N-1 first-ever): campaign={self.campaign_id}, "
                    f"entries={len(story_entries)}, duration={duration:.2f}s, "
                    f"cache_name={cache.name} (deferred — no old cache to use)"
                )
                # Return None — caller makes an uncached request this turn; promote next turn
                return CacheCreateResult(cache_name=None, deferred=True)

        except Exception as e:
            logging_util.error(
                f"Failed to create cache for campaign {self.campaign_id}: {e}"
            )
            raise

    def promote_pending_cache(self, client: genai.Client | None = None) -> bool:
        """
        Promote pending cache to active, deleting the old one.

        Called at the START of the next request after a rebuild, so the new
        cache has had time to propagate on Gemini's side.

        Args:
            client: Gemini client to delete the old remote cache

        Returns:
            True if a promotion occurred
        """
        if self._pending_cache_name is None:
            return False

        old_cache_name = self.cache_name
        self.cache_name = self._pending_cache_name
        self.cached_entry_count = self._pending_entry_count
        self.has_code_execution = self._pending_has_code_execution
        self._cached_model = self._pending_model
        self._pending_cache_name = None
        self._pending_entry_count = 0
        self._pending_has_code_execution = False
        self._pending_model = None

        # Delete old cache
        if old_cache_name and client:
            try:
                client.caches.delete(name=old_cache_name)
                logging_util.info(
                    f"📦 CACHE_PROMOTED: campaign={self.campaign_id}, "
                    f"old={old_cache_name} → new={self.cache_name} (old deleted)"
                )
            except Exception as e:
                logging_util.warning(
                    f"📦 CACHE_PROMOTED: campaign={self.campaign_id}, "
                    f"old={old_cache_name} → new={self.cache_name} "
                    f"(old delete failed: {e})"
                )
        else:
            logging_util.info(
                f"📦 CACHE_PROMOTED: campaign={self.campaign_id}, new={self.cache_name}"
            )

        return True

    def has_pending_cache(self) -> bool:
        """Check if there is a pending cache waiting to be promoted."""
        return self._pending_cache_name is not None

    def get_cache_name(self) -> str | None:
        """
        Get current cache name.

        Returns:
            Cache name if exists, None otherwise
        """
        return self.cache_name

    def reset_cache(self, client: genai.Client | None = None) -> None:
        """
        Reset cache state (for testing or recovery).

        Args:
            client: Optional Gemini client to delete remote cache before reset
        """
        # Delete remote caches before clearing local state to prevent orphaned caches
        for cache_label, cache_ref in [
            ("active", self.cache_name),
            ("pending", self._pending_cache_name),
        ]:
            if cache_ref and client:
                try:
                    client.caches.delete(name=cache_ref)
                    logging_util.info(
                        f"📦 CACHE_DELETED: campaign={self.campaign_id}, "
                        f"cache_name={cache_ref} ({cache_label})"
                    )
                except Exception as e:
                    logging_util.warning(
                        f"Failed to delete {cache_label} cache {cache_ref} during reset: {e}"
                    )

        self.cache_name = None
        self.cached_entry_count = 0
        self.has_code_execution = False
        self._cached_model = None
        self._cache_created_at = None
        self._pending_cache_name = None
        self._pending_entry_count = 0
        self._pending_has_code_execution = False
        self._pending_model = None


# Global cache manager registry
_cache_managers: dict[str, CampaignCacheManager] = {}


def get_cache_manager(campaign_id: str) -> CampaignCacheManager:
    """
    Get or create cache manager for a campaign.

    Args:
        campaign_id: Campaign identifier

    Returns:
        CampaignCacheManager instance
    """
    if campaign_id not in _cache_managers:
        _cache_managers[campaign_id] = CampaignCacheManager(campaign_id)

    return _cache_managers[campaign_id]
