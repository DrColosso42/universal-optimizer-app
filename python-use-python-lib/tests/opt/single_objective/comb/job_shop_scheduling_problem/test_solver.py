import contextlib
import io
import os
import sys
import unittest

from uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_const import (
    SaTemperatureConst,
)
from uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_linear import (
    SaTemperatureLinear,
)
from uo.algorithm.metaheuristic.simulated_annealing.sa_temperature_exponetial import (
    SaTemperatureExponential,
)

from opt.single_objective.comb.job_shop_scheduling_problem.job_shop_scheduling_problem import (
    JobShopSchedulingProblem,
)
from opt.single_objective.comb.job_shop_scheduling_problem.solver import (
    build_parser,
    build_temperature,
    main,
    solve_sa,
    solve_vns,
    solve_ga,
)

MINI3 = [
    [(0, 3), (1, 2), (2, 2)],
    [(0, 2), (2, 1), (1, 4)],
    [(1, 4), (2, 3), (0, 1)],
]

MINI3_MULTISET = [0, 0, 0, 1, 1, 1, 2, 2, 2]

MINI3_OPTIMUM = 11

MINI3_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))),
    "opt", "single_objective", "comb", "job_shop_scheduling_problem", "data", "mini3.txt",
)


def parse(*arguments: str):
    """Parse the supplied command line arguments of the solver."""
    return build_parser().parse_args(list(arguments))


class TestJobShopSchedulingProblemSolverParser(unittest.TestCase):

    def test_parser_accepts_every_method(self):
        for method in ("sa", "vns", "ga"):
            args = parse("--input-file", "instance.txt", "--method", method)
            self.assertEqual(args.input_file, "instance.txt")
            self.assertEqual(args.method, method)

    def test_parser_rejects_an_unknown_method(self):
        with self.assertRaises(SystemExit):
            parse("--input-file", "instance.txt", "--method", "aco")

    def test_parser_requires_the_input_file(self):
        with self.assertRaises(SystemExit):
            parse("--method", "sa")

    def test_parser_requires_the_method(self):
        with self.assertRaises(SystemExit):
            parse("--input-file", "instance.txt")

    def test_parser_has_defaults_for_every_method(self):
        args = parse("--input-file", "instance.txt", "--method", "sa")
        self.assertEqual(args.evaluations_max, 20000)
        self.assertEqual(args.sa_temperature, "exponential")
        self.assertEqual(args.sa_swaps, 1)
        self.assertEqual(args.k_min, 1)
        self.assertEqual(args.k_max, 3)
        self.assertEqual(args.local_search, "first")
        self.assertEqual(args.population_size, 100)
        self.assertEqual(args.elite_count, 2)
        self.assertEqual(args.tournament_size, 3)

    def test_parser_reads_supplied_values(self):
        args = parse(
            "--input-file", "instance.txt", "--method", "ga",
            "--seed", "7", "--evaluations-max", "500",
            "--population-size", "20", "--tournament-size", "5",
            "--crossover-probability", "0.5", "--mutation-probability", "0.1",
        )
        self.assertEqual(args.seed, 7)
        self.assertEqual(args.evaluations_max, 500)
        self.assertEqual(args.population_size, 20)
        self.assertEqual(args.tournament_size, 5)
        self.assertEqual(args.crossover_probability, 0.5)
        self.assertEqual(args.mutation_probability, 0.1)

    def test_parser_rejects_an_unknown_temperature_schedule(self):
        with self.assertRaises(SystemExit):
            parse("--input-file", "instance.txt", "--method", "sa",
                  "--sa-temperature", "quadratic")

    def test_parser_rejects_an_unknown_local_search_variant(self):
        with self.assertRaises(SystemExit):
            parse("--input-file", "instance.txt", "--method", "vns",
                  "--local-search", "random")


class TestJobShopSchedulingProblemSolverTemperature(unittest.TestCase):

    def test_const_schedule_is_built(self):
        args = parse("--input-file", "i.txt", "--method", "sa", "--sa-temperature", "const")
        self.assertIsInstance(build_temperature(args), SaTemperatureConst)

    def test_linear_schedule_is_built(self):
        args = parse("--input-file", "i.txt", "--method", "sa", "--sa-temperature", "linear")
        self.assertIsInstance(build_temperature(args), SaTemperatureLinear)

    def test_exponential_schedule_is_built(self):
        args = parse("--input-file", "i.txt", "--method", "sa", "--sa-temperature", "exponential")
        self.assertIsInstance(build_temperature(args), SaTemperatureExponential)


class TestJobShopSchedulingProblemSolverMethods(unittest.TestCase):

    def setUp(self):
        self.problem = JobShopSchedulingProblem(MINI3)

    def assert_solved(self, optimizer, solution):
        self.assertIsNotNone(solution)
        self.assertEqual(sorted(solution.representation), MINI3_MULTISET)
        self.assertTrue(solution.is_feasible)
        self.assertGreaterEqual(solution.objective_value, MINI3_OPTIMUM)
        self.assertEqual(solution.fitness_value, -solution.objective_value)
        self.assertGreater(optimizer.evaluation, 0)

    def test_simulated_annealing_returns_a_feasible_schedule(self):
        args = parse("--input-file", "i.txt", "--method", "sa",
                     "--evaluations-max", "300", "--seed", "11")
        self.assert_solved(*solve_sa(self.problem, args))

    def test_simulated_annealing_accepts_several_swaps_per_move(self):
        args = parse("--input-file", "i.txt", "--method", "sa",
                     "--evaluations-max", "300", "--sa-swaps", "3")
        self.assert_solved(*solve_sa(self.problem, args))

    def test_variable_neighborhood_search_with_first_improvement(self):
        args = parse("--input-file", "i.txt", "--method", "vns",
                     "--evaluations-max", "300", "--local-search", "first")
        self.assert_solved(*solve_vns(self.problem, args))

    def test_variable_neighborhood_search_with_best_improvement(self):
        args = parse("--input-file", "i.txt", "--method", "vns",
                     "--evaluations-max", "300", "--local-search", "best")
        self.assert_solved(*solve_vns(self.problem, args))

    def test_genetic_algorithm_returns_a_feasible_schedule(self):
        args = parse("--input-file", "i.txt", "--method", "ga",
                     "--evaluations-max", "300", "--population-size", "20")
        self.assert_solved(*solve_ga(self.problem, args))

    def test_every_method_reaches_the_optimum_of_mini3(self):
        args = parse("--input-file", "i.txt", "--method", "sa",
                     "--evaluations-max", "3000", "--population-size", "30")
        for solve in (solve_sa, solve_vns, solve_ga):
            _, solution = solve(self.problem, args)
            self.assertEqual(solution.objective_value, MINI3_OPTIMUM,
                             msg=solve.__name__)

    def test_the_same_seed_gives_the_same_result(self):
        args = parse("--input-file", "i.txt", "--method", "sa",
                     "--evaluations-max", "300", "--seed", "5")
        _, first = solve_sa(self.problem, args)
        _, second = solve_sa(self.problem, args)
        self.assertEqual(first.representation, second.representation)


class TestJobShopSchedulingProblemSolverMain(unittest.TestCase):

    def run_main(self, *arguments: str) -> str:
        argv = sys.argv
        sys.argv = ["solver.py", "--input-file", MINI3_FILE] + list(arguments)
        output = io.StringIO()
        try:
            with contextlib.redirect_stdout(output):
                main()
        finally:
            sys.argv = argv
        return output.getvalue()

    def test_main_reports_the_outcome_for_every_method(self):
        for method in ("sa", "vns", "ga"):
            text = self.run_main("--method", method, "--evaluations-max", "300",
                                 "--population-size", "20")
            self.assertIn("Method: " + method, text)
            self.assertIn("Jobs: 3", text)
            self.assertIn("Machines: 3", text)
            self.assertIn("Lower bound of the makespan: 10", text)
            self.assertIn("Best solution makespan:", text)
            self.assertIn("Best solution feasible: True", text)


if __name__ == "__main__":
    unittest.main()
