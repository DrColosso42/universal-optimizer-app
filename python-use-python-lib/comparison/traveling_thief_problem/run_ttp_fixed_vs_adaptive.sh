#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

DATA_DIR="$ROOT_DIR/opt/single_objective/comb/traveling_thief_problem/data"

RESULTS_DIR="$ROOT_DIR/comparison/traveling_thief_problem/results"
FIXED_DIR="$RESULTS_DIR/fixed"
ADAPTIVE_DIR="$RESULTS_DIR/adaptive"

mkdir -p "$FIXED_DIR"
mkdir -p "$ADAPTIVE_DIR"

SEEDS=(1 2 3)
ITERATIONS_MAX=300

for input_file in "$DATA_DIR"/*.ttp; do
    base_name="$(basename "$input_file" .ttp)"

    if [[ "$base_name" == rat195* ]]; then
        echo "Skipping $base_name (too large for a quick default run, test manually with --input-file)"
        continue
    fi

    for seed in "${SEEDS[@]}"; do
        echo "Running fixed for $base_name (seed=$seed)"

        poetry run python -m opt.single_objective.comb.traveling_thief_problem.solver \
            --input-file "$input_file" \
            --method fixed \
            --seed "$seed" \
            --iterations-max "$ITERATIONS_MAX" \
            > "$FIXED_DIR/${base_name}_seed${seed}_fixed.txt"

        echo "Running adaptive for $base_name (seed=$seed)"

        poetry run python -m opt.single_objective.comb.traveling_thief_problem.solver \
            --input-file "$input_file" \
            --method adaptive \
            --seed "$seed" \
            --iterations-max "$ITERATIONS_MAX" \
            > "$ADAPTIVE_DIR/${base_name}_seed${seed}_adaptive.txt"
    done
done

echo "Done."
