import tempfile
import unittest
from pathlib import Path

from opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem import (
    TravelingThiefProblem,
)
from opt.single_objective.comb.traveling_thief_problem.solver import (
    build_parser,
    solve_aco,
)


TINY_TTP_CONTENT = "\n".join([
    "DIMENSION: 4",
    "NUMBER OF ITEMS: 3",
    "CAPACITY OF KNAPSACK: 10",
    "MIN SPEED: 0.5",
    "MAX SPEED: 1.0",
    "RENTING RATIO: 1.0",
    "EDGE_WEIGHT_TYPE: EUC_2D",
    "NODE_COORD_SECTION",
    "1 0 0",
    "2 10 0",
    "3 10 10",
    "4 0 10",
    "ITEMS SECTION",
    "1 50 3 2",
    "2 40 4 3",
    "3 30 5 4",
])


class TestTravelingThiefProblemSolver(unittest.TestCase):

    def test_build_parser_accepts_fixed_method(self):
        parser = build_parser()

        args = parser.parse_args([
            "--input-file", "dummy.ttp",
            "--method", "fixed",
        ])

        self.assertEqual(args.input_file, "dummy.ttp")
        self.assertEqual(args.method, "fixed")

    def test_build_parser_accepts_adaptive_method(self):
        parser = build_parser()

        args = parser.parse_args([
            "--input-file", "dummy.ttp",
            "--method", "adaptive",
        ])

        self.assertEqual(args.input_file, "dummy.ttp")
        self.assertEqual(args.method, "adaptive")

    def test_build_parser_rejects_invalid_method(self):
        parser = build_parser()

        with self.assertRaises(SystemExit):
            parser.parse_args([
                "--input-file", "dummy.ttp",
                "--method", "invalid",
            ])

    def test_solve_aco_fixed_returns_optimizer_and_solution(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "tiny.ttp"
            input_path.write_text(TINY_TTP_CONTENT, encoding="utf-8")
            problem = TravelingThiefProblem.from_input_file(str(input_path))

        optimizer, best_solution = solve_aco(
            problem=problem,
            method="fixed",
            random_seed=123,
            iterations_max=5,
            n_ants=4,
            alpha=1.0,
            beta=2.0,
            rho=0.02,
            p_best=0.05,
            stagnation_limit=100,
            rho_scale=2.0,
        )

        self.assertIsNotNone(optimizer)
        self.assertIsNotNone(best_solution)
        self.assertIsNotNone(best_solution.representation)
        self.assertEqual(len(best_solution.representation.tour), problem.n)

    def test_solve_aco_adaptive_returns_optimizer_and_solution(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "tiny.ttp"
            input_path.write_text(TINY_TTP_CONTENT, encoding="utf-8")
            problem = TravelingThiefProblem.from_input_file(str(input_path))

        optimizer, best_solution = solve_aco(
            problem=problem,
            method="adaptive",
            random_seed=123,
            iterations_max=5,
            n_ants=4,
            alpha=1.0,
            beta=2.0,
            rho=0.02,
            p_best=0.05,
            stagnation_limit=100,
            rho_scale=2.0,
        )

        self.assertIsNotNone(optimizer)
        self.assertIsNotNone(best_solution)
        self.assertTrue(best_solution.is_feasible)

    def test_problem_can_be_loaded_from_temp_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "tiny.ttp"
            input_path.write_text(TINY_TTP_CONTENT, encoding="utf-8")

            problem = TravelingThiefProblem.from_input_file(str(input_path))

        self.assertEqual(problem.n, 4)
        self.assertEqual(problem.m, 3)
        self.assertEqual(problem.capacity, 10)


if __name__ == "__main__":
    unittest.main()
