#!/usr/bin/env python3
"""
Thompson Sampling Bandit for PR Technique Selection

Selects the best coding technique (SelfRefine, ET, PRM) for each PR
using Thompson sampling with Beta posteriors over score outcomes.

Usage:
    python3 technique_selector.py [--PR <number> [--score <n>] [--update]]
    python3 technique_selector.py --rank
    python3 technique_selector.py --suggest <PR_number>
    python3 technique_selector.py --eval <PR_number> <technique> <score>
"""

import argparse
import json
import math
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

PRIOR_ALPHA = 2  # Beta prior alpha (weakly informative)
PRIOR_BETA = 2   # Beta prior beta (weakly informative)

CANONICAL_SCORE_MIN = 50  # Min possible canonical score
CANONICAL_SCORE_MAX = 100  # Max possible canonical score
SCORE_RANGE = CANONICAL_SCORE_MAX - CANONICAL_SCORE_MIN

DATA_DIR = os.path.expanduser("~/.claude/projects/-Users-jleechan-llm-wiki/technique_bandit")
STATE_FILE = os.path.join(DATA_DIR, "bandit_state.json")


@dataclass
class TechniquePosterior:
    alpha: float = PRIOR_ALPHA
    beta: float = PRIOR_BETA
    observations: list = field(default_factory=list)

    def sample(self) -> float:
        """Sample from Beta posterior."""
        import random
        return random.betavariate(self.alpha, self.beta)

    def mean(self) -> float:
        return self.alpha / (self.alpha + self.beta)

    def add_observation(self, score: float):
        """Add a normalized score [0,1] observation."""
        norm = (score - CANONICAL_SCORE_MIN) / SCORE_RANGE
        norm = max(0.0, min(1.0, norm))
        self.alpha += norm
        self.beta += 1 - norm
        self.observations.append({"score": score, "norm": norm, "ts": datetime.now().isoformat()})


@dataclass
class BanditState:
    techniques: dict[str, TechniquePosterior] = field(default_factory=dict)
    history: list = field(default_factory=list)
    # PR feature store (for future feature-based selection)
    pr_features: dict = field(default_factory=dict)

    def __post_init__(self):
        if not self.techniques:
            for t in ["SelfRefine", "ET", "PRM"]:
                self.techniques[t] = TechniquePosterior()


def load_state() -> BanditState:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            data = json.load(f)
            state = BanditState()
            for t, p in data.get("techniques", {}).items():
                state.techniques[t] = TechniquePosterior(
                    alpha=p.get("alpha", PRIOR_ALPHA),
                    beta=p.get("beta", PRIOR_BETA),
                    observations=p.get("observations", [])
                )
            state.history = data.get("history", [])
            state.pr_features = data.get("pr_features", {})
            return state
    return BanditState()


def save_state(state: BanditState):
    os.makedirs(DATA_DIR, exist_ok=True)
    data = {
        "techniques": {
            t: {
                "alpha": p.alpha,
                "beta": p.beta,
                "observations": p.observations[-50:]  # keep last 50
            }
            for t, p in state.techniques.items()
        },
        "history": state.history[-100:],  # keep last 100
        "pr_features": state.pr_features,
        "updated": datetime.now().isoformat()
    }
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def select_technique(state: BanditState) -> tuple[str, dict]:
    """Select technique via Thompson sampling. Returns (technique, debug_info)."""
    import random
    samples = {}
    for t, p in state.techniques.items():
        # Clip to [0.5, 1.0] range since all our scores are 50-100
        s = p.sample()
        s = max(0.5, min(1.0, s))
        samples[t] = s

    winner = max(samples, key=samples.get)

    debug = {
        t: {
            "posterior_mean": round(p.mean() * SCORE_RANGE + CANONICAL_SCORE_MIN, 1),
            "sample": round(s * SCORE_RANGE + CANONICAL_SCORE_MIN, 1),
            "n": len(p.observations),
            "alpha": round(p.alpha, 2),
            "beta": round(p.beta, 2),
        }
        for t, (p, s) in zip(state.techniques.keys(), [(p, samples[t]) for t in state.techniques])
    }

    return winner, debug


def record_result(state: BanditState, technique: str, score: float, pr_num: int, delta: float):
    """Record a score result and update posterior."""
    if technique in state.techniques:
        state.techniques[technique].add_observation(score)

    state.history.append({
        "pr": pr_num,
        "technique": technique,
        "score": score,
        "delta": delta,
        "ts": datetime.now().isoformat(),
        "expected_score": round(state.techniques[technique].mean() * SCORE_RANGE + CANONICAL_SCORE_MIN, 1)
    })


def print_ranking(state: BanditState):
    print("\n=== Thompson Sampling Posterior State ===")
    for t, p in sorted(state.techniques.items(), key=lambda x: -x[1].mean()):
        avg = p.mean() * SCORE_RANGE + CANONICAL_SCORE_MIN
        print(f"  {t:15s}: mean={avg:.1f}  n={len(p.observations):3d}  "
              f"α={p.alpha:.1f} β={p.beta:.1f}")


def print_suggestion(state: BanditState, pr_num: int):
    winner, debug = select_technique(state)
    print(f"\n=== Technique Suggestion for PR #{pr_num} ===")
    print(f"  Recommended: {winner}")
    print(f"\n  Posterior samples:")
    for t, info in sorted(debug.items(), key=lambda x: -x[1]["sample"]):
        print(f"    {t:15s}: sample={info['sample']:.1f}  "
              f"(posterior mean={info['posterior_mean']:.1f}, n={info['n']})")


def main():
    parser = argparse.ArgumentParser(description="Thompson Sampling Technique Selector")
    parser.add_argument("--PR", type=int, help="PR number")
    parser.add_argument("--score", type=float, help="Score received (for update)")
    parser.add_argument("--technique", default=None, help="Technique used")
    parser.add_argument("--delta", type=float, help="Delta vs baseline")
    parser.add_argument("--update", action="store_true", help="Update with --PR/--score/--technique")
    parser.add_argument("--suggest", type=int, help="Get suggestion for PR number")
    parser.add_argument("--rank", action="store_true", help="Print current ranking")
    parser.add_argument("--history", action="store_true", help="Show history")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    import random
    random.seed(args.seed)

    state = load_state()

    if args.update:
        if not args.PR or not args.score or not args.technique:
            print("ERROR: --update requires --PR, --score, --technique")
            sys.exit(1)
        record_result(state, args.technique, args.score, args.PR, args.delta or 0)
        save_state(state)
        print(f"Updated: PR #{args.PR} {args.technique} score={args.score}")
        print_ranking(state)

    elif args.suggest:
        print_suggestion(state, args.suggest)

    elif args.rank:
        print_ranking(state)

    elif args.history:
        print("\n=== Recent History ===")
        for h in state.history[-20:]:
            print(f"  PR #{h['pr']:5d} {h['technique']:12s} score={h['score']:6.1f} "
                  f"Δ={h['delta']:+5.1f}  expected={h['expected_score']:.1f}")

    else:
        # Default: print ranking + suggestion if no args
        print_ranking(state)
        print("\nUsage: --suggest <PR>  --update --PR <n> --score <s> --technique <t>")
        print("        --rank  --history")


if __name__ == "__main__":
    main()
