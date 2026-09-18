import tempfile
import unittest
from pathlib import Path

from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem import (
    TravelingSalespersonProblem,
)
from opt.single_objective.comb.traveling_salesperson_problem.solver import (
    build_parser,
    solve_ga,
    solve_vns,
    solve_tabu,
)

DISTANCES = [[0, 2, 9, 10], [2, 0, 6, 4], [9, 6, 0, 8], [10, 4, 8, 0]]


class TestTravelingSalespersonProblemSolver(unittest.TestCase):

    def test_build_parser_accepts_ga_method(self):
        parser = build_parser()

        args = parser.parse_args([
            "--input-file", "dummy.txt",
            "--method", "ga",
        ])

        self.assertEqual(args.input_file, "dummy.txt")
        self.assertEqual(args.method, "ga")

    def test_build_parser_accepts_vns_method(self):
        parser = build_parser()

        args = parser.parse_args([
            "--input-file", "dummy.txt",
            "--method", "vns",
        ])

        self.assertEqual(args.input_file, "dummy.txt")
        self.assertEqual(args.method, "vns")

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

    def test_build_parser_default_values(self):
        parser = build_parser()

        args = parser.parse_args([
            "--input-file", "dummy.txt",
            "--method", "ga",
        ])

        self.assertEqual(args.seed, 43434343)
        self.assertEqual(args.evaluations_max, 5000)
        self.assertEqual(args.iterations_max, 0)
        self.assertEqual(args.population_size, 100)
        self.assertEqual(args.elite_count, 10)
        self.assertEqual(args.crossover_probability, 0.95)
        self.assertEqual(args.mutation_probability, 0.05)
        self.assertEqual(args.k_min, 1)
        self.assertEqual(args.k_max, 3)
        self.assertEqual(args.tabu_tenure, 10)

    def test_solve_ga_returns_optimizer_and_optimal_solution(self):
        problem = TravelingSalespersonProblem.from_distance_matrix(
            distances=DISTANCES
        )

        optimizer, best_solution = solve_ga(
            problem=problem,
            random_seed=123,
            evaluations_max=3000,
            population_size=20,
            elite_count=2,
            crossover_probability=0.9,
            mutation_probability=0.05,
        )

        self.assertIsNotNone(optimizer)
        self.assertIsNotNone(best_solution)
        self.assertIsNotNone(best_solution.fitness_value)
        self.assertTrue(best_solution.is_feasible)
        # optimal tour 0 -> 1 -> 3 -> 2 -> 0 has length 23
        self.assertEqual(best_solution.objective_value, 23.0)
        self.assertEqual(best_solution.fitness_value, -23.0)

    def test_solve_vns_returns_optimizer_and_optimal_solution(self):
        problem = TravelingSalespersonProblem.from_distance_matrix(
            distances=DISTANCES
        )

        optimizer, best_solution = solve_vns(
            problem=problem,
            random_seed=123,
            evaluations_max=3000,
            k_min=1,
            k_max=3,
        )

        self.assertIsNotNone(optimizer)
        self.assertIsNotNone(best_solution)
        self.assertIsNotNone(best_solution.fitness_value)
        self.assertTrue(best_solution.is_feasible)
        # optimal tour 0 -> 1 -> 3 -> 2 -> 0 has length 23
        self.assertEqual(best_solution.objective_value, 23.0)
        self.assertEqual(best_solution.fitness_value, -23.0)

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
