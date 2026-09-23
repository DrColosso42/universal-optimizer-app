import unittest
import unittest.mock as mocker
from random import seed

from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem import (
    TravelingSalespersonProblem,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_solution import (
    TravelingSalespersonProblemSolution,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_selection import (
    TravelingSalespersonProblemGaSelectionTournament,
)

DISTANCES = [[0, 2, 9, 10], [2, 0, 6, 4], [9, 6, 0, 8], [10, 4, 8, 0]]


class TestTravelingSalespersonProblemGaSelectionTournament(unittest.TestCase):

    def setUp(self):
        self.problem = TravelingSalespersonProblem.from_distance_matrix(
            distances=DISTANCES
        )

    def test_initialize_instance_with_valid_tournament_size(self):
        selection = TravelingSalespersonProblemGaSelectionTournament(tournament_size=3)

        self.assertEqual(selection.tournament_size, 3)

    def test_default_tournament_size(self):
        selection = TravelingSalespersonProblemGaSelectionTournament()

        self.assertEqual(selection.tournament_size, 3)

    def test_tournament_size_type_error(self):
        with self.assertRaises(TypeError):
            TravelingSalespersonProblemGaSelectionTournament(tournament_size="3")

    def test_tournament_size_must_be_at_least_two(self):
        with self.assertRaises(ValueError):
            TravelingSalespersonProblemGaSelectionTournament(tournament_size=1)

    def test_copy_returns_instance_with_same_properties(self):
        selection = TravelingSalespersonProblemGaSelectionTournament(tournament_size=5)

        copied = selection.copy()

        self.assertIsNot(selection, copied)
        self.assertEqual(copied.tournament_size, 5)

    def test_selection_requires_population(self):
        optimizer_stub = mocker.MagicMock()
        optimizer_stub.current_population = None
        selection = TravelingSalespersonProblemGaSelectionTournament()

        with self.assertRaises(AttributeError):
            selection.selection(optimizer_stub)

    def test_selection_requires_nonempty_population(self):
        optimizer_stub = mocker.MagicMock()
        optimizer_stub.current_population = []
        optimizer_stub.elite_count = 0
        selection = TravelingSalespersonProblemGaSelectionTournament()

        with self.assertRaises(AttributeError):
            selection.selection(optimizer_stub)

    def test_selection_keeps_elites_untouched(self):
        population = []
        for representation in [[0, 1, 3, 2], [0, 1, 2, 3], [0, 2, 1, 3],
                               [1, 0, 3, 2], [0, 3, 2, 1], [1, 3, 0, 2]]:
            solution = TravelingSalespersonProblemSolution()
            solution.init_from(representation, self.problem)
            solution.evaluate(self.problem)
            population.append(solution)
        optimizer_stub = mocker.MagicMock()
        optimizer_stub.current_population = population
        optimizer_stub.elite_count = 2
        selection = TravelingSalespersonProblemGaSelectionTournament(tournament_size=3)

        selection.selection(optimizer_stub)

        self.assertEqual(population[0].representation, [0, 1, 3, 2])
        self.assertEqual(population[1].representation, [0, 1, 2, 3])

    def test_selection_selects_members_of_population(self):
        population = []
        for representation in [[0, 1, 3, 2], [0, 1, 2, 3], [0, 2, 1, 3],
                               [1, 0, 3, 2], [0, 3, 2, 1], [1, 3, 0, 2]]:
            solution = TravelingSalespersonProblemSolution()
            solution.init_from(representation, self.problem)
            solution.evaluate(self.problem)
            population.append(solution)
        original_representations = [solution.representation.copy() for solution in population]
        optimizer_stub = mocker.MagicMock()
        optimizer_stub.current_population = population
        optimizer_stub.elite_count = 0
        selection = TravelingSalespersonProblemGaSelectionTournament(tournament_size=3)

        selection.selection(optimizer_stub)

        for solution in population:
            self.assertIn(solution.representation, original_representations)

    def test_selection_with_tournament_size_equal_to_population_returns_best(self):
        population = []
        for representation in [[0, 1, 2, 3], [0, 2, 1, 3], [0, 1, 3, 2], [1, 0, 3, 2]]:
            solution = TravelingSalespersonProblemSolution()
            solution.init_from(representation, self.problem)
            solution.evaluate(self.problem)
            population.append(solution)
        optimizer_stub = mocker.MagicMock()
        optimizer_stub.current_population = population
        optimizer_stub.elite_count = 0
        selection = TravelingSalespersonProblemGaSelectionTournament(tournament_size=4)

        # tournaments draw individuals with replacement, so a fixed seed makes
        # the drawing deterministic for the assertion
        seed(43434343)
        selection.selection(optimizer_stub)

        for solution in population:
            self.assertEqual(solution.objective_value, 23.0)


if __name__ == "__main__":
    unittest.main()
