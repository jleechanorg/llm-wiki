#!/usr/bin/env bash
#
# verify_setup.sh - Bootstrap bash script validating auto-research experiment setup
#
# Validates the directory/repo structure required for the v2.1 auto-research
# experiment per the gist specification.
#
# Exit codes:
#   0 - all checks passed
#   1 - one or more checks failed
#
# Usage:
#   ./scripts/verify_setup.sh
#

set -euo pipefail

# ─── Color output helpers ────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

pass() { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; }
warn() { echo -e "${YELLOW}!${NC} $1"; }

# ─── Constants ────────────────────────────────────────────────────────────────

# Top-level directories that must exist and be non-empty
REQUIRED_DIRS=(
    "raw"
    "canonical-repos"
    "test-prs"
    "wiki"
    "skills"
    "scripts"
)

# Skill files required under skills/
REQUIRED_SKILLS=(
    "auto_research_loop.md"
    "self_critique_verification_loop.md"
    "canonical_code_scorer.md"
)

# Base path — allow override via env for testing
BASE_DIR="${RESEARCH_WIKI_BASE:-${HOME}/research-wiki}"

# ─── Helpers ───────────────────────────────────────────────────────────────────

# check_dir_exists DIR
#   Exits 1 if DIR does not exist or is empty.
check_dir_exists() {
    local dir="$BASE_DIR/$1"
    if [[ ! -d "$dir" ]]; then
        fail "Required directory missing: $dir"
        return 1
    fi
    if [[ -z "$(ls -A "$dir" 2>/dev/null)" ]]; then
        fail "Required directory is empty: $dir"
        return 1
    fi
    pass "$dir (exists, non-empty)"
    return 0
}

# check_file_exists FILE
#   Exits 1 if FILE does not exist.
check_file_exists() {
    local file="$BASE_DIR/$1"
    if [[ ! -f "$file" ]]; then
        fail "Required file missing: $file"
        return 1
    fi
    pass "$file (exists)"
    return 0
}

# ─── Main ──────────────────────────────────────────────────────────────────────

errors=0

echo "=========================================="
echo "Auto-Research v2.1 Setup Verification"
echo "Base: $BASE_DIR"
echo "=========================================="
echo ""

# 1. Check required top-level directories exist and are non-empty
echo "--- Checking required directories ---"
for dir in "${REQUIRED_DIRS[@]}"; do
    check_dir_exists "$dir" || ((errors++))
done
echo ""

# 2. Check canonical-repos/ has at least one repo
echo "--- Checking canonical-repos/ has at least one repo ---"
canonical_repos_dir="$BASE_DIR/canonical-repos"
if [[ -d "$canonical_repos_dir" ]]; then
    repo_count=$(find "$canonical_repos_dir" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$repo_count" -ge 1 ]]; then
        pass "canonical-repos/ contains $repo_count repo(s)"
    else
        fail "canonical-repos/ has no repos (need at least 1)"
        ((errors++))
    fi
fi
echo ""

# 3. Check test-prs/ has at least one .md file
echo "--- Checking test-prs/ has at least one .md file ---"
test_prs_dir="$BASE_DIR/test-prs"
if [[ -d "$test_prs_dir" ]]; then
    md_count=$(find "$test_prs_dir" -mindepth 1 -name "*.md" -type f 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$md_count" -ge 1 ]]; then
        pass "test-prs/ contains $md_count .md file(s)"
    else
        fail "test-prs/ has no .md files (need at least 1)"
        ((errors++))
    fi
fi
echo ""

# 4. Check required skill files
echo "--- Checking required skill files ---"
skills_dir="$BASE_DIR/skills"
for skill in "${REQUIRED_SKILLS[@]}"; do
    check_file_exists "skills/$skill" || ((errors++))
done
echo ""

# ─── Summary ─────────────────────────────────────────────────────────────────

echo "=========================================="
if [[ "$errors" -eq 0 ]]; then
    echo -e "${GREEN}All checks passed. Setup is valid.${NC}"
    echo "=========================================="
    exit 0
else
    echo -e "${RED}$errors check(s) failed. See errors above.${NC}"
    echo "=========================================="
    exit 1
fi
