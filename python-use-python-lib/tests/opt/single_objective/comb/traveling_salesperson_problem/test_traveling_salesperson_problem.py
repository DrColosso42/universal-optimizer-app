import tempfile
import unittest
from pathlib import Path

from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem import (
    TravelingSalespersonProblem,
)


class TestTravelingSalespersonProblem(unittest.TestCase):

    def test_initialize_instance_with_valid_parameters(self):
        matrix = [
            [0, 10, 15],
            [10, 0, 20],
            [15, 20, 0],
        ]
        problem = TravelingSalespersonProblem(matrix)

        self.assertEqual(problem.distance_matrix, matrix)
        self.assertEqual(problem.dimension, 3)
        self.assertTrue(problem.is_minimization)
        self.assertFalse(problem.is_multi_objective)

    def test_distance_returns_matrix_entry(self):
        matrix = [
            [0, 10, 15],
            [10, 0, 20],
            [15, 20, 0],
        ]
        problem = TravelingSalespersonProblem(matrix)

        self.assertEqual(problem.distance(0, 1), 10)
        self.assertEqual(problem.distance(1, 2), 20)

    def test_copy_returns_independent_copy(self):
        matrix = [
            [0, 10, 15],
            [10, 0, 20],
            [15, 20, 0],
        ]
        problem = TravelingSalespersonProblem(matrix)

        copied = problem.copy()

        self.assertIsNot(problem, copied)
        self.assertEqual(problem.distance_matrix, copied.distance_matrix)

        copied.distance_matrix[0][1] = 99
        self.assertEqual(problem.distance_matrix[0][1], 10)

    def test_from_distance_matrix(self):
        matrix = [
            [0, 1, 2],
            [1, 0, 3],
            [2, 3, 0],
        ]
        problem = TravelingSalespersonProblem.from_distance_matrix(matrix)

        self.assertEqual(problem.distance_matrix, matrix)
        self.assertEqual(problem.dimension, 3)

    def test_distance_matrix_type_error(self):
        with self.assertRaises(TypeError):
            TravelingSalespersonProblem("not a list")

    def test_distance_matrix_must_have_at_least_two_cities(self):
        with self.assertRaises(ValueError):
            TravelingSalespersonProblem([[0]])

    def test_distance_matrix_must_be_square(self):
        with self.assertRaises(ValueError):
            TravelingSalespersonProblem([[0, 1], [1, 0, 5]])

    def test_distance_matrix_row_type_error(self):
        with self.assertRaises(TypeError):
            TravelingSalespersonProblem([[0, 1], "not a list"])

    def test_distance_matrix_must_be_non_negative(self):
        with self.assertRaises(ValueError):
            TravelingSalespersonProblem([[0, -1], [-1, 0]])

    def test_from_input_file_with_valid_file(self):
        content = "\n".join([
            "0 10 15",
            "10 0 20",
            "15 20 0",
        ])

        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "tsp.txt"
            input_path.write_text(content, encoding="utf-8")

            problem = TravelingSalespersonProblem.from_input_file(str(input_path))

        self.assertEqual(problem.dimension, 3)
        self.assertEqual(problem.distance(0, 1), 10.0)
        self.assertEqual(problem.distance(1, 2), 20.0)

    def test_from_input_file_raises_for_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            TravelingSalespersonProblem.from_input_file("definitely_missing_file.txt")

    def test_from_input_file_raises_for_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "bad.txt"
            input_path.write_text("", encoding="utf-8")

            with self.assertRaises(ValueError):
                TravelingSalespersonProblem.from_input_file(str(input_path))

    def test_from_input_file_raises_for_non_square_matrix(self):
        content = "\n".join([
            "0 10 15",
            "10 0 20",
        ])

        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "bad.txt"
            input_path.write_text(content, encoding="utf-8")

            with self.assertRaises(ValueError):
                TravelingSalespersonProblem.from_input_file(str(input_path))


if __name__ == "__main__":
    unittest.main()
