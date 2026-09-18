"""
.. _py_traveling_salesperson_problem_solver:
"""

import argparse
from random import seed

from uo.algorithm.metaheuristic.finish_control import FinishControl

from uo.algorithm.metaheuristic.genetic_algorithm.ga_optimizer_gen import (
    GaOptimizerGenerationalConstructionParameters,
    GaOptimizerGenerational,
)

from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_optimizer import (
    VnsOptimizerConstructionParameters,
    VnsOptimizer,
)

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
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_solution import (
    TravelingSalespersonProblemSolutionNn,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_permutation_solution import (
    TravelingSalespersonProblemPermutationSolution,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_support import (
    TravelingSalespersonProblemGaCrossoverSupportErx,
    TravelingSalespersonProblemGaMutationSupportInversion,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_selection import (
    TravelingSalespersonProblemGaSelectionTournament,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_vns_support import (
    TravelingSalespersonProblemVnsShakingSupport,
    TravelingSalespersonProblemVnsLocalSearchSupportDelta,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Solve Traveling Salesperson problem.")

    parser.add_argument(
        "--input-file",
        type=str,
        required=True,
        help="Path to input file describing the problem instance.",
    )
    parser.add_argument(
        "--method",
        type=str,
        required=True,
        choices=["ga", "vns", "tabu"],
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
        default=5000,
        help="Maximum number of evaluations.",
    )
    parser.add_argument(
        "--iterations-max",
        type=int,
        default=0,
        help="Maximum number of iterations (0 = no limit on iterations).",
    )

    # GA params
    parser.add_argument(
        "--population-size",
        type=int,
        default=100,
        help="Population size for GA.",
    )
    parser.add_argument(
        "--elite-count",
        type=int,
        default=10,
        help="Elite count for GA.",
    )
    parser.add_argument(
        "--crossover-probability",
        type=float,
        default=0.95,
        help="Crossover probability for GA.",
    )
    parser.add_argument(
        "--mutation-probability",
        type=float,
        default=0.05,
        help="Mutation probability for GA.",
    )

    # VNS params
    parser.add_argument(
        "--k-min",
        type=int,
        default=1,
        help="Minimal neighborhood size for VNS.",
    )
    parser.add_argument(
        "--k-max",
        type=int,
        default=3,
        help="Maximal neighborhood size for VNS.",
    )

    # Tabu Search params
    parser.add_argument(
        "--tabu-tenure",
        type=int,
        default=10,
        help="Number of most recent moves kept as tabu (forbidden) by the algorithm.",
    )

    return parser


def solve_ga(
    problem: TravelingSalespersonProblem,
    random_seed: int,
    evaluations_max: int,
    population_size: int,
    elite_count: int,
    crossover_probability: float,
    mutation_probability: float,
    iterations_max: int = 0,
) -> tuple[GaOptimizerGenerational, TravelingSalespersonProblemSolutionNn]:
    """Solve the TSP by a memetic Genetic Algorithm: edge recombination
    crossover, inversion mutation followed by a delta-evaluated 2-opt sweep
    over each offspring, tournament selection, elitism and nearest-neighbor
    initialization of the population."""

    solution = TravelingSalespersonProblemSolutionNn()

    criteria = "evaluations & iterations" if iterations_max > 0 else "evaluations"
    finish = FinishControl(
        criteria=criteria,
        evaluations_max=evaluations_max,
        iterations_max=iterations_max,
    )

    ga_selection = TravelingSalespersonProblemGaSelectionTournament()
    ga_crossover_support = TravelingSalespersonProblemGaCrossoverSupportErx(
        crossover_probability=crossover_probability
    )
    ga_mutation_support = TravelingSalespersonProblemGaMutationSupportInversion(
        mutation_probability=mutation_probability, apply_two_opt=True
    )

    params = GaOptimizerGenerationalConstructionParameters()
    params.problem = problem
    params.solution_template = solution
    params.finish_control = finish
    params.ga_selection = ga_selection
    params.ga_crossover_support = ga_crossover_support
    params.ga_mutation_support = ga_mutation_support
    params.random_seed = random_seed
    params.population_size = population_size
    params.elite_count = elite_count

    seed(random_seed)

    optimizer = GaOptimizerGenerational.from_construction_tuple(params)
    best_solution = optimizer.optimize()
    return optimizer, best_solution


def solve_vns(
    problem: TravelingSalespersonProblem,
    random_seed: int,
    evaluations_max: int,
    k_min: int,
    k_max: int,
    iterations_max: int = 0,
) -> tuple[VnsOptimizer, TravelingSalespersonProblemSolutionNn]:
    """Solve the TSP by Variable Neighborhood Search: relocation shaking with
    a growing kick strength and a delta-evaluated 2-opt + or-opt local
    search."""

    solution = TravelingSalespersonProblemSolutionNn()

    criteria = "evaluations & iterations" if iterations_max > 0 else "evaluations"
    finish = FinishControl(
        criteria=criteria,
        evaluations_max=evaluations_max,
        iterations_max=iterations_max,
    )

    dimension = problem.dimension
    vns_shaking_support = TravelingSalespersonProblemVnsShakingSupport(
        dimension=dimension
    )
    vns_ls_support = TravelingSalespersonProblemVnsLocalSearchSupportDelta(
        dimension=dimension
    )

    params = VnsOptimizerConstructionParameters()
    params.problem = problem
    params.solution_template = solution
    params.finish_control = finish
    params.random_seed = random_seed
    params.vns_shaking_support = vns_shaking_support
    params.vns_ls_support = vns_ls_support
    params.k_min = k_min
    params.k_max = k_max

    seed(random_seed)

    optimizer = VnsOptimizer.from_construction_tuple(params)
    best_solution = optimizer.optimize()
    return optimizer, best_solution


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

    if args.method == "ga":
        optimizer, best_solution = solve_ga(
            problem=problem,
            random_seed=args.seed,
            evaluations_max=args.evaluations_max,
            population_size=args.population_size,
            elite_count=args.elite_count,
            crossover_probability=args.crossover_probability,
            mutation_probability=args.mutation_probability,
            iterations_max=args.iterations_max,
        )
    elif args.method == "vns":
        optimizer, best_solution = solve_vns(
            problem=problem,
            random_seed=args.seed,
            evaluations_max=args.evaluations_max,
            k_min=args.k_min,
            k_max=args.k_max,
            iterations_max=args.iterations_max,
        )
    else:
        optimizer, best_solution = solve_tabu(
            problem=problem,
            random_seed=args.seed,
            evaluations_max=args.evaluations_max,
            tabu_tenure=args.tabu_tenure,
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
