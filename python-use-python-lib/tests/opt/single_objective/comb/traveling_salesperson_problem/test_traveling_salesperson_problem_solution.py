import unittest

from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem import (
    TravelingSalespersonProblem,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_solution import (
    TravelingSalespersonProblemSolution,
)

DISTANCES = [[0, 2, 9, 10], [2, 0, 6, 4], [9, 6, 0, 8], [10, 4, 8, 0]]


class TestTravelingSalespersonProblemSolution(unittest.TestCase):

    def setUp(self):
        self.problem = TravelingSalespersonProblem.from_distance_matrix(
            distances=DISTANCES
        )

    def test_initialize_instance_with_default_parameters(self):
        solution = TravelingSalespersonProblemSolution()

        self.assertIsNone(solution.representation)
        self.assertIsNone(solution.fitness_value)
        self.assertIsNone(solution.objective_value)
        self.assertFalse(solution.is_feasible)
        self.assertTrue(solution.is_minimization)

    def test_random_seed_type_error(self):
        with self.assertRaises(TypeError):
            TravelingSalespersonProblemSolution(random_seed="43434343")

    def test_copy_returns_independent_copy(self):
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 1, 2, 3], self.problem)

        copied = solution.copy()

        self.assertIsNot(solution, copied)
        self.assertEqual(copied.representation, [0, 1, 2, 3])

        copied.representation[0] = 3
        self.assertEqual(solution.representation[0], 0)

    def test_argument_returns_city_indexes_separated_by_dash(self):
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 1, 2, 3], self.problem)

        self.assertEqual(solution.argument(solution.representation), "0-1-2-3")

    def test_init_random_creates_valid_permutation(self):
        solution = TravelingSalespersonProblemSolution()

        solution.init_random(self.problem)

        self.assertEqual(sorted(solution.representation), [0, 1, 2, 3])

    def test_init_random_with_invalid_problem_type(self):
        solution = TravelingSalespersonProblemSolution()

        with self.assertRaises(TypeError):
            solution.init_random("problem")

    def test_init_from_with_valid_representation(self):
        solution = TravelingSalespersonProblemSolution()

        solution.init_from([3, 2, 1, 0], self.problem)

        self.assertEqual(solution.representation, [3, 2, 1, 0])

    def test_init_from_with_invalid_type(self):
        solution = TravelingSalespersonProblemSolution()

        with self.assertRaises(TypeError):
            solution.init_from("0-1-2-3", self.problem)

    def test_init_from_with_empty_representation(self):
        solution = TravelingSalespersonProblemSolution()

        with self.assertRaises(ValueError):
            solution.init_from([], self.problem)

    def test_init_from_with_non_integer_cities(self):
        solution = TravelingSalespersonProblemSolution()

        with self.assertRaises(ValueError):
            solution.init_from([0, "1", 2, 3], self.problem)

    def test_evaluate_computes_tour_length(self):
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 1, 2, 3], self.problem)

        solution.evaluate(self.problem)

        # tour 0 -> 1 -> 2 -> 3 -> 0 has length 2 + 6 + 8 + 10 = 26
        self.assertEqual(solution.objective_value, 26.0)
        self.assertEqual(solution.fitness_value, -26.0)
        self.assertTrue(solution.is_feasible)

    def test_evaluate_prefers_shorter_tour(self):
        shorter = TravelingSalespersonProblemSolution()
        shorter.init_from([0, 1, 3, 2], self.problem)
        shorter.evaluate(self.problem)

        longer = TravelingSalespersonProblemSolution()
        longer.init_from([0, 1, 2, 3], self.problem)
        longer.evaluate(self.problem)

        # tour 0 -> 1 -> 3 -> 2 -> 0 has length 2 + 4 + 8 + 9 = 23
        self.assertEqual(shorter.objective_value, 23.0)
        self.assertTrue(shorter.is_better(longer, self.problem))

    def test_evaluate_marks_non_permutation_as_infeasible(self):
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 0, 1, 1], self.problem)

        solution.evaluate(self.problem)

        self.assertFalse(solution.is_feasible)
        self.assertEqual(solution.objective_value, float("-inf"))

    def test_evaluate_with_invalid_representation_length(self):
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 1, 2], self.problem)

        with self.assertRaises(ValueError):
            solution.evaluate(self.problem)

    def test_native_representation_from_string(self):
        solution = TravelingSalespersonProblemSolution()

        representation = solution.native_representation("0-1-2-3")

        self.assertEqual(representation, [0, 1, 2, 3])

    def test_native_representation_with_invalid_type(self):
        solution = TravelingSalespersonProblemSolution()

        with self.assertRaises(TypeError):
            solution.native_representation([0, 1, 2, 3])

    def test_native_representation_with_invalid_content(self):
        solution = TravelingSalespersonProblemSolution()

        with self.assertRaises(ValueError):
            solution.native_representation("0-1-x-3")

    def test_representation_distance_is_zero_for_rotation(self):
        solution = TravelingSalespersonProblemSolution()

        distance = solution.representation_distance_directly(
            [0, 1, 2, 3], [1, 2, 3, 0]
        )

        self.assertEqual(distance, 0.0)

    def test_representation_distance_is_zero_for_reflection(self):
        solution = TravelingSalespersonProblemSolution()

        distance = solution.representation_distance_directly(
            [0, 1, 2, 3], [0, 3, 2, 1]
        )

        self.assertEqual(distance, 0.0)

    def test_representation_distance_counts_differing_edges(self):
        solution = TravelingSalespersonProblemSolution()

        distance = solution.representation_distance_directly(
            [0, 1, 2, 3], [0, 1, 3, 2]
        )

        # edges {0-1, 1-2, 2-3, 3-0} vs {0-1, 1-3, 3-2, 2-0}: 4 differing edges
        self.assertEqual(distance, 4.0)

    def test_representation_distance_with_different_lengths(self):
        solution = TravelingSalespersonProblemSolution()

        with self.assertRaises(ValueError):
            solution.representation_distance_directly([0, 1, 2, 3], [0, 1, 2])


if __name__ == "__main__":
    unittest.main()
