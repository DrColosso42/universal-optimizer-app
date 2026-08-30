import unittest

from bitstring import BitArray

from opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem import (
    TravelingThiefProblem,
    TtpItem,
)
from opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem_solution import (
    TravelingThiefProblemSolution,
    TtpRepresentation,
)


def make_tiny_problem() -> TravelingThiefProblem:
    return TravelingThiefProblem(
        cities=[(0.0, 0.0), (10.0, 0.0), (10.0, 10.0)],
        items=[
            TtpItem(index=0, city=1, profit=100.0, weight=5.0),
            TtpItem(index=1, city=2, profit=50.0, weight=20.0),
        ],
        capacity=10.0,
        v_min=0.5,
        v_max=1.0,
        renting_rate=1.0,
    )


class TestTravelingThiefProblemSolution(unittest.TestCase):

    def test_initialize_instance_with_default_parameters(self):
        solution = TravelingThiefProblemSolution()

        self.assertIsNone(solution.fitness_value)
        self.assertIsNone(solution.objective_value)
        self.assertFalse(solution.is_feasible)

    def test_init_random_method_with_problem(self):
        problem = make_tiny_problem()
        solution = TravelingThiefProblemSolution()

        solution.init_random(problem)

        self.assertIsInstance(solution.representation, TtpRepresentation)
        self.assertEqual(len(solution.representation.tour), problem.n)
        self.assertEqual(sorted(solution.representation.tour), list(range(problem.n)))
        self.assertEqual(len(solution.representation.packing), problem.m)

    def test_init_random_raises_for_wrong_problem_type(self):
        solution = TravelingThiefProblemSolution()

        with self.assertRaises(TypeError):
            solution.init_random("not_a_problem")

    def test_init_from_method_with_representation_and_problem(self):
        problem = make_tiny_problem()
        solution = TravelingThiefProblemSolution()
        representation = TtpRepresentation([0, 1, 2], BitArray(bin="11"))

        solution.init_from(representation, problem)

        self.assertEqual(solution.representation.tour, [0, 1, 2])
        self.assertEqual(solution.representation.packing.bin, "11")

    def test_init_from_raises_for_invalid_type(self):
        problem = make_tiny_problem()
        solution = TravelingThiefProblemSolution()

        with self.assertRaises(TypeError):
            solution.init_from("not_a_representation", problem)

    def test_calculate_quality_directly_with_feasible_solution(self):
        problem = make_tiny_problem()
        solution = TravelingThiefProblemSolution()
        representation = TtpRepresentation([0, 1, 2], BitArray(bin="10"))

        quality = solution.calculate_quality_directly(representation, problem)

        self.assertTrue(quality.is_feasible)
        self.assertEqual(quality.fitness_value, quality.objective_value)

    def test_calculate_quality_directly_with_infeasible_solution(self):
        problem = make_tiny_problem()
        solution = TravelingThiefProblemSolution()
        representation = TtpRepresentation([0, 1, 2], BitArray(bin="11"))

        quality = solution.calculate_quality_directly(representation, problem)

        self.assertFalse(quality.is_feasible)
        self.assertEqual(quality.objective_value, float("-inf"))
        self.assertLess(quality.fitness_value, 0)

    def test_calculate_quality_directly_raises_for_invalid_representation_type(self):
        problem = make_tiny_problem()
        solution = TravelingThiefProblemSolution()

        with self.assertRaises(TypeError):
            solution.calculate_quality_directly("not_a_representation", problem)

    def test_calculate_quality_directly_raises_for_invalid_problem_type(self):
        solution = TravelingThiefProblemSolution()
        representation = TtpRepresentation([0, 1], BitArray(bin="1"))

        with self.assertRaises(TypeError):
            solution.calculate_quality_directly(representation, "not_a_problem")

    def test_copy_method_returns_deep_copy(self):
        problem = make_tiny_problem()
        solution = TravelingThiefProblemSolution()
        solution.init_from(TtpRepresentation([0, 1, 2], BitArray(bin="10")), problem)

        copied = solution.copy()
        copied.representation.tour[0] = 99

        self.assertIsNot(solution, copied)
        self.assertEqual(solution.representation.tour, [0, 1, 2])

    def test_argument_method_returns_correct_string_representation(self):
        solution = TravelingThiefProblemSolution()
        representation = TtpRepresentation([0, 1, 2], BitArray(bin="10"))

        argument = solution.argument(representation)

        self.assertEqual(argument, "tour=[0, 1, 2]|packing=10")

    def test_tour_cost_sums_distances_around_the_cycle(self):
        problem = make_tiny_problem()
        solution = TravelingThiefProblemSolution()

        cost = solution.tour_cost(problem, [0, 1, 2])

        expected = 10.0 + 10.0 + (10.0 * (2 ** 0.5))
        self.assertAlmostEqual(cost, expected)

    def test_greedy_packing_respects_capacity(self):
        problem = make_tiny_problem()
        solution = TravelingThiefProblemSolution()

        packing = solution.greedy_packing(problem, [0, 1, 2])

        total_weight = sum(item.weight for item in problem.items if packing[item.index])
        self.assertLessEqual(total_weight, problem.capacity)

    def test_pack_iterative_does_not_exceed_capacity(self):
        problem = make_tiny_problem()
        solution = TravelingThiefProblemSolution()

        packing = solution.pack_iterative(problem, [0, 1, 2], max_passes=3)

        total_weight = sum(item.weight for item in problem.items if packing[item.index])
        self.assertLessEqual(total_weight, problem.capacity)

    def test_representation_distance_directly_is_zero_for_rotated_tour(self):
        solution = TravelingThiefProblemSolution()
        representation_1 = TtpRepresentation([0, 1, 2, 3], BitArray(bin="00"))
        representation_2 = TtpRepresentation([1, 2, 3, 0], BitArray(bin="00"))

        distance = solution.representation_distance_directly(representation_1, representation_2)

        self.assertEqual(distance, 0.0)

    def test_representation_distance_directly_counts_packing_differences(self):
        solution = TravelingThiefProblemSolution()
        representation_1 = TtpRepresentation([0, 1], BitArray(bin="00"))
        representation_2 = TtpRepresentation([0, 1], BitArray(bin="11"))

        distance = solution.representation_distance_directly(representation_1, representation_2)

        self.assertEqual(distance, 2.0)


if __name__ == "__main__":
    unittest.main()
