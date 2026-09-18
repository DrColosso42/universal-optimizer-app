#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

DATA_DIR="$ROOT_DIR/opt/single_objective/comb/job_shop_scheduling_problem/data"
RESULTS_DIR="$ROOT_DIR/comparison/job_shop_scheduling_problem/results"

PYTHON="${PYTHON:-python}"
SOLVER="opt.single_objective.comb.job_shop_scheduling_problem.solver"

SEEDS=(1 2 3 4 5)
EVALUATIONS_MAX="${EVALUATIONS_MAX:-20000}"
INSTANCES=(mini3 ft06 la01 la02 la03 la04 la05)
METHODS=(sa vns ga)

mkdir -p "$RESULTS_DIR"

SUMMARY="$RESULTS_DIR/summary.csv"
echo "instance,method,seed,makespan,lower_bound,iterations,evaluations" > "$SUMMARY"

for instance in "${INSTANCES[@]}"; do
    input_file="$DATA_DIR/$instance.txt"

    for method in "${METHODS[@]}"; do
        method_dir="$RESULTS_DIR/$method"
        mkdir -p "$method_dir"

        for seed in "${SEEDS[@]}"; do
            output_file="$method_dir/${instance}_seed${seed}.txt"

            echo "Running $method over $instance (seed=$seed, evaluations=$EVALUATIONS_MAX)"

            "$PYTHON" -m "$SOLVER" \
                --input-file "$input_file" \
                --method "$method" \
                --seed "$seed" \
                --evaluations-max "$EVALUATIONS_MAX" \
                > "$output_file"

            makespan="$(grep 'Best solution makespan:' "$output_file" | awk '{print $NF}')"
            lower_bound="$(grep 'Lower bound of the makespan:' "$output_file" | awk '{print $NF}')"
            iterations="$(grep 'Number of iterations:' "$output_file" | awk '{print $NF}')"
            evaluations="$(grep 'Number of evaluations:' "$output_file" | awk '{print $NF}')"

            echo "$instance,$method,$seed,$makespan,$lower_bound,$iterations,$evaluations" >> "$SUMMARY"
        done
    done
done

echo "Done. Summary written to $SUMMARY"
