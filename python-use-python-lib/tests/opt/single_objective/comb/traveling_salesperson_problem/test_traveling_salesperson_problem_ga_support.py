import unittest
import unittest.mock as mocker
from random import seed

from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem import (
    TravelingSalespersonProblem,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_solution import (
    TravelingSalespersonProblemSolution,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_support import (
    TravelingSalespersonProblemGaCrossoverSupportErx,
    TravelingSalespersonProblemGaMutationSupportInversion,
    _two_opt_sweep,
    _matrix_is_symmetric,
)

DISTANCES = [[0, 2, 9, 10], [2, 0, 6, 4], [9, 6, 0, 8], [10, 4, 8, 0]]


def build_optimizer_stub() -> mocker.MagicMock:
    """
    Optimizer stub used for unit testing of the GA supports, following the
    mocking convention of the existing support tests.
    """
    optimizer_stub = mocker.MagicMock()
    optimizer_stub.should_finish = mocker.Mock(return_value=False)
    optimizer_stub.write_output_values_if_needed = mocker.Mock(return_value=None)
    return optimizer_stub


def build_parent_solutions(problem: TravelingSalespersonProblem):
    parent_1 = TravelingSalespersonProblemSolution()
    parent_1.init_from([0, 1, 2, 3], problem)
    parent_1.evaluate(problem)
    parent_2 = TravelingSalespersonProblemSolution()
    parent_2.init_from([3, 2, 1, 0], problem)
    parent_2.evaluate(problem)
    return parent_1, parent_2


class TestTravelingSalespersonProblemGaCrossoverSupportErx(unittest.TestCase):

    def setUp(self):
        self.problem = TravelingSalespersonProblem.from_distance_matrix(
            distances=DISTANCES
        )
        seed(43434343)

    def test_initialize_instance_with_valid_probability(self):
        support = TravelingSalespersonProblemGaCrossoverSupportErx(
            crossover_probability=0.95
        )

        self.assertEqual(support.crossover_probability, 0.95)

    def test_copy_returns_instance_with_same_properties(self):
        support = TravelingSalespersonProblemGaCrossoverSupportErx(
            crossover_probability=0.9
        )

        copied = support.copy()

        self.assertIsNot(support, copied)
        self.assertEqual(copied.crossover_probability, 0.9)

    def test_crossover_produces_valid_permutations(self):
        support = TravelingSalespersonProblemGaCrossoverSupportErx(
            crossover_probability=1.0
        )
        optimizer_stub = build_optimizer_stub()

        for _ in range(20):
            parent_1, parent_2 = build_parent_solutions(self.problem)
            child_1 = parent_1.copy()
            child_2 = parent_2.copy()

            support.crossover(self.problem, parent_1, parent_2, child_1, child_2,
                    optimizer_stub)

            self.assertEqual(sorted(child_1.representation), [0, 1, 2, 3])
            self.assertEqual(sorted(child_2.representation), [0, 1, 2, 3])
            self.assertIsNotNone(child_1.objective_value)
            self.assertIsNotNone(child_2.objective_value)

    def test_crossover_evaluates_children(self):
        support = TravelingSalespersonProblemGaCrossoverSupportErx(
            crossover_probability=1.0
        )
        optimizer_stub = build_optimizer_stub()
        parent_1, parent_2 = build_parent_solutions(self.problem)
        child_1 = parent_1.copy()
        child_2 = parent_2.copy()
        child_1.objective_value = None
        child_2.objective_value = None

        support.crossover(self.problem, parent_1, parent_2, child_1, child_2,
                optimizer_stub)

        self.assertIsNotNone(child_1.objective_value)
        self.assertIsNotNone(child_2.objective_value)

    def test_crossover_without_probability_keeps_parents(self):
        support = TravelingSalespersonProblemGaCrossoverSupportErx(
            crossover_probability=0.0
        )
        optimizer_stub = build_optimizer_stub()
        parent_1, parent_2 = build_parent_solutions(self.problem)
        child_1 = parent_1.copy()
        child_2 = parent_2.copy()

        support.crossover(self.problem, parent_1, parent_2, child_1, child_2,
                optimizer_stub)

        self.assertEqual(child_1.representation, parent_1.representation)
        self.assertEqual(child_2.representation, parent_2.representation)

    def test_crossover_with_unevaluated_parents_copies_parents(self):
        support = TravelingSalespersonProblemGaCrossoverSupportErx(
            crossover_probability=1.0
        )
        optimizer_stub = build_optimizer_stub()
        parent_1 = TravelingSalespersonProblemSolution()
        parent_1.init_from([0, 1, 2, 3], self.problem)
        parent_2 = TravelingSalespersonProblemSolution()
        parent_2.init_from([3, 2, 1, 0], self.problem)
        child_1 = parent_1.copy()
        child_2 = parent_2.copy()

        support.crossover(self.problem, parent_1, parent_2, child_1, child_2,
                optimizer_stub)

        self.assertEqual(child_1.representation, parent_1.representation)
        self.assertEqual(child_2.representation, parent_2.representation)


class TestTravelingSalespersonProblemGaMutationSupportInversion(unittest.TestCase):

    def setUp(self):
        self.problem = TravelingSalespersonProblem.from_distance_matrix(
            distances=DISTANCES
        )
        seed(43434343)

    def test_initialize_instance_with_valid_probability(self):
        support = TravelingSalespersonProblemGaMutationSupportInversion(
            mutation_probability=0.05
        )

        self.assertEqual(support.mutation_probability, 0.05)

    def test_copy_returns_instance_with_same_properties(self):
        support = TravelingSalespersonProblemGaMutationSupportInversion(
            mutation_probability=0.1
        )

        copied = support.copy()

        self.assertIsNot(support, copied)
        self.assertEqual(copied.mutation_probability, 0.1)

    def test_mutation_keeps_permutation_valid(self):
        support = TravelingSalespersonProblemGaMutationSupportInversion(
            mutation_probability=0.5
        )
        optimizer_stub = build_optimizer_stub()

        for _ in range(20):
            solution = TravelingSalespersonProblemSolution()
            solution.init_from([0, 1, 2, 3], self.problem)
            solution.evaluate(self.problem)

            support.mutation(self.problem, solution, optimizer_stub)

            self.assertEqual(sorted(solution.representation), [0, 1, 2, 3])

    def test_mutation_evaluates_mutated_individual(self):
        support = TravelingSalespersonProblemGaMutationSupportInversion(
            mutation_probability=0.5
        )
        optimizer_stub = build_optimizer_stub()
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 2, 1, 3], self.problem)
        solution.evaluate(self.problem)

        support.mutation(self.problem, solution, optimizer_stub)

        self.assertIsNotNone(solution.objective_value)
        self.assertIsNotNone(solution.fitness_value)

    def test_mutation_without_representation_does_nothing(self):
        support = TravelingSalespersonProblemGaMutationSupportInversion(
            mutation_probability=0.5
        )
        optimizer_stub = build_optimizer_stub()
        solution = TravelingSalespersonProblemSolution()

        support.mutation(self.problem, solution, optimizer_stub)

        self.assertIsNone(solution.representation)

    def test_mutation_without_changes_skips_evaluation(self):
        support = TravelingSalespersonProblemGaMutationSupportInversion(
            mutation_probability=0.0, apply_two_opt=False
        )
        optimizer_stub = build_optimizer_stub()
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 1, 3, 2], self.problem)
        solution.evaluate(self.problem)
        objective_before = solution.objective_value

        support.mutation(self.problem, solution, optimizer_stub)

        self.assertEqual(solution.objective_value, objective_before)


class TestTwoOptSweep(unittest.TestCase):
    """Tests of the delta evaluated 2-opt sweep, applied to each offspring of
    the memetic GA."""

    def setUp(self):
        self.problem = TravelingSalespersonProblem.from_distance_matrix(
            distances=DISTANCES
        )

    def test_two_opt_improves_crossed_tour(self):
        representation = [0, 2, 1, 3]

        changed = _two_opt_sweep(self.problem.distances, representation, True)

        self.assertTrue(changed)
        self.assertEqual(sorted(representation), [0, 1, 2, 3])
        self.assertLess(
            self.problem.distance(representation[0], representation[1])
            + self.problem.distance(representation[1], representation[2])
            + self.problem.distance(representation[2], representation[3])
            + self.problem.distance(representation[3], representation[0]),
            29,
        )

    def test_two_opt_at_local_optimum_changes_nothing(self):
        representation = [0, 1, 3, 2]

        changed = _two_opt_sweep(self.problem.distances, representation, True)

        self.assertFalse(changed)
        self.assertEqual(representation, [0, 1, 3, 2])

    def test_matrix_is_symmetric_detection(self):
        self.assertTrue(_matrix_is_symmetric(DISTANCES))
        self.assertFalse(_matrix_is_symmetric([[0, 1, 5], [1, 0, 2], [2, 5, 0]]))


class TestTravelingSalespersonProblemGaSupportStringRepresentations(unittest.TestCase):
    """Tests of the string representation methods of the GA supports."""

    def test_crossover_supports_string_representations(self):
        supports = [
            TravelingSalespersonProblemGaCrossoverSupportErx(crossover_probability=0.95),
        ]

        for support in supports:
            with self.subTest(support=type(support).__name__):
                self.assertIn(type(support).__name__, str(support))
                self.assertIn(type(support).__name__, repr(support))
                self.assertIn(type(support).__name__, format(support))
                self.assertIn(type(support).__name__, support.string_rep("|"))

    def test_mutation_supports_string_representations(self):
        supports = [
            TravelingSalespersonProblemGaMutationSupportInversion(mutation_probability=0.05),
        ]

        for support in supports:
            with self.subTest(support=type(support).__name__):
                self.assertIn(type(support).__name__, str(support))
                self.assertIn(type(support).__name__, repr(support))
                self.assertIn(type(support).__name__, format(support))
                self.assertIn(type(support).__name__, support.string_rep("|"))


if __name__ == "__main__":
    unittest.main()
