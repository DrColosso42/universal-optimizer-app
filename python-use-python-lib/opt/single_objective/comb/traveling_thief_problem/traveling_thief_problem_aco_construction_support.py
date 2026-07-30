"""
The :mod:`~opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem_aco_construction_support`
module describes the class
:class:`~opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem_aco_construction_support.TravelingThiefProblemAcoConstructionSupport`.
"""

import sys
from pathlib import Path
from random import choices

directory = Path(__file__).resolve()
sys.path.append(str(directory.parent))
sys.path.append(str(directory.parent.parent))
sys.path.append(str(directory.parent.parent.parent))
sys.path.append(str(directory.parent.parent.parent.parent))
root_dir = directory.parent.parent.parent.parent.parent
sys.path.append(str(root_dir))

from uo.problem.problem import Problem
from uo.solution.solution import Solution
from uo.algorithm.metaheuristic.aco.aco_construction_support import AcoConstructionSupport

from opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem import (
    TravelingThiefProblem,
)
from opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem_solution import (
    TtpRepresentation,
)


class TravelingThiefProblemAcoConstructionSupport(AcoConstructionSupport):
    """
    ACO construction support for the Traveling Thief Problem: tour built
    via pheromone/heuristic-weighted roulette selection, packing decided
    by `TravelingThiefProblemSolution.greedy_packing`.
    """

    def copy(self) -> "TravelingThiefProblemAcoConstructionSupport":
        """
        Internal copy of the construction support.
        """
        return TravelingThiefProblemAcoConstructionSupport()

    def construct(self, problem: Problem, solution: Solution, optimizer) -> None:
        """
        Build a tour city by city via pheromone/heuristic-weighted roulette
        selection, then pack it greedily.
        """
        if not isinstance(problem, TravelingThiefProblem):
            raise TypeError("Parameter 'problem' must have type 'TravelingThiefProblem'.")

        n = problem.n
        tour = [0]
        visited = [False] * n
        visited[0] = True

        for _ in range(n - 1):
            current = tour[-1]
            candidates = []
            weights = []
            for j in range(n):
                if not visited[j]:
                    w = (optimizer.tau[current][j] ** optimizer.alpha) * \
                        (optimizer.eta[current][j] ** optimizer.beta)
                    candidates.append(j)
                    weights.append(w)
            next_city = choices(candidates, weights=weights, k=1)[0]
            tour.append(next_city)
            visited[next_city] = True

        packing = solution.greedy_packing(problem, tour)
        solution.representation = TtpRepresentation(tour, packing)

    def local_search(self, problem: Problem, solution: Solution, optimizer) -> None:
        """
        Improve a constructed solution with 2-opt on the tour and iterative
        local search on the packing.
        """
        if not isinstance(problem, TravelingThiefProblem):
            raise TypeError("Parameter 'problem' must have type 'TravelingThiefProblem'.")

        tour = solution.representation.tour
        packing = solution.representation.packing

        tour = solution.two_opt(problem, tour, packing, max_passes=1)
        packing = solution.pack_iterative(problem, tour, initial_packing=packing, max_passes=3)

        solution.representation = TtpRepresentation(tour, packing)
