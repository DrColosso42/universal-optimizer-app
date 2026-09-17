import os
import tempfile
import unittest

from opt.single_objective.comb.job_shop_scheduling_problem.job_shop_scheduling_problem import (
    JobShopSchedulingProblem,
)

MINI3 = [
    [(0, 3), (1, 2), (2, 2)],
    [(0, 2), (2, 1), (1, 4)],
    [(1, 4), (2, 3), (0, 1)],
]

MINI3_FILE = "3 3\n0 3 1 2 2 2\n0 2 2 1 1 4\n1 4 2 3 0 1\n"

DATA_DIRECTORY = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))),
    "opt", "single_objective", "comb", "job_shop_scheduling_problem", "data",
)


class TestJobShopSchedulingProblemCreation(unittest.TestCase):

    def test_created_with_valid_jobs(self):
        problem = JobShopSchedulingProblem(MINI3)
        self.assertEqual(problem.number_of_jobs, 3)
        self.assertEqual(problem.number_of_machines, 3)
        self.assertEqual(problem.dimension, 9)
        self.assertEqual(problem.jobs, MINI3)
        self.assertEqual(problem.name, "JobShopSchedulingProblem")
        self.assertTrue(problem.is_minimization)
        self.assertFalse(problem.is_multi_objective)

    def test_from_jobs_builds_the_same_instance(self):
        problem = JobShopSchedulingProblem.from_jobs(MINI3)
        self.assertEqual(problem.jobs, MINI3)

    def test_jobs_of_wrong_type_raise_type_error(self):
        with self.assertRaises(TypeError):
            JobShopSchedulingProblem("3 3")

    def test_empty_list_of_jobs_raises_value_error(self):
        with self.assertRaises(ValueError):
            JobShopSchedulingProblem([])

    def test_job_that_is_not_a_list_raises_type_error(self):
        with self.assertRaises(TypeError):
            JobShopSchedulingProblem([((0, 3), (1, 2))])

    def test_empty_job_raises_value_error(self):
        with self.assertRaises(ValueError):
            JobShopSchedulingProblem([[]])

    def test_operation_that_is_not_a_tuple_raises_type_error(self):
        with self.assertRaises(TypeError):
            JobShopSchedulingProblem([[[0, 3]]])

    def test_operation_of_wrong_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            JobShopSchedulingProblem([[(0, 3, 1)]])

    def test_operation_with_non_integer_values_raises_type_error(self):
        with self.assertRaises(TypeError):
            JobShopSchedulingProblem([[(0, 3.0)]])

    def test_negative_machine_raises_value_error(self):
        with self.assertRaises(ValueError):
            JobShopSchedulingProblem([[(-1, 3)]])

    def test_non_positive_duration_raises_value_error(self):
        with self.assertRaises(ValueError):
            JobShopSchedulingProblem([[(0, 0)]])

    def test_machines_that_are_not_consecutive_raise_value_error(self):
        with self.assertRaises(ValueError):
            JobShopSchedulingProblem([[(0, 3), (2, 2)]])

    def test_copy_returns_equal_but_distinct_instance(self):
        problem = JobShopSchedulingProblem(MINI3)
        duplicate = problem.copy()
        self.assertIsNot(duplicate, problem)
        self.assertEqual(duplicate.jobs, problem.jobs)
        self.assertEqual(duplicate.dimension, problem.dimension)
        self.assertEqual(duplicate.lower_bound, problem.lower_bound)


class TestJobShopSchedulingProblemLowerBound(unittest.TestCase):

    def test_lower_bound_of_mini3(self):
        self.assertEqual(JobShopSchedulingProblem(MINI3).lower_bound, 10)

    def test_lower_bound_is_the_longest_job_when_it_dominates(self):
        problem = JobShopSchedulingProblem([[(0, 5), (1, 5)], [(0, 1), (1, 1)]])
        self.assertEqual(problem.lower_bound, 10)

    def test_lower_bound_is_the_busiest_machine_when_it_dominates(self):
        problem = JobShopSchedulingProblem([[(0, 5)], [(0, 5)], [(0, 5)]])
        self.assertEqual(problem.lower_bound, 15)


class TestJobShopSchedulingProblemLoading(unittest.TestCase):

    def write_instance(self, directory: str, content: str) -> str:
        path = os.path.join(directory, "instance.txt")
        with open(path, "w", encoding="utf-8") as file:
            file.write(content)
        return path

    def test_instance_is_read_from_file(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_instance(directory, MINI3_FILE)
            problem = JobShopSchedulingProblem.from_input_file(path)
            self.assertEqual(problem.jobs, MINI3)
            self.assertEqual(problem.lower_bound, 10)

    def test_blank_lines_are_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_instance(directory, "\n3 3\n\n0 3 1 2 2 2\n0 2 2 1 1 4\n\n1 4 2 3 0 1\n\n")
            self.assertEqual(JobShopSchedulingProblem.from_input_file(path).jobs, MINI3)

    def test_empty_file_raises_value_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_instance(directory, "\n")
            with self.assertRaises(ValueError):
                JobShopSchedulingProblem.from_input_file(path)

    def test_malformed_first_line_raises_value_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_instance(directory, "3 3 3\n0 3 1 2 2 2\n")
            with self.assertRaises(ValueError):
                JobShopSchedulingProblem.from_input_file(path)

    def test_wrong_number_of_job_lines_raises_value_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_instance(directory, "3 3\n0 3 1 2 2 2\n")
            with self.assertRaises(ValueError):
                JobShopSchedulingProblem.from_input_file(path)

    def test_job_line_of_wrong_length_raises_value_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_instance(directory, "1 3\n0 3 1 2\n")
            with self.assertRaises(ValueError):
                JobShopSchedulingProblem.from_input_file(path)

    def test_distributed_instances_match_their_known_sizes_and_lower_bounds(self):
        expected = {
            "mini3": (3, 3, 9, 10),
            "ft06": (6, 6, 36, 47),
            "ft10": (10, 10, 100, 655),
            "ft20": (20, 5, 100, 1119),
            "la01": (10, 5, 50, 666),
            "la02": (10, 5, 50, 635),
            "la03": (10, 5, 50, 588),
            "la04": (10, 5, 50, 537),
            "la05": (10, 5, 50, 593),
        }
        for name, (jobs, machines, dimension, lower_bound) in expected.items():
            problem = JobShopSchedulingProblem.from_input_file(
                os.path.join(DATA_DIRECTORY, name + ".txt")
            )
            self.assertEqual(
                (problem.number_of_jobs, problem.number_of_machines,
                 problem.dimension, problem.lower_bound),
                (jobs, machines, dimension, lower_bound),
                msg="instance " + name,
            )


class TestJobShopSchedulingProblemStringRepresentation(unittest.TestCase):

    def test_string_representations(self):
        problem = JobShopSchedulingProblem(MINI3)
        text = str(problem)
        self.assertIn("JobShopSchedulingProblem", text)
        self.assertIn("number_of_jobs=3", text)
        self.assertIn("number_of_machines=3", text)
        self.assertIn("dimension=9", text)
        self.assertEqual(format(problem), problem.string_rep("|"))
        self.assertIn("number_of_jobs=3", repr(problem))

    def test_indentation_is_applied(self):
        problem = JobShopSchedulingProblem(MINI3)
        self.assertIn("...", problem.string_rep("|", 3, "."))


if __name__ == "__main__":
    unittest.main()
