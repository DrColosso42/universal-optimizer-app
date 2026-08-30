import unittest

import numpy as np

from opt_so_glob_min_branin_bo_real_exec import (
    build_optimizer,
    distance_to_nearest_minimizer,
)


class TestBraninBayesianOptimizer(unittest.TestCase):
    def test_optimizer_solves_bounded_minimization_problem(self):
        optimizer = build_optimizer()
        best = optimizer.optimize()
        bounds = optimizer.problem.bounds

        self.assertEqual(optimizer.evaluation, 40)
        self.assertEqual(optimizer.iteration, 34)
        self.assertEqual(optimizer.x_history.shape, (40, 2))
        self.assertEqual(optimizer.acquisition_history.shape, (34,))
        self.assertTrue(np.all(optimizer.x_history >= bounds[:, 0]))
        self.assertTrue(np.all(optimizer.x_history <= bounds[:, 1]))
        self.assertAlmostEqual(best.fitness_value, -best.objective_value)
        self.assertLess(best.objective_value, 1.0)
        self.assertLess(
            distance_to_nearest_minimizer(best.representation, optimizer.problem),
            0.5,
        )

    def test_fixed_seed_reproduces_evaluation_history(self):
        first = build_optimizer()
        second = build_optimizer()

        first.optimize()
        second.optimize()

        np.testing.assert_allclose(first.x_history, second.x_history)
        np.testing.assert_allclose(first.target_history, second.target_history)


if __name__ == "__main__":
    unittest.main()
