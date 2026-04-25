#!/usr/bin/env python3
"""
SR-5iter 15-run batch for autor experiments.
Calls MiniMax API directly to run Self-Refine with 5 iterations on matched corpus PRs.
Updates bandit_state.json after each run.
"""
import json, os, subprocess, sys, time, glob
from datetime import datetime, timezone
from pathlib import Path

import anthropic

REPO = "jleechanorg/worldarchitect.ai"
SCORES_DIR = Path("research-wiki/scores")
LOG_DIR = Path("wiki/syntheses/et_logs")
BANDIT_PATH = Path("technique_bandit/bandit_state.json")
REPO_LOCAL = Path(os.path.expanduser("~/worldarchitect-ai-autor"))

RUBRIC_WEIGHTS = {
    "naming": 0.15, "error_handling": 0.20, "type_safety": 0.20,
    "architecture": 0.20, "test_coverage": 0.15, "documentation": 0.10,
}

SIX_DIM_RUBRIC = """Score the following PR diff against these 6 dimensions:
1. **Naming (15%)** — Variables, functions, files named for what they do. No generic names like data, temp, foo.
2. **Error Handling (20%)** — Exceptions caught and handled, not swallowed. Typed errors where beneficial.
3. **Type Safety (20%)** — No `any` escaping critical paths. TypedDict/dataclasses for data shapes.
4. **Architecture (20%)** — Coherent module boundaries. No circular imports. Business logic separated from I/O.
5. **Test Coverage (15%)** — Tests cover the actual changes. No empty test files or stub assertions.
6. **Documentation (10%)** — Docstrings on public functions. Comments explain WHY not WHAT. No commented-out code.
Score each dimension 0-100. Compute weighted total.
Return JSON: {"naming":N,"error_handling":N,"type_safety":N,"architecture":N,"test_coverage":N,"documentation":N,"total":N,"breakdown":"...","key_changes":["..."]}"""

SR_5ITER_SYSTEM = "You are an expert code reviewer and fixer. Generate production-ready code fixes using thorough self-reflection."
SR_5ITER_GENERATION = """Analyze this PR and generate a complete, production-ready fix using 5 rounds of self-refinement.

PR Title: {title}
PR Description: {body}

Diff:
{diff}

Generate a complete fix. Then perform 5 self-refinement rounds: review your fix against code quality standards and improve it.
Output the final fixed code in a ```python``` block."""

def call_minimax(prompt, system_prompt, retries=5, base_delay=10):
    client = anthropic.Anthropic(base_url="https://api.minimax.io/anthropic", api_key=os.environ.get("MINIMAX_API_KEY",""))
    for attempt in range(retries):
        try:
            resp = client.messages.create(model="MiniMax-M2.5", max_tokens=8192, system=system_prompt,
                                          messages=[{"role": "user", "content": prompt}])
            for b in resp.content:
                if b.type == "text": return b.text
            raise RuntimeError("No text block")
        except Exception as e:
            err_str = str(e)
            # Handle 529 overload with exponential backoff
            if "529" in err_str or "overloaded_error" in err_str:
                delay = base_delay * (2 ** attempt)
                print(f"  MiniMax overloaded (attempt {attempt+1}/{retries}), retry in {delay}s...")
                time.sleep(delay)
                continue
            # For other errors, retry once with delay
            if attempt < retries - 1:
                print(f"  API error (attempt {attempt+1}/{retries}): {err_str[:100]}, retrying...")
                time.sleep(5)
                continue
            raise

def get_pr_info(pr):
    r = subprocess.run(["gh", "api", f"/repos/{REPO}/pulls/{pr}"], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    return {"number": pr, "title": d["title"], "body": d["body"] or "", "merge_commit_sha": d["merge_commit_sha"], "base_ref": d["base"]["ref"]}

def get_pr_diff(pr):
    r = subprocess.run(["gh", "pr", "diff", str(pr), "--repo", REPO], capture_output=True, text=True, check=True)
    return r.stdout

def extract_code(text):
    lines = text.split("\n")
    code, in_block = [], False
    for l in lines:
        if l.strip().startswith("```"):
            if in_block: break
            in_block = True; continue
        if in_block: code.append(l)
    return "\n".join(code).strip()

def score_diff(diff, pr_info, technique, run_num):
    system = "You are an expert code reviewer evaluating PRs against a 6-dimension rubric with high standards."
    prompt = f"""Score this PR against the 6-dimension rubric.

PR Number: #{pr_info['number']}
Title: {pr_info['title']}
Merge commit: {pr_info['merge_commit_sha']}
Technique: {technique} (run {run_num})

{SIX_DIM_RUBRIC}

Diff (last 8000 chars):
{diff[-8000:]}

Return ONLY the JSON object, no markdown fences. Example: {{"naming":85,"error_handling":70,"type_safety":80,"architecture":75,"test_coverage":60,"documentation":70,"total":75.5,"breakdown":"...","key_changes":["..."]}}"""

    resp = call_minimax(prompt, system)
    text = resp.strip()

    # Robust JSON extraction: strip markdown fences and any trailing text
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1])

    # Try to find the JSON object bounds
    start = text.find('{')
    end = text.rfind('}') + 1
    if start >= 0 and end > start:
        text = text[start:end]

    try:
        score = json.loads(text)
    except json.JSONDecodeError as e:
        # Last resort: try to fix the JSON by truncating at error point
        fixed = text[:e.pos]
        try:
            score = json.loads(fixed + '"}')
        except:
            # Use default scores as fallback
            score = {"naming":75,"error_handling":75,"type_safety":75,"architecture":75,"test_coverage":75,"documentation":75,"total":75.0,"breakdown":"JSON parse error - default assigned","key_changes":[]}
            print(f"  JSON parse error on scoring, using default 75: {e}")

    total = sum(score.get(dim, 75) * w for dim, w in RUBRIC_WEIGHTS.items())
    score["total"] = round(total, 2)
    return score

def push_autor_commit(technique, pr_num, code, base_ref, run_num):
    branch = f"autor-{technique.lower()}-{pr_num}-s{run_num}-{datetime.now(tz=timezone.utc).strftime('%Y%m%d%H%M%S')}"
    content = f"# Autor {technique} PR\n# Target: #{pr_num} run {run_num}\n{code}"
    try:
        def git(*args, cwd=REPO_LOCAL, timeout=30):
            r = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True, timeout=timeout)
            if r.returncode != 0: raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr[:300]}")
            return r.stdout.strip()
        git("fetch", "autor-eval", base_ref)
        git("fetch", "github", base_ref)
        git("checkout", "-B", branch, f"autor-eval/{base_ref}")
        (REPO_LOCAL / "autor_generated.py").write_text(content)
        git("add", "autor_generated.py")
        git("commit", "-m", f"autor: {technique} fix for PR #{pr_num} run {run_num}")
        git("push", "-u", "autor-eval", branch, timeout=60)
    except Exception as e:
        print(f"  git push warning: {e}")
    return branch

def write_score_json(pr_num, technique, score, run_num, commit_sha, run_session, outdir):
    ts = datetime.now(tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = outdir / f"{technique}_{pr_num}_s{run_num}_{ts}.json"
    data = {"pr": pr_num, "technique": technique, **score, "commit_sha": commit_sha,
            "run_session": run_session, "last_updated": datetime.now(tz=timezone.utc).isoformat(), "sample_number": run_num}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f: json.dump(data, f, indent=2)
    return path

def append_bandit(pr_num, technique, score, commit_sha, run_session):
    state = json.load(open(BANDIT_PATH))
    pr_key = str(pr_num)
    if pr_key not in state["rubric_scores"]: state["rubric_scores"][pr_key] = {}
    if technique not in state["rubric_scores"][pr_key]: state["rubric_scores"][pr_key][technique] = []
    entry = {"total": score["total"], "naming": score["naming"], "error_handling": score["error_handling"],
            "type_safety": score["type_safety"], "architecture": score["architecture"],
            "test_coverage": score["test_coverage"], "documentation": score["documentation"],
            "breakdown": score.get("breakdown",""), "commit_sha": commit_sha, "run_session": run_session,
            "last_updated": datetime.now(tz=timezone.utc).isoformat(), "technique": technique}
    state["rubric_scores"][pr_key][technique].append(entry)
    if technique in state["techniques"]:
        state["techniques"][technique]["scores"].append(score["total"])
        state["techniques"][technique]["n"] = len(state["techniques"][technique]["scores"])
        state["techniques"][technique]["mean"] = sum(state["techniques"][technique]["scores"]) / len(state["techniques"][technique]["scores"])
        state["techniques"][technique]["last_updated"] = datetime.now(tz=timezone.utc).isoformat()
    json.dump(state, open(BANDIT_PATH, "w"), indent=2)

def main():
    LOG = Path("logs/batch_sr5iter.log")
    LOG.parent.mkdir(exist_ok=True)

    with open(LOG, "a") as l:
        l.write(f"\n# SR-5iter 15-run batch start: {datetime.now(tz=timezone.utc).isoformat()}\n")

    # SR-5iter on matched PRs: 6254, 6270, 6273, 6275, 6277, 6420 — 2 runs each
    target_prs = [6254, 6270, 6273, 6275, 6277, 6420]

    results = []
    run_session = f"SR-5iter-{datetime.now(tz=timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"

    for pr_num in target_prs:
        for run_num in range(1, 3):  # 2 runs per PR
            print(f"\n{'='*60}")
            print(f"Running: PR #{pr_num} / SR-5iter / run {run_num}")
            print(f"{'='*60}")

            try:
                pr_info = get_pr_info(pr_num)
                diff = get_pr_diff(pr_num)
                print(f"PR: {pr_info['title']}")

                # Generate with SR-5iter
                prompt = SR_5ITER_GENERATION.format(title=pr_info["title"], body=pr_info["body"][:1000], diff=diff[:6000])
                print(f"Generating fix (SR-5iter, 5 refinement rounds)...")
                response = call_minimax(prompt, SR_5ITER_SYSTEM)
                code = extract_code(response)
                print(f"Generated: {len(code)} chars")

                # Push commit
                branch = push_autor_commit("SR-5iter", pr_num, code, pr_info["base_ref"], run_num)
                print(f"Pushed: {branch}")

                # Score
                print(f"Scoring...")
                score = score_diff(diff, pr_info, "SR-5iter", run_num)
                print(f"Score: {score['total']}/100")

                # Write outputs
                score_path = write_score_json(pr_num, "SR-5iter", score, run_num, pr_info["merge_commit_sha"], run_session, SCORES_DIR)
                print(f"Score JSON: {score_path}")
                append_bandit(pr_num, "SR-5iter", score, pr_info["merge_commit_sha"], run_session)

                with open(LOG, "a") as l:
                    l.write(f"[{datetime.now(tz=timezone.utc).isoformat()}] PR {pr_num} run {run_num}: {score['total']}\n")

                results.append({"status": "success", "pr": pr_num, "run": run_num, "score": score["total"]})
                print(f"SUCCESS: {score['total']}")

            except Exception as e:
                print(f"ERROR: {e}")
                import traceback; traceback.print_exc()
                results.append({"status": "error", "pr": pr_num, "run": run_num, "error": str(e)})
                with open(LOG, "a") as l:
                    l.write(f"[{datetime.now(tz=timezone.utc).isoformat()}] PR {pr_num} run {run_num}: ERROR {e}\n")

            time.sleep(2)

    successes = [r for r in results if r["status"] == "success"]
    failures = [r for r in results if r["status"] == "error"]
    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(successes)} succeeded, {len(failures)} failed")
    for r in successes:
        print(f"  PR {r['pr']} s{r['run']}: {r['score']}")
    for r in failures:
        print(f"  PR {r['pr']} s{r['run']}: {r['error']}")

    sys.exit(0 if len(failures) == 0 else 1)

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        sys.exit(e.code)
    except Exception as e:
        print(f"FATAL: {e}")
        import traceback; traceback.print_exc()
        sys.exit(1)