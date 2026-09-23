import unittest
import unittest.mock as mocker

from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem import (
    TravelingSalespersonProblem,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_solution import (
    TravelingSalespersonProblemSolution,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_vns_support import (
    TravelingSalespersonProblemVnsShakingSupport,
    TravelingSalespersonProblemVnsLocalSearchSupportDelta,
)

DISTANCES = [[0, 2, 9, 10], [2, 0, 6, 4], [9, 6, 0, 8], [10, 4, 8, 0]]


def build_optimizer_stub(k_min: int, k_max: int) -> mocker.MagicMock:
    """
    Optimizer stub used for unit testing of the VNS supports, following the
    mocking convention of the existing support tests.
    """
    optimizer_stub = mocker.MagicMock()
    optimizer_stub.should_finish = mocker.Mock(return_value=False)
    type(optimizer_stub).evaluation = mocker.PropertyMock(return_value=0)
    optimizer_stub.write_output_values_if_needed = mocker.Mock(return_value=None)
    optimizer_stub.k_min = k_min
    optimizer_stub.k_max = k_max
    # the shaking support reads the incumbent from the optimizer
    optimizer_stub.best_solution = mocker.MagicMock()
    optimizer_stub.best_solution.representation = [0, 1, 2, 3]
    optimizer_stub.best_solution.objective_value = 29.0
    optimizer_stub.best_solution.fitness_value = -29.0
    return optimizer_stub


class TestTravelingSalespersonProblemVnsShakingSupport(unittest.TestCase):

    def setUp(self):
        self.problem = TravelingSalespersonProblem.from_distance_matrix(
            distances=DISTANCES
        )

    def test_initialize_instance_with_valid_dimension(self):
        support = TravelingSalespersonProblemVnsShakingSupport(dimension=4)

        self.assertEqual(support.dimension, 4)

    def test_dimension_must_exist(self):
        with self.assertRaises(ValueError):
            TravelingSalespersonProblemVnsShakingSupport(dimension=None)

    def test_dimension_must_be_int(self):
        with self.assertRaises(TypeError):
            TravelingSalespersonProblemVnsShakingSupport(dimension="4")

    def test_copy_returns_instance_with_same_properties(self):
        support = TravelingSalespersonProblemVnsShakingSupport(dimension=4)

        copied = support.copy()

        self.assertIsNot(support, copied)
        self.assertEqual(copied.dimension, 4)

    def test_shaking_keeps_permutation_valid(self):
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 1, 2, 3], self.problem)
        support = TravelingSalespersonProblemVnsShakingSupport(dimension=4)
        optimizer_stub = build_optimizer_stub(k_min=1, k_max=3)

        result = support.shaking(k=1, problem=self.problem,
                solution=solution, optimizer=optimizer_stub)

        self.assertTrue(result)
        self.assertEqual(sorted(solution.representation), [0, 1, 2, 3])

    def test_shaking_changes_starting_tour(self):
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 1, 2, 3], self.problem)
        support = TravelingSalespersonProblemVnsShakingSupport(dimension=4)
        optimizer_stub = build_optimizer_stub(k_min=1, k_max=3)

        support.shaking(k=2, problem=self.problem,
                solution=solution, optimizer=optimizer_stub)

        self.assertNotEqual(solution.representation, [0, 1, 2, 3])

    def test_shaking_rejects_k_out_of_range(self):
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 1, 2, 3], self.problem)
        support = TravelingSalespersonProblemVnsShakingSupport(dimension=4)
        optimizer_stub = build_optimizer_stub(k_min=1, k_max=3)

        result = support.shaking(k=7, problem=self.problem,
                solution=solution, optimizer=optimizer_stub)

        self.assertFalse(result)

    def test_shaking_evaluates_shaken_solution(self):
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 1, 2, 3], self.problem)
        support = TravelingSalespersonProblemVnsShakingSupport(dimension=4)
        optimizer_stub = build_optimizer_stub(k_min=1, k_max=3)

        support.shaking(k=1, problem=self.problem,
                solution=solution, optimizer=optimizer_stub)

        self.assertIsNotNone(solution.fitness_value)
        optimizer_stub.write_output_values_if_needed.assert_any_call(
            "before_evaluation", "b_e"
        )
        optimizer_stub.write_output_values_if_needed.assert_any_call(
            "after_evaluation", "a_e"
        )



class TestTravelingSalespersonProblemVnsLocalSearchSupportDelta(unittest.TestCase):

    def setUp(self):
        self.problem = TravelingSalespersonProblem.from_distance_matrix(
            distances=DISTANCES
        )

    def test_initialize_instance_with_valid_dimension(self):
        support = TravelingSalespersonProblemVnsLocalSearchSupportDelta(dimension=4)

        self.assertEqual(support.dimension, 4)

    def test_dimension_must_exist(self):
        with self.assertRaises(ValueError):
            TravelingSalespersonProblemVnsLocalSearchSupportDelta(dimension=None)

    def test_dimension_must_be_int(self):
        with self.assertRaises(TypeError):
            TravelingSalespersonProblemVnsLocalSearchSupportDelta(dimension="4")

    def test_copy_returns_instance_with_same_properties(self):
        support = TravelingSalespersonProblemVnsLocalSearchSupportDelta(dimension=4)

        copied = support.copy()

        self.assertIsNot(support, copied)
        self.assertEqual(copied.dimension, 4)

    def test_local_search_improves_suboptimal_tour_to_optimum(self):
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 2, 1, 3], self.problem)
        solution.evaluate(self.problem)
        support = TravelingSalespersonProblemVnsLocalSearchSupportDelta(dimension=4)
        optimizer_stub = build_optimizer_stub(k_min=1, k_max=3)

        result = support.local_search(k=1, problem=self.problem,
                solution=solution, optimizer=optimizer_stub)

        self.assertTrue(result)
        # optimal tour 0 -> 1 -> 3 -> 2 -> 0 has length 23
        self.assertEqual(solution.objective_value, 23.0)

    def test_local_search_returns_false_at_local_optimum(self):
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 1, 3, 2], self.problem)
        solution.evaluate(self.problem)
        support = TravelingSalespersonProblemVnsLocalSearchSupportDelta(dimension=4)
        optimizer_stub = build_optimizer_stub(k_min=1, k_max=3)

        result = support.local_search(k=1, problem=self.problem,
                solution=solution, optimizer=optimizer_stub)

        self.assertFalse(result)
        self.assertEqual(solution.objective_value, 23.0)

    def test_local_search_rejects_k_out_of_range(self):
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 1, 2, 3], self.problem)
        solution.evaluate(self.problem)
        support = TravelingSalespersonProblemVnsLocalSearchSupportDelta(dimension=4)
        optimizer_stub = build_optimizer_stub(k_min=1, k_max=3)

        self.assertFalse(support.local_search(k=0, problem=self.problem,
                solution=solution, optimizer=optimizer_stub))
        self.assertFalse(support.local_search(k=4, problem=self.problem,
                solution=solution, optimizer=optimizer_stub))

    def test_local_search_rejects_block_not_shorter_than_tour(self):
        solution = TravelingSalespersonProblemSolution()
        solution.init_from([0, 1, 2, 3], self.problem)
        solution.evaluate(self.problem)
        support = TravelingSalespersonProblemVnsLocalSearchSupportDelta(dimension=4)
        optimizer_stub = build_optimizer_stub(k_min=1, k_max=5)

        self.assertFalse(support.local_search(k=4, problem=self.problem,
                solution=solution, optimizer=optimizer_stub))


if __name__ == "__main__":
    unittest.main()
