import unittest

import numpy as np

from opt.single_objective.glob.branin_min_problem import (
    BraninMinProblem,
    BraninMinProblemRealSolution,
)


class TestBraninMinProblemRealSolution(unittest.TestCase):
    def setUp(self):
        self.problem = BraninMinProblem()
        self.solution = BraninMinProblemRealSolution(random_seed=17)

    def test_known_minimizers_have_known_objective(self):
        for minimizer in self.problem.known_minimizers:
            quality = self.solution.calculate_quality_directly(minimizer, self.problem)
            self.assertAlmostEqual(
                quality.objective_value, self.problem.known_minimum, places=12
            )
            self.assertAlmostEqual(
                quality.fitness_value, -self.problem.known_minimum, places=12
            )
            self.assertTrue(quality.is_feasible)

    def test_evaluate_sets_objective_and_negative_fitness(self):
        self.solution.init_from(np.asarray([0.0, 0.0]), self.problem)
        self.solution.evaluate(self.problem)

        self.assertGreater(self.solution.objective_value, 0.0)
        self.assertEqual(self.solution.fitness_value, -self.solution.objective_value)
        self.assertTrue(self.solution.is_feasible)

    def test_init_from_copies_representation(self):
        point = np.asarray([1.0, 2.0])
        self.solution.init_from(point, self.problem)
        point[:] = 0.0

        np.testing.assert_array_equal(self.solution.representation, [1.0, 2.0])

    def test_copy_has_independent_representation(self):
        self.solution.init_from(np.asarray([1.0, 2.0]), self.problem)
        copied = self.solution.copy()
        copied.representation[0] = 4.0

        self.assertEqual(self.solution.representation[0], 1.0)

    def test_invalid_representations_are_rejected(self):
        with self.assertRaises(ValueError):
            self.solution.init_from(np.asarray([1.0]), self.problem)
        with self.assertRaises(ValueError):
            self.solution.init_from(np.asarray([np.nan, 1.0]), self.problem)
        with self.assertRaises(ValueError):
            self.solution.init_from(np.asarray([-6.0, 1.0]), self.problem)
        with self.assertRaises(TypeError):
            self.solution.init_from(np.asarray(["x", "y"]), self.problem)

    def test_native_representation_and_distance(self):
        parsed = self.solution.native_representation("[-3.0, 4.0]")

        np.testing.assert_array_equal(parsed, [-3.0, 4.0])
        self.assertEqual(
            self.solution.representation_distance_directly(
                np.asarray([0.0, 0.0]), np.asarray([3.0, 4.0])
            ),
            5.0,
        )

    def test_seeded_random_initialization_is_reproducible_and_bounded(self):
        first = BraninMinProblemRealSolution(random_seed=17)
        second = BraninMinProblemRealSolution(random_seed=17)
        first.init_random(self.problem)
        second.init_random(self.problem)

        np.testing.assert_array_equal(first.representation, second.representation)
        bounds = self.problem.bounds
        self.assertTrue(np.all(first.representation >= bounds[:, 0]))
        self.assertTrue(np.all(first.representation <= bounds[:, 1]))


if __name__ == "__main__":
    unittest.main()
