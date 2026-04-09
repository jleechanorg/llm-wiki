"""
Firestore Service - Database Operations and Game State Management

This module provides comprehensive database operations for WorldArchitect.AI,
including campaign management, game state synchronization, and robust data handling.

Key Responsibilities:
- Campaign CRUD operations (Create, Read, Update, Delete)
- Game state serialization and persistence
- Complex state update processing with merge logic
- Mission management and data conversion
- Defensive programming patterns for data integrity
- JSON serialization utilities for Firestore compatibility

Architecture:
- Uses Firebase Firestore for data persistence
- Implements robust state update mechanisms
- Provides mission handling with smart conversion
- Includes comprehensive error handling and logging
- Supports legacy data cleanup and migration

Dependencies:
- Firebase Admin SDK for Firestore operations
- Custom GameState class for state management
- NumericFieldConverter for data type handling
- Logging utilities for comprehensive debugging
"""

# ruff: noqa: PLR0911, PLR0912, UP038

import collections.abc
import copy
import datetime
import json
import operator
import os
import time
from typing import Any
from urllib.parse import urlparse

import firebase_admin
from firebase_admin import credentials, firestore, storage

from mvp_site import constants, logging_util
from mvp_site.custom_types import CampaignId, UserId
from mvp_site.decorators import log_exceptions
from mvp_site.game_state import GameState, migrate_legacy_state_for_schema
from mvp_site.numeric_field_converter import NumericFieldConverter
from mvp_site.schemas import validation as schema_validation
from mvp_site.serialization import json_default_serializer, json_serial

try:  # pragma: no cover - import guard
    from google.api_core.exceptions import GoogleAPIError
except ImportError:  # pragma: no cover - import guard
    # Avoid catching all exceptions as "infrastructure errors" when google libs aren't present.
    class GoogleAPIError(Exception):  # noqa: N818 - match upstream naming
        pass


try:  # pragma: no cover - import guard
    from google.cloud.firestore_v1.base_aggregation import (  # type: ignore[import-untyped]
        AggregationQuery as AGGREGATION_QUERY,  # noqa: N814
    )
except Exception:  # pragma: no cover - import guard
    AGGREGATION_QUERY = None

__all__ = ["json_default_serializer", "json_serial"]

MAX_TEXT_BYTES: int = 1000000
MAX_LOG_LINES: int = 20
DELETE_TOKEN: str = "__DELETE__"  # noqa: S105 - Token used to mark fields for deletion in state updates

# Compatibility shim for datetime.UTC (Python 3.11+)
try:  # pragma: no cover - import guard
    UTC = datetime.UTC
except AttributeError:  # pragma: no cover - Python < 3.11
    UTC = datetime.UTC


def _mask_api_key_value(value: Any) -> Any:
    """Mask API keys for logging."""
    if not isinstance(value, str) or value is None:
        return value
    if value == "":
        return value
    if len(value) <= 4:
        return "***"
    return f"***{value[-4:]}"


def _redact_settings_for_log(settings: dict[str, Any]) -> dict[str, Any]:
    """Redact API keys in settings before logging."""
    redacted = settings.copy()
    for key in (
        "gemini_api_key",
        "openrouter_api_key",
        "cerebras_api_key",
        "openclaw_api_key",
        "openclaw_gateway_token",
    ):
        if key in redacted:
            redacted[key] = _mask_api_key_value(redacted[key])
    return redacted


class FirestoreWriteError(RuntimeError):
    """Raised when Firestore write operations return unexpected responses."""


def _log_story_entry_contract_warnings(
    entry_data: dict[str, Any],
    *,
    campaign_id: CampaignId,
    actor: str,
    stage: str,
) -> None:
    """Run non-blocking story-entry contract validation and log warnings."""
    validation_payload = entry_data.copy()
    timestamp_value = validation_payload.get("timestamp")
    if hasattr(timestamp_value, "isoformat"):
        try:
            validation_payload["timestamp"] = timestamp_value.isoformat()
        except Exception:
            validation_payload["timestamp"] = str(timestamp_value)

    errors = schema_validation.validate_story_entry(validation_payload)
    if not errors:
        return
    preview = ", ".join(errors[:3])
    if len(errors) > 3:
        preview += f" (+{len(errors) - 3} more)"
    logging_util.warning(
        "Story entry contract validation warning (%s, campaign=%s, actor=%s): %s",
        stage,
        campaign_id,
        actor,
        preview,
    )


def _normalize_story_entry_contract_fields(
    entry_data: dict[str, Any],
) -> dict[str, Any]:
    """Normalize story entry fields to satisfy StoryEntry contract expectations.

    This keeps writes schema-aligned without changing caller behavior:
    - `resources` must be a string in StoryEntry, but model output may provide `{}`.
    - `action_resolution` (when present) requires `reinterpreted` + `audit_flags`.
    """
    normalized = dict(entry_data)

    resources = normalized.get("resources")
    if isinstance(resources, dict):
        if resources:
            normalized["resources"] = json.dumps(
                resources, sort_keys=True, ensure_ascii=True
            )
        else:
            normalized["resources"] = ""

    action_resolution = normalized.get("action_resolution")
    if isinstance(action_resolution, dict):
        action_resolution_norm = dict(action_resolution)
        action_resolution_norm.setdefault("reinterpreted", False)
        audit_flags = action_resolution_norm.get("audit_flags")
        if audit_flags is None:
            action_resolution_norm["audit_flags"] = []
        elif not isinstance(audit_flags, list):
            action_resolution_norm["audit_flags"] = [str(audit_flags)]
        mechanics = action_resolution_norm.get("mechanics")
        if isinstance(mechanics, dict):
            mechanics_norm = dict(mechanics)
            rolls = mechanics_norm.get("rolls")
            if isinstance(rolls, list):
                normalized_rolls: list[Any] = []
                for roll in rolls:
                    if not isinstance(roll, dict):
                        normalized_rolls.append(roll)
                        continue
                    roll_norm = dict(roll)
                    if "success" not in roll_norm:
                        roll_norm["success"] = False
                    normalized_rolls.append(roll_norm)
                mechanics_norm["rolls"] = normalized_rolls
            action_resolution_norm["mechanics"] = mechanics_norm
        normalized["action_resolution"] = action_resolution_norm

    return normalized


# Note: Tests patch the fully-qualified module path (`mvp_site.firestore_service`).

# ruff: noqa: PLR0915


class _InMemoryFirestoreDocument:
    """Simple in-memory document used when MOCK_SERVICES_MODE is enabled."""

    def __init__(self, doc_id: str, parent_path: str = "") -> None:
        self.id = doc_id
        self._data: dict[str, Any] = {}
        self._parent_path = parent_path
        self._collections: dict[str, _InMemoryFirestoreCollection] = {}

    def set(self, data: dict[str, Any], merge: bool = False) -> None:
        if not merge:
            self._data = data
            return

        def deep_merge(target: dict[str, Any], source: dict[str, Any]) -> None:
            for key, value in source.items():
                if (
                    key in target
                    and isinstance(target[key], dict)
                    and isinstance(value, dict)
                ):
                    deep_merge(target[key], value)
                else:
                    target[key] = value

        deep_merge(self._data, data)

    def update(self, updates: dict[str, Any]) -> None:
        for key, value in updates.items():
            if "." in key:
                parts = key.split(".")
                current = self._data
                for part in parts[:-1]:
                    current = current.setdefault(part, {})
                current[parts[-1]] = value
            else:
                self._data[key] = value

    def get(self) -> "_InMemoryFirestoreDocument":
        return self

    @property
    def exists(self) -> bool:
        return bool(self._data)

    def to_dict(self) -> dict[str, Any]:
        return copy.deepcopy(self._data)

    def collection(self, name: str) -> "_InMemoryFirestoreCollection":
        path = f"{self._parent_path}/{self.id}" if self._parent_path else self.id
        return self._collections.setdefault(
            name, _InMemoryFirestoreCollection(name, parent_path=path)
        )


class _InMemoryFirestoreQuery:
    """Query wrapper for in-memory Firestore collections."""

    def __init__(
        self,
        docs: list["_InMemoryFirestoreDocument"],
        order_by: list[tuple[Any, Any]] | None = None,
        limit: int | None = None,
        filters: list[tuple[Any, Any, Any]] | None = None,
        start_after: tuple[Any, ...] | None = None,
        select_fields: list[str] | None = None,
    ) -> None:
        self._docs = list(docs)
        self._order_by = order_by or []
        self._limit = limit
        self._filters = filters or []
        self._start_after = start_after
        self._select_fields = select_fields

    def order_by(self, field: Any, direction: Any = None) -> "_InMemoryFirestoreQuery":
        return _InMemoryFirestoreQuery(
            self._docs,
            order_by=list(self._order_by) + [(field, direction)],
            limit=self._limit,
            filters=self._filters,
            start_after=self._start_after,
            select_fields=self._select_fields,
        )

    def limit(self, count: int) -> "_InMemoryFirestoreQuery":
        return _InMemoryFirestoreQuery(
            self._docs,
            order_by=self._order_by,
            limit=count,
            filters=self._filters,
            start_after=self._start_after,
            select_fields=self._select_fields,
        )

    def where(self, field: Any, op: str, value: Any) -> "_InMemoryFirestoreQuery":
        return _InMemoryFirestoreQuery(
            self._docs,
            order_by=self._order_by,
            limit=self._limit,
            filters=self._filters + [(field, op, value)],
            start_after=self._start_after,
            select_fields=self._select_fields,
        )

    def start_after(self, *values: Any) -> "_InMemoryFirestoreQuery":
        return _InMemoryFirestoreQuery(
            self._docs,
            order_by=self._order_by,
            limit=self._limit,
            filters=self._filters,
            start_after=tuple(values),
            select_fields=self._select_fields,
        )

    def select(self, field_paths: Any) -> "_InMemoryFirestoreQuery":
        if isinstance(field_paths, str):
            selected_fields = [field_paths]
        else:
            selected_fields = list(field_paths)
        return _InMemoryFirestoreQuery(
            self._docs,
            order_by=self._order_by,
            limit=self._limit,
            filters=self._filters,
            start_after=self._start_after,
            select_fields=selected_fields,
        )

    def _get_value(self, doc: "_InMemoryFirestoreDocument", field: Any) -> Any:
        data = doc.to_dict()
        if field in data:
            return data[field]

        field_name = str(field)
        if field_name == "__name__" or field_name.endswith("DOCUMENT_ID"):
            return getattr(doc, "id", None)
        return None

    def stream(self) -> list["_InMemoryFirestoreDocument"]:
        results = list(self._docs)

        # Apply filters
        for field, op, value in self._filters:

            def compare(doc_val: Any, target_val: Any, op_func) -> bool:
                if doc_val is None:
                    return False

                d_v = doc_val
                t_v = target_val

                if hasattr(d_v, "timestamp") and isinstance(t_v, str):
                    try:  # noqa: SIM105
                        t_v = datetime.datetime.fromisoformat(
                            t_v.replace("Z", "+00:00")
                        )
                    except ValueError:
                        pass

                try:
                    return op_func(d_v, t_v)
                except Exception:
                    return False

            ops = {
                "<": operator.lt,
                "<=": operator.le,
                ">": operator.gt,
                ">=": operator.ge,
                "==": operator.eq,
                "!=": operator.ne,
            }

            op_func = ops.get(op)
            if op_func is None:
                continue

            results = [
                d for d in results if compare(self._get_value(d, field), value, op_func)
            ]

        # Apply sort
        if self._order_by:
            direction = self._order_by[0][1]
            reverse = False
            if direction is not None:
                dir_str = str(direction).upper()
                reverse = dir_str.endswith("DESCENDING")

            def get_key(doc: _InMemoryFirestoreDocument) -> tuple[Any, ...]:
                key_parts: list[Any] = []
                for field, _ in self._order_by:
                    val = self._get_value(doc, field)
                    if val is None:
                        val = datetime.datetime.min.replace(tzinfo=UTC)
                    key_parts.append(val)
                return tuple(key_parts)

            try:  # noqa: SIM105
                results.sort(key=get_key, reverse=reverse)
            except Exception:  # noqa: S110
                pass

        # Apply start_after cursor
        if self._start_after and self._order_by:
            cursor = []
            cursor_doc_id = None
            for value in self._start_after:
                if hasattr(value, "id"):
                    # Extract ordered field values from document cursor
                    for field, _ in self._order_by:
                        cursor_value = self._get_value(value, field)
                        if hasattr(cursor_value, "id"):
                            cursor_value = cursor_value.id
                        cursor.append(cursor_value)
                    # Capture document ID for tie-breaking when sort values are equal
                    cursor_doc_id = value.id
                else:
                    cursor.append(value)

            def cmp(a: Any, b: Any) -> int:
                if isinstance(a, datetime.datetime) and isinstance(
                    b, datetime.datetime
                ):
                    return (a > b) - (a < b)
                return (str(a) > str(b)) - (str(a) < str(b))

            def is_after(
                key_values: tuple[Any, ...], cursor_values: list[Any], doc_id: str
            ) -> bool:
                for key_value, cursor_value in zip(
                    key_values, cursor_values, strict=False
                ):
                    comparison = cmp(key_value, cursor_value)
                    if comparison == 0:
                        continue
                    return comparison < 0 if reverse else comparison > 0
                # All order_by values are equal - use document ID as tie-breaker
                # This matches Firestore behavior for deterministic pagination
                if cursor_doc_id is not None:
                    doc_id_comparison = cmp(doc_id, cursor_doc_id)
                    return doc_id_comparison < 0 if reverse else doc_id_comparison > 0
                return False

            filtered = []
            for doc in results:
                key_values: list[Any] = []
                for field, _ in self._order_by:
                    key_value = self._get_value(doc, field)
                    if hasattr(key_value, "id"):
                        key_value = key_value.id
                    key_values.append(key_value)
                if is_after(tuple(key_values), cursor, doc.id):
                    filtered.append(doc)
            results = filtered

        # Apply limit
        if self._limit is not None:
            results = results[: self._limit]

        if self._select_fields:
            selected = []
            for doc in results:
                data = doc.to_dict()
                filtered_data = {key: data.get(key) for key in self._select_fields}
                selected_doc = _InMemoryFirestoreDocument(
                    doc.id, parent_path=doc._parent_path
                )
                selected_doc._data = filtered_data
                selected.append(selected_doc)
            results = selected

        return results


class _InMemoryFirestoreCountQuery:
    """Count aggregate query for in-memory collections."""

    def __init__(
        self, collection: "_InMemoryFirestoreCollection", alias: str = "total"
    ) -> None:
        self._collection = collection
        self._alias = alias

    def get(self) -> list[dict[str, int]]:
        return [{self._alias: len(list(self._collection.stream()))}]


class _InMemoryFirestoreCollection:
    """Simple in-memory collection used when MOCK_SERVICES_MODE is enabled."""

    def __init__(self, name: str, parent_path: str = "") -> None:
        self.name = name
        self._parent_path = parent_path
        self._docs: dict[str, _InMemoryFirestoreDocument] = {}
        self._doc_counter = 0

    def document(self, doc_id: str | None = None) -> _InMemoryFirestoreDocument:
        if doc_id is None:
            self._doc_counter += 1
            doc_id = f"generated-id-{self._doc_counter}"

        if doc_id not in self._docs:
            path = (
                f"{self._parent_path}/{self.name}" if self._parent_path else self.name
            )
            self._docs[doc_id] = _InMemoryFirestoreDocument(doc_id, parent_path=path)

        return self._docs[doc_id]

    def stream(self) -> list[_InMemoryFirestoreDocument]:
        return list(self._docs.values())

    def add(
        self, data: dict[str, Any]
    ) -> tuple[datetime.datetime, _InMemoryFirestoreDocument]:
        doc = self.document()
        doc.set(data)
        fake_timestamp = datetime.datetime.now(UTC)
        return fake_timestamp, doc

    def order_by(self, field: Any, direction: Any = None) -> "_InMemoryFirestoreQuery":
        return _InMemoryFirestoreQuery(
            self._docs.values(), order_by=[(field, direction)]
        )

    def limit(self, limit: int) -> "_InMemoryFirestoreQuery":
        """Mock limit method."""
        return _InMemoryFirestoreQuery(self._docs.values(), limit=limit)

    def where(self, field: Any, op: str, value: Any) -> "_InMemoryFirestoreQuery":
        return _InMemoryFirestoreQuery(
            self._docs.values(), filters=[(field, op, value)]
        )

    def start_after(self, *values: Any) -> "_InMemoryFirestoreQuery":
        """Mock start_after method."""
        return _InMemoryFirestoreQuery(self._docs.values(), start_after=tuple(values))

    def select(self, field_paths: Any) -> "_InMemoryFirestoreQuery":
        if isinstance(field_paths, str):
            selected_fields = [field_paths]
        else:
            selected_fields = list(field_paths)
        return _InMemoryFirestoreQuery(
            self._docs.values(), select_fields=selected_fields
        )

    def count(self, alias: str = "total") -> "_InMemoryFirestoreCountQuery":
        """Mock count() aggregation."""
        return _InMemoryFirestoreCountQuery(self, alias=alias)


class _InMemoryFirestoreClient:
    def __init__(self) -> None:
        self._collections: dict[str, _InMemoryFirestoreCollection] = {}

    def collection(self, path: str) -> _InMemoryFirestoreCollection:
        return self._collections.setdefault(
            path, _InMemoryFirestoreCollection(path, parent_path="")
        )

    def document(self, path: str) -> _InMemoryFirestoreDocument:
        parts = path.split("/")
        if len(parts) == 2:
            collection_name, doc_id = parts
            return self.collection(collection_name).document(doc_id)
        if len(parts) == 4:
            parent_collection, parent_id, sub_collection, doc_id = parts
            parent_doc = self.collection(parent_collection).document(parent_id)
            return parent_doc.collection(sub_collection).document(doc_id)
        doc_id = parts[-1] if parts else "unknown"
        return _InMemoryFirestoreDocument(doc_id)

    def reset(self) -> None:
        """Reset all collections (useful for testing)."""
        self._collections.clear()


# Singleton instance for MOCK_SERVICES_MODE to persist state across tool calls
_mock_client_singleton: _InMemoryFirestoreClient | None = None


def reset_mock_firestore() -> None:
    """Reset the mock Firestore singleton (useful for testing).

    This clears all data from the in-memory Firestore client and resets
    the singleton instance. Should only be called in test environments.
    """
    global _mock_client_singleton  # noqa: PLW0602
    if _mock_client_singleton is not None:
        _mock_client_singleton.reset()
        logging_util.info("Mock Firestore singleton reset")


def _truncate_log_json(
    data: Any,
    max_lines: int = MAX_LOG_LINES,
    json_serializer: Any = json_default_serializer,
) -> str:
    """Truncate JSON logs to max_lines to prevent log spam."""
    try:
        # Use provided serializer or fallback to str
        serializer = json_serializer if json_serializer is not None else str
        json_str = json.dumps(data, indent=2, default=serializer)
        lines = json_str.split("\n")
        if len(lines) <= max_lines:
            return json_str

        # Truncate and add indicator
        truncated_lines = lines[: max_lines - 1] + [
            f"... (truncated, showing {max_lines - 1}/{len(lines)} lines)"
        ]
        return "\n".join(truncated_lines)
    except Exception:
        # Fallback to string representation if JSON fails
        return str(data)[:500] + "..." if len(str(data)) > 500 else str(data)


def _perform_append(
    target_list: list,
    items_to_append: Any | list[Any],
    key_name: str,
    deduplicate: bool = False,
) -> None:
    """
    Safely appends one or more items to a target list, with an option to prevent duplicates.
    This function modifies the target_list in place.
    """
    if not isinstance(items_to_append, list):
        items_to_append = [items_to_append]  # Standardize to list

    newly_added_items: list[Any] = []
    for item in items_to_append:
        # If deduplication is on, skip items already in the list
        if deduplicate and item in target_list:
            continue
        target_list.append(item)
        newly_added_items.append(item)

    if newly_added_items:
        logging_util.info(
            f"APPEND/SAFEGUARD: Added {len(newly_added_items)} new items to '{key_name}'."
        )
    else:
        logging_util.info(
            f"APPEND/SAFEGUARD: No new items were added to '{key_name}' (duplicates may have been found)."
        )


class MissionHandler:
    """
    Handles mission-related operations for game state management.
    Consolidates mission processing, conversion, and updates.
    """

    @staticmethod
    def initialize_missions_list(state_to_update: dict[str, Any], key: str) -> None:
        """Initialize active_missions as empty list if it doesn't exist or is wrong type."""
        if key not in state_to_update or not isinstance(state_to_update.get(key), list):
            state_to_update[key] = []

    @staticmethod
    def find_existing_mission_index(
        missions_list: list[dict[str, Any]], mission_id: str
    ) -> int:
        """Find the index of an existing mission by mission_id. Returns -1 if not found."""
        for i, existing_mission in enumerate(missions_list):
            if (
                isinstance(existing_mission, dict)
                and existing_mission.get("mission_id") == mission_id
            ):
                return i
        return -1

    @staticmethod
    def process_mission_data(
        state_to_update: dict[str, Any],
        key: str,
        mission_id: str,
        mission_data: dict[str, Any],
    ) -> None:
        """Process a single mission, either updating existing or adding new."""
        # Ensure the mission has an ID
        if "mission_id" not in mission_data:
            mission_data["mission_id"] = mission_id

        # Check if this mission already exists (by mission_id)
        existing_mission_index = MissionHandler.find_existing_mission_index(
            state_to_update[key], mission_id
        )

        if existing_mission_index != -1:
            # Update existing mission
            logging_util.info(f"Updating existing mission: {mission_id}")
            state_to_update[key][existing_mission_index].update(mission_data)
        else:
            # Add new mission
            logging_util.info(f"Adding new mission: {mission_id}")
            state_to_update[key].append(mission_data)

    @staticmethod
    def handle_missions_dict_conversion(
        state_to_update: dict[str, Any], key: str, missions_dict: dict[str, Any]
    ) -> None:
        """Convert dictionary format missions to list append format."""
        for mission_id, mission_data in missions_dict.items():
            if isinstance(mission_data, dict):
                MissionHandler.process_mission_data(
                    state_to_update, key, mission_id, mission_data
                )
            else:
                logging_util.warning(
                    f"Skipping invalid mission data for {mission_id}: not a dictionary"
                )

    @staticmethod
    def handle_active_missions_conversion(
        state_to_update: dict[str, Any], key: str, value: Any
    ) -> None:
        """Handle smart conversion of active_missions from various formats to list."""
        logging_util.warning(
            f"SMART CONVERSION: AI attempted to set 'active_missions' as {type(value).__name__}. Converting to list append."
        )

        # Initialize active_missions as empty list if it doesn't exist
        MissionHandler.initialize_missions_list(state_to_update, key)

        # Convert based on value type
        if isinstance(value, dict):
            # AI is providing missions as a dict like {"main_quest_1": {...}, "side_quest_1": {...}}
            MissionHandler.handle_missions_dict_conversion(state_to_update, key, value)
        else:
            # For other non-list types, log error and skip
            logging_util.error(
                f"Cannot convert {type(value).__name__} to mission list. Skipping."
            )


def _handle_append_syntax(
    state_to_update: dict[str, Any], key: str, value: dict[str, Any]
) -> bool:
    """
    Handle explicit append syntax {'append': ...}.

    Returns:
        bool: True if handled, False otherwise
    """
    if not (isinstance(value, dict) and "append" in value):
        return False

    logging_util.info(f"update_state: Detected explicit append for '{key}'.")
    if key not in state_to_update or not isinstance(state_to_update.get(key), list):
        state_to_update[key] = []
    _perform_append(
        state_to_update[key], value["append"], key, deduplicate=(key == "core_memories")
    )
    return True


def _handle_core_memories_safeguard(
    state_to_update: dict[str, Any], key: str, value: Any
) -> bool:
    """
    Handle safeguard for direct 'core_memories' overwrite.

    Returns:
        bool: True if handled, False otherwise
    """
    if key != "core_memories":
        return False

    logging_util.warning(
        "CRITICAL SAFEGUARD: Intercepted direct overwrite on 'core_memories'. Converting to safe, deduplicated append."
    )
    if key not in state_to_update or not isinstance(state_to_update.get(key), list):
        state_to_update[key] = []
    _perform_append(state_to_update[key], value, key, deduplicate=True)
    return True


# Critical inventory/equipment fields that must be protected from complete overwrite
PROTECTED_INVENTORY_FIELDS = frozenset({"inventory", "equipment", "backpack", "items"})


def _inventory_item_signature(item: Any) -> str:
    """Return a stable signature for inventory list items."""
    if isinstance(item, dict):
        try:
            return json.dumps(item, sort_keys=True)
        except (TypeError, ValueError):
            return str(item)
    return str(item)


def _extract_inventory_delete_criteria(item: dict[str, Any]) -> dict[str, Any]:
    """Return deletion criteria from a list marker item."""
    if item.get(DELETE_TOKEN) != DELETE_TOKEN:
        return {}
    return {key: value for key, value in item.items() if key != DELETE_TOKEN}


def _remove_matching_inventory_item(
    existing_items: list[Any], delete_criteria: dict[str, Any]
) -> bool:
    """Remove one matching item from an existing inventory list."""
    if not delete_criteria:
        return False

    for index, existing_item in enumerate(existing_items):
        if isinstance(existing_item, dict):
            if all(
                existing_item.get(key) == value
                for key, value in delete_criteria.items()
            ):
                del existing_items[index]
                return True
            continue

        if "name" in delete_criteria and existing_item == delete_criteria.get("name"):
            del existing_items[index]
            return True

    return False


def _merge_inventory_items(
    key: str, existing_items: list[Any], incoming_items: list[Any]
) -> list[Any]:
    """Merge list updates for inventory-like fields with delete marker support."""
    merged = list(existing_items)
    seen = {_inventory_item_signature(item) for item in merged}

    for item in incoming_items:
        if isinstance(item, dict) and item.get(DELETE_TOKEN) == DELETE_TOKEN:
            delete_criteria = _extract_inventory_delete_criteria(item)
            if _remove_matching_inventory_item(merged, delete_criteria):
                logging_util.warning(
                    f"INVENTORY SAFEGUARD: Removed item from '{key}' via __DELETE__ marker "
                    f"using criteria {_inventory_item_signature(delete_criteria)}"
                )
            else:
                logging_util.warning(
                    f"INVENTORY SAFEGUARD: No match for '__DELETE__' on '{key}' "
                    f"using criteria {_inventory_item_signature(delete_criteria)}"
                )
            continue

        signature = _inventory_item_signature(item)
        if signature in seen:
            continue
        seen.add(signature)
        merged.append(item)

    return merged


def _handle_inventory_safeguard(
    state_to_update: dict[str, Any], key: str, value: Any
) -> bool:
    """
    Handle safeguard for critical inventory and equipment fields.

    Prevents complete overwrite of inventory-related fields (inventory, equipment,
    backpack, items) by converting direct overwrites to safe merge operations.
    This ensures character items are never accidentally lost or compressed.

    CRITICAL: Character inventory and key secondary character equipment must NEVER
    be forgotten or compressed, per system requirements.

    Returns:
        bool: True if handled, False otherwise
    """
    if key not in PROTECTED_INVENTORY_FIELDS:
        return False

    existing_value = state_to_update.get(key)

    # If there's no existing value, allow the new value to be set
    if existing_value is None:
        return False

    # If both existing and new values are dicts, we'll let dict merge handle it
    if isinstance(existing_value, dict) and isinstance(value, dict):
        return False

    # If both are lists, perform a safe merge with deduplication instead of overwrite
    if isinstance(existing_value, list) and isinstance(value, list):
        logging_util.warning(
            f"INVENTORY SAFEGUARD: Intercepted list overwrite on '{key}'. "
            f"Existing items: {len(existing_value)}, new items: {len(value)}. "
            "Performing safe merge with deduplication to preserve existing items."
        )
        merged = _merge_inventory_items(key, existing_value, value)
        state_to_update[key] = merged
        return True

    # If existing is dict and new is something else, preserve dict structure
    if isinstance(existing_value, dict) and not isinstance(value, dict):
        logging_util.warning(
            f"INVENTORY SAFEGUARD: Blocked type conversion on '{key}' from dict to {type(value).__name__}. "
            "Preserving existing inventory structure."
        )
        return True  # Block the update, keeping existing value

    # If existing is list and new is something else...
    if isinstance(existing_value, list) and not isinstance(value, list):
        # Allow "upgrading" from list to dict if dict has 'items' list
        if (
            isinstance(value, dict)
            and "items" in value
            and isinstance(value["items"], list)
        ):
            logging_util.warning(
                f"INVENTORY SAFEGUARD: Converting '{key}' from list to dict. "
                f"Merging {len(existing_value)} existing items into new 'items' list."
            )
            # Preserve all existing items while applying delete markers from incoming payload.
            merged = _merge_inventory_items(key, existing_value, value["items"])

            value["items"] = merged

            state_to_update[key] = value
            return True  # Handled (allowed with merge)

        logging_util.warning(
            f"INVENTORY SAFEGUARD: Blocked type conversion on '{key}' from list to {type(value).__name__}. "
            "Preserving existing inventory list."
        )
        return True  # Block the update, keeping existing value

    return False


def _handle_companion_equipment_safeguard(
    state_to_update: dict[str, Any], key: str, value: Any
) -> bool:
    """
    Handle safeguard for companion/NPC equipment and inventory data.

    Key secondary characters (companions) have their equipment tracked in npc_data.
    This safeguard ensures companion equipment is never accidentally deleted or
    completely overwritten during state updates.

    CRITICAL: Companion equipment must NEVER be forgotten or compressed.

    Returns:
        bool: True if handled, False otherwise
    """
    # Only handle npc_data updates
    if key != "npc_data":
        return False

    if not isinstance(value, dict):
        return False

    existing_npcs = state_to_update.get(key, {})
    if not isinstance(existing_npcs, dict):
        return False

    # Check each NPC being updated
    for npc_name, npc_update in value.items():
        if npc_update == DELETE_TOKEN:
            # Allow explicit deletion (handled elsewhere)
            continue

        if not isinstance(npc_update, dict):
            continue

        existing_npc = existing_npcs.get(npc_name, {})
        if not isinstance(existing_npc, dict):
            continue

        # Check if this is a companion/party member (key secondary character)
        relationship_raw = existing_npc.get("relationship", "")
        relationship_normalized = (
            relationship_raw.lower() if isinstance(relationship_raw, str) else ""
        )
        is_companion = relationship_normalized in (
            "companion",
            "party_member",
            "ally",
            "follower",
        )
        is_important = existing_npc.get("is_important", False)

        if not (is_companion or is_important):
            continue

        # Protect equipment fields for companions/key NPCs
        for eq_field in ("equipment", "inventory", "items", "backpack"):
            if eq_field not in npc_update:
                continue

            existing_eq = existing_npc.get(eq_field)
            new_eq = npc_update[eq_field]

            if existing_eq is None:
                continue

            # Allow explicit deletion token to pass through unchanged
            if new_eq == DELETE_TOKEN:
                continue

            # Protect list-type equipment from complete overwrite
            if isinstance(existing_eq, list) and isinstance(new_eq, list):
                logging_util.warning(
                    f"COMPANION EQUIPMENT SAFEGUARD: Protecting '{npc_name}' {eq_field}. "
                    f"Merging {len(new_eq)} new items with {len(existing_eq)} existing items."
                )
                # Preserve all existing items and only deduplicate incoming items
                merged = _merge_inventory_items(
                    f"npc_data[{npc_name}].{eq_field}", existing_eq, new_eq
                )
                npc_update[eq_field] = merged

            # Block list equipment from being overwritten by non-lists
            elif isinstance(existing_eq, list) and not isinstance(new_eq, list):
                logging_util.warning(
                    f"COMPANION EQUIPMENT SAFEGUARD: Blocked type conversion for '{npc_name}' {eq_field} "
                    f"from list to {type(new_eq).__name__}. Preserving existing equipment list."
                )
                del npc_update[eq_field]

            # Protect dict-type equipment from type change
            elif isinstance(existing_eq, dict) and not isinstance(new_eq, dict):
                logging_util.warning(
                    f"COMPANION EQUIPMENT SAFEGUARD: Blocked type conversion for '{npc_name}' {eq_field}. "
                    "Preserving existing equipment structure."
                )
                del npc_update[eq_field]

    # Let normal dict merge handle the actual update
    # We've just modified the value dict to protect equipment
    return False  # Return False so dict_merge still processes


def _coerce_npc_data_entry(entry_name: str, entry_value: Any) -> dict[str, Any]:
    """Normalize malformed npc_data entries before merge operations."""
    if isinstance(entry_value, dict):
        return dict(entry_value)

    if isinstance(entry_value, list):
        normalized: dict[str, Any] = {"name": entry_name}
        status_values: list[str] = []

        for item in entry_value:
            if isinstance(item, dict):
                normalized.update(item)
                continue
            if not isinstance(item, str):
                status_values.append(str(item))
                continue

            if ":" in item:
                key, value = item.split(":", 1)
                normalized[key.strip()] = value.strip()
            else:
                status_values.append(item.strip())

        if status_values and "status" not in normalized:
            normalized["status"] = ", ".join(status_values)

        if len(normalized) == 1:
            logging_util.warning(
                f"⚠️ NPC '{entry_name}' state update entry is unparsable list: {entry_value}"
            )
        return normalized

    if isinstance(entry_value, str):
        if not entry_value.strip():
            return {"name": entry_name}
        return {"name": entry_name, "status": entry_value.strip()}

    if entry_value is None:
        return {"name": entry_name}

    return {"name": entry_name, "status": str(entry_value)}


def _merge_background_events(existing: list[Any], updates: list[Any]) -> list[Any]:
    """Merge background_events (or rumors) lists by actor key.

    When the LLM emits a partial update object such as
    ``{"actor": "Trade Ship", "status": "discovered"}`` it only intends to
    update the status of an existing event — not to replace it.  A plain list
    overwrite would clobber all other fields (action, event_type, location …).
    This helper matches incoming entries to existing ones by ``actor`` and
    merges only the provided keys, preserving the rest.

    New entries (no matching actor) are appended unchanged.
    """
    result: list[Any] = [copy.deepcopy(e) for e in existing if isinstance(e, dict)]
    for update_event in updates:
        if not isinstance(update_event, dict):
            result.append(update_event)
            continue
        actor = update_event.get("actor")
        if not actor:
            result.append(copy.deepcopy(update_event))
            continue
        matched = next(
            (e for e in result if isinstance(e, dict) and e.get("actor") == actor),
            None,
        )
        if matched is not None:
            matched.update(update_event)
        else:
            result.append(copy.deepcopy(update_event))
    return result


def _handle_dict_merge(state_to_update: dict[str, Any], key: str, value: Any) -> bool:
    """
    Handle dictionary merging and creation.

    Returns:
        bool: True if handled, False otherwise
    """
    if not isinstance(value, dict):
        return False

    # Case 1: Recursive merge for nested dictionaries
    if isinstance(state_to_update.get(key), collections.abc.Mapping):
        state_to_update[key] = update_state_with_changes(
            state_to_update.get(key, {}), value
        )
        return True

    # Case 2: Create new dictionary when incoming value is dict but existing is not
    state_to_update[key] = update_state_with_changes({}, value)
    return True


def _handle_delete_token(state_to_update: dict[str, Any], key: str, value: Any) -> bool:
    """
    Handle DELETE_TOKEN for field deletion.

    Returns:
        bool: True if handled, False otherwise
    """
    if value != DELETE_TOKEN:
        return False

    if key in state_to_update:
        logging_util.info(f"update_state: Deleting key '{key}' due to DELETE_TOKEN.")
        del state_to_update[key]
    else:
        logging_util.info(
            f"update_state: Attempted to delete key '{key}' but it doesn't exist."
        )
    return True


def _handle_string_to_dict_update(
    state_to_update: dict[str, Any], key: str, value: Any
) -> bool:
    """
    Handle string updates to existing dictionaries (preserve dict structure).

    Returns:
        bool: True if handled, False otherwise
    """
    if not isinstance(state_to_update.get(key), collections.abc.Mapping):
        return False

    logging_util.info(
        f"update_state: Preserving dict structure for key '{key}', adding 'status' field."
    )
    existing_dict = state_to_update[key].copy()
    existing_dict["status"] = value
    state_to_update[key] = existing_dict

    return True


def update_state_with_changes(
    state_to_update: dict[str, Any], changes: dict[str, Any]
) -> dict[str, Any]:
    """
    Recursively updates a state dictionary with a changes dictionary using intelligent merge logic.

    This is the core function for applying AI-generated state updates to the game state.
    It implements sophisticated handling for different data types and update patterns.

    Key Features:
    - Explicit append syntax: {'append': [items]} for safe list operations
    - Core memories safeguard: Prevents accidental overwrite of important game history
    - Inventory safeguard: Protects character inventory/equipment from compression
    - Companion equipment safeguard: Protects key secondary character equipment
    - Recursive dictionary merging: Deep merge for nested objects
    - DELETE_TOKEN support: Allows removal of specific fields
    - Mission smart conversion: Handles various mission data formats
    - Numeric field conversion: Ensures proper data types
    - Defensive programming: Validates data structures before operations

    Update Patterns Handled:
    1. DELETE_TOKEN - Removes fields marked for deletion
    2. Explicit append - Safe list operations with deduplication
    3. Core memories safeguard - Protects critical game history
    4. Inventory safeguard - Protects inventory/equipment/backpack/items from overwrite
    5. Companion equipment safeguard - Protects key secondary character equipment
    6. Mission conversion - Handles dict-to-list conversion for missions
    7. Dictionary merging - Recursive merge for nested structures
    8. String-to-dict preservation - Maintains existing dict structures
    9. Simple overwrite - Default behavior for primitive values

    CRITICAL SAFEGUARDS:
    - Character inventory must NEVER be forgotten or compressed
    - Key secondary character (companion) equipment must NEVER be forgotten
    - These safeguards convert overwrites to safe merge operations

    Args:
        state_to_update (dict): The current game state to modify
        changes (dict): Changes to apply (typically from AI response)

    Returns:
        dict: Updated state dictionary with changes applied

    Example Usage:
        current_state = {"health": 100, "items": ["sword"]}
        changes = {"health": 80, "items": {"append": ["potion"]}}
        result = update_state_with_changes(current_state, changes)
        # Result: {"health": 80, "items": ["sword", "potion"]}
    """
    if logging_util.getLogger().isEnabledFor(logging_util.DEBUG):
        logging_util.debug(
            "--- update_state_with_changes: applying changes:\n%s",
            _truncate_log_json(changes),
        )

    # Auto-initialize completed_missions if active_missions exists but completed_missions doesn't
    # Fix for older campaigns that predate the completed_missions field
    if (
        "active_missions" in state_to_update
        and "completed_missions" not in state_to_update
    ):
        logging_util.info(
            "Auto-initializing completed_missions field for older campaign"
        )
        state_to_update["completed_missions"] = []

    # Normalize dotted keys in changes (e.g., "player_character_data.level" -> nested dict)
    # This handles LLM responses that use dotted paths instead of nested structures
    changes = _normalize_dotted_keys_in_place(changes)

    for key, value in changes.items():
        # Try each handler in order of precedence

        # Case 1: Handle DELETE_TOKEN first (highest priority)
        if _handle_delete_token(state_to_update, key, value):
            continue

        # Case 2: Explicit append syntax
        if _handle_append_syntax(state_to_update, key, value):
            continue

        # Case 3: Core memories safeguard
        if _handle_core_memories_safeguard(state_to_update, key, value):
            continue

        # Case 4: Inventory safeguard - protect character items from overwrite
        if _handle_inventory_safeguard(state_to_update, key, value):
            continue

        # Case 5: Companion equipment safeguard - protect key secondary character equipment
        # Note: This modifies value dict in-place but returns False to let dict_merge proceed
        _handle_companion_equipment_safeguard(state_to_update, key, value)

        if key == "npc_data" and isinstance(value, dict):
            existing_npc_data = (
                state_to_update.get(key)
                if isinstance(state_to_update.get(key), dict)
                else {}
            )
            normalized_npc_data = {
                str(npc_name): (
                    _coerce_npc_data_entry(str(npc_name), npc_update)
                    if npc_update != DELETE_TOKEN
                    else npc_update
                )
                for npc_name, npc_update in value.items()
            }
            for npc_name, npc_update in value.items():
                npc_name_str = str(npc_name)
                if npc_update == DELETE_TOKEN:
                    continue
                existing_entry = (
                    existing_npc_data.get(npc_name_str, {})
                    if isinstance(existing_npc_data, dict)
                    else {}
                )
                if not isinstance(existing_entry, dict):
                    continue
                existing_name = existing_entry.get("name")
                if existing_name is not None:
                    normalized_entry = normalized_npc_data[npc_name_str]
                    normalized_name = normalized_entry.get("name")
                    if normalized_name is None or str(normalized_name) == npc_name_str:
                        normalized_entry["name"] = existing_name
            value = normalized_npc_data  # noqa: PLW2901

        # Case 6: Auto-initialize completed_missions if active_missions is being updated
        # CRITICAL: Must run BEFORE smart conversion (which calls continue)
        # Fix for bug where older campaigns don't have completed_missions field
        if key == "active_missions" and "completed_missions" not in state_to_update:
            logging_util.info(
                "Auto-initializing completed_missions field (missing in older campaigns)"
            )
            state_to_update["completed_missions"] = []

        # Case 7: Active missions smart conversion
        if key == "active_missions" and not isinstance(value, list):
            MissionHandler.handle_active_missions_conversion(
                state_to_update, key, value
            )
            continue

        # Case 8: Completed missions smart conversion (same as active_missions)
        if key == "completed_missions" and not isinstance(value, list):
            MissionHandler.handle_active_missions_conversion(
                state_to_update, key, value
            )
            continue

        # Case 9: Dictionary operations (merge or create)
        if _handle_dict_merge(state_to_update, key, value):
            continue

        # Case 10: String to dict updates (preserve structure)
        if _handle_string_to_dict_update(state_to_update, key, value):
            continue

        # Case 10b: background_events / rumors — actor-keyed merge to preserve fields.
        # LLM sometimes emits partial update objects (e.g. {"actor": "X", "status": "discovered"})
        # to update a single field on an existing event.  Simple overwrite would clobber all
        # other fields (action, event_type, location, …).  Match by actor and merge instead.
        if key in ("background_events", "rumors") and isinstance(value, list):
            existing = state_to_update.get(key)
            if isinstance(existing, list):
                state_to_update[key] = _merge_background_events(existing, value)
                continue

        # Case 11: Simple overwrite for everything else
        # Convert numeric fields from strings to integers
        # Note: We handle conversion here instead of in _handle_dict_merge to avoid
        # double conversion when dictionaries are recursively processed
        if isinstance(value, dict):
            # For dictionaries, use convert_dict to handle nested conversions
            converted_value = NumericFieldConverter.convert_dict(value)
        else:
            # For simple values, use convert_value
            converted_value = NumericFieldConverter.convert_value(key, value)
        state_to_update[key] = converted_value
    logging_util.debug("--- update_state_with_changes: finished ---")
    return state_to_update


def _expand_dot_notation(d: dict[str, Any]) -> dict[str, Any]:
    """
    Expands a dictionary with dot-notation keys into a nested dictionary.
    Example: {'a.b': 1, 'c': 2} -> {'a': {'b': 1}, 'c': 2}

    Dot characters are reserved for path notation. Keys with literal dots are
    not supported by this helper and should be avoided in update payloads.
    """
    expanded_dict: dict[str, Any] = {}
    terminal_paths: set[tuple[str, ...]] = set()
    for k, v in d.items():
        if "." in k:
            keys = k.split(".")
            if any(part == "" for part in keys):
                raise ValueError(
                    "Invalid dot-notation key; leading, trailing, or repeated dots "
                    f"are not supported: '{k}'"
                )
            d_ref = expanded_dict
            prefix: list[str] = []
            for part in keys[:-1]:
                prefix.append(part)
                if tuple(prefix) in terminal_paths:
                    raise ValueError(
                        "Conflicting keys in dot-notation expansion: "
                        f"cannot set '{k}' because '{'.'.join(prefix)}' "
                        "already exists as a terminal value"
                    )
                existing = d_ref.get(part)
                if existing is not None and not isinstance(existing, dict):
                    raise ValueError(
                        "Conflicting keys in dot-notation expansion: "
                        f"cannot set '{k}' because '{part}' already exists as "
                        "a non-dict value"
                    )
                if part not in d_ref:
                    d_ref[part] = {}
                d_ref = d_ref[part]
            final_key = keys[-1]
            if tuple(keys) in terminal_paths:
                raise ValueError(
                    "Conflicting keys in dot-notation expansion: "
                    f"'{k}' already exists as a terminal value"
                )
            existing_final = d_ref.get(final_key)
            if existing_final is not None and isinstance(existing_final, dict):
                raise ValueError(
                    "Conflicting keys in dot-notation expansion: "
                    f"'{k}' would overwrite an existing nested structure"
                )
            d_ref[final_key] = v
            terminal_paths.add(tuple(keys))
        else:
            if k in expanded_dict:
                raise ValueError(
                    "Conflicting keys in dot-notation expansion: "
                    f"'{k}' overlaps with an existing nested update"
                )
            expanded_dict[k] = v
            terminal_paths.add((k,))
    return expanded_dict


def _normalize_dotted_keys_in_place(d: dict[str, Any]) -> dict[str, Any]:
    """
    Normalize a dict by merging dotted-notation keys into nested structures.

    Unlike _expand_dot_notation which creates a new dict, this function:
    1. Works with existing nested structures in the dict
    2. Merges dotted keys into those structures
    3. Removes the original dotted keys

    Example:
        Input: {"player": {"name": "X"}, "player.level": 5}
        Output: {"player": {"name": "X", "level": 5}}

    This handles the common case where LLM outputs both nested objects AND
    dotted paths for additional fields.
    """
    # Find all dotted keys
    dotted_keys = [k for k in d if "." in k]

    for dotted_key in dotted_keys:
        parts = dotted_key.split(".")
        value = d[dotted_key]

        # Navigate/create nested structure
        current = d
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            elif not isinstance(current[part], dict):
                # Can't merge into non-dict - skip this key
                logging_util.warning(
                    f"Cannot merge dotted key '{dotted_key}': '{part}' is not a dict"
                )
                break
            current = current[part]
        else:
            # Successfully navigated - set the value
            final_key = parts[-1]
            current[final_key] = value
            # Remove the original dotted key
            del d[dotted_key]

    return d


# json_serial and json_default_serializer are now imported from mvp_site.serialization


# ===== Avatar Storage Functions =====

_STORAGE_BUCKET = os.environ.get(
    "AVATAR_STORAGE_BUCKET",
    os.environ.get("FIREBASE_STORAGE_BUCKET", "worldarchitecture-ai-frontend-static"),
)
# Reject Firebase URL-format bucket names — they aren't valid GCS bucket names.
# The actual GCS bucket for avatar storage is worldarchitecture-ai-frontend-static.
if _STORAGE_BUCKET.endswith(".firebasestorage.app"):
    _STORAGE_BUCKET = "worldarchitecture-ai-frontend-static"


def upload_user_avatar(
    user_id: str,
    file_data: bytes,
    content_type: str,
    file_extension: str,
) -> str:
    """Upload user avatar to Firebase Storage and return public URL.

    Args:
        user_id: The user ID to associate with the avatar
        file_data: Raw bytes of the image file
        content_type: MIME type of the image (e.g., 'image/jpeg')
        file_extension: Validated file extension derived from file contents

    Returns:
        Public URL of the uploaded avatar (avatars are stored as public assets)
    """
    if file_extension not in AVATAR_EXTENSIONS:
        raise ValueError(f"Unsupported avatar extension: {file_extension}")

    try:
        bucket = storage.bucket(_STORAGE_BUCKET)
        blob = bucket.blob(f"avatars/{user_id}/avatar.{file_extension}")
        blob.upload_from_string(file_data, content_type=content_type)
        blob.make_public()
        return blob.public_url
    except Exception as exc:  # noqa: BLE001 - bubble up for API error handling
        logging_util.error(f"Avatar upload failed for user {user_id}: {exc}")
        raise


def delete_user_avatar(user_id: str) -> int:
    """Delete user's avatar from Firebase Storage.

    Args:
        user_id: The user ID whose avatar should be deleted

    Returns:
        Number of avatar blobs deleted
    """
    try:
        bucket = storage.bucket(_STORAGE_BUCKET)
        blobs = bucket.list_blobs(prefix=f"avatars/{user_id}/")
    except Exception as exc:  # noqa: BLE001 - surface critical storage errors
        logging_util.error(f"Failed to list avatar blobs for user {user_id}: {exc}")
        raise

    deleted_count = 0
    for blob in blobs:
        try:
            blob.delete()
            deleted_count += 1
        except Exception as exc:  # noqa: BLE001 - continue best-effort deletion
            logging_util.warning(
                f"Failed to delete avatar blob for user {user_id}: {exc}"
            )
    return deleted_count


def upload_campaign_avatar(
    user_id: str, campaign_id: str, file_data: bytes, content_type: str
) -> str:
    """Upload campaign-specific avatar to Firebase Storage.

    Args:
        user_id: The user ID who owns the campaign
        campaign_id: The campaign ID to associate with the avatar
        file_data: Raw bytes of the image file
        content_type: MIME type of the image (e.g., 'image/jpeg')

    Returns:
        Public URL of the uploaded avatar

    Raises:
        ValueError: If the content_type is not an allowed image type.
    """
    ext = content_type.split("/")[-1]
    if ext not in AVATAR_EXTENSIONS:
        raise ValueError(f"Unsupported campaign avatar type: {content_type}")

    try:
        bucket = storage.bucket(_STORAGE_BUCKET)
        blob = bucket.blob(f"campaign_avatars/{user_id}/{campaign_id}/avatar.{ext}")
        blob.upload_from_string(file_data, content_type=content_type)
        blob.make_public()
        return blob.public_url
    except Exception as exc:
        logging_util.error(
            f"Failed to upload campaign avatar for {user_id}/{campaign_id}: {exc}"
        )
        raise


def delete_campaign_avatar(user_id: str, campaign_id: str) -> int:
    """Delete campaign-specific avatar from Firebase Storage.

    Args:
        user_id: The user ID who owns the campaign
        campaign_id: The campaign ID whose avatar should be deleted

    Returns:
        Number of avatar blobs deleted
    """
    try:
        bucket = storage.bucket(_STORAGE_BUCKET)
        blobs = bucket.list_blobs(prefix=f"campaign_avatars/{user_id}/{campaign_id}/")
    except Exception as exc:  # noqa: BLE001 - surface critical storage errors
        logging_util.error(
            f"Failed to list campaign avatar blobs for {user_id}/{campaign_id}: {exc}"
        )
        raise

    deleted_count = 0
    for blob in blobs:
        try:
            blob.delete()
            deleted_count += 1
        except Exception as exc:  # noqa: BLE001 - continue best-effort deletion
            logging_util.warning(
                f"Failed to delete campaign avatar blob {user_id}/{campaign_id}: {exc}"
            )
    return deleted_count


AVATAR_EXTENSIONS: tuple[str, ...] = ("jpeg", "png", "gif", "webp")
AVATAR_CONTENT_TYPE_BY_EXT: dict[str, str] = {
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
}
_CONTENT_TYPE_MAP: dict[str, str] = AVATAR_CONTENT_TYPE_BY_EXT


def _get_avatar_extension_from_url(avatar_url: str | None) -> str | None:
    """Derive avatar extension from a GCS public URL.

    Extracts the file extension by parsing the URL path and matching the
    basename against ``avatar.<ext>`` for known extensions.
    Returns ``None`` if the URL is absent or the path basename does not
    match an avatar file.
    """
    if not avatar_url:
        return None
    try:
        basename = urlparse(avatar_url).path.split("/")[-1]
    except Exception:  # noqa: BLE001
        return None
    for ext in AVATAR_EXTENSIONS:
        if basename == f"avatar.{ext}":
            return ext
    return None


def _probe_avatar_extension(blob_prefix: str) -> str | None:
    """Return the extension of the most recently updated avatar blob under blob_prefix.

    Returns ``None`` if no avatar exists. Propagates GCS API errors so callers
    receive 500 rather than a misleading 404.
    """
    bucket = storage.bucket(_STORAGE_BUCKET)
    candidates = [
        (ext, blob.updated)
        for blob in bucket.list_blobs(prefix=blob_prefix)
        for ext in [blob.name.split("/")[-1].removeprefix("avatar.")]
        if ext in AVATAR_EXTENSIONS
    ]
    if not candidates:
        return None
    return max(
        candidates,
        key=lambda c: c[1]
        if c[1] is not None
        else datetime.datetime.min.replace(tzinfo=datetime.UTC),
    )[0]


def _probe_avatar_extension_for_user(user_id: str) -> str | None:
    """Try to detect avatar extension for a user by probing GCS."""
    return _probe_avatar_extension(f"avatars/{user_id}/avatar.")


def _probe_avatar_extension_for_campaign(user_id: str, campaign_id: str) -> str | None:
    """Try to detect avatar extension for a campaign by probing GCS."""
    return _probe_avatar_extension(f"campaign_avatars/{user_id}/{campaign_id}/avatar.")


def download_user_avatar(
    user_id: str, *, avatar_url_from_firestore: str | None = None
) -> tuple[bytes, str]:
    """Download user avatar from Firebase Storage.

    Extension resolution order:
    1. Authoritative extension parsed from the stored ``avatar_url`` (fastest).
    2. GCS probe as fallback — raises on GCS failures so callers receive a
       500 instead of a misleading 404.

    Args:
        user_id: The user ID whose avatar to download.
        avatar_url_from_firestore: Optional avatar_url from Firestore user settings.
            When provided, its extension is used directly.

    Returns:
        Tuple of ``(bytes, content_type)``.

    Raises:
        ValueError: No avatar found for this user.
    """
    ext = _get_avatar_extension_from_url(avatar_url_from_firestore)
    if ext is None:
        ext = _probe_avatar_extension_for_user(user_id)
    if ext is None:
        raise ValueError(f"No avatar found for user {user_id}")

    content_type = _CONTENT_TYPE_MAP[ext]
    bucket = storage.bucket(_STORAGE_BUCKET)
    blob = bucket.blob(f"avatars/{user_id}/avatar.{ext}")
    try:
        data = blob.download_as_bytes()
    except Exception as e:
        if "NotFound" in type(e).__name__ or "404" in str(e):
            # Firestore hint may be stale — re-probe for a different extension.
            fallback_ext = _probe_avatar_extension_for_user(user_id)
            if fallback_ext and fallback_ext != ext:
                fallback_blob = bucket.blob(f"avatars/{user_id}/avatar.{fallback_ext}")
                try:
                    data = fallback_blob.download_as_bytes()
                    return data, _CONTENT_TYPE_MAP[fallback_ext]
                except Exception as fe:
                    # Re-raise non-404 storage errors (auth failures, 500s, etc.) so
                    # callers receive an accurate status rather than a misleading 404.
                    if "NotFound" not in type(fe).__name__ and "404" not in str(fe):
                        raise
            raise ValueError(
                f"No avatar found for user {user_id} (blob deleted)"
            ) from e
        raise
    return data, content_type


def download_campaign_avatar(
    user_id: str,
    campaign_id: str,
    *,
    avatar_url_from_firestore: str | None = None,
) -> tuple[bytes, str]:
    """Download campaign avatar from Firebase Storage.

    Extension resolution order:
    1. Authoritative extension parsed from the stored ``avatar_url`` (fastest).
    2. GCS probe as fallback — raises on GCS failures so callers receive a
       500 instead of a misleading 404.

    Args:
        user_id: The user ID who owns the campaign.
        campaign_id: The campaign ID whose avatar to download.
        avatar_url_from_firestore: Optional avatar_url from the campaign Firestore
            document. When provided, its extension is used directly.

    Returns:
        Tuple of ``(bytes, content_type)``.

    Raises:
        ValueError: No avatar found for this campaign.
    """
    ext = _get_avatar_extension_from_url(avatar_url_from_firestore)
    if ext is None:
        ext = _probe_avatar_extension_for_campaign(user_id, campaign_id)
    if ext is None:
        raise ValueError(f"No avatar found for campaign {campaign_id}")

    content_type = _CONTENT_TYPE_MAP[ext]
    bucket = storage.bucket(_STORAGE_BUCKET)
    blob = bucket.blob(f"campaign_avatars/{user_id}/{campaign_id}/avatar.{ext}")
    try:
        data = blob.download_as_bytes()
    except Exception as e:
        if "NotFound" in type(e).__name__ or "404" in str(e):
            # Firestore hint may be stale — re-probe for a different extension.
            fallback_ext = _probe_avatar_extension_for_campaign(user_id, campaign_id)
            if fallback_ext and fallback_ext != ext:
                fallback_blob = bucket.blob(
                    f"campaign_avatars/{user_id}/{campaign_id}/avatar.{fallback_ext}"
                )
                try:
                    data = fallback_blob.download_as_bytes()
                    return data, _CONTENT_TYPE_MAP[fallback_ext]
                except Exception as fe:
                    # Re-raise non-404 storage errors (auth failures, 500s, etc.) so
                    # callers receive an accurate status rather than a misleading 404.
                    if "NotFound" not in type(fe).__name__ and "404" not in str(fe):
                        raise
            raise ValueError(
                f"No avatar found for campaign {campaign_id} (blob deleted)"
            ) from e
        raise
    return data, content_type


def get_db() -> firestore.Client:
    """Return an initialized Firestore client or fail fast.

    Tests should patch this helper rather than relying on in-module mocks so that
    production code paths always exercise the real Firestore SDK.

    In MOCK_SERVICES_MODE, returns a singleton in-memory client to persist state
    across tool calls within the same MCP server session.
    """
    global _mock_client_singleton  # noqa: PLW0603

    if os.getenv("MOCK_SERVICES_MODE", "").lower() == "true":
        if _mock_client_singleton is None:
            logging_util.info(
                "MOCK_SERVICES_MODE enabled - creating singleton in-memory Firestore client"
            )
            _mock_client_singleton = _InMemoryFirestoreClient()
        else:
            logging_util.info(
                "MOCK_SERVICES_MODE enabled - reusing singleton in-memory Firestore client"
            )
        return _mock_client_singleton

    try:
        firebase_admin.get_app()
    except ValueError:
        try:
            logging_util.info("Firebase not initialized - attempting to initialize now")

            # Import the service account loader
            from mvp_site.service_account_loader import get_service_account_credentials

            # WORLDAI_* vars take precedence for WorldArchitect.AI repo-specific config
            worldai_creds_path = os.getenv("WORLDAI_GOOGLE_APPLICATION_CREDENTIALS")

            # Try loading credentials (file first, then env vars fallback)
            try:
                creds_dict = get_service_account_credentials(
                    file_path=worldai_creds_path,
                    fallback_to_env=True,
                    require_env_vars=False,
                )
                logging_util.info("Successfully loaded service account credentials")
                firebase_admin.initialize_app(credentials.Certificate(creds_dict))
            except Exception as creds_error:
                # Fallback to default credentials (for GCP environments)
                logging_util.warning(
                    f"Failed to load explicit credentials: {creds_error}. "
                    "Attempting default application credentials."
                )
                firebase_admin.initialize_app()

        except Exception as init_error:
            logging_util.error(f"Failed to initialize Firebase: {init_error}")
            raise ValueError(
                "Firebase initialization failed. Ensure proper configuration is available."
            ) from init_error

    try:
        return firestore.client()
    except Exception as client_error:
        logging_util.error(f"Failed to create Firestore client: {client_error}")
        raise ValueError(
            "Firestore client creation failed. Check Firebase configuration and network connectivity."
        ) from client_error


# Backward-compatible alias — some callers may reference the old name
get_firestore_client = get_db


@log_exceptions
def get_campaigns_for_user(
    user_id: UserId,
    limit: int = 50,
    sort_by: str = "last_played",
    start_after: dict[str, Any] | None = None,
    include_total_count: bool = False,
) -> tuple[list[dict[str, Any]], dict[str, Any] | None, int | None]:
    """Retrieves campaigns for a given user with pagination and sorting.

    Args:
        user_id: Firebase user ID
        limit: Maximum number of campaigns to return (default: 50 - display full list)
        sort_by: Sort field ('created_at' or 'last_played'), defaults to 'last_played'
        start_after: Cursor for pagination - dict with 'timestamp' and 'id' keys

    Returns:
        Tuple of (campaign_list, next_cursor) where next_cursor is None if no more results
    """
    db = get_db()
    campaigns_ref = db.collection("users").document(user_id).collection("campaigns")
    # Fetch only fields needed for list display (excludes large fields like 'story')
    # initial_prompt is truncated to 100 chars by frontend for snippet display
    # Include legacy prompt to avoid dropping older campaigns without initial_prompt
    campaigns_query = campaigns_ref.select(
        ["title", "created_at", "last_played", "initial_prompt", "prompt"]
    )

    # Apply sorting (handle empty sort_by values)
    if not sort_by or not sort_by.strip():
        sort_by = "last_played"  # Default sort field
    campaigns_query = campaigns_query.order_by(sort_by, direction="DESCENDING")

    # Apply cursor-based pagination if provided
    # Note: Firestore's start_after requires a document snapshot, but we can simulate
    # cursor-based pagination by fetching the cursor document first, then using start_after
    applied_cursor = False
    if start_after:
        doc_id = start_after.get("id")
        if doc_id:
            try:
                # Get the cursor document to use as start_after reference
                cursor_doc_ref = campaigns_ref.document(doc_id)
                cursor_doc = cursor_doc_ref.get()
                if cursor_doc.exists:
                    campaigns_query = campaigns_query.start_after(cursor_doc)
                    applied_cursor = True
            except Exception as e:
                logging_util.warning(f"Error using cursor for pagination: {e}")

        # Fall back to timestamp-based filtering if cursor doc lookup failed or doc doesn't exist
        if not applied_cursor:
            sort_field_value = start_after.get("timestamp")
            if sort_field_value:
                if isinstance(sort_field_value, str):
                    try:
                        sort_field_value = datetime.datetime.fromisoformat(
                            sort_field_value.replace("Z", "+00:00")
                        )
                    except Exception:
                        logging_util.warning(
                            f"Invalid timestamp in cursor: {sort_field_value}"
                        )
                        sort_field_value = None

                if sort_field_value:
                    # Firestore requires range filters to be on the same field as the first order_by
                    # Since we already have order_by(sort_by, "DESCENDING"), this is valid
                    campaigns_query = campaigns_query.where(
                        sort_by, "<=", sort_field_value
                    )
                    applied_cursor = True

    # Apply limit (request one extra to check if there are more)
    # If limit is None, use default of 50 (display full campaigns list)
    effective_limit = limit if limit is not None else 50
    campaigns_query = campaigns_query.limit(effective_limit + 1)

    campaign_list: list[dict[str, Any]] = []
    next_cursor: dict[str, Any] | None = None

    docs = list(campaigns_query.stream())

    # Check if we have more results
    has_more = len(docs) > effective_limit
    if has_more:
        docs = docs[:effective_limit]  # Take only the requested limit
        # Create cursor from the last document
        last_doc = docs[-1]
        last_data = last_doc.to_dict()
        sort_value = last_data.get(sort_by)

        # Use ISO format for timestamp if it's a datetime object
        if sort_value and hasattr(sort_value, "isoformat"):
            sort_value = sort_value.isoformat()

        # next_cursor must be provided if has_more is True to allow fetching next page
        next_cursor = {
            "timestamp": sort_value,
            "id": last_doc.id,
        }

    # Get total count if requested (only on first page for efficiency)
    total_count = None
    if include_total_count and start_after is None:
        try:
            # Use Firestore count aggregation query (modern API - SDK 2.11+)
            # This only counts documents without reading their contents.
            # Keep compatibility with older tests that patch AGGREGATION_QUERY.
            if AGGREGATION_QUERY is not None:
                count_query = AGGREGATION_QUERY(campaigns_ref).count(alias="total")
            else:
                count_query = campaigns_ref.count(alias="total")
            result = count_query.get()

            # Extract count from aggregation result
            # result can vary by SDK version/mocks:
            # - AggregationResult tuple-like: aggregation_result[0].value
            # - Dict-like mock: aggregation_result.get("total")
            parsed_total = False
            for aggregation_result in result:
                if hasattr(aggregation_result, "get"):
                    maybe_total = aggregation_result.get("total")
                    if maybe_total is not None:
                        total_count = int(maybe_total)
                        parsed_total = True
                        break
                try:
                    total_count = int(aggregation_result[0].value)
                except Exception:  # noqa: S112
                    continue
                parsed_total = True
                break
            if not parsed_total:
                raise ValueError(
                    "Count aggregation returned results, but none were parseable as a total count"
                )
        except Exception as e:
            # Fallback: if count aggregation fails, try streaming (expensive)
            logging_util.warning(
                f"Count aggregation failed, using stream fallback: {e}"
            )
            try:
                # This is expensive but works as fallback
                total_count = len(list(campaigns_ref.stream()))
            except Exception as fallback_error:
                logging_util.warning(
                    f"Failed to get total campaign count: {fallback_error}"
                )
                total_count = None

    # Sanity check: If we have more results than limit, but total_count says we don't,
    # then total_count is clearly wrong (likely count aggregation ignored documents or limit issue).
    # In this case, we should invalidate total_count rather than showing a confusing "50 of 50" state.
    if has_more and total_count is not None and total_count <= effective_limit:
        logging_util.warning(
            f"Total count contradiction detected: has_more=True but total_count={total_count} <= limit={effective_limit}. "
            "Invalidating total_count to prevent UI confusion."
        )
        total_count = None

    for campaign_doc in docs:
        campaign_data = campaign_doc.to_dict()
        campaign_data["id"] = campaign_doc.id

        # Safely get and format timestamps
        created_at = campaign_data.get("created_at")
        if created_at and hasattr(created_at, "isoformat"):
            campaign_data["created_at"] = created_at.isoformat()

        last_played = campaign_data.get("last_played")
        if last_played and hasattr(last_played, "isoformat"):
            campaign_data["last_played"] = last_played.isoformat()

        # Truncate initial_prompt to 100 chars for list view (frontend shows snippet)
        # This reduces payload size significantly when prompts are large
        prompt_value = campaign_data.get("initial_prompt") or campaign_data.get(
            "prompt"
        )
        if isinstance(prompt_value, str) and len(prompt_value) > 100:
            prompt_value = f"{prompt_value[:100]}..."
        if prompt_value is not None:
            campaign_data["initial_prompt"] = prompt_value
        # Remove the full prompt field to reduce payload size for list views
        if "prompt" in campaign_data:
            del campaign_data["prompt"]
        campaign_list.append(campaign_data)

    return (campaign_list, next_cursor, total_count)


@log_exceptions
def campaign_exists(user_id: UserId, campaign_id: CampaignId) -> bool:
    """Fast existence check for a campaign document (no story fetch)."""
    if not user_id or not campaign_id:
        raise ValueError("User ID and Campaign ID are required.")
    db = get_db()
    campaign_ref = (
        db.collection("users")
        .document(user_id)
        .collection("campaigns")
        .document(campaign_id)
    )
    doc = campaign_ref.get()
    return bool(getattr(doc, "exists", False))


@log_exceptions
def get_campaign_by_id(
    user_id: UserId, campaign_id: CampaignId
) -> tuple[dict[str, Any] | None, list[dict[str, Any]] | None]:
    """
    Retrieves a single campaign and its full story using a robust, single query
    and in-memory sort to handle all data types.
    """
    db = get_db()
    campaign_ref = (
        db.collection("users")
        .document(user_id)
        .collection("campaigns")
        .document(campaign_id)
    )

    campaign_doc = campaign_ref.get()
    if not campaign_doc.exists:
        return None, None

    # --- SIMPLIFIED FETCH LOGIC ---
    # 1. Fetch ALL documents, ordered only by the field that always exists: timestamp.
    story_ref = campaign_ref.collection("story").order_by("timestamp")
    story_docs = story_ref.stream()

    # 2. Convert to a list of dictionaries
    all_story_entries: list[dict[str, Any]] = [doc.to_dict() for doc in story_docs]

    # 🚨 DEBUG: Log story retrieval details
    logging_util.info(
        f"📖 FETCHED STORY ENTRIES: user={user_id}, campaign={campaign_id}, "
        f"total_entries={len(all_story_entries)}"
    )

    # Count entries by actor
    user_entries: list[dict[str, Any]] = [
        entry for entry in all_story_entries if entry.get("actor") == "user"
    ]
    ai_entries: list[dict[str, Any]] = [
        entry for entry in all_story_entries if entry.get("actor") == "gemini"
    ]
    other_entries: list[dict[str, Any]] = [
        entry
        for entry in all_story_entries
        if entry.get("actor") not in ["user", "gemini"]
    ]

    logging_util.info(
        f"📊 STORY BREAKDOWN: user_entries={len(user_entries)}, "
        f"ai_entries={len(ai_entries)}, other_entries={len(other_entries)}"
    )

    # Log recent entries for debugging
    if all_story_entries:
        recent_entries: list[dict[str, Any]] = all_story_entries[-5:]  # Last 5 entries
        logging_util.info(f"🔍 RECENT ENTRIES (last {len(recent_entries)}):")
        for i, entry in enumerate(recent_entries, 1):
            actor = entry.get("actor", "unknown")
            mode = entry.get("mode", "N/A")
            text_preview = (
                entry.get("text", "")[:50] + "..."
                if len(entry.get("text", "")) > 50
                else entry.get("text", "")
            )
            timestamp = entry.get("timestamp", "unknown")
            logging_util.info(f"  {i}. [{actor}] {mode} | {text_preview} | {timestamp}")
    else:
        logging_util.warning(f"⚠️ NO STORY ENTRIES FOUND for campaign {campaign_id}")

    # 3. Sort the list in Python, which is more powerful than a Firestore query.
    # We sort by timestamp first, and then by the 'part' number.
    # If 'part' is missing (for old docs), we treat it as 1.
    def _norm_ts(ts: Any) -> datetime.datetime:
        # Handle None/missing timestamps first
        if ts is None:
            return datetime.datetime.fromtimestamp(0, UTC)

        # Handle datetime objects - ensure timezone consistency
        if hasattr(ts, "isoformat"):
            # If datetime is timezone-naive, make it UTC
            if ts.tzinfo is None:
                return ts.replace(tzinfo=UTC)
            return ts

        # Handle string timestamps
        if isinstance(ts, str):
            if not ts.strip():  # Empty string
                return datetime.datetime.fromtimestamp(0, UTC)
            # Best-effort parse; fallback to epoch for invalid strings
            try:
                parsed = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                # Ensure timezone consistency - make UTC if naive
                if parsed.tzinfo is None:
                    return parsed.replace(tzinfo=UTC)
                return parsed
            except Exception:
                # Invalid string - return epoch for stable sorting
                return datetime.datetime.fromtimestamp(0, UTC)

        # Handle integer/float timestamps (epoch seconds)
        if isinstance(ts, (int, float)):
            try:
                return datetime.datetime.fromtimestamp(ts, UTC)
            except (ValueError, OverflowError):
                # Invalid timestamp value - return epoch
                return datetime.datetime.fromtimestamp(0, UTC)

        # Fallback to epoch for any other unknown types (list, dict, etc.)
        return datetime.datetime.fromtimestamp(0, UTC)

    all_story_entries.sort(
        key=lambda x: (_norm_ts(x.get("timestamp")), x.get("part", 1))
    )

    # 4. Add a sequence ID and convert timestamps AFTER sorting.
    # TERMINOLOGY: sequence_id = absolute position (ALL entries)
    #              user_scene_number = user-facing "Scene #X" (AI responses only)
    # See llm_service.py module docstring for full turn/scene terminology.
    user_scene_counter: int = 0
    for i, entry in enumerate(all_story_entries):
        entry["sequence_id"] = i + 1

        # Only increment user scene number for AI responses (case-insensitive)
        actor_value = entry.get("actor")
        normalized_actor = actor_value.lower() if isinstance(actor_value, str) else None
        if normalized_actor == "gemini":
            user_scene_counter += 1
            entry["user_scene_number"] = user_scene_counter
        else:
            entry["user_scene_number"] = None

        # Convert timestamp to ISO format if it's not already a string
        if hasattr(entry["timestamp"], "isoformat"):
            entry["timestamp"] = entry["timestamp"].isoformat()
        # If it's already a string, leave it as is

    return campaign_doc.to_dict(), all_story_entries


@log_exceptions
def get_campaign_metadata(
    user_id: UserId, campaign_id: CampaignId
) -> dict[str, Any] | None:
    """Get campaign metadata without loading story entries (fast, lightweight)."""
    db = get_db()
    campaign_ref = (
        db.collection("users")
        .document(user_id)
        .collection("campaigns")
        .document(campaign_id)
    )
    campaign_doc = campaign_ref.get()
    if not campaign_doc.exists:
        return None
    return campaign_doc.to_dict()


@log_exceptions
def get_story_count(user_id: UserId, campaign_id: CampaignId) -> int:
    """Get total story entry count for a campaign (efficient count query)."""
    db = get_db()
    story_ref = (
        db.collection("users")
        .document(user_id)
        .collection("campaigns")
        .document(campaign_id)
        .collection("story")
    )
    # Use modern Firestore count aggregation API (SDK 2.11+)
    try:
        count_query = story_ref.count(alias="total")
        results = count_query.get()
        for aggregation_result in results:
            return int(aggregation_result[0].value)
        return 0
    except Exception as e:
        # Fallback: aggregation failed at runtime
        logging_util.warning(
            f"Count aggregation failed for story_ref, using stream fallback: {e}"
        )
        return sum(1 for _ in story_ref.stream())


@log_exceptions
def get_story_paginated(
    user_id: UserId,
    campaign_id: CampaignId,
    limit: int = 300,
    before_timestamp: str | None = None,
    before_id: str | None = None,
    newer_count: int = 0,
    newer_gemini_count: int = 0,
) -> dict[str, Any]:
    """
    Fetch story entries with pagination, optimized to avoid loading all entries into memory.

    Entries are stored with a ``timestamp`` field. Pagination is implemented as
    "load older": given an optional ``before_timestamp``/``before_id`` cursor,
    this function returns up to ``limit`` entries whose timestamps are earlier
    than that cursor (or the newest entries if no cursor is provided), ordered
    from oldest to newest within the returned batch.

    Args:
        user_id: User ID
        campaign_id: Campaign ID
        limit: Maximum number of entries to return (default 300)
        before_timestamp: ISO timestamp to fetch entries before (for "load older"
            pagination). Only entries with ``timestamp`` strictly earlier than
            this value are returned.
        before_id: Optional document ID to disambiguate cursors when multiple
            entries share the same timestamp.
        newer_count: Number of newer entries already fetched (for absolute
            sequence_id calculation across pages).
        newer_gemini_count: Number of newer Gemini entries already fetched (for
            absolute user_scene_number calculation across pages).

    Returns:
        dict with:
        - entries: List of story entries (oldest to newest within the fetched batch)
        - total_count: Total number of story entries in the campaign
        - has_older: Boolean indicating if there may be older entries available
            before this batch. This is computed by fetching ``limit + 1`` entries
            and trimming to ``limit``; it is ``True`` when an extra entry exists
            beyond the requested page size.
        - oldest_timestamp: Timestamp of oldest entry in this batch (use as the
            ``before_timestamp`` value for the next pagination call)
        - oldest_id: Document ID of the oldest entry in this batch (use with the
            cursor to avoid dropping entries that share timestamps)
    """
    db = get_db()
    campaign_ref = (
        db.collection("users")
        .document(user_id)
        .collection("campaigns")
        .document(campaign_id)
    )

    # Get total count for pagination metadata
    total_count = get_story_count(user_id, campaign_id)
    total_gemini_count = 0
    try:
        # Count Gemini responses separately for accurate user_scene_number values
        gemini_ref = campaign_ref.collection("story").where("actor", "==", "gemini")

        try:
            # Use modern Firestore count aggregation API (SDK 2.11+)
            count_query = gemini_ref.count(alias="total")
            results = count_query.get()
            for aggregation_result in results:
                total_gemini_count = int(aggregation_result[0].value)
                break
        except Exception as e:
            logging_util.warning(
                f"Gemini count aggregation failed, using stream fallback: {e}"
            )
            total_gemini_count = sum(1 for _ in gemini_ref.stream())
    except Exception:
        # Best-effort: keep zero if counting fails
        total_gemini_count = 0

    # Build query: order by timestamp DESCENDING with document ID tie-breaker
    story_ref = campaign_ref.collection("story").order_by(
        "timestamp", direction=firestore.Query.DESCENDING
    )
    try:
        story_ref = story_ref.order_by(
            firestore.FieldPath.document_id(),
            direction=firestore.Query.DESCENDING,
        )
    except Exception:
        story_ref = story_ref.order_by("__name__", direction=firestore.Query.DESCENDING)

    tie_docs: list[Any] = []

    # If paginating (loading older entries), capture older and same-timestamp entries
    if before_timestamp:
        try:
            cursor_ts = datetime.datetime.fromisoformat(
                before_timestamp.replace("Z", "+00:00")
            )
        except (ValueError, TypeError) as e:
            logging_util.warning(f"Invalid before_timestamp '{before_timestamp}': {e}")
            raise ValueError(f"Invalid before_timestamp: {before_timestamp}") from None

        story_ref = story_ref.where("timestamp", "<", cursor_ts)

        if before_id:
            try:
                tie_query = (
                    campaign_ref.collection("story")
                    .where("timestamp", "==", cursor_ts)
                    .order_by("__name__", direction=firestore.Query.DESCENDING)
                )
                tie_docs = [doc for doc in tie_query.stream() if doc.id < before_id]
            except Exception:
                tie_docs = []

    # Apply limit + 1 to detect if more entries exist
    story_docs = list(story_ref.limit(limit + 1).stream())
    story_docs.extend(tie_docs)

    # Deduplicate by document ID and sort newest -> oldest for slicing
    deduped_docs: list[Any] = []
    seen_ids: set[str] = set()
    for doc in story_docs:
        if doc.id in seen_ids:
            continue
        seen_ids.add(doc.id)
        deduped_docs.append(doc)

    deduped_docs.sort(
        key=lambda d: (
            d.to_dict().get("timestamp"),
            d.id,
        ),
        reverse=True,
    )

    has_older = len(deduped_docs) > limit
    story_docs = deduped_docs[:limit]

    # Convert to list and add IDs
    entries: list[dict[str, Any]] = []
    for doc in story_docs:
        entry = doc.to_dict() or {}
        entry.setdefault("id", doc.id)
        ts = entry.get("timestamp")
        if ts is not None and hasattr(ts, "isoformat"):
            entry["timestamp"] = ts.isoformat()
        entries.append(entry)

    # Ensure chronological order (oldest to newest)
    def _ts_key(entry: dict[str, Any]) -> datetime.datetime:
        ts_val = entry.get("timestamp")
        if isinstance(ts_val, str):
            try:
                return datetime.datetime.fromisoformat(ts_val.replace("Z", "+00:00"))
            except Exception:
                return datetime.datetime.fromtimestamp(0, UTC)
        if hasattr(ts_val, "isoformat"):
            return ts_val
        return datetime.datetime.fromtimestamp(0, UTC)

    entries.sort(key=lambda e: (_ts_key(e), e.get("id") or ""))

    oldest_timestamp = entries[0].get("timestamp") if entries else None
    oldest_id = entries[0].get("id") if entries else None

    # Derive sequence_id and user_scene_number without loading the full story
    start_sequence = (
        total_count - max(newer_count, 0) - len(entries) + 1 if entries else 0
    )
    start_sequence = max(start_sequence, 1) if entries else 0

    batch_gemini_count = sum(
        1
        for entry in entries
        if isinstance(entry.get("actor"), str)
        and entry.get("actor", "").lower() == "gemini"
    )
    gemini_base = max(total_gemini_count - newer_gemini_count - batch_gemini_count, 0)
    gemini_counter = gemini_base

    for idx, entry in enumerate(entries):
        entry["sequence_id"] = start_sequence + idx

        actor_value = entry.get("actor")
        if isinstance(actor_value, str) and actor_value.lower() == "gemini":
            gemini_counter += 1
            entry["user_scene_number"] = gemini_counter
        else:
            entry["user_scene_number"] = None

    logging_util.info(
        f"📖 PAGINATED STORY: user={user_id}, campaign={campaign_id}, "
        f"fetched={len(entries)}, total={total_count}, has_older={has_older}"
    )

    return {
        "entries": entries,
        "total_count": total_count,
        "has_older": has_older,
        "oldest_timestamp": oldest_timestamp,
        "oldest_id": oldest_id,
        "fetched_count": len(entries),
    }


@log_exceptions
def add_story_entry(
    user_id: UserId,
    campaign_id: CampaignId,
    actor: str,
    text: str,
    mode: str | None = None,
    structured_fields: dict[str, Any] | None = None,
) -> None:
    """Add a story entry to Firestore with write-then-read pattern for data integrity.

    This function implements the write-then-read pattern:
    1. Write data to Firestore
    2. Read it back immediately to verify persistence
    3. Only return success if read confirms write succeeded

    This prevents data loss from failed writes that appear successful to users.

    Args:
        user_id: User ID
        campaign_id: Campaign ID
        actor: Actor type ('user' or 'gemini')
        text: Story text content
        mode: Optional mode (e.g., 'god', 'character')
        structured_fields: Required dict for AI responses containing structured response fields
    """
    # Start timing for latency measurement
    start_time: float = time.time()

    # In mock services mode, skip verification since mocks don't support read-back
    # NOTE: Can't rely on fakes alone - even perfect fakes add 0.9s latency per test
    # Unit tests need to be fast, so bypassing verification entirely is correct
    mock_mode: bool = os.getenv("MOCK_SERVICES_MODE") == "true"
    if mock_mode:
        # Use original write-only implementation for testing
        _write_story_entry_to_firestore(
            user_id, campaign_id, actor, text, mode, structured_fields
        )
        logging_util.info(
            f"✅ Write-then-read (mock mode): user={user_id}, campaign={campaign_id}, actor={actor}"
        )

        # Return None to match original add_story_entry behavior for mock tests
        return

    # Write to Firestore and capture document ID for verification
    write_start_time: float = time.time()
    document_id: str = _write_story_entry_to_firestore(
        user_id, campaign_id, actor, text, mode, structured_fields
    )
    write_duration: float = time.time() - write_start_time

    logging_util.info(
        f"✍️ Write completed: {write_duration:.3f}s, document_id: {document_id}"
    )

    # Direct document verification using document ID (much more reliable than text matching)
    verify_start_time: float = time.time()
    entry_found: bool = False

    # Try verification with progressive delays for Firestore eventual consistency
    # NOTE: Keeping synchronous sleep - Flask is sync, async would require major refactor
    for attempt in range(constants.VERIFICATION_MAX_ATTEMPTS):
        delay: float = constants.VERIFICATION_INITIAL_DELAY + (
            attempt * constants.VERIFICATION_DELAY_INCREMENT
        )
        time.sleep(delay)

        logging_util.debug(
            f"🔍 VERIFICATION: Attempt {attempt + 1}/{constants.VERIFICATION_MAX_ATTEMPTS} after {delay}s delay"
        )
        entry_found = verify_document_by_id(user_id, campaign_id, document_id, actor)

        if entry_found:
            logging_util.info(
                f"✅ VERIFICATION: Found document {document_id} on attempt {attempt + 1}"
            )
            break

        if attempt < constants.VERIFICATION_MAX_ATTEMPTS - 1:
            logging_util.debug(
                f"⚠️ VERIFICATION: Attempt {attempt + 1} failed, retrying..."
            )

    verify_duration: float = time.time() - verify_start_time

    if not entry_found:
        logging_util.error(
            f"❌ VERIFICATION: All {constants.VERIFICATION_MAX_ATTEMPTS} attempts failed after {verify_duration:.3f}s"
        )
        raise Exception(
            f"Write-then-read verification failed: Could not find document '{document_id}' "
            f"for actor='{actor}' after {constants.VERIFICATION_MAX_ATTEMPTS} attempts"
        )

    # Calculate total latency
    total_duration: float = time.time() - start_time

    logging_util.info(
        f"📖 Verify-latest timing: {verify_duration:.3f}s (checked latest 10 entries)"
    )
    logging_util.info(
        f"⏱️ Write-then-read TOTAL latency: {total_duration:.3f}s "
        f"(write: {write_duration:.3f}s, verify: {verify_duration:.3f}s, sleep: 0.100s)"
    )
    logging_util.info(
        f"✅ Write-then-read verification successful: "
        f"user={user_id}, campaign={campaign_id}, actor={actor}"
    )

    # Return None to match original add_story_entry API
    return


def _write_story_entry_to_firestore(
    user_id: UserId,
    campaign_id: CampaignId,
    actor: str,
    text: str,
    mode: str | None = None,
    structured_fields: dict[str, Any] | None = None,
) -> str:  # noqa: PLR0915
    """Internal implementation to write story entry data directly to Firestore

    Writes story entries using the standard collection.add() method without transactions.
    Text is automatically chunked if it exceeds Firestore's size limits.

    Returns:
        str: Document ID of the first chunk (used for verification)
    """
    db = get_db()
    story_ref = (
        db.collection("users")
        .document(user_id)
        .collection("campaigns")
        .document(campaign_id)
    )
    text_bytes: bytes = text.encode("utf-8")
    chunks: list[bytes] = [
        text_bytes[i : i + MAX_TEXT_BYTES]
        for i in range(0, len(text_bytes), MAX_TEXT_BYTES)
    ]

    if not chunks:
        # Handle empty text for both user and AI actors
        if actor == constants.ACTOR_GEMINI:
            god_mode_empty_narrative = bool(
                structured_fields and structured_fields.get("god_mode_response")
            )
            if god_mode_empty_narrative:
                logging_util.info(
                    f"🛡️ GOD_MODE_EMPTY_NARRATIVE: Accepting empty narrative for campaign {campaign_id} "
                    "because god_mode_response is present."
                )
                chunks = [b""]
            else:
                # AI returned empty narrative - this is an LLM compliance error
                # Do not mask with placeholder text - surface the error
                logging_util.error(
                    f"🚨 EMPTY_NARRATIVE_ERROR: LLM returned empty narrative for campaign {campaign_id}. "
                    f"This indicates a system prompt compliance issue. structured_fields present: {bool(structured_fields)}"
                )
                raise FirestoreWriteError(
                    f"LLM returned empty narrative for campaign {campaign_id}. "
                    "The AI must always provide narrative content. Check system prompts for narrative requirements."
                )
        else:
            # Create a placeholder for empty user inputs (this is valid - user submitted empty)
            placeholder_text = "[Empty input]"
            chunks = [placeholder_text.encode("utf-8")]
    base_entry_data: dict[str, Any] = {"actor": actor}
    if mode:
        base_entry_data["mode"] = mode

    # For AI responses, structured_fields should always be provided
    # Save ALL fields from structured_fields to Firestore
    if structured_fields:
        # Simply merge all structured fields into base_entry_data
        # This ensures we capture any field that Gemini provides
        for field_name, field_value in structured_fields.items():
            # Skip None values to avoid storing null fields
            if field_value is not None:
                base_entry_data[field_name] = field_value
    elif actor == constants.ACTOR_GEMINI:
        # Log warning if AI response missing structured fields
        logging_util.warning(
            f"AI response missing structured_fields for campaign {campaign_id}"
        )

    # Simple and reliable write with document ID capture
    timestamp: datetime.datetime = datetime.datetime.now(UTC)
    document_id: str | None = None

    for i, chunk in enumerate(chunks):
        entry_data: dict[str, Any] = base_entry_data.copy()
        entry_data["text"] = chunk.decode("utf-8")
        entry_data["timestamp"] = timestamp
        entry_data["part"] = i + 1
        entry_data = _normalize_story_entry_contract_fields(entry_data)
        _log_story_entry_contract_warnings(
            entry_data,
            campaign_id=campaign_id,
            actor=actor,
            stage="pre_write",
        )

        try:
            # Create the story entry and capture document ID
            add_result = story_ref.collection("story").add(entry_data)
            # Handle both real Firestore (tuple) and mock (direct reference)
            doc_ref = None
            if isinstance(add_result, tuple):
                for candidate in add_result:
                    if hasattr(candidate, "id"):
                        doc_ref = candidate
                        break
                if doc_ref is None and len(add_result) >= 2:
                    doc_ref = add_result[1]
                elif doc_ref is None and len(add_result) >= 1:
                    doc_ref = add_result[0]
            else:
                doc_ref = add_result

            if i == 0:  # Store the first chunk's document ID for verification
                if doc_ref is not None and hasattr(doc_ref, "id"):
                    document_id = doc_ref.id
                    logging_util.debug(
                        f"✍️ WRITE: Created document {document_id} with actor='{actor}'"
                    )
                else:
                    # CRITICAL: This should never happen in production!
                    mock_mode = os.getenv("MOCK_SERVICES_MODE") == "true"
                    logging_util.error(
                        f"🚨 CRITICAL: doc_ref missing .id attribute! "
                        f"mock_mode={mock_mode}, doc_ref={doc_ref}, "
                        f"add_result={add_result}, type={type(add_result)}"
                    )
                    raise FirestoreWriteError(
                        "Firestore add() failed to return a document reference with an id. "
                        f"add_result={add_result}, type={type(add_result)}"
                    )
        except Exception:
            raise  # Re-raise the exception to maintain original behavior

    try:
        story_ref.update({"last_played": timestamp})
    except Exception:
        raise

    # Return document ID for verification - must be set by this point
    # FirestoreWriteError is raised above if doc_ref doesn't have an id
    if document_id is None:
        raise FirestoreWriteError(
            "Document ID was not captured during write. "
            "This indicates an unexpected error in the Firestore write operation."
        )
    return document_id


def verify_document_by_id(
    user_id: UserId, campaign_id: CampaignId, document_id: str, expected_actor: str
) -> bool:
    """Verify a story entry was written by directly reading the document by ID

    Args:
        user_id: User ID
        campaign_id: Campaign ID
        document_id: Document ID to verify
        expected_actor: Expected actor type for validation

    Returns:
        bool: True if document exists and has correct actor
    """
    if not document_id:
        logging_util.error("🔍 VERIFICATION: No document_id provided")
        return False

    try:
        db = get_db()
        campaign_ref = (
            db.collection("users")
            .document(user_id)
            .collection("campaigns")
            .document(campaign_id)
        )
        doc_ref = campaign_ref.collection("story").document(document_id)

        # Direct document read by ID
        doc = doc_ref.get()

        if not doc.exists:
            logging_util.warning(
                f"🔍 VERIFICATION: Document {document_id} does not exist"
            )
            return False

        entry = doc.to_dict()
        if isinstance(entry, dict):
            _log_story_entry_contract_warnings(
                entry,
                campaign_id=campaign_id,
                actor=expected_actor,
                stage="read_back",
            )
        actual_actor = entry.get("actor", constants.ACTOR_UNKNOWN)

        if actual_actor == expected_actor:
            return True
        logging_util.warning(
            f"🔄 VERIFICATION: Actor mismatch - expected '{expected_actor}', got '{actual_actor}'"
        )
        return False

    except Exception as e:
        logging_util.error(
            f"❌ VERIFICATION: Error reading document {document_id}: {str(e)}"
        )
        return False


def verify_latest_entry(
    user_id: UserId, campaign_id: CampaignId, actor: str, text: str, limit: int = 10
) -> bool:
    """Efficiently verify a story entry was written by reading only the latest entries

    Args:
        user_id: User ID
        campaign_id: Campaign ID
        actor: Expected actor type
        text: Expected text content
        limit: Number of latest entries to check (default 10)

    Returns:
        bool: True if matching entry found in latest entries
    """
    db = get_db()
    campaign_ref = (
        db.collection("users")
        .document(user_id)
        .collection("campaigns")
        .document(campaign_id)
    )

    # Read only the latest N entries, ordered by timestamp descending
    story_ref = (
        campaign_ref.collection("story")
        .order_by("timestamp", direction="DESCENDING")
        .limit(limit)
    )
    story_docs = story_ref.stream()

    # Check if our entry is among the latest entries
    for _i, doc in enumerate(story_docs):
        entry = doc.to_dict()
        entry_actor = entry.get("actor", constants.ACTOR_UNKNOWN)
        entry_text = entry.get("text", "NO_TEXT")

        # Check for exact match
        if entry_actor == actor and entry_text == text:
            return True

    return False


@log_exceptions
def create_campaign(
    user_id: UserId,
    title: str,
    initial_prompt: str,
    opening_story: str,
    initial_game_state: dict[str, Any],
    selected_prompts: list[str] | None = None,
    use_default_world: bool = False,
    opening_story_structured_fields: dict[str, Any] | None = None,
) -> CampaignId:
    db = get_db()
    campaigns_collection = (
        db.collection("users").document(user_id).collection("campaigns")
    )

    initial_state = copy.deepcopy(initial_game_state)
    if not isinstance(initial_state, dict):
        initial_state = {}

    if not isinstance(initial_state.get("player_turn"), int):
        initial_state["player_turn"] = 0
    if not isinstance(initial_state.get("last_living_world_turn"), int):
        initial_state["last_living_world_turn"] = 0
    if "last_living_world_time" not in initial_state or (
        initial_state.get("last_living_world_time") is not None
        and not isinstance(initial_state.get("last_living_world_time"), dict)
    ):
        initial_state["last_living_world_time"] = None
    initial_state, _ = migrate_legacy_state_for_schema(initial_state)

    # Create the main campaign document
    campaign_ref: firestore.DocumentReference = campaigns_collection.document()
    campaign_data: dict[str, Any] = {
        "title": title,
        "initial_prompt": initial_prompt,
        "created_at": datetime.datetime.now(UTC),
        "last_played": datetime.datetime.now(UTC),
        "selected_prompts": selected_prompts or [],
        "use_default_world": use_default_world,
        "living_world_state": {
            "last_turn": initial_state.get("last_living_world_turn", 0),
            "last_time": initial_state.get("last_living_world_time"),
        },
    }
    campaign_ref.set(campaign_data)

    # Create the initial game state document
    game_state_ref: firestore.DocumentReference = campaign_ref.collection(
        "game_states"
    ).document("current_state")
    game_state_ref.set(initial_state)

    # Assuming 'god' mode for the very first conceptual prompt.
    # You might want to make this mode configurable or infer it.
    add_story_entry(user_id, campaign_ref.id, "user", initial_prompt, mode="god")

    add_story_entry(
        user_id,
        campaign_ref.id,
        "gemini",
        opening_story,
        structured_fields=opening_story_structured_fields,
    )

    return campaign_ref.id


@log_exceptions
def get_campaign_game_state(
    user_id: UserId, campaign_id: CampaignId
) -> GameState | None:
    """Fetches the current game state for a given campaign."""
    db = get_db()
    game_state_ref = (
        db.collection("users")
        .document(user_id)
        .collection("campaigns")
        .document(campaign_id)
        .collection("game_states")
        .document("current_state")
    )

    game_state_doc = game_state_ref.get()
    if not game_state_doc.exists:
        return None
    game_state = GameState.from_dict(game_state_doc.to_dict())
    if game_state is None:
        logging_util.warning(
            "GET_CAMPAIGN_GAME_STATE: GameState.from_dict returned None, returning empty GameState"
        )
        return GameState(user_id=user_id)
    return game_state


@log_exceptions
def update_campaign_game_state(
    user_id: UserId, campaign_id: CampaignId, game_state_update: dict[str, Any]
) -> None:
    """Updates the game state for a campaign, overwriting with the provided dict."""
    if not user_id or not campaign_id:
        raise ValueError("User ID and Campaign ID are required.")

    db = get_db()
    game_state_ref = (
        db.collection("users")
        .document(user_id)
        .collection("campaigns")
        .document(campaign_id)
        .collection("game_states")
        .document("current_state")
    )

    try:
        # NOTE: This function now expects a COMPLETE game state dictionary.
        # The merge logic has been moved to the handle_interaction function in main.py
        # to ensure consistency across all update types (AI, GOD_MODE, etc.)

        # Normalize dotted keys (e.g., "player_character_data.level" -> nested in player_character_data)
        # This handles LLM output that uses both nested objects AND dotted paths
        game_state_update = _normalize_dotted_keys_in_place(game_state_update)

        # Add the last updated timestamp before setting.
        game_state_update["last_state_update_timestamp"] = firestore.SERVER_TIMESTAMP

        game_state_ref.set(game_state_update)
        logging_util.info(
            "Successfully set new game state for campaign %s.",
            campaign_id,
        )
        # Keep full-state dumps at DEBUG to avoid serialization cost in default INFO mode.
        if logging_util.getLogger().isEnabledFor(logging_util.DEBUG):
            logging_util.debug(
                "Final state written to Firestore for campaign %s:\n%s",
                campaign_id,
                _truncate_log_json(game_state_update),
            )

    except Exception as e:
        logging_util.error(
            f"Failed to update game state for campaign {campaign_id}: {e}",
            exc_info=True,
        )
        raise


# --- NEWLY ADDED FUNCTION ---
@log_exceptions
def update_campaign_title(
    user_id: UserId, campaign_id: CampaignId, new_title: str
) -> bool:
    """Updates the title of a specific campaign."""
    db = get_db()
    campaign_ref = (
        db.collection("users")
        .document(user_id)
        .collection("campaigns")
        .document(campaign_id)
    )
    campaign_doc = campaign_ref.get()
    if not campaign_doc.exists:
        logging_util.warning(
            "update_campaign_title: campaign document not found "
            f"(user_id={user_id}, campaign_id={campaign_id})"
        )
        return False
    campaign_ref.set({"title": new_title}, merge=True)
    return True


@log_exceptions
def update_campaign(
    user_id: UserId, campaign_id: CampaignId, updates: dict[str, Any]
) -> bool:
    """Updates a campaign with arbitrary updates.

    Supports dot-notation paths for nested field updates.
    Example: {"game_state.arc_milestones.quest1": {"status": "completed"}}
    will correctly update the nested structure.
    Dot characters are reserved for nested paths; literal dots in field names are
    not supported by this helper.

    Args:
        user_id: User ID
        campaign_id: Campaign ID
        updates: Dictionary of updates, supports dot-notation keys for nested paths

    Returns:
        bool: True if update succeeded
    """
    db = get_db()
    campaign_ref = (
        db.collection("users")
        .document(user_id)
        .collection("campaigns")
        .document(campaign_id)
    )
    campaign_doc = campaign_ref.get()
    if not campaign_doc.exists:
        logging_util.error(
            "update_campaign: campaign document not found "
            f"(user_id={user_id}, campaign_id={campaign_id})"
        )
        raise ValueError(
            f"Campaign {campaign_id} not found for user {user_id}; "
            "cannot apply updates."
        )

    # Check if any keys use dot-notation
    has_dot_notation = any("." in key for key in updates)

    if has_dot_notation:
        # Expand dot-notation to nested dicts and use set(merge=True).
        # We intentionally avoid Firestore's update() with dot-paths here because:
        #   - update() operates on exact field paths and can overwrite or recreate
        #     intermediate maps if the existing document shape does not match what
        #     the path assumes (e.g., when a parent field is missing or is not a map).
        #   - Small changes to the stored structure (or legacy/migrated documents)
        #     can cause update() with a dot-path to behave differently across
        #     campaigns, sometimes creating flat fields instead of the nested
        #     structure our code expects.
        # By first expanding dot-notation into a nested dict and then calling
        # set(..., merge=True), we ask Firestore to merge at the map level:
        #   - Only the specified nested fields are updated.
        #   - Unspecified sibling fields under the same parent map are preserved.
        #   - The behavior is consistent even when some intermediate maps are
        #     missing (Firestore will create them as needed during the merge).
        # This makes nested updates more predictable and resilient than relying
        # directly on update() with dot-paths against documents that may evolve
        # over time.
        expanded_updates = _expand_dot_notation(updates)
        logging_util.info(
            f"update_campaign: Expanded dot-notation updates for campaign {campaign_id}"
        )
        campaign_ref.set(expanded_updates, merge=True)
    else:
        # No dot-notation, use standard update
        logging_util.info(
            f"update_campaign: Using standard update for campaign {campaign_id}"
        )
        campaign_ref.update(updates)

    return True


# --- USER SETTINGS FUNCTIONS ---
@log_exceptions
def get_user_settings(user_id: UserId) -> dict[str, Any] | None:
    """Get user settings from Firestore.

    Args:
        user_id: User ID to get settings for

    Returns:
        Dict containing user settings, empty dict if user exists but no settings,
        or None if user doesn't exist or database error
    """
    try:
        db = get_db()
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            data = user_doc.to_dict()
            return data.get("settings", {})  # Empty dict for user with no settings
        # Return None for users that don't exist yet
        return None
    except Exception as e:
        # Hash user_id for security in logs
        user_hash = str(hash(user_id))[-6:] if user_id else "unknown"
        logging_util.error(
            f"Failed to get user settings for user_{user_hash}: {str(e)}"
        )
        # Return None to distinguish database errors from no settings
        return None


@log_exceptions
def update_user_settings(user_id: UserId, settings: dict[str, Any]) -> bool:
    """Update user settings in Firestore.

    Uses nested field updates to prevent clobbering sibling settings fields.

    Args:
        user_id: User ID to update settings for
        settings: Dictionary of settings to update

    Returns:
        bool: True if update succeeded, False otherwise
    """
    try:
        db = get_db()
        user_ref = db.collection("users").document(user_id)

        # Check if user document exists first
        user_doc = user_ref.get()

        # Use Firestore SERVER_TIMESTAMP - SDK import is guaranteed at module level
        timestamp = firestore.SERVER_TIMESTAMP

        if user_doc.exists:
            # Use nested field update to avoid clobbering sibling settings
            update_data = {}
            for key, value in settings.items():
                update_data[f"settings.{key}"] = value
            update_data["lastUpdated"] = timestamp

            user_ref.update(update_data)
        else:
            # Create new document with settings
            user_data = {
                "settings": settings,
                "lastUpdated": timestamp,
                "createdAt": timestamp,
            }
            user_ref.set(user_data)

        logging_util.info(
            "Updated settings for user %s: %s",
            user_id,
            _redact_settings_for_log(settings),
        )
        return True
    except Exception as e:
        logging_util.error(
            f"Failed to update user settings for {user_id}: {str(e)}", exc_info=True
        )
        return False


# --- PERSONAL API KEY FUNCTIONS ---


@log_exceptions
def lookup_personal_api_key(
    key_hash: str,
) -> "tuple[UserId | None, str | None]":
    """Resolve a hashed personal API key to its owner's user ID and email.

    Args:
        key_hash: sha256 hex digest of the raw key

    Returns:
        Tuple of (user_id, email). email may be None if not stored in Firestore.
    """
    try:
        db = get_db()
        doc = db.collection("api_keys").document(key_hash).get()
        if not doc.exists:
            return None, None
        raw_uid = doc.to_dict().get("uid")
        if not isinstance(raw_uid, str):
            return None, None
        # Look up the user's email from their Firestore profile
        email: str | None = None
        try:
            user_doc = db.collection("users").document(raw_uid).get()
            if user_doc.exists:
                raw_email = user_doc.to_dict().get("email")
                # Coerce to string or None — downstream uses .lower() which crashes on non-strings
                if isinstance(raw_email, str):
                    email = raw_email
                elif raw_email is not None:
                    email = str(raw_email)
        except Exception as email_err:
            logging_util.debug(
                "Could not look up email for uid %s (best-effort): %s",
                raw_uid,
                email_err,
            )
        return raw_uid, email
    except Exception as e:
        logging_util.error(f"Failed to lookup personal API key: {e}", exc_info=True)
        return None, None


@log_exceptions
def rotate_personal_api_key(
    user_id: UserId,
    new_key_hash: str,
) -> bool:
    """Atomically rotate a personal API key using a Firestore transaction.

    Reads the current settings.personal_api_key_hash inside the transaction,
    deletes the old api_keys doc (if any), creates the new api_keys doc, and
    updates the user settings pointer — all atomically and concurrency-safe.

    Two concurrent generate requests can no longer leave orphan active key docs
    because each transaction reads the live old hash and overwrites it;
    the Firestore optimistic-concurrency retry ensures only one writer wins
    each round.

    Uses set(..., merge=True) for the user doc so first-time users without
    a pre-existing profile doc are handled safely (no update-on-missing error).

    Args:
        user_id: Owner of the key
        new_key_hash: sha256 of the newly generated key

    Returns:
        True if the transaction committed successfully, False otherwise
    """
    try:
        db = get_db()
        user_ref = db.collection("users").document(user_id)
        new_key_ref = db.collection("api_keys").document(new_key_hash)

        @firestore.transactional
        def _run(transaction):
            user_snap = user_ref.get(transaction=transaction)
            old_hash = None
            if user_snap.exists:
                settings = (user_snap.to_dict() or {}).get("settings") or {}
                old_hash = settings.get("personal_api_key_hash")

            if old_hash:
                old_key_ref = db.collection("api_keys").document(old_hash)
                transaction.delete(old_key_ref)

            transaction.set(
                new_key_ref, {"uid": user_id, "created_at": firestore.SERVER_TIMESTAMP}
            )

            if user_snap.exists:
                # Use dot-notation update to preserve all other settings fields.
                transaction.update(
                    user_ref,
                    {
                        "settings.personal_api_key_hash": new_key_hash,
                        "lastUpdated": firestore.SERVER_TIMESTAMP,
                    },
                )
            else:
                # New user doc: set+merge is safe here since there are no existing settings.
                transaction.set(
                    user_ref,
                    {
                        "settings": {"personal_api_key_hash": new_key_hash},
                        "lastUpdated": firestore.SERVER_TIMESTAMP,
                    },
                    merge=True,
                )

        _run(db.transaction())
        logging_util.info("Rotated personal API key for user %s", user_id)
        return True
    except Exception as e:
        logging_util.error(
            f"Failed to rotate personal API key for {user_id}: {e}", exc_info=True
        )
        return False


@log_exceptions
def revoke_personal_api_key(user_id: UserId) -> bool:
    """Atomically revoke the personal API key for a user using a Firestore transaction.

    Reads settings.personal_api_key_hash inside the transaction, deletes the
    api_keys doc, and clears the pointer — all in one atomic operation.
    Mirrors rotate_personal_api_key's concurrency-safe pattern.

    Args:
        user_id: Owner of the key

    Returns:
        True if committed (including no-op when no key exists), False on error
    """
    try:
        db = get_db()
        user_ref = db.collection("users").document(user_id)

        @firestore.transactional
        def _run(transaction):
            user_snap = user_ref.get(transaction=transaction)
            if not user_snap.exists:
                return
            settings = (user_snap.to_dict() or {}).get("settings") or {}
            existing_hash = settings.get("personal_api_key_hash")
            if existing_hash:
                key_ref = db.collection("api_keys").document(existing_hash)
                transaction.delete(key_ref)
            # Use dot-notation update to preserve all other settings fields.
            transaction.update(
                user_ref,
                {
                    "settings.personal_api_key_hash": firestore.DELETE_FIELD,
                    "lastUpdated": firestore.SERVER_TIMESTAMP,
                },
            )

        _run(db.transaction())
        logging_util.info("Revoked personal API key for user %s", user_id)
        return True
    except Exception as e:
        logging_util.error(
            f"Failed to revoke personal API key for {user_id}: {e}", exc_info=True
        )
        return False
