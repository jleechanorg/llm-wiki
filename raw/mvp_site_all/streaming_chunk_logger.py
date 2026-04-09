"""Server-side LLM chunk timing logger for streaming evidence validation.

This module captures per-chunk timing data on the server side to enable
precise measurement of LLM chunk generation timing vs HTTP SSE delivery timing.

Required for BD-iwr streaming evidence standard compliance.
"""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from json import dumps as stdlib_json_dumps
from json import loads as stdlib_json_loads
from pathlib import Path
from typing import Any

from mvp_site import logging_util

STREAMING_BUNDLE_VERSION = "1.0.0"
STREAMING_SESSION_START_EPOCH = time.time()


@dataclass
class ChunkTimingRecord:
    """Record of a single LLM chunk with timing information."""

    sequence: int
    llm_ts_utc: str  # ISO 8601 format
    text_length: int
    campaign_id: str | None
    request_id: str | None


class StreamingChunkLogger:
    """Logger for capturing LLM chunk timing data during streaming responses.

    Usage:
        logger = StreamingChunkLogger(campaign_id="abc123", request_id="req456")
        logger.log_chunk(sequence=0, text="Hello", timestamp=datetime.now(timezone.utc))
        logger.save()
    """

    def __init__(
        self,
        campaign_id: str | None = None,
        request_id: str | None = None,
        branch_name: str | None = None,
    ):
        """Initialize chunk logger.

        Args:
            campaign_id: Campaign identifier for correlation
            request_id: Request identifier for correlation
            branch_name: Git branch name for evidence path
        """
        self.campaign_id = campaign_id
        self.request_id = request_id or "unknown"
        self.records: list[ChunkTimingRecord] = []

        # Determine evidence directory
        if branch_name is None:
            try:
                import subprocess

                result = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=2,
                )
                branch_name = result.stdout.strip()
            except Exception:
                branch_name = "unknown-branch"
        self.branch_name = branch_name

        self.evidence_dir = Path(
            f"/tmp/worldarchitect.ai/{branch_name}/streaming_validation"
        )
        self.evidence_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _write_checksum_for_file(filepath: Path) -> None:
        content = filepath.read_bytes()
        digest = hashlib.sha256(content).hexdigest()
        checksum_file = Path(str(filepath) + ".sha256")
        checksum_file.write_text(f"{digest}  {filepath.name}\n", encoding="utf-8")

    @staticmethod
    def _capture_git_context() -> dict[str, Any]:
        git_context: dict[str, Any] = {}
        try:
            git_context["git_head"] = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                text=True,
                timeout=5,
            ).strip()
            git_context["git_branch"] = subprocess.check_output(
                ["git", "branch", "--show-current"],
                text=True,
                timeout=5,
            ).strip()
            status = subprocess.check_output(
                ["git", "status", "--porcelain=v1"],
                text=True,
                timeout=5,
            ).strip()
            git_context["working_tree_dirty"] = bool(status)
        except Exception as exc:  # noqa: BLE001
            git_context["git_error"] = str(exc)
        return git_context

    def _write_capture_summary(self, output_path: Path) -> Path:
        chunk_count = len(self.records)
        first_ts = self.records[0].llm_ts_utc if self.records else None
        last_ts = self.records[-1].llm_ts_utc if self.records else None
        capture_status = "pass" if chunk_count > 0 else "fail"
        errors = [] if chunk_count > 0 else ["No chunks captured for streaming request."]

        capture_data = {
            "version": STREAMING_BUNDLE_VERSION,
            "captured_at": datetime.now(UTC).isoformat(),
            "request_id": self.request_id,
            "campaign_id": self.campaign_id,
            "branch_name": self.branch_name,
            "chunk_count": chunk_count,
            "first_chunk_ts": first_ts,
            "last_chunk_ts": last_ts,
            "status": capture_status,
            "errors": errors,
            "artifacts": {
                "chunk_log_csv": output_path.name,
            },
        }

        capture_path = self.evidence_dir / f"stream_capture_{self.request_id}.json"
        capture_path.write_text(
            stdlib_json_dumps(capture_data, indent=2), encoding="utf-8"
        )
        self._write_checksum_for_file(capture_path)
        return capture_path

    def _refresh_canonical_bundle(self) -> None:
        capture_files = sorted(
            capture_file
            for capture_file in self.evidence_dir.glob("stream_capture_*.json")
            if capture_file.stat().st_mtime >= (STREAMING_SESSION_START_EPOCH - 1.0)
        )
        scenarios: list[dict[str, Any]] = []
        passed = 0
        failed = 0
        total_chunks = 0
        empty_count = 0

        for capture_file in capture_files:
            try:
                capture = stdlib_json_loads(capture_file.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001
                scenarios.append(
                    {
                        "name": capture_file.stem,
                        "request_id": capture_file.stem.replace("stream_capture_", ""),
                        "campaign_id": None,
                        "passed": False,
                        "errors": [f"Invalid capture JSON: {exc}"],
                    }
                )
                failed += 1
                continue
            if not isinstance(capture, dict):
                scenarios.append(
                    {
                        "name": capture_file.stem,
                        "request_id": None,
                        "campaign_id": None,
                        "passed": False,
                        "errors": ["Malformed capture metadata: expected JSON object."],
                    }
                )
                failed += 1
                continue
            if "chunk_count" not in capture:
                scenarios.append(
                    {
                        "name": capture_file.stem,
                        "request_id": capture.get("request_id"),
                        "campaign_id": capture.get("campaign_id"),
                        "passed": False,
                        "errors": ["Malformed capture metadata: missing chunk_count."],
                    }
                )
                failed += 1
                continue

            chunk_count = int(capture.get("chunk_count") or 0)
            capture_passed = bool(capture.get("status") == "pass" and chunk_count > 0)
            if capture_passed:
                passed += 1
            else:
                failed += 1
            if chunk_count == 0:
                empty_count += 1
            total_chunks += chunk_count
            scenarios.append(
                {
                    "name": f"streaming_request_{capture.get('request_id', 'unknown')}",
                    "request_id": capture.get("request_id"),
                    "campaign_id": capture.get("campaign_id"),
                    "passed": capture_passed,
                    "errors": (
                        capture.get("errors", [])
                        if isinstance(capture.get("errors"), list)
                        and capture.get("errors")
                        else (
                            []
                            if capture_passed
                            else ["No chunks captured for streaming request."]
                        )
                    ),
                    "checks": {
                        "chunk_count": chunk_count,
                        "first_chunk_ts": capture.get("first_chunk_ts"),
                        "last_chunk_ts": capture.get("last_chunk_ts"),
                    },
                    "evidence_files": [capture_file.name],
                }
            )

        run_payload = {
            "version": STREAMING_BUNDLE_VERSION,
            "generated_at": datetime.now(UTC).isoformat(),
            "scenarios": scenarios,
            "summary": {
                "total": len(scenarios),
                "passed": passed,
                "failed": failed,
                "empty_chunk_logs": empty_count,
                "total_chunk_events_observed": total_chunks,
                "pass_rate": f"{passed}/{len(scenarios)}"
                if scenarios
                else "0/0",
            },
        }
        run_path = self.evidence_dir / "run.json"
        run_path.write_text(stdlib_json_dumps(run_payload, indent=2), encoding="utf-8")
        self._write_checksum_for_file(run_path)

        metadata_payload = {
            "version": STREAMING_BUNDLE_VERSION,
            "generated_at": datetime.now(UTC).isoformat(),
            "streaming_validation": {
                "capture_files": len(capture_files),
                "empty_chunk_logs": empty_count,
            },
            "git_provenance": self._capture_git_context(),
        }
        metadata_path = self.evidence_dir / "metadata.json"
        metadata_path.write_text(
            stdlib_json_dumps(metadata_payload, indent=2), encoding="utf-8"
        )
        self._write_checksum_for_file(metadata_path)

        evidence_text = (
            "# Streaming Validation Evidence\n\n"
            f"- Generated at: {datetime.now(UTC).isoformat()}\n"
            f"- Total streaming captures: {len(scenarios)}\n"
            f"- Passed captures: {passed}\n"
            f"- Failed captures: {failed}\n"
            f"- Empty chunk logs: {empty_count}\n\n"
            "## Gate\n\n"
            "- Empty chunk logs are treated as failures unless explicitly expected.\n"
        )
        evidence_path = self.evidence_dir / "evidence.md"
        evidence_path.write_text(evidence_text, encoding="utf-8")
        self._write_checksum_for_file(evidence_path)

    def log_chunk(
        self,
        sequence: int,
        text: str,
        timestamp: datetime | None = None,
    ) -> None:
        """Log a single LLM chunk with timing information.

        Args:
            sequence: Chunk sequence number (0-indexed)
            text: Chunk text content
            timestamp: UTC timestamp (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.now(UTC)

        record = ChunkTimingRecord(
            sequence=sequence,
            llm_ts_utc=timestamp.isoformat(),
            text_length=len(text),
            campaign_id=self.campaign_id,
            request_id=self.request_id,
        )
        self.records.append(record)

        # Log first chunk explicitly for debugging
        if sequence == 0:
            logging_util.info(
                f"🔍 STREAMING_EVIDENCE | First LLM chunk | "
                f"campaign_id={self.campaign_id} request_id={self.request_id} "
                f"timestamp={timestamp.isoformat()} sequence=0"
            )

    def save(self) -> Path:
        """Save chunk timing records to CSV file.

        Returns:
            Path to saved CSV file

        File format:
            sequence,llm_ts_utc,text_length,campaign_id,request_id
            0,2026-02-11T23:53:42.123456+00:00,45,abc123,req456
            1,2026-02-11T23:53:42.234567+00:00,38,abc123,req456
            ...
        """
        output_path = self.evidence_dir / f"llm_chunk_log_{self.request_id}.csv"

        with output_path.open("w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                ["sequence", "llm_ts_utc", "text_length", "campaign_id", "request_id"]
            )

            for record in self.records:
                writer.writerow(
                    [
                        record.sequence,
                        record.llm_ts_utc,
                        record.text_length,
                        record.campaign_id,
                        record.request_id,
                    ]
                )

        logging_util.info(
            f"📁 STREAMING_EVIDENCE | Saved LLM chunk log | "
            f"path={output_path} chunks={len(self.records)} "
            f"campaign_id={self.campaign_id} request_id={self.request_id}"
        )
        self._write_capture_summary(output_path)
        self._refresh_canonical_bundle()

        return output_path

    def get_first_chunk_timestamp(self) -> datetime | None:
        """Get timestamp of first chunk (sequence 0).

        Returns:
            First chunk timestamp or None if no chunks logged
        """
        if not self.records:
            return None

        first_record = min(self.records, key=lambda r: r.sequence)
        return datetime.fromisoformat(first_record.llm_ts_utc)


# Global registry for chunk loggers (per request_id)
_CHUNK_LOGGERS: dict[str, StreamingChunkLogger] = {}


def get_or_create_chunk_logger(
    request_id: str,
    campaign_id: str | None = None,
) -> StreamingChunkLogger:
    """Get or create a chunk logger for a request.

    Args:
        request_id: Request identifier
        campaign_id: Campaign identifier

    Returns:
        StreamingChunkLogger instance
    """
    if request_id not in _CHUNK_LOGGERS:
        _CHUNK_LOGGERS[request_id] = StreamingChunkLogger(
            campaign_id=campaign_id,
            request_id=request_id,
        )
    return _CHUNK_LOGGERS[request_id]


def finalize_chunk_logger(request_id: str) -> Path | None:
    """Finalize and save chunk logger for a request.

    Args:
        request_id: Request identifier

    Returns:
        Path to saved CSV file or None if logger not found
    """
    logger = _CHUNK_LOGGERS.pop(request_id, None)
    if logger is None:
        return None

    return logger.save()
