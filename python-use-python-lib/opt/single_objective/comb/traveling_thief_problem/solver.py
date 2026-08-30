"""
.. _py_traveling_thief_problem_solver:
"""

import argparse
from random import seed

from uo.algorithm.metaheuristic.finish_control import FinishControl

from uo.algorithm.metaheuristic.aco.aco_optimizer import AcoOptimizerConstructionParameters
from uo.algorithm.metaheuristic.aco.aco_optimizer_standard import AcoOptimizerStandard
from uo.algorithm.metaheuristic.aco.aco_evaporation_support import (
    AcoEvaporationSupportFixed,
    AcoEvaporationSupportAdaptive,
)

from opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem import (
    TravelingThiefProblem,
)
from opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem_solution import (
    TravelingThiefProblemSolution,
)
from opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem_aco_construction_support import (
    TravelingThiefProblemAcoConstructionSupport,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Solve Traveling Thief Problem using ACO.")

    parser.add_argument(
        "--input-file", type=str, required=True, help="Path to input .ttp file."
    )
    parser.add_argument(
        "--method", type=str, required=True, choices=["fixed", "adaptive"],
        help="Evaporation control variant to use.",
    )
    parser.add_argument("--seed", type=int, default=43434343, help="Random seed.")
    parser.add_argument(
        "--iterations-max", type=int, default=200, help="Maximum number of iterations."
    )
    parser.add_argument(
        "--n-ants", type=int, default=None, help="Number of ants (default: problem size)."
    )
    parser.add_argument("--alpha", type=float, default=1.0, help="Pheromone influence.")
    parser.add_argument("--beta", type=float, default=2.0, help="Heuristic influence.")
    parser.add_argument("--rho", type=float, default=0.02, help="Base evaporation rate.")
    parser.add_argument("--p-best", type=float, default=0.05, help="MMAS tau_min parameter.")
    parser.add_argument(
        "--stagnation-limit", type=int, default=100,
        help="Iterations without improvement before tau reset.",
    )
    parser.add_argument(
        "--rho-scale", type=float, default=2.0, help="Adaptive evaporation scale factor."
    )

    return parser


def solve_aco(
    problem: TravelingThiefProblem,
    method: str,
    random_seed: int,
    iterations_max: int,
    n_ants: int | None,
    alpha: float,
    beta: float,
    rho: float,
    p_best: float,
    stagnation_limit: int,
    rho_scale: float,
) -> tuple[AcoOptimizerStandard, TravelingThiefProblemSolution]:
    solution = TravelingThiefProblemSolution()

    finish = FinishControl(
        criteria="iterations",
        iterations_max=iterations_max,
    )

    construction_support = TravelingThiefProblemAcoConstructionSupport()
    if method == "fixed":
        evaporation_support = AcoEvaporationSupportFixed()
    else:
        evaporation_support = AcoEvaporationSupportAdaptive(rho_scale=rho_scale)

    params = AcoOptimizerConstructionParameters()
    params.construction_support = construction_support
    params.evaporation_support = evaporation_support
    params.n_ants = n_ants if n_ants is not None else problem.n
    params.alpha = alpha
    params.beta = beta
    params.rho = rho
    params.p_best = p_best
    params.stagnation_limit = stagnation_limit
    params.finish_control = finish
    params.problem = problem
    params.solution_template = solution
    params.random_seed = random_seed

    seed(random_seed)

    optimizer = AcoOptimizerStandard.from_construction_tuple(params)
    best_solution = optimizer.optimize()

    return optimizer, best_solution


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    problem = TravelingThiefProblem.from_input_file(args.input_file)

    optimizer, best_solution = solve_aco(
        problem=problem,
        method=args.method,
        random_seed=args.seed,
        iterations_max=args.iterations_max,
        n_ants=args.n_ants,
        alpha=args.alpha,
        beta=args.beta,
        rho=args.rho,
        p_best=args.p_best,
        stagnation_limit=args.stagnation_limit,
        rho_scale=args.rho_scale,
    )

    print("Best solution representation: {}".format(best_solution.representation))
    print("Best solution code: {}".format(best_solution.string_representation()))
    print("Best solution objective: {}".format(best_solution.objective_value))
    print("Best solution fitness: {}".format(best_solution.fitness_value))
    print("Best solution feasible: {}".format(best_solution.is_feasible))
    print("Number of iterations: {}".format(optimizer.iteration))
    print("Number of evaluations: {}".format(optimizer.evaluation))


if __name__ == "__main__":
    main()
