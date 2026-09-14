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


def main():
    problem_to_solve = TravelingSalespersonProblem.from_input_file(
        "opt/single_objective/comb/traveling_salesperson_problem/inputs/usa-1.txt"
    )

    solution = TravelingSalespersonProblemPermutationSolution()

    finish = FinishControl(criteria="evaluations & seconds", evaluations_max=20000, seconds_max=10)

    tabu_search_support = TabuSearchSupportStandardPermutation(dimension=problem_to_solve.dimension)

    tabu_search_construction_params = TabuSearchOptimizerConstructionParameters()
    tabu_search_construction_params.problem = problem_to_solve
    tabu_search_construction_params.solution_template = solution
    tabu_search_construction_params.finish_control = finish
    tabu_search_construction_params.tabu_search_support = tabu_search_support
    tabu_search_construction_params.tabu_tenure = 10
    tabu_search_construction_params.random_seed = 43434343

    seed(tabu_search_construction_params.random_seed)

    optimizer = TabuSearchOptimizer.from_construction_tuple(tabu_search_construction_params)
    best_solution = optimizer.optimize()

    print("Best tour: {}".format(best_solution.representation))
    print("Best solution code: {}".format(best_solution.string_representation()))
    print("Best tour length (objective): {}".format(best_solution.objective_value))
    print("Best solution fitness: {}".format(best_solution.fitness_value))
    print("Best solution feasible: {}".format(best_solution.is_feasible))
    print("Number of iterations: {}".format(optimizer.iteration))
    print("Number of evaluations: {}".format(optimizer.evaluation))


if __name__ == "__main__":
    main()
