import tempfile
import unittest
from pathlib import Path

from opt.single_objective.comb.graph_coloring_problem.graph_coloring_problem import (
    GraphColoringProblem,
)


class TestGraphColoringProblem(unittest.TestCase):

    def test_initialize_instance_with_valid_parameters(self):
        problem = GraphColoringProblem(
            4,
            [(0, 1), (1, 2), (2, 3)],
        )

        self.assertEqual(problem.number_of_vertices, 4)
        self.assertEqual(
            problem.edges,
            [(0, 1), (1, 2), (2, 3)],
        )
        self.assertEqual(problem.dimension, 4)
        self.assertTrue(problem.is_minimization)
        self.assertFalse(problem.is_multi_objective)

    def test_copy_returns_independent_copy(self):
        problem = GraphColoringProblem(
            4,
            [(0, 1), (1, 2)],
        )

        copied = problem.copy()

        self.assertIsNot(problem, copied)
        self.assertEqual(
            problem.number_of_vertices,
            copied.number_of_vertices,
        )
        self.assertEqual(problem.edges, copied.edges)

        copied.edges[0] = (2, 3)

        self.assertEqual(problem.edges[0], (0, 1))

    def test_from_number_of_vertices_and_edges(self):
        problem = (
            GraphColoringProblem
            .from_number_of_vertices_and_edges(
                number_of_vertices=5,
                edges=[(0, 1), (1, 2), (3, 4)],
            )
        )

        self.assertEqual(problem.number_of_vertices, 5)
        self.assertEqual(
            problem.edges,
            [(0, 1), (1, 2), (3, 4)],
        )
        self.assertEqual(problem.dimension, 5)

    def test_edges_are_normalized(self):
        problem = GraphColoringProblem(
            4,
            [(2, 0), (3, 1)],
        )

        self.assertEqual(
            problem.edges,
            [(0, 2), (1, 3)],
        )

    def test_duplicate_edges_are_removed(self):
        problem = GraphColoringProblem(
            4,
            [(0, 1), (1, 0), (0, 1)],
        )

        self.assertEqual(problem.edges, [(0, 1)])

    def test_number_of_vertices_type_error(self):
        with self.assertRaises(TypeError):
            GraphColoringProblem(
                "4",
                [(0, 1), (1, 2)],
            )

    def test_edges_type_error(self):
        with self.assertRaises(TypeError):
            GraphColoringProblem(4, "0 1")

    def test_number_of_vertices_must_be_positive(self):
        with self.assertRaises(ValueError):
            GraphColoringProblem(0, [])

    def test_edge_must_be_tuple(self):
        with self.assertRaises(ValueError):
            GraphColoringProblem(4, [[0, 1]])

    def test_edge_must_have_two_vertices(self):
        with self.assertRaises(ValueError):
            GraphColoringProblem(4, [(0, 1, 2)])

    def test_edge_vertices_must_be_integers(self):
        with self.assertRaises(ValueError):
            GraphColoringProblem(4, [(0, "1")])

    def test_edge_vertices_must_be_non_negative(self):
        with self.assertRaises(ValueError):
            GraphColoringProblem(4, [(-1, 2)])

    def test_edge_vertices_must_be_smaller_than_number_of_vertices(
        self,
    ):
        with self.assertRaises(ValueError):
            GraphColoringProblem(4, [(0, 4)])

    def test_self_loops_are_not_allowed(self):
        with self.assertRaises(ValueError):
            GraphColoringProblem(4, [(2, 2)])

    def test_from_input_file_with_valid_file(self):
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

        self.assertEqual(problem.number_of_vertices, 4)
        self.assertEqual(
            problem.edges,
            [(0, 1), (1, 2), (2, 3), (0, 3)],
        )
        self.assertEqual(problem.dimension, 4)

    def test_from_input_file_raises_for_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            GraphColoringProblem.from_input_file(
                "definitely_missing_file.txt"
            )

    def test_from_input_file_raises_for_empty_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "bad.txt"
            input_path.write_text("", encoding="utf-8")

            with self.assertRaises(ValueError):
                GraphColoringProblem.from_input_file(
                    str(input_path)
                )

    def test_from_input_file_raises_for_bad_first_line(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "bad.txt"
            input_path.write_text(
                "4\n0 1\n",
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                GraphColoringProblem.from_input_file(
                    str(input_path)
                )

    def test_from_input_file_raises_for_wrong_number_of_edges(
        self,
    ):
        content = "\n".join([
            "4 3",
            "0 1",
            "1 2",
        ])

        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "bad.txt"
            input_path.write_text(
                content,
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                GraphColoringProblem.from_input_file(
                    str(input_path)
                )

    def test_from_input_file_raises_for_bad_edge_line(self):
        content = "\n".join([
            "4 2",
            "0 1",
            "2",
        ])

        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "bad.txt"
            input_path.write_text(
                content,
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                GraphColoringProblem.from_input_file(
                    str(input_path)
                )


if __name__ == "__main__":
    unittest.main()