import unittest

from opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem import (
    TravelingThiefProblem,
    TtpItem,
)
from opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem_solution import (
    TravelingThiefProblemSolution,
)
from opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem_aco_construction_support import (
    TravelingThiefProblemAcoConstructionSupport,
)


def make_tiny_problem() -> TravelingThiefProblem:
    return TravelingThiefProblem(
        cities=[(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)],
        items=[
            TtpItem(index=0, city=1, profit=50.0, weight=3.0),
            TtpItem(index=1, city=2, profit=40.0, weight=4.0),
        ],
        capacity=10.0,
        v_min=0.5,
        v_max=1.0,
        renting_rate=1.0,
    )


class FakeOptimizer:
    def __init__(self, n: int, alpha: float = 1.0, beta: float = 2.0):
        self.tau = [[1.0] * n for _ in range(n)]
        self.eta = [[1.0 if i != j else 0.0 for j in range(n)] for i in range(n)]
        self.alpha = alpha
        self.beta = beta


class TestTravelingThiefProblemAcoConstructionSupport(unittest.TestCase):

    def test_construct_builds_a_full_tour_and_feasible_packing(self):
        problem = make_tiny_problem()
        solution = TravelingThiefProblemSolution()
        optimizer = FakeOptimizer(n=problem.n)
        support = TravelingThiefProblemAcoConstructionSupport()

        support.construct(problem, solution, optimizer)

        tour = solution.representation.tour
        self.assertEqual(sorted(tour), list(range(problem.n)))
        weight = sum(item.weight for item in problem.items if solution.representation.packing[item.index])
        self.assertLessEqual(weight, problem.capacity)

    def test_construct_raises_for_wrong_problem_type(self):
        solution = TravelingThiefProblemSolution()
        optimizer = FakeOptimizer(n=4)
        support = TravelingThiefProblemAcoConstructionSupport()

        with self.assertRaises(TypeError):
            support.construct("not_a_problem", solution, optimizer)

    def test_local_search_keeps_solution_feasible(self):
        problem = make_tiny_problem()
        solution = TravelingThiefProblemSolution()
        optimizer = FakeOptimizer(n=problem.n)
        support = TravelingThiefProblemAcoConstructionSupport()
        support.construct(problem, solution, optimizer)

        support.local_search(problem, solution, optimizer)

        weight = sum(item.weight for item in problem.items if solution.representation.packing[item.index])
        self.assertLessEqual(weight, problem.capacity)

    def test_copy_returns_new_instance(self):
        support = TravelingThiefProblemAcoConstructionSupport()

        copied = support.copy()

        self.assertIsNot(support, copied)
        self.assertIsInstance(copied, TravelingThiefProblemAcoConstructionSupport)


if __name__ == "__main__":
    unittest.main()
