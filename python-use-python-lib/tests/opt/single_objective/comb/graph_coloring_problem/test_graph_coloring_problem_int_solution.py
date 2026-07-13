import unittest

from opt.single_objective.comb.graph_coloring_problem.graph_coloring_problem import (
    GraphColoringProblem,
)
from opt.single_objective.comb.graph_coloring_problem.graph_coloring_problem_int_solution import (
    GraphColoringProblemIntSolution,
)


class TestGraphColoringProblemIntSolution(unittest.TestCase):

    def test_initialize_instance_with_valid_parameters(self):
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        self.assertEqual(solution.colors_count, 3)
        self.assertEqual(solution.bits_per_color, 2)
        self.assertIsNone(solution.fitness_value)
        self.assertIsNone(solution.objective_value)
        self.assertFalse(solution.is_feasible)
        self.assertTrue(solution.is_minimization)

    def test_bits_per_color_for_power_of_two(self):
        solution = GraphColoringProblemIntSolution(
            colors_count=4
        )

        self.assertEqual(solution.bits_per_color, 2)

    def test_bits_per_color_for_non_power_of_two(self):
        solution = GraphColoringProblemIntSolution(
            colors_count=5
        )

        self.assertEqual(solution.bits_per_color, 3)

    def test_colors_count_type_error(self):
        with self.assertRaises(TypeError):
            GraphColoringProblemIntSolution(
                colors_count="3"
            )

    def test_colors_count_must_be_positive(self):
        with self.assertRaises(ValueError):
            GraphColoringProblemIntSolution(
                colors_count=0
            )

    def test_random_seed_type_error(self):
        with self.assertRaises(TypeError):
            GraphColoringProblemIntSolution(
                colors_count=3,
                random_seed="123",
            )

    def test_init_random_method_with_problem(self):
        problem = GraphColoringProblem(
            4,
            [(0, 1), (1, 2)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=4
        )

        solution.init_random(problem)

        self.assertIsInstance(
            solution.representation,
            int,
        )
        self.assertGreaterEqual(
            solution.representation,
            0,
        )

        colors = solution.decode_coloring(
            representation=solution.representation,
            number_of_vertices=4,
        )

        self.assertEqual(len(colors), 4)

        for color in colors:
            self.assertGreaterEqual(color, 0)
            self.assertLess(color, 4)

    def test_init_random_raises_for_invalid_problem_type(self):
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        with self.assertRaises(TypeError):
            solution.init_random("not_a_problem")

    def test_init_random_raises_when_color_count_does_not_match(
        self,
    ):
        problem = GraphColoringProblem(
            4,
            [(0, 1)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        with self.assertRaises(ValueError):
            solution.init_random(problem)

    def test_init_from_method_with_integer_representation(self):
        problem = GraphColoringProblem(
            4,
            [(0, 1)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=4
        )

        solution.init_from(5, problem)

        self.assertEqual(solution.representation, 5)

    def test_init_from_raises_for_invalid_type(self):
        problem = GraphColoringProblem(
            4,
            [(0, 1)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=4
        )

        with self.assertRaises(TypeError):
            solution.init_from("5", problem)

    def test_init_from_raises_for_negative_representation(self):
        problem = GraphColoringProblem(
            4,
            [(0, 1)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=4
        )

        with self.assertRaises(ValueError):
            solution.init_from(-1, problem)

    def test_init_from_raises_for_invalid_problem_type(self):
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        with self.assertRaises(TypeError):
            solution.init_from(5, "not_a_problem")

    def test_init_from_raises_when_color_count_does_not_match(
        self,
    ):
        problem = GraphColoringProblem(
            4,
            [(0, 1)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        with self.assertRaises(ValueError):
            solution.init_from(5, problem)

    def test_decode_color(self):
        solution = GraphColoringProblemIntSolution(
            colors_count=4
        )

        representation = 0
        representation |= 1 << 0
        representation |= 2 << 2
        representation |= 3 << 4

        self.assertEqual(
            solution.decode_color(representation, 0),
            1,
        )
        self.assertEqual(
            solution.decode_color(representation, 1),
            2,
        )
        self.assertEqual(
            solution.decode_color(representation, 2),
            3,
        )

    def test_decode_coloring(self):
        solution = GraphColoringProblemIntSolution(
            colors_count=4
        )

        representation = 0
        representation |= 1 << 0
        representation |= 2 << 2
        representation |= 3 << 4
        representation |= 0 << 6

        coloring = solution.decode_coloring(
            representation=representation,
            number_of_vertices=4,
        )

        self.assertEqual(coloring, [1, 2, 3, 0])

    def test_decode_coloring_preserves_trailing_zero_colors(
        self,
    ):
        solution = GraphColoringProblemIntSolution(
            colors_count=4
        )

        representation = 1

        coloring = solution.decode_coloring(
            representation=representation,
            number_of_vertices=4,
        )

        self.assertEqual(coloring, [1, 0, 0, 0])

    def test_decode_coloring_raises_for_invalid_representation(
        self,
    ):
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        with self.assertRaises(TypeError):
            solution.decode_coloring(
                representation="5",
                number_of_vertices=3,
            )

    def test_decode_coloring_raises_for_invalid_vertex_count_type(
        self,
    ):
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        with self.assertRaises(TypeError):
            solution.decode_coloring(
                representation=5,
                number_of_vertices="3",
            )

    def test_decode_coloring_requires_positive_vertex_count(
        self,
    ):
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        with self.assertRaises(ValueError):
            solution.decode_coloring(
                representation=5,
                number_of_vertices=0,
            )

    def test_used_colors_count(self):
        problem = GraphColoringProblem(
            4,
            [(0, 1)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=4
        )

        representation = 0
        representation |= 0 << 0
        representation |= 1 << 2
        representation |= 0 << 4
        representation |= 2 << 6

        used_colors = solution.used_colors_count(
            representation=representation,
            problem=problem,
        )

        self.assertEqual(used_colors, 3)

    def test_used_colors_count_ignores_invalid_colors(self):
        problem = GraphColoringProblem(
            3,
            [],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        # Za tri boje koriste se dva bita.
        # Vrednost 3 je zato moguća u zapisu, ali nije validna boja.
        representation = 0
        representation |= 0 << 0
        representation |= 1 << 2
        representation |= 3 << 4

        used_colors = solution.used_colors_count(
            representation=representation,
            problem=problem,
        )

        self.assertEqual(used_colors, 2)

    def test_calculate_quality_with_feasible_coloring(self):
        problem = GraphColoringProblem(
            3,
            [(0, 1), (1, 2)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        # Bojenje: [0, 1, 0].
        # Za svaku boju se koriste dva bita.
        representation = 0
        representation |= 0 << 0
        representation |= 1 << 2
        representation |= 0 << 4

        quality = solution.calculate_quality_directly(
            representation,
            problem,
        )

        self.assertEqual(
            quality.objective_value,
            2.0,
        )
        self.assertEqual(
            quality.fitness_value,
            -2.0,
        )
        self.assertTrue(quality.is_feasible)

    def test_calculate_quality_with_conflicts(self):
        problem = GraphColoringProblem(
            3,
            [(0, 1), (1, 2)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        # Bojenje [0, 0, 0] ima dva konflikta
        # i koristi jednu boju.
        representation = 0

        quality = solution.calculate_quality_directly(
            representation,
            problem,
        )

        self.assertEqual(
            quality.objective_value,
            2001.0,
        )
        self.assertEqual(
            quality.fitness_value,
            -2001.0,
        )
        self.assertFalse(quality.is_feasible)

    def test_calculate_quality_with_invalid_color(self):
        problem = GraphColoringProblem(
            3,
            [],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        # Bojenje [0, 1, 3].
        # Boja 3 nije validna jer su dozvoljene boje 0, 1 i 2.
        representation = 0
        representation |= 0 << 0
        representation |= 1 << 2
        representation |= 3 << 4

        quality = solution.calculate_quality_directly(
            representation,
            problem,
        )

        self.assertEqual(
            quality.objective_value,
            1000002.0,
        )
        self.assertEqual(
            quality.fitness_value,
            -1000002.0,
        )
        self.assertFalse(quality.is_feasible)

    def test_invalid_color_and_conflict_are_both_penalized(
        self,
    ):
        problem = GraphColoringProblem(
            3,
            [(1, 2)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        # Bojenje [0, 3, 3]:
        # - dve nevalidne boje,
        # - jedan konflikt,
        # - jedna validna korišćena boja.
        representation = 0
        representation |= 0 << 0
        representation |= 3 << 2
        representation |= 3 << 4

        quality = solution.calculate_quality_directly(
            representation,
            problem,
        )

        self.assertEqual(
            quality.objective_value,
            2001001.0,
        )
        self.assertFalse(quality.is_feasible)

    def test_quality_prefers_fewer_used_colors(self):
        problem = GraphColoringProblem(
            4,
            [(0, 1), (1, 2), (2, 3)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=4
        )

        # Validno bojenje sa dve boje: [0, 1, 0, 1].
        two_color_representation = 0
        two_color_representation |= 0 << 0
        two_color_representation |= 1 << 2
        two_color_representation |= 0 << 4
        two_color_representation |= 1 << 6

        # Validno bojenje sa četiri boje: [0, 1, 2, 3].
        four_color_representation = 0
        four_color_representation |= 0 << 0
        four_color_representation |= 1 << 2
        four_color_representation |= 2 << 4
        four_color_representation |= 3 << 6

        two_color_quality = (
            solution.calculate_quality_directly(
                two_color_representation,
                problem,
            )
        )
        four_color_quality = (
            solution.calculate_quality_directly(
                four_color_representation,
                problem,
            )
        )

        self.assertTrue(two_color_quality.is_feasible)
        self.assertTrue(four_color_quality.is_feasible)
        self.assertEqual(
            two_color_quality.objective_value,
            2.0,
        )
        self.assertEqual(
            four_color_quality.objective_value,
            4.0,
        )
        self.assertLess(
            two_color_quality.objective_value,
            four_color_quality.objective_value,
        )

    def test_calculate_quality_raises_for_invalid_representation_type(
        self,
    ):
        problem = GraphColoringProblem(
            3,
            [(0, 1)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        with self.assertRaises(TypeError):
            solution.calculate_quality_directly(
                "0",
                problem,
            )

    def test_calculate_quality_raises_for_invalid_problem_type(
        self,
    ):
        solution = GraphColoringProblemIntSolution(
            colors_count=2
        )

        with self.assertRaises(TypeError):
            solution.calculate_quality_directly(
                0,
                "not_a_problem",
            )

    def test_calculate_quality_raises_when_color_count_does_not_match(
        self,
    ):
        problem = GraphColoringProblem(
            4,
            [(0, 1)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        with self.assertRaises(ValueError):
            solution.calculate_quality_directly(
                0,
                problem,
            )

    def test_native_representation_method_with_string(self):
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        self.assertEqual(
            solution.native_representation("12"),
            12,
        )

    def test_native_representation_raises_for_invalid_type(self):
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        with self.assertRaises(TypeError):
            solution.native_representation(12)

    def test_representation_distance_directly(self):
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        distance = (
            solution.representation_distance_directly(
                "5",
                "7",
            )
        )

        self.assertEqual(distance, 1)

    def test_representation_distance_rejects_invalid_first_code(
        self,
    ):
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        with self.assertRaises(TypeError):
            solution.representation_distance_directly(
                5,
                "7",
            )

    def test_representation_distance_rejects_invalid_second_code(
        self,
    ):
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        with self.assertRaises(TypeError):
            solution.representation_distance_directly(
                "5",
                7,
            )

    def test_copy_method_returns_independent_copy(self):
        problem = GraphColoringProblem(
            3,
            [(0, 1)],
        )
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )
        solution.init_from(5, problem)

        copied = solution.copy()

        self.assertIsNot(solution, copied)
        self.assertEqual(
            solution.representation,
            copied.representation,
        )
        self.assertEqual(
            solution.colors_count,
            copied.colors_count,
        )
        self.assertEqual(
            solution.bits_per_color,
            copied.bits_per_color,
        )

        copied.representation = 10

        self.assertEqual(solution.representation, 5)

    def test_value_returns_fitness_value(self):
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )
        solution.fitness_value = -2.0

        self.assertEqual(solution.value, -2.0)


    def test_is_better_than_returns_true_for_better_solution(self):
        better = GraphColoringProblemIntSolution(
            colors_count=3
        )
        worse = GraphColoringProblemIntSolution(
            colors_count=3
        )

        better.fitness_value = -2.0
        worse.fitness_value = -4.0

        self.assertTrue(better.is_better_than(worse))
        self.assertFalse(worse.is_better_than(better))


    def test_is_better_than_raises_for_invalid_type(self):
        solution = GraphColoringProblemIntSolution(
            colors_count=3
        )

        with self.assertRaises(TypeError):
            solution.is_better_than("not_a_solution")

    def test_argument_returns_all_vertex_colors(self):
        solution = GraphColoringProblemIntSolution(
            colors_count=4
        )

        representation = 0
        representation |= 1 << 0
        representation |= 2 << 2

        self.assertEqual(
            solution.argument(representation),
            "1 2 0 0",
        )


if __name__ == "__main__":
    unittest.main()