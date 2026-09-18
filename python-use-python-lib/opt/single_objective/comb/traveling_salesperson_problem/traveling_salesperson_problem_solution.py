"""
..  _py_traveling_salesperson_problem_solution:
"""

import sys
from pathlib import Path

directory = Path(__file__).resolve()
sys.path.append(str(directory))
sys.path.append(str(directory.parent))
sys.path.append(str(directory.parent.parent.parent))
sys.path.append(str(directory.parent.parent.parent.parent))
root_dir = directory.parent.parent.parent.parent.parent
sys.path.append(str(root_dir))

from random import randrange, shuffle
from typing import Optional

from uo.problem.problem import Problem
from uo.solution.quality_of_solution import QualityOfSolution
from uo.solution.solution import Solution

from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem import (
    TravelingSalespersonProblem,
)


class TravelingSalespersonProblemSolution(Solution[list[int], str]):
    """
    Permutation-based solution for the Traveling Salesperson Problem.

    The representation is a list of city indexes, where each city is visited
    exactly once. The tour returns to the starting city. The objective is to
    minimize the total traveled distance.
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
        Create new `TravelingSalespersonProblemSolution` instance.
        """
        if not isinstance(random_seed, int) and random_seed is not None:
            raise TypeError("Parameter 'random_seed' must be 'int' or 'None'.")

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
            distance_calculation_cache_max_size=distance_calculation_cache_max_size
        )
        self.is_minimization = True

    def copy(self) -> "TravelingSalespersonProblemSolution":
        """
        Internal copy of the solution.
        """
        sol = TravelingSalespersonProblemSolution(self.random_seed)
        sol.copy_from(self)
        return sol

    def copy_from(self, original) -> None:
        """
        Copy all data from the original target solution.
        """
        super().copy_from(original)

    def argument(self, representation: list[int]) -> str:
        """
        Convert internal representation to solution code.
        """
        return "-".join(str(city) for city in representation)

    def init_random(self, problem: Problem) -> None:
        """
        Random initialization of the solution.
        """
        if not isinstance(problem, TravelingSalespersonProblem):
            raise TypeError("Parameter 'problem' must have type 'TravelingSalespersonProblem'.")

        representation: list[int] = list(range(problem.dimension))
        shuffle(representation)
        self.representation = representation

    def init_from(self, representation: list[int], problem: Problem) -> None:
        """
        Initialization of the solution by setting its native representation.
        """
        if not isinstance(representation, list):
            raise TypeError("Parameter 'representation' must have type 'list'.")
        if len(representation) == 0:
            raise ValueError("Representation must have positive length.")
        if any((not isinstance(city, int)) for city in representation):
            raise ValueError("All cities in the representation must be integers.")
        self.representation = representation.copy()

    @staticmethod
    def __is_permutation(representation: list[int], dimension: int) -> bool:
        """
        Checks if the representation is a permutation of all city indexes.
        """
        return sorted(representation) == list(range(dimension))

    @staticmethod
    def __tour_length(
        representation: list[int],
        distances: list[list[int]]
    ) -> float:
        """
        Total length of the cyclic tour determined by the representation.
        """
        dimension: int = len(representation)
        total_length: float = 0
        for i in range(dimension):
            total_length += distances[representation[i]][representation[(i + 1) % dimension]]
        return total_length

    def calculate_quality_directly(
        self,
        representation: list[int],
        problem: TravelingSalespersonProblem
    ) -> QualityOfSolution:
        """
        Fitness calculation of the traveling salesperson permutation solution.

        The objective value is the total tour length, while the fitness value
        is the negated tour length, so that maximization of fitness corresponds
        to minimization of the tour length.
        """
        if not isinstance(representation, list):
            raise TypeError("Parameter 'representation' must have type 'list'.")
        if not isinstance(problem, TravelingSalespersonProblem):
            raise TypeError("Parameter 'problem' must have type 'TravelingSalespersonProblem'.")

        if len(representation) != problem.dimension:
            raise ValueError("Representation length must match problem dimension.")

        if not self.__is_permutation(representation, problem.dimension):
            return QualityOfSolution(
                fitness_value=float(-1000000),
                fitness_values=None,
                objective_value=float("-inf"),
                objective_values=None,
                is_feasible=False
            )

        tour_length: float = self.__tour_length(representation, problem.distances)

        return QualityOfSolution(
            fitness_value=float(-tour_length),
            fitness_values=None,
            objective_value=float(tour_length),
            objective_values=None,
            is_feasible=True
        )

    def native_representation(self, representation_str: str) -> list[int]:
        """
        Native solution representation from its string representation.
        """
        if not isinstance(representation_str, str):
            raise TypeError("Parameter 'representation_str' must be 'str'.")
        cities: list[int] = []
        for part in representation_str.split("-"):
            if not part.isdigit():
                raise ValueError(
                    "Representation string should contain only city indexes separated by '-'."
                )
            cities.append(int(part))
        return cities

    @staticmethod
    def __tour_edges(tour: list[int]) -> set[tuple[int, int]]:
        """
        Undirected edge set of the tour, used for a rotation/reflection
        invariant tour distance.
        """
        dimension: int = len(tour)
        return {tuple(sorted((tour[i], tour[(i + 1) % dimension]))) for i in range(dimension)}

    def representation_distance_directly(
        self,
        representation_1: list[int],
        representation_2: list[int]
    ) -> float:
        """
        Distance between two tours, determined as the number of undirected
        edges in which the tours differ. The distance is invariant to tour
        rotation and reflection.
        """
        if not isinstance(representation_1, list):
            raise TypeError("Parameter 'representation_1' must have type 'list'.")
        if not isinstance(representation_2, list):
            raise TypeError("Parameter 'representation_2' must have type 'list'.")
        if len(representation_1) != len(representation_2):
            raise ValueError("Representations should have the same length.")

        edges_1: set[tuple[int, int]] = self.__tour_edges(representation_1)
        edges_2: set[tuple[int, int]] = self.__tour_edges(representation_2)
        return float(len(edges_1 ^ edges_2))

    def string_rep(
        self,
        delimiter: str = "\n",
        indentation: int = 0,
        indentation_symbol: str = "   ",
        group_start: str = "{",
        group_end: str = "}"
    ) -> str:
        """
        String representation of the solution instance.
        """
        s = group_start
        s += super().string_rep(
            delimiter=delimiter,
            indentation=indentation,
            indentation_symbol=indentation_symbol,
            group_start="",
            group_end=""
        )
        s += delimiter + "string_representation()="
        s += "" if self.representation is None else self.argument(self.representation)
        s += group_end
        return s

    def __str__(self) -> str:
        return self.string_rep("|", 0, "", "{", "}")

    def __repr__(self) -> str:
        return self.string_rep("\n", 0, "   ", "{", "}")

    def __format__(self, spec: str = "") -> str:
        return self.string_rep("|")


class TravelingSalespersonProblemSolutionNn(TravelingSalespersonProblemSolution):
    """
    Permutation-based solution for the TSP that is randomly initialized by
    the randomized nearest-neighbor greedy construction: the tour starts from
    a randomly selected city and each next city is the closest unvisited one.
    """

    def copy(self) -> "TravelingSalespersonProblemSolutionNn":
        """
        Internal copy of the solution.
        """
        sol = TravelingSalespersonProblemSolutionNn(self.random_seed)
        sol.copy_from(self)
        return sol

    def init_random(self, problem: Problem) -> None:
        """
        Random initialization of the solution, by the nearest-neighbor greedy
        construction from a randomly selected starting city.

        :param `Problem` problem: problem that is solved
        """
        if not isinstance(problem, TravelingSalespersonProblem):
            raise TypeError("Parameter 'problem' must have type 'TravelingSalespersonProblem'.")

        dimension: int = problem.dimension
        distances: list[list[int]] = problem.distances
        start: int = randrange(dimension)
        unvisited: set[int] = set(range(dimension))
        unvisited.remove(start)
        representation: list[int] = [start]
        current: int = start
        while unvisited:
            current = min(unvisited, key=lambda city: distances[current][city])
            representation.append(current)
            unvisited.remove(current)
        self.representation = representation
