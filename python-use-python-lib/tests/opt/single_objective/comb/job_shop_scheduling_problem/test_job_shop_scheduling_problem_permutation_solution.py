import itertools
import os
import unittest

from opt.single_objective.comb.job_shop_scheduling_problem.job_shop_scheduling_problem import (
    JobShopSchedulingProblem,
)
from opt.single_objective.comb.job_shop_scheduling_problem.job_shop_scheduling_problem_permutation_solution import (
    JobShopSchedulingProblemPermutationSolution,
)

MINI3 = [
    [(0, 3), (1, 2), (2, 2)],
    [(0, 2), (2, 1), (1, 4)],
    [(1, 4), (2, 3), (0, 1)],
]

MINI3_MULTISET = [0, 0, 0, 1, 1, 1, 2, 2, 2]

MINI3_OPTIMUM = 11

DATA_DIRECTORY = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))),
    "opt", "single_objective", "comb", "job_shop_scheduling_problem", "data",
)


class TestJobShopSchedulingProblemPermutationSolutionCreation(unittest.TestCase):

    def test_created_without_arguments(self):
        solution = JobShopSchedulingProblemPermutationSolution()
        self.assertIsNone(solution.fitness_value)
        self.assertIsNone(solution.objective_value)
        self.assertFalse(solution.is_feasible)
        self.assertTrue(solution.is_minimization)

    def test_created_with_random_seed(self):
        self.assertEqual(
            JobShopSchedulingProblemPermutationSolution(random_seed=7).random_seed, 7)

    def test_random_seed_of_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            JobShopSchedulingProblemPermutationSolution(random_seed="7")

    def test_value_is_minus_infinity_before_evaluation(self):
        self.assertEqual(
            JobShopSchedulingProblemPermutationSolution().value, float("-inf"))


class TestJobShopSchedulingProblemPermutationSolutionInitialization(unittest.TestCase):

    def setUp(self):
        self.problem = JobShopSchedulingProblem(MINI3)
        self.solution = JobShopSchedulingProblemPermutationSolution()

    def test_sorted_representation_repeats_every_job(self):
        self.assertEqual(
            JobShopSchedulingProblemPermutationSolution.sorted_representation(self.problem),
            MINI3_MULTISET)

    def test_init_random_yields_the_required_multiset(self):
        for seed in range(20):
            solution = JobShopSchedulingProblemPermutationSolution(random_seed=seed)
            solution.init_random(self.problem)
            self.assertEqual(sorted(solution.representation), MINI3_MULTISET)

    def test_init_random_is_reproducible_for_the_same_seed(self):
        first = JobShopSchedulingProblemPermutationSolution(random_seed=42)
        second = JobShopSchedulingProblemPermutationSolution(random_seed=42)
        first.init_random(self.problem)
        second.init_random(self.problem)
        self.assertEqual(first.representation, second.representation)

    def test_init_random_with_wrong_problem_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.solution.init_random("problem")

    def test_init_from_sets_the_representation(self):
        self.solution.init_from(MINI3_MULTISET, self.problem)
        self.assertEqual(self.solution.representation, MINI3_MULTISET)

    def test_init_from_copies_the_supplied_list(self):
        representation = list(MINI3_MULTISET)
        self.solution.init_from(representation, self.problem)
        representation[0] = 2
        self.assertEqual(self.solution.representation, MINI3_MULTISET)

    def test_init_from_with_representation_of_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.solution.init_from("000111222", self.problem)

    def test_init_from_with_wrong_problem_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.solution.init_from(MINI3_MULTISET, "problem")

    def test_init_from_with_wrong_multiset_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.solution.init_from([0, 0, 0, 0, 1, 1, 2, 2, 2], self.problem)

    def test_init_from_with_wrong_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.solution.init_from([0, 1, 2], self.problem)


class TestJobShopSchedulingProblemPermutationSolutionDecoding(unittest.TestCase):

    def setUp(self):
        self.problem = JobShopSchedulingProblem(MINI3)
        self.solution = JobShopSchedulingProblemPermutationSolution()

    def test_schedule_starts_every_operation_when_job_and_machine_are_free(self):
        schedule = self.solution.schedule(MINI3_MULTISET, self.problem)
        self.assertEqual(schedule["start"][(0, 0)], 0)
        self.assertEqual(schedule["end"][(0, 0)], 3)
        self.assertEqual(schedule["start"][(0, 1)], 3)
        self.assertEqual(schedule["end"][(0, 2)], 7)
        self.assertEqual(schedule["start"][(1, 0)], 3)

    def test_schedule_respects_the_order_of_operations_within_a_job(self):
        schedule = self.solution.schedule(MINI3_MULTISET, self.problem)
        for job_index, job in enumerate(MINI3):
            for operation_index in range(len(job) - 1):
                self.assertLessEqual(
                    schedule["end"][(job_index, operation_index)],
                    schedule["start"][(job_index, operation_index + 1)])

    def test_schedule_never_overlaps_two_operations_on_one_machine(self):
        schedule = self.solution.schedule(MINI3_MULTISET, self.problem)
        per_machine = {}
        for job_index, job in enumerate(MINI3):
            for operation_index, (machine, _) in enumerate(job):
                per_machine.setdefault(machine, []).append(
                    (schedule["start"][(job_index, operation_index)],
                     schedule["end"][(job_index, operation_index)]))
        for intervals in per_machine.values():
            intervals.sort()
            for earlier, later in zip(intervals, intervals[1:]):
                self.assertLessEqual(earlier[1], later[0])

    def test_makespan_is_the_end_of_the_last_operation(self):
        schedule = self.solution.schedule(MINI3_MULTISET, self.problem)
        self.assertEqual(schedule["makespan"], max(schedule["end"].values()))

    def test_schedule_of_a_representation_with_wrong_multiset_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.solution.schedule([0, 1, 2], self.problem)

    def test_exhaustive_search_of_mini3_reaches_its_known_optimum(self):
        best = min(
            self.solution.schedule(list(candidate), self.problem)["makespan"]
            for candidate in set(itertools.permutations(MINI3_MULTISET)))
        self.assertEqual(best, MINI3_OPTIMUM)

    def test_every_makespan_is_at_least_the_lower_bound(self):
        for candidate in set(itertools.permutations(MINI3_MULTISET)):
            self.assertGreaterEqual(
                self.solution.schedule(list(candidate), self.problem)["makespan"],
                self.problem.lower_bound)


class TestJobShopSchedulingProblemPermutationSolutionQuality(unittest.TestCase):

    def setUp(self):
        self.problem = JobShopSchedulingProblem(MINI3)
        self.solution = JobShopSchedulingProblemPermutationSolution()
        self.solution.init_from(MINI3_MULTISET, self.problem)

    def test_evaluation_fills_objective_fitness_and_feasibility(self):
        self.solution.evaluate(self.problem)
        self.assertEqual(self.solution.objective_value, 20)
        self.assertEqual(self.solution.fitness_value, -20)
        self.assertTrue(self.solution.is_feasible)

    def test_value_equals_fitness_after_evaluation(self):
        self.solution.evaluate(self.problem)
        self.assertEqual(self.solution.value, self.solution.fitness_value)

    def test_quality_of_wrong_problem_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.solution.calculate_quality_directly(MINI3_MULTISET, "problem")

    def test_shorter_makespan_is_better(self):
        better = JobShopSchedulingProblemPermutationSolution()
        better.init_from([1, 2, 0, 1, 0, 2, 1, 2, 0], self.problem)
        better.evaluate(self.problem)
        self.solution.evaluate(self.problem)
        self.assertLess(better.objective_value, self.solution.objective_value)
        self.assertTrue(better.is_better_than(self.solution))
        self.assertFalse(self.solution.is_better_than(better))

    def test_unevaluated_solution_is_never_better(self):
        fresh = JobShopSchedulingProblemPermutationSolution()
        self.solution.evaluate(self.problem)
        self.assertFalse(fresh.is_better_than(self.solution))
        self.assertTrue(self.solution.is_better_than(fresh))

    def test_comparison_with_wrong_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.solution.is_better_than("solution")


class TestJobShopSchedulingProblemPermutationSolutionUtilities(unittest.TestCase):

    def setUp(self):
        self.problem = JobShopSchedulingProblem(MINI3)
        self.solution = JobShopSchedulingProblemPermutationSolution()
        self.solution.init_from(MINI3_MULTISET, self.problem)

    def test_argument_and_native_representation_are_inverse(self):
        text = self.solution.argument(MINI3_MULTISET)
        self.assertEqual(text, "0 0 0 1 1 1 2 2 2")
        self.assertEqual(self.solution.native_representation(text), MINI3_MULTISET)

    def test_distance_counts_differing_positions(self):
        self.assertEqual(
            self.solution.representation_distance_directly([0, 1, 2], [0, 2, 1]), 2.0)
        self.assertEqual(
            self.solution.representation_distance_directly([0, 1, 2], [0, 1, 2]), 0.0)

    def test_distance_of_representations_of_different_length_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.solution.representation_distance_directly([0, 1], [0, 1, 2])

    def test_copy_returns_equal_but_distinct_instance(self):
        self.solution.evaluate(self.problem)
        duplicate = self.solution.copy()
        self.assertIsNot(duplicate, self.solution)
        self.assertEqual(duplicate.representation, self.solution.representation)
        self.assertEqual(duplicate.objective_value, self.solution.objective_value)
        self.assertEqual(duplicate.fitness_value, self.solution.fitness_value)

    def test_copy_does_not_share_the_representation(self):
        duplicate = self.solution.copy()
        duplicate.representation[0] = 2
        self.assertEqual(self.solution.representation, MINI3_MULTISET)

    def test_copy_from_overwrites_the_target(self):
        target = JobShopSchedulingProblemPermutationSolution()
        target.copy_from(self.solution)
        self.assertEqual(target.representation, self.solution.representation)

    def test_string_representations(self):
        text = str(self.solution)
        self.assertIn("representation=", text)
        self.assertEqual(format(self.solution), self.solution.string_rep("|"))
        self.assertIn("representation=", repr(self.solution))

    def test_indentation_is_applied(self):
        self.assertIn("...", self.solution.string_rep("|", 3, "."))


class TestJobShopSchedulingProblemPermutationSolutionOnDistributedInstances(unittest.TestCase):

    def test_random_solutions_are_feasible_and_above_the_lower_bound(self):
        for name in ("mini3", "ft06", "la05"):
            problem = JobShopSchedulingProblem.from_input_file(
                os.path.join(DATA_DIRECTORY, name + ".txt"))
            solution = JobShopSchedulingProblemPermutationSolution(random_seed=1)
            solution.init_random(problem)
            solution.evaluate(problem)
            self.assertTrue(solution.is_feasible, msg="instance " + name)
            self.assertGreaterEqual(
                solution.objective_value, problem.lower_bound, msg="instance " + name)


if __name__ == "__main__":
    unittest.main()
