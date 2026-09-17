"""
Example of solving the Job Shop Scheduling Problem by variable neighborhood search, over a
permutation with repetition. The instance is `ft06` of Fisher and Thompson, whose optimal
makespan is 55.
"""

import os
from random import seed

from uo.algorithm.metaheuristic.finish_control import FinishControl
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_shaking_support_standard_permutation import (
    VnsShakingSupportStandardPermutation,
)
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_ls_support_standard_fi_permutation import (
    VnsLocalSearchSupportStandardFirstImprovementPermutation,
)
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_optimizer import (
    VnsOptimizerConstructionParameters,
    VnsOptimizer,
)

from opt.single_objective.comb.job_shop_scheduling_problem.job_shop_scheduling_problem import (
    JobShopSchedulingProblem,
)
from opt.single_objective.comb.job_shop_scheduling_problem.job_shop_scheduling_problem_permutation_solution import (
    JobShopSchedulingProblemPermutationSolution,
)

INSTANCE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "opt", "single_objective", "comb", "job_shop_scheduling_problem", "data", "ft06.txt",
)


def main():
    random_seed = 43434343

    problem_to_solve = JobShopSchedulingProblem.from_input_file(INSTANCE)

    solution = JobShopSchedulingProblemPermutationSolution(random_seed=random_seed)

    finish = FinishControl(criteria="evaluations & seconds", evaluations_max=20000, seconds_max=30)

    problem_dimension = problem_to_solve.dimension

    vns_shaking_support = VnsShakingSupportStandardPermutation[str](
        dimension=problem_dimension
    )
    vns_ls_support = VnsLocalSearchSupportStandardFirstImprovementPermutation[str](
        dimension=problem_dimension
    )

    vns_construction_params = VnsOptimizerConstructionParameters()
    vns_construction_params.problem = problem_to_solve
    vns_construction_params.solution_template = solution
    vns_construction_params.finish_control = finish
    vns_construction_params.vns_shaking_support = vns_shaking_support
    vns_construction_params.vns_ls_support = vns_ls_support
    vns_construction_params.random_seed = random_seed
    vns_construction_params.k_min = 1
    vns_construction_params.k_max = 3

    seed(random_seed)

    optimizer = VnsOptimizer.from_construction_tuple(vns_construction_params)
    best_solution = optimizer.optimize()

    print("Best solution representation: {}".format(best_solution.representation))
    print("Best solution makespan: {}".format(best_solution.objective_value))
    print("Best solution fitness: {}".format(best_solution.fitness_value))
    print("Best solution feasible: {}".format(best_solution.is_feasible))
    print("Lower bound of the makespan: {}".format(problem_to_solve.lower_bound))
    print("Number of iterations: {}".format(optimizer.iteration))
    print("Number of evaluations: {}".format(optimizer.evaluation))


if __name__ == "__main__":
    main()
