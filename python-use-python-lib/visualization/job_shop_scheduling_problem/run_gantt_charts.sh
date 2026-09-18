#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

PYTHON="${PYTHON:-python}"

"$PYTHON" "$ROOT_DIR/visualization/job_shop_scheduling_problem/draw_gantt_chart.py"
