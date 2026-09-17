"""
.. _py_job_shop_scheduling_problem_solver:

Entry point for every method aimed at solving the Job Shop Scheduling Problem. All parameters that
govern the execution of a method are supplied through command line arguments.

Example, simulated annealing over the instance `ft06` with a budget of fifty thousand evaluations::

    python opt/single_objective/comb/job_shop_scheduling_problem/solver.py \\
        --input-file opt/single_objective/comb/job_shop_scheduling_problem/data/ft06.txt \\
        --method sa --evaluations-max 50000
"""

import argparse
from random import seed

from uo.algorithm.metaheuristic.finish_control import FinishControl

from uo.algorithm.metaheuristic.simulated_annealing.sa_optimizer import SaOptimizer
from uo.algorithm.metaheuristic.simulated_annealing.sa_neighborhood_permutation import (
    SaNeighborhoodPermutation,
)
from uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_const import (
    SaTemperatureConst,
)
from uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_linear import (
    SaTemperatureLinear,
)
from uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_exponetial import (
    SaTemperatureExponential,
)

from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_shaking_support_standard_permutation import (
    VnsShakingSupportStandardPermutation,
)
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_ls_support_standard_fi_permutation import (
    VnsLocalSearchSupportStandardFirstImprovementPermutation,
)
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_ls_support_standard_bi_permutation import (
    VnsLocalSearchSupportStandardBestImprovementPermutation,
)
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_optimizer import (
    VnsOptimizerConstructionParameters,
    VnsOptimizer,
)

from uo.algorithm.metaheuristic.genetic_algorithm.ga_selection_tournament import (
    GaSelectionTournament,
)
from uo.algorithm.metaheuristic.genetic_algorithm.ga_crossover_support_ppx_permutation import (
    GaCrossoverSupportPpxPermutation,
)
from uo.algorithm.metaheuristic.genetic_algorithm.ga_mutation_support_swap_permutation import (
    GaMutationSupportSwapPermutation,
)
from uo.algorithm.metaheuristic.genetic_algorithm.ga_optimizer_gen import (
    GaOptimizerGenerationalConstructionParameters,
    GaOptimizerGenerational,
)

from opt.single_objective.comb.job_shop_scheduling_problem.job_shop_scheduling_problem import (
    JobShopSchedulingProblem,
)
from opt.single_objective.comb.job_shop_scheduling_problem.job_shop_scheduling_problem_permutation_solution import (
    JobShopSchedulingProblemPermutationSolution,
)


def build_parser() -> argparse.ArgumentParser:
    """
    Build the command line parser of the solver.

    :return: parser holding every parameter that governs the execution
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Solve the Job Shop Scheduling Problem over a permutation with repetition.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--input-file",
        type=str,
        required=True,
        help="Path to the input file describing the problem instance.",
    )
    parser.add_argument(
        "--method",
        type=str,
        required=True,
        choices=["sa", "vns", "ga"],
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
        help="Maximum number of evaluations, the budget that is shared by all methods.",
    )

    sa_group = parser.add_argument_group("simulated annealing")
    sa_group.add_argument(
        "--sa-temperature",
        type=str,
        default="exponential",
        choices=["const", "linear", "exponential"],
        help="Schedule of the probability of accepting a worse solution.",
    )
    sa_group.add_argument(
        "--sa-initial-temperature",
        type=float,
        default=0.9,
        help="Initial probability of accepting a worse solution, between 0 and 1.",
    )
    sa_group.add_argument(
        "--sa-decay-factor",
        type=float,
        default=0.9995,
        help="Factor by which the exponential schedule decays in every iteration.",
    )
    sa_group.add_argument(
        "--sa-decay-step",
        type=float,
        default=0.0001,
        help="Amount by which the linear schedule decreases in every iteration.",
    )
    sa_group.add_argument(
        "--sa-swaps",
        type=int,
        default=1,
        help="Number of swaps that form a single move of the simulated annealing.",
    )

    vns_group = parser.add_argument_group("variable neighborhood search")
    vns_group.add_argument(
        "--k-min",
        type=int,
        default=1,
        help="Minimal number of swaps applied while shaking.",
    )
    vns_group.add_argument(
        "--k-max",
        type=int,
        default=3,
        help="Maximal number of swaps applied while shaking.",
    )
    vns_group.add_argument(
        "--local-search",
        type=str,
        default="first",
        choices=["first", "best"],
        help="Variant of the local search that is used within the search.",
    )

    ga_group = parser.add_argument_group("genetic algorithm")
    ga_group.add_argument(
        "--population-size",
        type=int,
        default=100,
        help="Population size.",
    )
    ga_group.add_argument(
        "--elite-count",
        type=int,
        default=2,
        help="Number of individuals carried over unchanged into the next generation.",
    )
    ga_group.add_argument(
        "--tournament-size",
        type=int,
        default=3,
        help="Number of individuals taking part in a single tournament.",
    )
    ga_group.add_argument(
        "--crossover-probability",
        type=float,
        default=0.9,
        help="Probability that two parents are actually crossed.",
    )
    ga_group.add_argument(
        "--mutation-probability",
        type=float,
        default=0.02,
        help="Probability that a single position of the permutation takes part in a swap.",
    )

    return parser


def build_temperature(args: argparse.Namespace):
    """
    Build the temperature function of the simulated annealing out of the supplied arguments.

    :param argparse.Namespace args: parsed command line arguments
    :return: temperature schedule
    """
    if args.sa_temperature == "const":
        return SaTemperatureConst(args.sa_initial_temperature)
    if args.sa_temperature == "linear":
        return SaTemperatureLinear(args.sa_initial_temperature, args.sa_decay_step)
    return SaTemperatureExponential(args.sa_initial_temperature, args.sa_decay_factor)


def solve_sa(
    problem: JobShopSchedulingProblem,
    args: argparse.Namespace,
) -> tuple[SaOptimizer, JobShopSchedulingProblemPermutationSolution]:
    """
    Solve the problem by simulated annealing.

    :param JobShopSchedulingProblem problem: problem that is solved
    :param argparse.Namespace args: parsed command line arguments
    :return: optimizer that was executed, and the best solution it found
    :rtype: tuple
    """
    seed(args.seed)

    optimizer = SaOptimizer(
        sa_neighborhood=SaNeighborhoodPermutation(problem.dimension, args.sa_swaps),
        sa_temperature=build_temperature(args),
        finish_control=FinishControl(
            criteria="evaluations",
            evaluations_max=args.evaluations_max,
        ),
        problem=problem,
        solution_template=JobShopSchedulingProblemPermutationSolution(
            random_seed=args.seed
        ),
        random_seed=args.seed,
    )

    best_solution = optimizer.optimize()

    return optimizer, best_solution


def solve_vns(
    problem: JobShopSchedulingProblem,
    args: argparse.Namespace,
) -> tuple[VnsOptimizer, JobShopSchedulingProblemPermutationSolution]:
    """
    Solve the problem by variable neighborhood search.

    :param JobShopSchedulingProblem problem: problem that is solved
    :param argparse.Namespace args: parsed command line arguments
    :return: optimizer that was executed, and the best solution it found
    :rtype: tuple
    """
    if args.local_search == "best":
        vns_ls_support = VnsLocalSearchSupportStandardBestImprovementPermutation[str](
            dimension=problem.dimension
        )
    else:
        vns_ls_support = VnsLocalSearchSupportStandardFirstImprovementPermutation[str](
            dimension=problem.dimension
        )

    params = VnsOptimizerConstructionParameters()
    params.problem = problem
    params.solution_template = JobShopSchedulingProblemPermutationSolution(
        random_seed=args.seed
    )
    params.finish_control = FinishControl(
        criteria="evaluations",
        evaluations_max=args.evaluations_max,
    )
    params.random_seed = args.seed
    params.vns_shaking_support = VnsShakingSupportStandardPermutation[str](
        dimension=problem.dimension
    )
    params.vns_ls_support = vns_ls_support
    params.k_min = args.k_min
    params.k_max = args.k_max

    seed(args.seed)

    optimizer = VnsOptimizer.from_construction_tuple(params)
    best_solution = optimizer.optimize()

    return optimizer, best_solution


def solve_ga(
    problem: JobShopSchedulingProblem,
    args: argparse.Namespace,
) -> tuple[GaOptimizerGenerational, JobShopSchedulingProblemPermutationSolution]:
    """
    Solve the problem by a generational genetic algorithm.

    :param JobShopSchedulingProblem problem: problem that is solved
    :param argparse.Namespace args: parsed command line arguments
    :return: optimizer that was executed, and the best solution it found
    :rtype: tuple
    """
    params = GaOptimizerGenerationalConstructionParameters()
    params.problem = problem
    params.solution_template = JobShopSchedulingProblemPermutationSolution(
        random_seed=args.seed
    )
    params.finish_control = FinishControl(
        criteria="evaluations",
        evaluations_max=args.evaluations_max,
    )
    params.random_seed = args.seed
    params.ga_selection = GaSelectionTournament(args.tournament_size)
    params.ga_crossover_support = GaCrossoverSupportPpxPermutation[str](
        crossover_probability=args.crossover_probability
    )
    params.ga_mutation_support = GaMutationSupportSwapPermutation[str](
        mutation_probability=args.mutation_probability
    )
    params.population_size = args.population_size
    params.elite_count = args.elite_count

    seed(args.seed)

    optimizer = GaOptimizerGenerational.from_construction_tuple(params)
    best_solution = optimizer.optimize()

    return optimizer, best_solution


def main() -> None:
    """
    Read the instance, run the selected method over it, and report the outcome.
    """
    parser = build_parser()
    args = parser.parse_args()

    problem = JobShopSchedulingProblem.from_input_file(args.input_file)

    if args.method == "sa":
        optimizer, best_solution = solve_sa(problem, args)
    elif args.method == "vns":
        optimizer, best_solution = solve_vns(problem, args)
    else:
        optimizer, best_solution = solve_ga(problem, args)

    print("Instance: {}".format(args.input_file))
    print("Jobs: {}".format(problem.number_of_jobs))
    print("Machines: {}".format(problem.number_of_machines))
    print("Lower bound of the makespan: {}".format(problem.lower_bound))
    print("Method: {}".format(args.method))
    print("Best solution representation: {}".format(best_solution.representation))
    print("Best solution makespan: {}".format(best_solution.objective_value))
    print("Best solution fitness: {}".format(best_solution.fitness_value))
    print("Best solution feasible: {}".format(best_solution.is_feasible))
    print("Number of iterations: {}".format(optimizer.iteration))
    print("Number of evaluations: {}".format(optimizer.evaluation))


if __name__ == "__main__":
    main()
