"""
Example of solving the Job Shop Scheduling Problem by simulated annealing, over a permutation
with repetition. The instance is `ft06` of Fisher and Thompson, whose optimal makespan is 55.
"""

import os
from random import seed

from uo.algorithm.metaheuristic.finish_control import FinishControl
from uo.algorithm.metaheuristic.simulated_annealing.sa_optimizer import SaOptimizer
from uo.algorithm.metaheuristic.simulated_annealing.sa_neighborhood_permutation import (
    SaNeighborhoodPermutation,
)
from uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_exponetial import (
    SaTemperatureExponential,
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

    seed(random_seed)

    optimizer = SaOptimizer(
        sa_neighborhood=SaNeighborhoodPermutation(problem_to_solve.dimension, k=1),
        sa_temperature=SaTemperatureExponential(0.9, 0.9995),
        finish_control=finish,
        problem=problem_to_solve,
        solution_template=solution,
        random_seed=random_seed,
    )

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
