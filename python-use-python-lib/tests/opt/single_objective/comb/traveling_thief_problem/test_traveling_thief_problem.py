import tempfile
import unittest
from pathlib import Path

from opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem import (
    TravelingThiefProblem,
    TtpItem,
)

TINY_TTP_CONTENT = "\n".join([
    "PROBLEM NAME: tiny_n7_m6",
    "KNAPSACK DATA TYPE: uncorrelated",
    "DIMENSION: 7",
    "NUMBER OF ITEMS: 6",
    "CAPACITY OF KNAPSACK: 30",
    "MIN SPEED: 0.1",
    "MAX SPEED: 1.0",
    "RENTING RATIO: 2.5",
    "EDGE_WEIGHT_TYPE: EUC_2D",
    "NODE_COORD_SECTION",
    "1 0 0",
    "2 4 0",
    "3 8 3",
    "4 7 8",
    "5 3 10",
    "6 0 7",
    "7 2 3",
    "ITEMS SECTION",
    "1 120 14 2",
    "2 90 10 3",
    "3 200 22 4",
    "4 70 8 5",
    "5 50 5 6",
    "6 110 12 7",
])


class TestTravelingThiefProblem(unittest.TestCase):

    def test_initialize_instance_with_valid_parameters(self):
        problem = TravelingThiefProblem(
            cities=[(0.0, 0.0), (1.0, 0.0)],
            items=[TtpItem(index=0, city=1, profit=10.0, weight=2.0)],
            capacity=5.0,
            v_min=0.1,
            v_max=1.0,
            renting_rate=1.0,
        )

        self.assertEqual(problem.n, 2)
        self.assertEqual(problem.m, 1)
        self.assertEqual(problem.capacity, 5.0)
        self.assertFalse(problem.is_minimization)
        self.assertFalse(problem.is_multi_objective)

    def test_initialize_raises_for_empty_cities(self):
        with self.assertRaises(ValueError):
            TravelingThiefProblem(
                cities=[], items=[], capacity=5.0, v_min=0.1, v_max=1.0, renting_rate=1.0
            )

    def test_initialize_raises_for_non_positive_capacity(self):
        with self.assertRaises(ValueError):
            TravelingThiefProblem(
                cities=[(0.0, 0.0)], items=[], capacity=0, v_min=0.1, v_max=1.0, renting_rate=1.0
            )

    def test_initialize_raises_for_invalid_speed_range(self):
        with self.assertRaises(ValueError):
            TravelingThiefProblem(
                cities=[(0.0, 0.0)], items=[], capacity=5.0, v_min=1.0, v_max=0.1, renting_rate=1.0
            )

    def test_items_by_city_groups_items_correctly(self):
        items = [
            TtpItem(index=0, city=0, profit=5.0, weight=1.0),
            TtpItem(index=1, city=0, profit=3.0, weight=1.0),
            TtpItem(index=2, city=1, profit=7.0, weight=1.0),
        ]
        problem = TravelingThiefProblem(
            cities=[(0.0, 0.0), (1.0, 0.0)],
            items=items,
            capacity=5.0,
            v_min=0.1,
            v_max=1.0,
            renting_rate=1.0,
        )

        self.assertEqual(len(problem.items_by_city[0]), 2)
        self.assertEqual(len(problem.items_by_city[1]), 1)

    def test_copy_creates_independent_instance(self):
        problem = TravelingThiefProblem(
            cities=[(0.0, 0.0), (1.0, 0.0)],
            items=[TtpItem(index=0, city=1, profit=10.0, weight=2.0)],
            capacity=5.0,
            v_min=0.1,
            v_max=1.0,
            renting_rate=1.0,
        )

        copied = problem.copy()
        copied.cities.append((2.0, 2.0))

        self.assertEqual(len(problem.cities), 2)
        self.assertEqual(len(copied.cities), 3)

    def test_from_input_file_loads_tiny_instance(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "tiny.ttp"
            input_path.write_text(TINY_TTP_CONTENT, encoding="utf-8")

            problem = TravelingThiefProblem.from_input_file(str(input_path))

        self.assertEqual(problem.n, 7)
        self.assertEqual(problem.m, 6)
        self.assertEqual(problem.capacity, 30)
        self.assertEqual(problem.v_min, 0.1)
        self.assertEqual(problem.v_max, 1.0)
        self.assertEqual(problem.renting_rate, 2.5)

    def test_from_input_file_raises_for_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            TravelingThiefProblem.from_input_file("definitely_missing_file.ttp")

    def test_from_input_file_raises_for_missing_header_fields(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "bad.ttp"
            input_path.write_text("DIMENSION: 7\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                TravelingThiefProblem.from_input_file(str(input_path))

    def test_distances_are_symmetric_and_zero_on_diagonal(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            input_path = Path(tmp_dir) / "tiny.ttp"
            input_path.write_text(TINY_TTP_CONTENT, encoding="utf-8")

            problem = TravelingThiefProblem.from_input_file(str(input_path))

        for i in range(problem.n):
            self.assertEqual(problem.distances[i][i], 0.0)
            for j in range(problem.n):
                self.assertAlmostEqual(problem.distances[i][j], problem.distances[j][i])


if __name__ == "__main__":
    unittest.main()
