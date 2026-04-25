#!/usr/bin/env python3
"""
aggregate_p14.py — Aggregate P14 Mode Router Benchmark results.

Reads all P14_*.json score files from research-wiki/scores/ and produces:
  1. Per-mode mean scores and win counts
  2. Per-query breakdown
  3. Router routing accuracy (did router pick the best mode?)
  4. Domain × mode heatmap
  5. Complexity × mode heatmap
"""
from __future__ import annotations

import json
import os
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

SCORES_DIR = Path(__file__).parent / "research-wiki" / "scores"


def load_p14_scores() -> list[dict]:
    """Load all P14 score JSON files."""
    scores = []
    for f in SCORES_DIR.glob("P14_*.json"):
        try:
            with open(f) as fh:
                scores.append(json.load(fh))
        except Exception as e:
            print(f"WARN: could not read {f}: {e}", file=sys.stderr)
    return scores


def aggregate(scores: list[dict]) -> dict:
    """Compute all aggregations."""
    MODES = ["single", "fixed", "gnn", "router"]
    domains = ["business", "policy", "science", "technical"]
    complexities = ["low", "medium", "high"]

    by_mode: dict[str, list[float]] = defaultdict(list)
    by_mode_latency: dict[str, list[float]] = defaultdict(list)
    by_query: dict[str, dict[str, float]] = defaultdict(dict)
    by_domain: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    by_complexity: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    router_routing: dict[str, dict] = {}  # query_id → {predicted, actual, scores}

    for s in scores:
        mode = s.get("technique", "")
        qid = s.get("pr", "")
        total = s.get("total", 50.0)
        domain = s.get("domain", "unknown")
        complexity = s.get("complexity", "unknown")
        latency = s.get("latency", 0.0)
        routed_to = s.get("routed_to", mode)

        if mode not in MODES:
            return  # skip non-P14 scores

        by_mode[mode].append(total)
        if latency > 0:
            by_mode_latency[mode].append(latency)

        by_query[qid][mode] = total

        if domain in domains:
            by_domain[domain][mode].append(total)
        if complexity in complexities:
            by_complexity[complexity][mode].append(total)

        if mode == "router":
            router_routing[qid] = {
                "predicted": routed_to,
                "scores": {m: by_query[qid].get(m, 0) for m in MODES},
            }

    # Per-mode summary
    mode_summary = {}
    for mode in MODES:
        vals = by_mode.get(mode, [])
        if vals:
            mode_summary[mode] = {
                "n": len(vals),
                "mean": round(statistics.mean(vals), 2),
                "stdev": round(statistics.stdev(vals), 2) if len(vals) > 1 else 0.0,
                "min": round(min(vals), 2),
                "max": round(max(vals), 2),
                "latency_mean": round(statistics.mean(by_mode_latency.get(mode, [0.0])), 2),
            }

    # Win counts (mode with highest score per query)
    win_counts = {mode: 0 for mode in MODES}
    for qid, qscores in by_query.items():
        if not qscores:
            continue
        best_mode = max(qscores, key=lambda m: qscores[m])
        win_counts[best_mode] += 1

    # Per-query breakdown
    query_breakdown = {}
    for qid, qscores in sorted(by_query.items()):
        if not qscores:
            continue
        best = max(qscores.values())
        best_mode = max(qscores, key=lambda m: qscores[m])
        query_breakdown[qid] = {
            "scores": {m: round(qscores.get(m, 0), 2) for m in MODES},
            "best": round(best, 2),
            "best_mode": best_mode,
        }

    # Router routing accuracy
    router_accuracy = {"correct": 0, "incorrect": 0, "ties": 0, "queries": []}
    for qid, info in router_routing.items():
        scores_dict = info["scores"]
        predicted = info["predicted"]

        # Best actual mode for this query
        best_actual = max(scores_dict, key=lambda m: scores_dict[m])
        if predicted == best_actual:
            router_accuracy["correct"] += 1
            verdict = "correct"
        elif abs(scores_dict[predicted] - scores_dict[best_actual]) < 0.5:
            router_accuracy["ties"] += 1
            verdict = "tie"
        else:
            router_accuracy["incorrect"] += 1
            verdict = "incorrect"
        router_accuracy["queries"].append({
            "qid": qid,
            "predicted": predicted,
            "best_actual": best_actual,
            "verdict": verdict,
            "scores": {m: round(scores_dict[m], 2) for m in MODES},
        })

    # Domain × mode heatmap
    domain_heatmap = {}
    for domain in domains:
        domain_heatmap[domain] = {}
        for mode in MODES:
            vals = by_domain[domain].get(mode, [])
            if vals:
                domain_heatmap[domain][mode] = round(statistics.mean(vals), 2)
            else:
                domain_heatmap[domain][mode] = None

    # Complexity × mode heatmap
    complexity_heatmap = {}
    for complexity in complexities:
        complexity_heatmap[complexity] = {}
        for mode in MODES:
            vals = by_complexity[complexity].get(mode, [])
            if vals:
                complexity_heatmap[complexity][mode] = round(statistics.mean(vals), 2)
            else:
                complexity_heatmap[complexity][mode] = None

    return {
        "mode_summary": mode_summary,
        "win_counts": win_counts,
        "query_breakdown": query_breakdown,
        "router_accuracy": router_accuracy,
        "domain_heatmap": domain_heatmap,
        "complexity_heatmap": complexity_heatmap,
        "total_scores": len(scores),
    }


def format_text(report: dict) -> str:
    lines = []
    MODES = ["single", "fixed", "gnn", "router"]

    lines.append("=" * 60)
    lines.append("P14 MODE ROUTER BENCHMARK — AGGREGATE RESULTS")
    lines.append("=" * 60)

    # Mode summary
    lines.append("\n### PER-MODE SUMMARY")
    lines.append(f"{'Mode':<12} {'n':>4} {'Mean':>7} {'StDev':>7} {'Min':>7} {'Max':>7} {'Latency':>8}")
    lines.append("-" * 60)
    for mode in MODES:
        s = report["mode_summary"].get(mode, {})
        if s:
            lines.append(f"{mode:<12} {s['n']:>4} {s['mean']:>7.2f} {s['stdev']:>7.2f} "
                         f"{s['min']:>7.2f} {s['max']:>7.2f} {s['latency_mean']:>8.2f}s")

    # Win counts
    lines.append("\n### WIN COUNTS (most wins per query)")
    for mode in MODES:
        count = report["win_counts"].get(mode, 0)
        lines.append(f"  {mode}: {count} wins")

    # Router accuracy
    lines.append("\n### ROUTER ACCURACY")
    ra = report["router_accuracy"]
    total = ra["correct"] + ra["incorrect"] + ra["ties"]
    if total > 0:
        acc = ra["correct"] / total
        lines.append(f"  Correct: {ra['correct']}/{total} ({acc:.1%})")
        lines.append(f"  Ties: {ra['ties']}")
        lines.append(f"  Incorrect: {ra['incorrect']}")
        lines.append("\n  Query-level routing:")
        for q in ra["queries"]:
            lines.append(f"    {q['qid']}: predicted={q['predicted']}, "
                         f"best={q['best_actual']} ({q['verdict']}) | "
                         f"scores: " + ", ".join(f"{m}={q['scores'][m]}" for m in MODES))

    # Domain heatmap
    lines.append("\n### DOMAIN × MODE HEATMAP")
    lines.append(f"{'Domain':<12}" + "".join(f"{m:>10}" for m in MODES))
    lines.append("-" * (12 + 10 * len(MODES)))
    for domain in ["business", "policy", "science", "technical"]:
        row = domain_heatmap_display(report, domain, MODES)
        lines.append(f"{domain:<12}" + "".join(f"{v:>10}" for v in row))

    # Complexity heatmap
    lines.append("\n### COMPLEXITY × MODE HEATMAP")
    lines.append(f"{'Complexity':<12}" + "".join(f"{m:>10}" for m in MODES))
    lines.append("-" * (12 + 10 * len(MODES)))
    for complexity in ["low", "medium", "high"]:
        row = complexity_heatmap_display(report, complexity, MODES)
        lines.append(f"{complexity:<12}" + "".join(f"{v:>10}" for v in row))

    # Query breakdown
    lines.append("\n### QUERY BREAKDOWN")
    for qid, info in sorted(report["query_breakdown"].items()):
        lines.append(f"\n  {qid} (best: {info['best_mode']}={info['best']:.2f})")
        for mode in MODES:
            score = info["scores"].get(mode, 0)
            marker = " ★" if mode == info["best_mode"] else ""
            lines.append(f"    {mode}: {score:.2f}{marker}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def domain_heatmap_display(report: dict, domain: str, modes: list[str]) -> list:
    dh = report["domain_heatmap"].get(domain, {})
    return [str(dh.get(m, "—")) if dh.get(m) is not None else "—" for m in modes]


def complexity_heatmap_display(report: dict, complexity: str, modes: list[str]) -> list:
    ch = report["complexity_heatmap"].get(complexity, {})
    return [str(ch.get(m, "—")) if ch.get(m) is not None else "—" for m in modes]


def main():
    scores = load_p14_scores()
    if not scores:
        print("No P14 score files found in research-wiki/scores/P14_*.json")
        sys.exit(1)

    report = aggregate(scores)
    text = format_text(report)
    print(text)

    # Also write JSON report
    out = Path(__file__).parent / "P14_report.json"
    with open(out, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nJSON report: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
