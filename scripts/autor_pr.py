"""Helpers for the autor PR lifecycle.

Autor PRs are evaluation artifacts. They must be opened as drafts with the
[autor] label plus a technique tag, then closed (never merged) after a score
JSON has been written. This module encodes that contract so a weaker model
cannot route around it by calling `gh pr create` directly.

See CLAUDE.md > "Autor PR Lifecycle (MANDATORY)" for the policy.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Iterable, Sequence

DEFAULT_REPO = "jleechanorg/worldarchitect.ai"
ALLOWED_TECHNIQUES = frozenset({
    "SR", "ET", "PRM", "SelfRefine", "ExtendedThinking",
    "SR-5iter", "SR-fewshot", "SR-adversarial",
    "SR-metaharness", "SR-prtype", "SR-multi-exemplar",
})
AUTOR_LABEL = "autor"


class AutorLifecycleError(RuntimeError):
    """Raised when the caller violates the autor PR lifecycle contract."""


def _run_gh(args: Sequence[str], *, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["gh", *args],
        check=check,
        capture_output=True,
        text=True,
    )


def _normalize_technique(technique: str) -> str:
    technique = technique.strip()
    if technique not in ALLOWED_TECHNIQUES:
        raise AutorLifecycleError(
            f"Unknown technique {technique!r}; expected one of {sorted(ALLOWED_TECHNIQUES)}"
        )
    return technique


def open_draft_autor_pr(
    *,
    technique: str,
    title: str,
    body: str,
    branch: str,
    base: str = "main",
    repo: str = DEFAULT_REPO,
    extra_labels: Iterable[str] = (),
) -> int:
    """Open a draft autor PR and return its number.

    Forces `--draft`, adds the `autor` label and a `technique:<tech>` label,
    and prefixes the title with `[autor][<tech>]` if not already present.
    Returns the PR number.
    """
    technique = _normalize_technique(technique)

    prefix = f"[autor][{technique}]"
    if prefix not in title:
        title = f"{prefix} {title}"

    labels = {AUTOR_LABEL, f"technique:{technique}", *extra_labels}

    cmd = [
        "pr",
        "create",
        "--repo",
        repo,
        "--draft",
        "--base",
        base,
        "--head",
        branch,
        "--title",
        title,
        "--body",
        body,
    ]
    for label in sorted(labels):
        cmd.extend(["--label", label])

    result = _run_gh(cmd)
    url = result.stdout.strip().splitlines()[-1]
    try:
        return int(url.rsplit("/", 1)[-1])
    except ValueError as exc:
        raise AutorLifecycleError(
            f"Could not parse PR number from gh output: {url!r}"
        ) from exc


def close_after_score(
    *,
    pr: int,
    technique: str,
    score: float,
    score_json_path: os.PathLike | str,
    repo: str = DEFAULT_REPO,
    extra_comment: str = "",
) -> None:
    """Close an autor PR after a score artifact has been committed.

    Refuses to close unless `score_json_path` points to an existing file on
    disk. This prevents closing the PR before the evaluation record exists.
    """
    technique = _normalize_technique(technique)
    score_path = Path(score_json_path)
    if not score_path.is_file():
        raise FileNotFoundError(
            f"Refusing to close autor PR #{pr}: score JSON {score_path} does not exist"
        )

    try:
        json.loads(score_path.read_text())
    except json.JSONDecodeError as exc:
        raise AutorLifecycleError(
            f"Score JSON {score_path} is not valid JSON: {exc}"
        ) from exc

    comment_lines = [
        f"Autor evaluation complete — closing without merge.",
        f"- Technique: **{technique}**",
        f"- Score: **{score:.1f}/100**",
        f"- Artifact: `{score_path}`",
    ]
    if extra_comment:
        comment_lines.append("")
        comment_lines.append(extra_comment)
    comment = "\n".join(comment_lines)

    _run_gh(
        [
            "pr",
            "close",
            str(pr),
            "--repo",
            repo,
            "--comment",
            comment,
        ]
    )


__all__ = [
    "ALLOWED_TECHNIQUES",
    "AUTOR_LABEL",
    "AutorLifecycleError",
    "DEFAULT_REPO",
    "close_after_score",
    "open_draft_autor_pr",
]
