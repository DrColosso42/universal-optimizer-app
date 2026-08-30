import unittest

import numpy as np

from opt.single_objective.glob.branin_min_problem import BraninMinProblem


class TestBraninMinProblem(unittest.TestCase):
    def test_problem_metadata(self):
        problem = BraninMinProblem()

        self.assertTrue(problem.is_minimization)
        self.assertFalse(problem.is_multi_objective)
        self.assertEqual(problem.dimension, 2)
        np.testing.assert_array_equal(
            problem.bounds,
            np.asarray([[-5.0, 10.0], [0.0, 15.0]]),
        )
        self.assertAlmostEqual(problem.known_minimum, 0.39788735772973816)

    def test_array_properties_are_defensive_copies(self):
        problem = BraninMinProblem()
        bounds = problem.bounds
        minimizers = problem.known_minimizers

        bounds[:] = 0.0
        minimizers[:] = 0.0

        self.assertFalse(np.all(problem.bounds == 0.0))
        self.assertFalse(np.all(problem.known_minimizers == 0.0))

    def test_copy_is_independent(self):
        problem = BraninMinProblem()
        copied = problem.copy()

        self.assertIsInstance(copied, BraninMinProblem)
        self.assertIsNot(problem, copied)
        np.testing.assert_array_equal(problem.bounds, copied.bounds)


if __name__ == "__main__":
    unittest.main()
