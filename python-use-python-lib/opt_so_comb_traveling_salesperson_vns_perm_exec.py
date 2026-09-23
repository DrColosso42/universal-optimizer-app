from random import seed

from uo.algorithm.metaheuristic.finish_control import FinishControl

from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_optimizer import (
    VnsOptimizerConstructionParameters,
    VnsOptimizer,
)

from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem import (
    TravelingSalespersonProblem,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_solution import (
    TravelingSalespersonProblemSolutionNn,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_vns_support import (
    TravelingSalespersonProblemVnsShakingSupport,
    TravelingSalespersonProblemVnsLocalSearchSupportDelta,
)


def main():
    problem_to_solve = TravelingSalespersonProblem.from_distance_matrix(
        distances=[
            [0, 2, 9, 10],
            [2, 0, 6, 4],
            [9, 6, 0, 8],
            [10, 4, 8, 0],
        ]
    )

    solution = TravelingSalespersonProblemSolutionNn()

    finish = FinishControl(criteria="evaluations & seconds", evaluations_max=15000, seconds_max=5)

    problem_dimension = problem_to_solve.dimension

    vns_shaking_support = TravelingSalespersonProblemVnsShakingSupport(
        dimension=problem_dimension
    )
    vns_ls_support = TravelingSalespersonProblemVnsLocalSearchSupportDelta(
        dimension=problem_dimension
    )

    vns_construction_params = VnsOptimizerConstructionParameters()
    vns_construction_params.problem = problem_to_solve
    vns_construction_params.solution_template = solution
    vns_construction_params.finish_control = finish
    vns_construction_params.vns_shaking_support = vns_shaking_support
    vns_construction_params.vns_ls_support = vns_ls_support
    vns_construction_params.random_seed = 43434343
    vns_construction_params.k_min = 1
    vns_construction_params.k_max = 3

    seed(vns_construction_params.random_seed)

    optimizer = VnsOptimizer.from_construction_tuple(vns_construction_params)
    best_solution = optimizer.optimize()

    print("Best solution representation: {}".format(best_solution.representation))
    print("Best solution code: {}".format(best_solution.string_representation()))
    print("Best solution objective: {}".format(best_solution.objective_value))
    print("Best solution fitness: {}".format(best_solution.fitness_value))
    print("Best solution feasible: {}".format(best_solution.is_feasible))
    print("Number of iterations: {}".format(optimizer.iteration))
    print("Number of evaluations: {}".format(optimizer.evaluation))


if __name__ == "__main__":
    main()
