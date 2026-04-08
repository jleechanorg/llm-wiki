#!/usr/bin/env python3
"""
Mass fetch all .md files from GitHub repos and local directories.
Stores fetched files in /tmp/wiki_fetch/ for later ingestion.

Usage:
    python tools/mass_fetch.py --repos          # Fetch from GitHub repos
    python tools/mass_fetch.py --local          # Fetch from local dirs
    python tools/mass_fetch.py --all            # Both
    python tools/mass_fetch.py --status        # Show status
"""
import os, sys, json, re, subprocess, base64, hashlib
from pathlib import Path
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import argparse

WIKI_DIR = Path("/Users/jleechan/llm_wiki")
FETCH_DIR = Path("/tmp/wiki_fetch")
MAX_WORKERS = 24

SKIP_PATTERNS = {"node_modules", ".git", "dist", "build", "coverage", "__pycache__", ".venv", "venv", ".next", ".cache", ".test", "test.", "spec."}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".tar", ".gz", ".ico", ".svg", ".mp4", ".mp3"}

@dataclass
class FFile:
    repo: str; path: str; content: str; url: str; sha: str; source: str

def gh(args: list, timeout=30) -> str:
    try:
        r = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=timeout)
        return r.stdout if r.returncode == 0 else ""
    except: return ""

def get_repos() -> list[dict]:
    repos = []
    for org in ["jleechanorg", "jleechan2015"]:
        out = gh(["repo", "list", org, "--limit", "200", "--json", "name,description,url,defaultBranchRef"])
        if out:
            try:
                for r in json.loads(out):
                    repos.append({
                        "full_name": f"{org}/{r['name']}",
                        "name": r["name"], "org": org,
                        "description": r.get("description") or "",
                        "branch": (r.get("defaultBranchRef") or {}).get("name", "main")
                    })
            except: pass
    return repos

def fetch_readme(repo_full: str, branch: str) -> list[FFile]:
    for fname in ["README.md", "README.rst", "readme.md", "README.txt"]:
        out = gh(["api", f"repos/{repo_full}/contents/{fname}?ref={branch}"])
        if not out: continue
        try:
            d = json.loads(out)
            content = base64.b64decode(d.get("content", "")).decode("utf-8", errors="replace")
            if len(content) < 20: continue
            return [FFile(
                repo=repo_full, path=fname,
                content=content[:50000],
                url=d.get("html_url", f"https://github.com/{repo_full}/blob/{branch}/{fname}"),
                sha=d.get("sha", ""), source="github"
            )]
        except: pass
    return []

def fetch_md_files(repo_full: str, branch: str) -> list[FFile]:
    results = []
    out = gh(["search", "code", f"repo:{repo_full}", "filename:.md", "--limit", "30",
              "--json", "path,content,url,sha"], timeout=60)
    if not out: return results
    try:
        for item in json.loads(out):
            p = item.get("path", "")
            if any(s in p.lower() for s in SKIP_PATTERNS): continue
            if Path(p).suffix.lower() in SKIP_EXT: continue
            try:
                content = base64.b64decode(item.get("content", "")).decode("utf-8", errors="replace")
                if len(content) < 30: continue
                results.append(FFile(
                    repo=repo_full, path=p,
                    content=content[:50000],
                    url=item.get("url", ""),
                    sha=item.get("sha", ""), source="github"
                ))
            except: pass
    except: pass
    return results

def fetch_local_files() -> list[FFile]:
    results = []
    dirs = [
        Path.home() / "Documents", Path.home() / "Desktop",
        Path.home() / "projects", Path.home() / "repos",
    ]
    for base in dirs:
        if not base.exists(): continue
        try:
            for f in base.rglob("*.md"):
                if any(s in str(f).lower() for s in SKIP_PATTERNS): continue
                try:
                    content = f.read_text(encoding="utf-8", errors="replace")
                    if len(content) < 30: continue
                    rel = f.relative_to(base.parent)
                    results.append(FFile(
                        repo=f"local:{base.name}", path=str(rel),
                        content=content[:50000],
                        url=f"file://{f}",
                        sha=hashlib.sha256(content.encode()).hexdigest()[:16],
                        source="local"
                    ))
                except: pass
        except: pass
    # Top-level homedir .md files
    for f in Path.home().glob("*.md"):
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            if len(content) >= 30:
                results.append(FFile(
                    repo="local:homedir", path=f.name,
                    content=content[:50000],
                    url=f"file://{f}",
                    sha=hashlib.sha256(content.encode()).hexdigest()[:16],
                    source="local"
                ))
        except: pass
    return results

def save_fetched(entries: list[FFile]) -> int:
    FETCH_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path = FETCH_DIR / "manifest.json"
    manifest = []
    count = 0
    for e in entries:
        slug = re.sub(r'[^a-z0-9-]', '-', f"{e.repo}-{e.path}".lower())
        slug = re.sub(r'-+', '-', slug).strip('-')[:100]
        slug = hashlib.sha256(f"{e.repo}:{e.path}".encode()).hexdigest()[:12] + "-" + slug[:80]
        fpath = FETCH_DIR / f"{slug}.json"
        data = {"repo": e.repo, "path": e.path, "content": e.content, "url": e.url, "sha": e.sha, "source": e.source}
        with open(fpath, 'w') as f:
            json.dump(data, f)
        manifest.append({"slug": slug, "repo": e.repo, "path": e.path, "source": e.source})
        count += 1
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f)
    return count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repos", action="store_true")
    parser.add_argument("--local", action="store_true")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()

    manifest_path = FETCH_DIR / "manifest.json"
    if args.status:
        if manifest_path.exists():
            with open(manifest_path) as f:
                m = json.load(f)
            by_source = {}
            for e in m:
                by_source.setdefault(e.get("source", "?"), []).append(e["repo"])
            print(f"Total fetched: {len(m)} files")
            for src, repos in sorted(by_source.items()):
                unique_repos = len(set(repos))
                print(f"  {src}: {len(repos)} files from ~{unique_repos} repos")
        else:
            print("No fetched files yet. Run with --all")
        return

    all_entries = []
    total_repos = 0

    if args.all or args.repos:
        print("Fetching from GitHub repos...")
        repos = get_repos()
        total_repos = len(repos)
        print(f"  Found {len(repos)} repos")

        print("  Fetching READMEs...")
        with ThreadPoolExecutor(max_workers=16) as ex:
            futures = {ex.submit(fetch_readme, r["full_name"], r["branch"]): r for r in repos}
            done = 0
            for f in as_completed(futures):
                done += 1
                if done % 20 == 0: print(f"    README: {done}/{len(repos)}")
                for entry in f.result():
                    all_entries.append(entry)

        print(f"  Got {len(all_entries)} README files")

        print("  Fetching additional .md files...")
        # Prioritize repos with docs in name
        doc_repos = [r for r in repos if re.search(r'doc|guide|note|plan|spec|readme|wiki', r.get("description","") or "", re.I)]
        if not doc_repos: doc_repos = repos[:30]

        with ThreadPoolExecutor(max_workers=16) as ex:
            futures = {ex.submit(fetch_md_files, r["full_name"], r["branch"]): r for r in doc_repos}
            done = 0
            for f in as_completed(futures):
                done += 1
                if done % 10 == 0: print(f"    MD: {done}/{len(doc_repos)}")
                for entry in f.result():
                    all_entries.append(entry)

    if args.all or args.local:
        print("Fetching from local directories...")
        local = fetch_local_files()
        all_entries.extend(local)
        print(f"  Got {len(local)} local files")

    # Deduplicate by repo+path
    seen = set()
    unique = []
    for e in all_entries:
        key = (e.repo, e.path)
        if key not in seen:
            seen.add(key)
            unique.append(e)

    print(f"Total unique files: {len(unique)}")
    count = save_fetched(unique)
    print(f"Saved {count} files to {FETCH_DIR}")
    print(f"Run: python tools/mass_ingest.py --ingest to ingest them")

if __name__ == "__main__":
    main()
