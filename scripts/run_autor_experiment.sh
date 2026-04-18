#!/usr/bin/env bash
# Shell launcher for run_autor_experiment.py
# Handles MINIMAX_API_KEY and other environment setup

set -euo pipefail

# Ensure MINIMAX_API_KEY is set
if [[ -z "${MINIMAX_API_KEY:-}" ]]; then
    echo "ERROR: MINIMAX_API_KEY environment variable is not set"
    echo "Set it with: export MINIMAX_API_KEY=<your-key>"
    exit 1
fi

# Change to the repo root (where this script lives at scripts/run_autor_experiment.sh)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Run the Python script with all arguments
exec python3 "$SCRIPT_DIR/run_autor_experiment.py" "$@"
