from random import seed

from uo.algorithm.metaheuristic.finish_control import FinishControl
from uo.algorithm.metaheuristic.genetic_algorithm.ga_optimizer_gen import (
    GaOptimizerGenerationalConstructionParameters,
    GaOptimizerGenerational,
)

from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem import (
    TravelingSalespersonProblem,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_solution import (
    TravelingSalespersonProblemSolutionNn,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_support import (
    TravelingSalespersonProblemGaCrossoverSupportErx,
    TravelingSalespersonProblemGaMutationSupportInversion,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_selection import (
    TravelingSalespersonProblemGaSelectionTournament,
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

    finish = FinishControl(criteria="evaluations", evaluations_max=5000)

    ga_selection = TravelingSalespersonProblemGaSelectionTournament()
    ga_crossover_support = TravelingSalespersonProblemGaCrossoverSupportErx(
        crossover_probability=0.95
    )
    ga_mutation_support = TravelingSalespersonProblemGaMutationSupportInversion(
        mutation_probability=0.05, apply_two_opt=True
    )

    ga_construction_params = GaOptimizerGenerationalConstructionParameters()
    ga_construction_params.problem = problem_to_solve
    ga_construction_params.solution_template = solution
    ga_construction_params.finish_control = finish
    ga_construction_params.ga_selection = ga_selection
    ga_construction_params.ga_crossover_support = ga_crossover_support
    ga_construction_params.ga_mutation_support = ga_mutation_support
    ga_construction_params.random_seed = 43434343
    ga_construction_params.population_size = 100
    ga_construction_params.elite_count = 10

    seed(ga_construction_params.random_seed)

    optimizer = GaOptimizerGenerational.from_construction_tuple(
        ga_construction_params
    )
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
