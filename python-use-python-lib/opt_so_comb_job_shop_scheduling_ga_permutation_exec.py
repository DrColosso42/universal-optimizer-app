"""
Example of solving the Job Shop Scheduling Problem by a generational genetic algorithm, over a
permutation with repetition. Crossover is the precedence preservative crossover of Bierwirth and
Mattfeld, which is what keeps every offspring a valid permutation. The instance is `ft06` of
Fisher and Thompson, whose optimal makespan is 55.
"""

import os
from random import seed

from uo.algorithm.metaheuristic.finish_control import FinishControl
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

INSTANCE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "opt", "single_objective", "comb", "job_shop_scheduling_problem", "data", "ft06.txt",
)


def main():
    random_seed = 43434343

    problem_to_solve = JobShopSchedulingProblem.from_input_file(INSTANCE)

    solution = JobShopSchedulingProblemPermutationSolution(random_seed=random_seed)

    finish = FinishControl(criteria="evaluations & seconds", evaluations_max=20000, seconds_max=30)

    ga_construction_params = GaOptimizerGenerationalConstructionParameters()
    ga_construction_params.problem = problem_to_solve
    ga_construction_params.solution_template = solution
    ga_construction_params.finish_control = finish
    ga_construction_params.ga_selection = GaSelectionTournament(tournament_size=3)
    ga_construction_params.ga_crossover_support = GaCrossoverSupportPpxPermutation[str](
        crossover_probability=0.9
    )
    ga_construction_params.ga_mutation_support = GaMutationSupportSwapPermutation[str](
        mutation_probability=0.02
    )
    ga_construction_params.random_seed = random_seed
    ga_construction_params.population_size = 100
    ga_construction_params.elite_count = 2

    seed(random_seed)

    optimizer = GaOptimizerGenerational.from_construction_tuple(ga_construction_params)
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
