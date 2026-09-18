#!/usr/bin/env python3
"""
Draws a Gantt chart of the best schedule found for an instance of the Job Shop Scheduling Problem.

"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.patches as patches
import matplotlib.pyplot as plt

ROOT_DIR = Path(__file__).resolve().parents[2]

sys.path.append(str(ROOT_DIR))

from opt.single_objective.comb.job_shop_scheduling_problem.job_shop_scheduling_problem import (
    JobShopSchedulingProblem,
)
from opt.single_objective.comb.job_shop_scheduling_problem.job_shop_scheduling_problem_permutation_solution import (
    JobShopSchedulingProblemPermutationSolution,
)

RESULTS_DIR = ROOT_DIR / "comparison" / "job_shop_scheduling_problem" / "results"
DATA_DIR = ROOT_DIR / "opt" / "single_objective" / "comb" / "job_shop_scheduling_problem" / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "charts"

REPRESENTATION_PATTERN = re.compile(r"^Best solution representation:\s*\[(.*)\]\s*$")
MAKESPAN_PATTERN = re.compile(r"^Best solution makespan:\s*(\d+)\s*$")

FILE_NAME_PATTERN = re.compile(r"^(?P<instance>.+)_seed(?P<seed>\d+)$")


def parse_result_file(file_path: Path) -> tuple[list[int], int]:
    """
    Read one output file of the solver.

    :param Path file_path: output file of a single run of the solver
    :return: permutation of the best solution, and its makespan
    :rtype: tuple[list[int], int]
    """
    representation: list[int] = []
    makespan = -1

    for line in file_path.read_text(encoding="utf-8").splitlines():
        representation_match = REPRESENTATION_PATTERN.match(line)
        if representation_match:
            representation = [
                int(part) for part in representation_match.group(1).split(",")
            ]
        makespan_match = MAKESPAN_PATTERN.match(line)
        if makespan_match:
            makespan = int(makespan_match.group(1))

    if not representation or makespan < 0:
        raise ValueError(f"Output file does not hold a solution: {file_path}")

    return representation, makespan


def best_run_per_instance() -> dict[str, tuple[str, int, list[int], int]]:
    """
    Find, for every instance, the run that reached the shortest makespan.

    :return: for every instance, the method, the seed, the permutation and the makespan
    :rtype: dict[str, tuple[str, int, list[int], int]]
    """
    best: dict[str, tuple[str, int, list[int], int]] = {}

    for method_dir in sorted(RESULTS_DIR.iterdir()):
        if not method_dir.is_dir():
            continue
        for file_path in sorted(method_dir.glob("*.txt")):
            name_match = FILE_NAME_PATTERN.match(file_path.stem)
            if not name_match:
                continue
            instance = name_match.group("instance")
            seed = int(name_match.group("seed"))
            representation, makespan = parse_result_file(file_path)
            if instance not in best or makespan < best[instance][3]:
                best[instance] = (method_dir.name, seed, representation, makespan)

    return best


def draw_gantt_chart(
    instance: str,
    method: str,
    seed: int,
    representation: list[int],
    makespan: int,
) -> Path:
    """
    Draw the Gantt chart of one schedule and write it as a picture.

    :param str instance: name of the instance
    :param str method: method that produced the schedule
    :param int seed: random seed of the run
    :param list[int] representation: permutation that encodes the schedule
    :param int makespan: makespan of the schedule
    :return: path of the written picture
    :rtype: Path
    """
    problem = JobShopSchedulingProblem.from_input_file(str(DATA_DIR / f"{instance}.txt"))
    solution = JobShopSchedulingProblemPermutationSolution()
    schedule = solution.schedule(representation, problem)

    colours = plt.get_cmap("tab20")(
        [job_index % 20 for job_index in range(problem.number_of_jobs)]
    )

    figure, axes = plt.subplots(
        figsize=(max(8.0, makespan / 40.0), 1.0 + 0.4 * problem.number_of_machines)
    )

    for job_index, job in enumerate(problem.jobs):
        for operation_index, (machine, duration) in enumerate(job):
            started_at = schedule["start"][(job_index, operation_index)]
            axes.add_patch(
                patches.Rectangle(
                    (started_at, machine - 0.4),
                    duration,
                    0.8,
                    facecolor=colours[job_index],
                    edgecolor="black",
                    linewidth=0.4,
                )
            )
            if duration >= makespan / 60.0:
                axes.text(
                    started_at + duration / 2.0,
                    machine,
                    str(job_index),
                    ha="center",
                    va="center",
                    fontsize=6,
                )

    axes.set_xlim(0, makespan)
    axes.set_ylim(-0.6, problem.number_of_machines - 0.4)
    axes.set_yticks(range(problem.number_of_machines))
    axes.set_yticklabels([f"M{machine}" for machine in range(problem.number_of_machines)])
    axes.invert_yaxis()
    axes.set_xlabel("time")
    axes.set_title(
        f"{instance}: makespan {makespan}, lower bound {problem.lower_bound} "
        f"({method}, seed {seed})"
    )
    axes.grid(axis="x", linestyle=":", linewidth=0.4)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{instance}_{method}_seed{seed}.png"
    figure.tight_layout()
    figure.savefig(output_path, dpi=150)
    plt.close(figure)

    return output_path


def main() -> None:
    """
    Draw one chart for every instance of the comparison experiment.
    """
    if not RESULTS_DIR.is_dir():
        raise SystemExit(
            f"No results to visualize. Run the comparison experiment first, "
            f"it writes into {RESULTS_DIR}."
        )

    best = best_run_per_instance()

    if not best:
        raise SystemExit(f"No output files of the solver were found under {RESULTS_DIR}.")

    for instance in sorted(best):
        method, seed, representation, makespan = best[instance]
        output_path = draw_gantt_chart(instance, method, seed, representation, makespan)
        print(f"{instance}: makespan {makespan} by {method} (seed {seed}) -> {output_path}")


if __name__ == "__main__":
    main()
