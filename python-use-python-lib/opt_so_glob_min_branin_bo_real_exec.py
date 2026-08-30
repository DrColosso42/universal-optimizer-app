"""Solve the two-dimensional Branin problem with Bayesian optimization."""

import numpy as np

from uo.algorithm.bayesian_optimization.optimizer import (
    AcquisitionConfig,
    BayesianOptimizer,
    BayesianOptimizerConstructionParameters,
)

from opt.single_objective.glob.branin_min_problem import (
    BraninMinProblem,
    BraninMinProblemRealSolution,
)

RANDOM_SEED = 17
EVALUATION_BUDGET = 40
NUMBER_OF_INITIAL_POINTS = 6


def build_optimizer() -> BayesianOptimizer:
    """Build the deterministic optimizer used by the runnable example."""
    problem = BraninMinProblem()
    parameters = BayesianOptimizerConstructionParameters(
        problem=problem,
        solution_template=BraninMinProblemRealSolution(random_seed=RANDOM_SEED),
        bounds=problem.bounds,
        evaluation_budget=EVALUATION_BUDGET,
        number_of_initial_points=NUMBER_OF_INITIAL_POINTS,
        random_seed=RANDOM_SEED,
        acquisition_config=AcquisitionConfig(number_of_restarts=8),
    )
    return BayesianOptimizer.from_construction_tuple(parameters)


def distance_to_nearest_minimizer(
    point: np.ndarray, problem: BraninMinProblem
) -> float:
    """Return Euclidean distance from a point to the nearest known minimizer."""
    distances = np.linalg.norm(problem.known_minimizers - point, axis=1)
    return float(np.min(distances))


def main() -> None:
    """Run Bayesian optimization and print a concise result summary."""
    optimizer = build_optimizer()
    best = optimizer.optimize()
    nearest_distance = distance_to_nearest_minimizer(
        best.representation, optimizer.problem
    )

    print(f"Problem: {optimizer.problem.name}")
    print(f"Best vector: {best.representation}")
    print(f"Best objective: {best.objective_value:.12f}")
    print(f"Best fitness: {best.fitness_value:.12f}")
    print(f"Nearest known minimizer distance: {nearest_distance:.12f}")
    print(f"Evaluations: {optimizer.evaluation}")
    print(f"Iterations: {optimizer.iteration}")


if __name__ == "__main__":
    main()
