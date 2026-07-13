import argparse
from random import seed

from uo.algorithm.metaheuristic.finish_control import FinishControl

from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_shaking_support_standard_int import (
    VnsShakingSupportStandardInt,
)
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_ls_support_standard_bi_int import (
    VnsLocalSearchSupportStandardBestImprovementInt,
)
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_optimizer import (
    VnsOptimizerConstructionParameters,
    VnsOptimizer,
)

from uo.algorithm.metaheuristic.simulated_annealing.sa_neighborhood_int import (
    SaNeighborhoodInt,
)
from uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_exponetial import (
    SaTemperatureExponential,
)
from uo.algorithm.metaheuristic.simulated_annealing.sa_optimizer import (
    SaOptimizerConstructionParameters,
    SaOptimizer,
)

from opt.single_objective.comb.graph_coloring_problem.graph_coloring_problem import (
    GraphColoringProblem,
)
from opt.single_objective.comb.graph_coloring_problem.graph_coloring_problem_int_solution import (
    GraphColoringProblemIntSolution,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Solve Graph Coloring problem."
    )

    parser.add_argument(
        "--input-file",
        type=str,
        required=True,
        help="Path to input file describing the graph.",
    )

    parser.add_argument(
        "--method",
        type=str,
        required=True,
        choices=["vns", "sa"],
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

    # SA params
    parser.add_argument(
        "--initial-temp",
        type=float,
        default=0.9,
        help="Initial temperature for SA.",
    )

    parser.add_argument(
        "--decay-factor",
        type=float,
        default=0.95,
        help="Temperature decay factor for SA.",
    )

    return parser


def encoded_dimension(
    problem: GraphColoringProblem,
) -> int:
    """
    Return the number of bits used by the integer representation.

    The maximum number of available colors is equal to the number of graph
    vertices.
    """
    colors_count = problem.number_of_vertices

    bits_per_color = max(
        1,
        (colors_count - 1).bit_length(),
    )

    return problem.dimension * bits_per_color


def solve_vns(
    problem: GraphColoringProblem,
    random_seed: int,
    evaluations_max: int,
    k_min: int,
    k_max: int,
) -> tuple[VnsOptimizer, GraphColoringProblemIntSolution]:
    """
    Solve the Graph Coloring Problem using VNS.

    The maximum number of available colors is automatically set to the number
    of graph vertices. The objective function minimizes the number of colors
    used while penalizing invalid colors and conflicts.
    """
    colors_count = problem.number_of_vertices

    solution = GraphColoringProblemIntSolution(
        colors_count=colors_count
    )

    finish = FinishControl(
        criteria="evaluations",
        evaluations_max=evaluations_max,
    )

    dimension = encoded_dimension(problem)

    vns_shaking_support = VnsShakingSupportStandardInt(
        dimension=dimension
    )

    vns_ls_support = (
        VnsLocalSearchSupportStandardBestImprovementInt(
            dimension=dimension
        )
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


def solve_sa(
    problem: GraphColoringProblem,
    random_seed: int,
    evaluations_max: int,
    initial_temp: float,
    decay_factor: float,
) -> tuple[SaOptimizer, GraphColoringProblemIntSolution]:
    """
    Solve the Graph Coloring Problem using Simulated Annealing.

    The maximum number of available colors is automatically set to the number
    of graph vertices. The objective function minimizes the number of colors
    used while penalizing invalid colors and conflicts.
    """
    colors_count = problem.number_of_vertices

    solution = GraphColoringProblemIntSolution(
        colors_count=colors_count
    )

    finish = FinishControl(
        criteria="evaluations",
        evaluations_max=evaluations_max,
    )

    dimension = encoded_dimension(problem)

    sa_neighborhood = SaNeighborhoodInt(
        dimension=dimension,
        k=1,
    )

    sa_temperature = SaTemperatureExponential(
        initial_temp=initial_temp,
        decay_factor=decay_factor,
    )

    params = SaOptimizerConstructionParameters()
    params.problem = problem
    params.solution_template = solution
    params.finish_control = finish
    params.random_seed = random_seed
    params.sa_neighborhood = sa_neighborhood
    params.sa_temperature = sa_temperature

    seed(random_seed)

    optimizer = SaOptimizer.from_construction_tuple(params)
    best_solution = optimizer.optimize()

    return optimizer, best_solution


def print_solution(
    problem: GraphColoringProblem,
    optimizer,
    best_solution: GraphColoringProblemIntSolution,
) -> None:
    """
    Print optimization results.
    """
    used_colors_count = best_solution.used_colors_count(
        representation=best_solution.representation,
        problem=problem,
    )

    print(
        "Best solution representation: {}".format(
            best_solution.representation
        )
    )

    print(
        "Best solution code: {}".format(
            best_solution.string_representation()
        )
    )

    print(
        "Best solution objective: {}".format(
            best_solution.objective_value
        )
    )

    print(
        "Best solution fitness: {}".format(
            best_solution.fitness_value
        )
    )

    print(
        "Best solution feasible: {}".format(
            best_solution.is_feasible
        )
    )

    print(
        "Number of used colors: {}".format(
            used_colors_count
        )
    )

    print(
        "Number of iterations: {}".format(
            optimizer.iteration
        )
    )

    print(
        "Number of evaluations: {}".format(
            optimizer.evaluation
        )
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    problem = GraphColoringProblem.from_input_file(
        args.input_file
    )

    if args.method == "vns":
        optimizer, best_solution = solve_vns(
            problem=problem,
            random_seed=args.seed,
            evaluations_max=args.evaluations_max,
            k_min=args.k_min,
            k_max=args.k_max,
        )
    else:
        optimizer, best_solution = solve_sa(
            problem=problem,
            random_seed=args.seed,
            evaluations_max=args.evaluations_max,
            initial_temp=args.initial_temp,
            decay_factor=args.decay_factor,
        )

    print_solution(
        problem=problem,
        optimizer=optimizer,
        best_solution=best_solution,
    )


if __name__ == "__main__":
    main()