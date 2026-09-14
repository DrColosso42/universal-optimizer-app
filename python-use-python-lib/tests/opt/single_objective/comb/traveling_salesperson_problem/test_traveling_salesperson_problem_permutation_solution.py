import unittest

from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem import (
    TravelingSalespersonProblem,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_permutation_solution import (
    TravelingSalespersonProblemPermutationSolution,
)


class TestTravelingSalespersonProblemPermutationSolution(unittest.TestCase):

    def test_initialize_instance_with_default_parameters(self):
        solution = TravelingSalespersonProblemPermutationSolution()

        self.assertIsNone(solution.fitness_value)
        self.assertIsNone(solution.fitness_values)
        self.assertIsNone(solution.objective_value)
        self.assertIsNone(solution.objective_values)
        self.assertFalse(solution.is_feasible)

    def test_init_random_method_with_problem(self):
        problem = TravelingSalespersonProblem([
            [0, 1, 2, 3],
            [1, 0, 4, 5],
            [2, 4, 0, 6],
            [3, 5, 6, 0],
        ])
        solution = TravelingSalespersonProblemPermutationSolution()

        solution.init_random(problem)

        self.assertIsInstance(solution.representation, list)
        self.assertEqual(sorted(solution.representation), list(range(problem.dimension)))

    def test_init_random_raises_when_problem_has_no_dimension(self):
        solution = TravelingSalespersonProblemPermutationSolution()

        class DummyProblem:
            dimension = None

        with self.assertRaises(ValueError):
            solution.init_random(DummyProblem())

    def test_init_from_method_with_valid_permutation(self):
        problem = TravelingSalespersonProblem([
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0],
        ])
        solution = TravelingSalespersonProblemPermutationSolution()

        solution.init_from([2, 0, 1], problem)

        self.assertEqual(solution.representation, [2, 0, 1])

    def test_init_from_raises_for_invalid_type(self):
        problem = TravelingSalespersonProblem([
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0],
        ])
        solution = TravelingSalespersonProblemPermutationSolution()

        with self.assertRaises(TypeError):
            solution.init_from("012", problem)

    def test_init_from_raises_for_non_permutation(self):
        problem = TravelingSalespersonProblem([
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0],
        ])
        solution = TravelingSalespersonProblemPermutationSolution()

        with self.assertRaises(ValueError):
            solution.init_from([0, 0, 1], problem)

    def test_tour_length_closes_the_cycle(self):
        problem = TravelingSalespersonProblem([
            [0, 1, 2, 3],
            [1, 0, 4, 5],
            [2, 4, 0, 6],
            [3, 5, 6, 0],
        ])
        solution = TravelingSalespersonProblemPermutationSolution()

        length = solution.tour_length([0, 1, 2, 3], problem)

        self.assertEqual(length, 14)

    def test_calculate_quality_directly_is_always_feasible(self):
        problem = TravelingSalespersonProblem([
            [0, 1, 2, 3],
            [1, 0, 4, 5],
            [2, 4, 0, 6],
            [3, 5, 6, 0],
        ])
        solution = TravelingSalespersonProblemPermutationSolution()

        quality = solution.calculate_quality_directly([0, 1, 2, 3], problem)

        self.assertEqual(quality.objective_value, 14)
        self.assertEqual(quality.fitness_value, -14)
        self.assertTrue(quality.is_feasible)

    def test_calculate_quality_directly_raises_for_invalid_representation_type(self):
        problem = TravelingSalespersonProblem([
            [0, 1],
            [1, 0],
        ])
        solution = TravelingSalespersonProblemPermutationSolution()

        with self.assertRaises(TypeError):
            solution.calculate_quality_directly("01", problem)

    def test_calculate_quality_directly_raises_for_invalid_problem_type(self):
        solution = TravelingSalespersonProblemPermutationSolution()

        with self.assertRaises(TypeError):
            solution.calculate_quality_directly([0, 1], "not_a_problem")

    def test_calculate_quality_directly_raises_for_wrong_length(self):
        problem = TravelingSalespersonProblem([
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0],
        ])
        solution = TravelingSalespersonProblemPermutationSolution()

        with self.assertRaises(ValueError):
            solution.calculate_quality_directly([0, 1], problem)

    def test_native_representation_parses_bracketed_list(self):
        solution = TravelingSalespersonProblemPermutationSolution()

        native_representation = solution.native_representation("[0, 3, 1, 2]")

        self.assertEqual(native_representation, [0, 3, 1, 2])

    def test_native_representation_raises_for_invalid_type(self):
        solution = TravelingSalespersonProblemPermutationSolution()

        with self.assertRaises(TypeError):
            solution.native_representation([0, 1, 2])

    def test_representation_distance_directly(self):
        solution = TravelingSalespersonProblemPermutationSolution()

        distance = solution.representation_distance_directly([0, 1, 2, 3], [0, 2, 1, 3])

        self.assertEqual(distance, 2)

    def test_representation_distance_directly_raises_for_invalid_first_type(self):
        solution = TravelingSalespersonProblemPermutationSolution()

        with self.assertRaises(TypeError):
            solution.representation_distance_directly("0123", [0, 1, 2, 3])

    def test_representation_distance_directly_raises_for_invalid_second_type(self):
        solution = TravelingSalespersonProblemPermutationSolution()

        with self.assertRaises(TypeError):
            solution.representation_distance_directly([0, 1, 2, 3], "0123")

    def test_representation_distance_directly_raises_value_error(self):
        solution = TravelingSalespersonProblemPermutationSolution()

        with self.assertRaises(ValueError):
            solution.representation_distance_directly([0, 1, 2], [0, 1])

    def test_copy_method_returns_deep_copy(self):
        problem = TravelingSalespersonProblem([
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0],
        ])
        solution = TravelingSalespersonProblemPermutationSolution()
        solution.init_from([2, 0, 1], problem)

        copied = solution.copy()

        self.assertIsNot(solution, copied)
        self.assertEqual(solution.representation, copied.representation)

        copied.representation[0] = 99
        self.assertEqual(solution.representation[0], 2)

    def test_argument_method_returns_copy_of_representation(self):
        solution = TravelingSalespersonProblemPermutationSolution()

        argument = solution.argument([2, 0, 1])

        self.assertEqual(argument, [2, 0, 1])


if __name__ == "__main__":
    unittest.main()
