import argparse
from random import seed

from uo.algorithm.metaheuristic.finish_control import FinishControl

from uo.algorithm.metaheuristic.tabu_search.tabu_search_support_standard_permutation import (
    TabuSearchSupportStandardPermutation,
)
from uo.algorithm.metaheuristic.tabu_search.tabu_search_optimizer import (
    TabuSearchOptimizerConstructionParameters,
    TabuSearchOptimizer,
)

from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem import (
    TravelingSalespersonProblem,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_permutation_solution import (
    TravelingSalespersonProblemPermutationSolution,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Solve Traveling Salesperson Problem.")

    parser.add_argument(
        "--input-file",
        type=str,
        required=True,
        help="Path to input file with the distance matrix describing the problem instance.",
    )
    parser.add_argument(
        "--method",
        type=str,
        required=True,
        choices=["tabu"],
        help="Optimization method to use.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=43434343,
        help="Random seed.",
    )
    parser.add_argument(
        "--evaluations-max",
        type=int,
        default=20000,
        help="Maximum number of evaluations.",
    )

    parser.add_argument(
        "--tabu-tenure",
        type=int,
        default=10,
        help="Number of most recent moves kept as tabu (forbidden) by the algorithm.",
    )

    return parser


def solve_tabu(
    problem: TravelingSalespersonProblem,
    random_seed: int,
    evaluations_max: int,
    tabu_tenure: int,
) -> tuple[TabuSearchOptimizer, TravelingSalespersonProblemPermutationSolution]:
    solution = TravelingSalespersonProblemPermutationSolution()

    finish = FinishControl(
        criteria="evaluations",
        evaluations_max=evaluations_max,
    )

    tabu_search_support = TabuSearchSupportStandardPermutation(dimension=problem.dimension)

    params = TabuSearchOptimizerConstructionParameters()
    params.problem = problem
    params.solution_template = solution
    params.finish_control = finish
    params.tabu_search_support = tabu_search_support
    params.tabu_tenure = tabu_tenure
    params.random_seed = random_seed

    seed(random_seed)

    optimizer = TabuSearchOptimizer.from_construction_tuple(params)
    best_solution = optimizer.optimize()
    return optimizer, best_solution


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    problem = TravelingSalespersonProblem.from_input_file(args.input_file)

    optimizer, best_solution = solve_tabu(
        problem=problem,
        random_seed=args.seed,
        evaluations_max=args.evaluations_max,
        tabu_tenure=args.tabu_tenure,
    )

    print("Best tour: {}".format(best_solution.representation))
    print("Best solution code: {}".format(best_solution.string_representation()))
    print("Best tour length (objective): {}".format(best_solution.objective_value))
    print("Best solution fitness: {}".format(best_solution.fitness_value))
    print("Best solution feasible: {}".format(best_solution.is_feasible))
    print("Number of iterations: {}".format(optimizer.iteration))
    print("Number of evaluations: {}".format(optimizer.evaluation))


if __name__ == "__main__":
    main()
