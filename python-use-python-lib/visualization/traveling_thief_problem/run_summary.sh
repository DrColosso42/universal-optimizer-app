#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

poetry run python "$ROOT_DIR/visualization/traveling_thief_problem/summarize_results.py"
