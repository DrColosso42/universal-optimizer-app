"""
..  _py_traveling_thief_problem_solution:
"""

import sys
from pathlib import Path
from typing import Optional
from random import random, shuffle

from bitstring import BitArray

directory = Path(__file__).resolve()
sys.path.append(str(directory.parent))
sys.path.append(str(directory.parent.parent))
sys.path.append(str(directory.parent.parent.parent))
sys.path.append(str(directory.parent.parent.parent.parent))
root_dir = directory.parent.parent.parent.parent.parent
sys.path.append(str(root_dir))

from uo.problem.problem import Problem
from uo.solution.quality_of_solution import QualityOfSolution
from uo.solution.solution import Solution

from opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem import (
    TravelingThiefProblem,
)


class TtpRepresentation:
    """
    Combined tour + packing representation for a TTP solution.
    """

    def __init__(self, tour: list[int], packing: BitArray) -> None:
        """
        Create new `TtpRepresentation` instance.
        """
        self.tour = tour
        self.packing = packing

    def copy(self) -> "TtpRepresentation":
        """
        Copy of the representation.
        """
        return TtpRepresentation(self.tour.copy(), BitArray(bin=self.packing.bin))

    def __str__(self) -> str:
        return f"tour={self.tour}|packing={self.packing.bin}"


class TravelingThiefProblemSolution(Solution[TtpRepresentation, str]):
    """
    Combined tour + packing solution for the Traveling Thief Problem.
    """

    def __init__(
        self,
        random_seed: Optional[int] = None,
        evaluation_cache_is_used: bool = False,
        evaluation_cache_max_size: int = 0,
        distance_calculation_cache_is_used: bool = False,
        distance_calculation_cache_max_size: int = 0
    ) -> None:
        """
        Create new `TravelingThiefProblemSolution` instance.
        """
        super().__init__(
            random_seed=random_seed,
            fitness_value=None,
            fitness_values=None,
            objective_value=None,
            objective_values=None,
            is_feasible=False,
            evaluation_cache_is_used=evaluation_cache_is_used,
            evaluation_cache_max_size=evaluation_cache_max_size,
            distance_calculation_cache_is_used=distance_calculation_cache_is_used,
            distance_calculation_cache_max_size=distance_calculation_cache_max_size,
        )
        self.is_minimization = False

    def copy(self) -> "TravelingThiefProblemSolution":
        """
        Internal copy of the solution.
        """
        sol = TravelingThiefProblemSolution(self.random_seed)
        sol.copy_from(self)
        return sol

    def copy_from(self, original) -> None:
        """
        Copy all data from the original target solution.
        """
        super().copy_from(original)

    def argument(self, representation: TtpRepresentation) -> str:
        """
        Convert internal representation to solution code.
        """
        return str(representation)

    def init_random(self, problem: Problem) -> None:
        """
        Random initialization of the solution.
        """
        if not isinstance(problem, TravelingThiefProblem):
            raise TypeError("Parameter 'problem' must have type 'TravelingThiefProblem'.")

        tour = list(range(problem.n))
        shuffle(tour)

        packing = BitArray(problem.m)
        for i in range(problem.m):
            if random() > 0.5:
                packing[i] = True

        self.representation = TtpRepresentation(tour, packing)

    def init_from(self, representation: TtpRepresentation, problem: Problem) -> None:
        """
        Initialization of the solution by setting its native representation.
        """
        if not isinstance(representation, TtpRepresentation):
            raise TypeError("Parameter 'representation' must have type 'TtpRepresentation'.")
        self.representation = representation.copy()

    def __speed_at_weight(self, problem: TravelingThiefProblem, weight: float) -> float:
        """
        Thief's travel speed as a function of current knapsack weight.
        """
        ratio = weight / problem.capacity
        return problem.v_max - ratio * (problem.v_max - problem.v_min)

    def calculate_quality_directly(
        self, representation: TtpRepresentation, problem: TravelingThiefProblem
    ) -> QualityOfSolution:
        """
        Fitness calculation of the TTP solution.
        """
        if not isinstance(representation, TtpRepresentation):
            raise TypeError("Parameter 'representation' must have type 'TtpRepresentation'.")
        if not isinstance(problem, TravelingThiefProblem):
            raise TypeError("Parameter 'problem' must have type 'TravelingThiefProblem'.")

        tour = representation.tour
        packing = representation.packing

        total_weight = sum(
            item.weight for item in problem.items if packing[item.index]
        )
        if total_weight > problem.capacity:
            overflow = total_weight - problem.capacity
            max_possible_profit = sum(item.profit for item in problem.items)
            objective_value = float("-inf")
            fitness_value = -(max_possible_profit * overflow + total_weight)
            return QualityOfSolution(
                fitness_value=fitness_value,
                fitness_values=None,
                objective_value=objective_value,
                objective_values=None,
                is_feasible=False,
            )

        weight = 0.0
        profit = 0.0
        total_time = 0.0

        for idx in range(len(tour)):
            current_city = tour[idx]
            next_city = tour[(idx + 1) % len(tour)]

            for item in problem.items_by_city.get(current_city, []):
                if packing[item.index]:
                    weight += item.weight
                    profit += item.profit

            distance = problem.distances[current_city][next_city]
            speed = self.__speed_at_weight(problem, weight)
            total_time += distance / speed

        objective_value = profit - problem.renting_rate * total_time
        fitness_value = objective_value

        return QualityOfSolution(
            fitness_value=fitness_value,
            fitness_values=None,
            objective_value=objective_value,
            objective_values=None,
            is_feasible=True,
        )

    def tour_cost(self, problem: TravelingThiefProblem, tour: list[int]) -> float:
        """
        Total tour length (sum of edge distances), ignoring packing.
        """
        n = problem.n
        return sum(
            problem.distances[tour[k]][tour[(k + 1) % n]] for k in range(n)
        )

    def greedy_packing(
        self, problem: TravelingThiefProblem, tour: list[int]
    ) -> BitArray:
        """
        Greedy packing heuristic: pick items by profit/(weight * remaining
        tour distance) ratio, respecting knapsack capacity.
        """
        n = problem.n
        remaining = [0.0] * n
        for k in range(n - 2, -1, -1):
            remaining[k] = remaining[k + 1] + problem.distances[tour[k]][tour[k + 1]]
        city_to_pos = {city: k for k, city in enumerate(tour)}

        def score(item):
            dist = remaining[city_to_pos[item.city]] + 1e-9
            return item.profit / (item.weight * dist)

        sorted_items = sorted(problem.items, key=score, reverse=True)

        packing = BitArray(problem.m)
        weight = 0.0
        for item in sorted_items:
            if weight + item.weight <= problem.capacity:
                packing[item.index] = True
                weight += item.weight
        return packing

    def two_opt(
        self, problem: TravelingThiefProblem, tour: list[int], packing: BitArray,
        max_passes: Optional[int] = None
    ) -> list[int]:
        """
        2-opt local search over the tour; a swap is accepted only if it
        improves the full TTP fitness (not just tour length).
        """
        n = problem.n
        dist = problem.distances
        passes = 0
        improved = True

        current_score = self.calculate_quality_directly(
            TtpRepresentation(tour, packing), problem
        ).fitness_value

        while improved and (max_passes is None or passes < max_passes):
            improved = False
            passes += 1
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    a, b = tour[i - 1], tour[i]
                    c, d = tour[j], tour[(j + 1) % n]
                    # cheap prefilter: shorter distance doesn't guarantee better TTP score
                    if dist[a][c] + dist[b][d] >= dist[a][b] + dist[c][d]:
                        continue
                    new_tour = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
                    score = self.calculate_quality_directly(
                        TtpRepresentation(new_tour, packing), problem
                    ).fitness_value
                    if score > current_score:
                        tour = new_tour
                        current_score = score
                        improved = True
                        break
                if improved:
                    break
        return tour

    def pack_iterative(
        self, problem: TravelingThiefProblem, tour: list[int],
        initial_packing: Optional[BitArray] = None, max_passes: Optional[int] = None
    ) -> BitArray:
        """
        Iterative local search over the packing: flip one item at a time,
        keep the flip only if it improves fitness and stays within capacity.
        """
        if initial_packing is not None:
            packing = BitArray(bin=initial_packing.bin)
        else:
            packing = BitArray(problem.m)

        current_weight = sum(
            item.weight for item in problem.items if packing[item.index]
        )
        current_score = self.calculate_quality_directly(
            TtpRepresentation(tour, packing), problem
        ).fitness_value

        improved = True
        passes = 0
        while improved and (max_passes is None or passes < max_passes):
            improved = False
            passes += 1
            for item in problem.items:
                k = item.index
                if not packing[k] and current_weight + item.weight > problem.capacity:
                    continue
                packing[k] = not packing[k]
                new_score = self.calculate_quality_directly(
                    TtpRepresentation(tour, packing), problem
                ).fitness_value
                if new_score > current_score:
                    current_weight += item.weight if packing[k] else -item.weight
                    current_score = new_score
                    improved = True
                else:
                    packing[k] = not packing[k]
        return packing

    def native_representation(self, representation_str: str) -> TtpRepresentation:
        """
        Native solution representation from its string representation.
        """
        tour_part, packing_part = representation_str.split("|")
        tour = [int(x) for x in tour_part.split("=")[1].split(",")]
        packing_bits = packing_part.split("=")[1]
        return TtpRepresentation(tour, BitArray(bin=packing_bits))

    @staticmethod
    def __tour_edges(tour: list[int]) -> set[tuple[int, int]]:
        """
        Undirected edge set of the tour, used for a rotation/reflection
        invariant tour distance.
        """
        n = len(tour)
        return {tuple(sorted((tour[i], tour[(i + 1) % n]))) for i in range(n)}

    def representation_distance_directly(
        self, representation_1: TtpRepresentation, representation_2: TtpRepresentation
    ) -> float:
        """
        Combined distance between two representations: Hamming distance on
        the packing plus edge-set distance on the tour.
        """
        packing_distance = sum(
            1 for a, b in zip(representation_1.packing, representation_2.packing) if a != b
        )
        edges_1 = self.__tour_edges(representation_1.tour)
        edges_2 = self.__tour_edges(representation_2.tour)
        tour_distance = len(edges_1 ^ edges_2)
        return float(packing_distance + tour_distance)

    def string_rep(
        self, delimiter: str = "\n", indentation: int = 0, indentation_symbol: str = "   ",
        group_start: str = "{", group_end: str = "}"
    ) -> str:
        """
        String representation of the solution instance.
        """
        s = group_start
        s += super().string_rep(delimiter, indentation, indentation_symbol, "", "")
        s += delimiter + "string_representation()="
        s += "" if self.representation is None else str(self.representation)
        s += group_end
        return s

    def __str__(self) -> str:
        return self.string_rep("|", 0, "", "{", "}")

    def __repr__(self) -> str:
        return self.string_rep("\n", 0, "   ", "{", "}")

    def __format__(self, spec: str = "") -> str:
        return self.string_rep("|")
