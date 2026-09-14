import tempfile
import unittest
from pathlib import Path

from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem import (
    TravelingSalespersonProblem,
)
from opt.single_objective.comb.traveling_salesperson_problem.solver import (
    build_parser,
    solve_tabu,
)


class TestTravelingSalespersonProblemSolver(unittest.TestCase):

    def test_build_parser_accepts_tabu_method(self):
        parser = build_parser()

        args = parser.parse_args([
            "--input-file", "dummy.txt",
            "--method", "tabu",
        ])

        self.assertEqual(args.input_file, "dummy.txt")
        self.assertEqual(args.method, "tabu")
        self.assertEqual(args.tabu_tenure, 10)

    def test_build_parser_rejects_invalid_method(self):
        parser = build_parser()

        with self.assertRaises(SystemExit):
            parser.parse_args([
                "--input-file", "dummy.txt",
                "--method", "invalid",
            ])

    def test_solve_tabu_returns_optimizer_and_solution(self):
        problem = TravelingSalespersonProblem([
            [0, 1, 2, 3],
            [1, 0, 4, 5],
            [2, 4, 0, 6],
            [3, 5, 6, 0],
        ])

        optimizer, best_solution = solve_tabu(
            problem=problem,
            random_seed=123,
            evaluations_max=200,
            tabu_tenure=3,
        )

        self.assertIsNotNone(optimizer)
        self.assertIsNotNone(best_solution)
        self.assertIsNotNone(best_solution.representation)
        self.assertEqual(sorted(best_solution.representation), list(range(problem.dimension)))
        self.assertTrue(best_solution.is_feasible)

    def test_problem_can_be_loaded_from_temp_file(self):
        content = "\n".join([
            "0 1 2 3",
            "1 0 4 5",
            "2 4 0 6",
            "3 5 6 0",
        ])

        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "tsp.txt"
            input_path.write_text(content, encoding="utf-8")

            problem = TravelingSalespersonProblem.from_input_file(str(input_path))

        self.assertEqual(problem.dimension, 4)


if __name__ == "__main__":
    unittest.main()
