import tempfile
import unittest
from pathlib import Path

from opt.single_objective.comb.graph_coloring_problem.graph_coloring_problem import (
    GraphColoringProblem,
)
from opt.single_objective.comb.graph_coloring_problem.solver import (
    build_parser,
    encoded_dimension,
    solve_sa,
    solve_vns,
)


class TestGraphColoringProblemSolver(unittest.TestCase):

    def test_build_parser_accepts_vns_method(self):
        parser = build_parser()

        args = parser.parse_args([
            "--input-file",
            "dummy.txt",
            "--method",
            "vns",
        ])

        self.assertEqual(args.input_file, "dummy.txt")
        self.assertEqual(args.method, "vns")

    def test_build_parser_accepts_sa_method(self):
        parser = build_parser()

        args = parser.parse_args([
            "--input-file",
            "dummy.txt",
            "--method",
            "sa",
        ])

        self.assertEqual(args.input_file, "dummy.txt")
        self.assertEqual(args.method, "sa")

    def test_build_parser_uses_default_parameters(self):
        parser = build_parser()

        args = parser.parse_args([
            "--input-file",
            "dummy.txt",
            "--method",
            "vns",
        ])

        self.assertEqual(args.seed, 43434343)
        self.assertEqual(args.evaluations_max, 5000)
        self.assertEqual(args.k_min, 1)
        self.assertEqual(args.k_max, 3)
        self.assertEqual(args.initial_temp, 0.9)
        self.assertEqual(args.decay_factor, 0.95)

    def test_build_parser_accepts_custom_vns_parameters(self):
        parser = build_parser()

        args = parser.parse_args([
            "--input-file",
            "dummy.txt",
            "--method",
            "vns",
            "--seed",
            "123",
            "--evaluations-max",
            "200",
            "--k-min",
            "2",
            "--k-max",
            "5",
        ])

        self.assertEqual(args.seed, 123)
        self.assertEqual(args.evaluations_max, 200)
        self.assertEqual(args.k_min, 2)
        self.assertEqual(args.k_max, 5)

    def test_build_parser_accepts_custom_sa_parameters(self):
        parser = build_parser()

        args = parser.parse_args([
            "--input-file",
            "dummy.txt",
            "--method",
            "sa",
            "--seed",
            "123",
            "--evaluations-max",
            "200",
            "--initial-temp",
            "1.5",
            "--decay-factor",
            "0.8",
        ])

        self.assertEqual(args.seed, 123)
        self.assertEqual(args.evaluations_max, 200)
        self.assertEqual(args.initial_temp, 1.5)
        self.assertEqual(args.decay_factor, 0.8)

    def test_build_parser_rejects_invalid_method(self):
        parser = build_parser()

        with self.assertRaises(SystemExit):
            parser.parse_args([
                "--input-file",
                "dummy.txt",
                "--method",
                "invalid",
            ])

    def test_build_parser_requires_input_file(self):
        parser = build_parser()

        with self.assertRaises(SystemExit):
            parser.parse_args([
                "--method",
                "vns",
            ])

    def test_build_parser_requires_method(self):
        parser = build_parser()

        with self.assertRaises(SystemExit):
            parser.parse_args([
                "--input-file",
                "dummy.txt",
            ])

    def test_parser_no_longer_accepts_colors_count(self):
        parser = build_parser()

        with self.assertRaises(SystemExit):
            parser.parse_args([
                "--input-file",
                "dummy.txt",
                "--method",
                "vns",
                "--colors-count",
                "3",
            ])

    def test_parser_no_longer_accepts_auto_colors(self):
        parser = build_parser()

        with self.assertRaises(SystemExit):
            parser.parse_args([
                "--input-file",
                "dummy.txt",
                "--method",
                "vns",
                "--auto-colors",
            ])

    def test_encoded_dimension_for_four_vertices(self):
        problem = GraphColoringProblem(
            number_of_vertices=4,
            edges=[],
        )

        self.assertEqual(
            encoded_dimension(problem),
            8,
        )

    def test_encoded_dimension_for_five_vertices(self):
        problem = GraphColoringProblem(
            number_of_vertices=5,
            edges=[],
        )

        self.assertEqual(
            encoded_dimension(problem),
            15,
        )

    def test_encoded_dimension_for_one_vertex(self):
        problem = GraphColoringProblem(
            number_of_vertices=1,
            edges=[],
        )

        self.assertEqual(
            encoded_dimension(problem),
            1,
        )

    def test_solve_vns_returns_optimizer_and_solution(self):
        problem = GraphColoringProblem(
            number_of_vertices=4,
            edges=[
                (0, 1),
                (1, 2),
                (2, 3),
                (3, 0),
            ],
        )

        optimizer, best_solution = solve_vns(
            problem=problem,
            random_seed=123,
            evaluations_max=20,
            k_min=1,
            k_max=3,
        )

        self.assertIsNotNone(optimizer)
        self.assertIsNotNone(best_solution)
        self.assertIsNotNone(
            best_solution.representation
        )
        self.assertEqual(
            best_solution.colors_count,
            problem.number_of_vertices,
        )
        self.assertEqual(
            best_solution.bits_per_color,
            2,
        )

    def test_solve_sa_returns_optimizer_and_solution(self):
        problem = GraphColoringProblem(
            number_of_vertices=4,
            edges=[
                (0, 1),
                (1, 2),
                (2, 3),
                (3, 0),
            ],
        )

        optimizer, best_solution = solve_sa(
            problem=problem,
            random_seed=123,
            evaluations_max=20,
            initial_temp=0.9,
            decay_factor=0.95,
        )

        self.assertIsNotNone(optimizer)
        self.assertIsNotNone(best_solution)
        self.assertIsNotNone(
            best_solution.representation
        )
        self.assertEqual(
            best_solution.colors_count,
            problem.number_of_vertices,
        )
        self.assertEqual(
            best_solution.bits_per_color,
            2,
        )

    def test_problem_can_be_loaded_from_temp_file(self):
        content = "\n".join([
            "4 4",
            "0 1",
            "1 2",
            "2 3",
            "3 0",
        ])

        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = (
                Path(tmp_dir) / "graph_coloring.txt"
            )
            input_path.write_text(
                content,
                encoding="utf-8",
            )

            problem = GraphColoringProblem.from_input_file(
                str(input_path)
            )

        self.assertEqual(
            problem.number_of_vertices,
            4,
        )
        self.assertEqual(problem.dimension, 4)
        self.assertEqual(
            problem.edges,
            [
                (0, 1),
                (1, 2),
                (2, 3),
                (0, 3),
            ],
        )


if __name__ == "__main__":
    unittest.main()
