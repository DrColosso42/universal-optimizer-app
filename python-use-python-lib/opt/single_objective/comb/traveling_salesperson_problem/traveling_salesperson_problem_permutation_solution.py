import sys
from pathlib import Path

directory = Path(__file__).resolve()
sys.path.append(str(directory))
sys.path.append(str(directory.parent))
sys.path.append(str(directory.parent.parent.parent))
sys.path.append(str(directory.parent.parent.parent.parent))
root_dir = directory.parent.parent.parent.parent.parent
sys.path.append(str(root_dir))

from typing import Optional
from random import shuffle

from uo.problem.problem import Problem
from uo.solution.quality_of_solution import QualityOfSolution
from uo.solution.solution import Solution

from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem import (
    TravelingSalespersonProblem,
)


class TravelingSalespersonProblemPermutationSolution(Solution[list[int], list[int]]):

    def __init__(
        self,
        random_seed: Optional[int] = None,
        evaluation_cache_is_used: bool = False,
        evaluation_cache_max_size: int = 0,
        distance_calculation_cache_is_used: bool = False,
        distance_calculation_cache_max_size: int = 0
    ) -> None:
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

    def copy(self) -> "TravelingSalespersonProblemPermutationSolution":
        sol = TravelingSalespersonProblemPermutationSolution(self.random_seed)
        sol.copy_from(self)
        return sol

    def copy_from(self, original) -> None:
        super().copy_from(original)

    def argument(self, representation: list[int]) -> list[int]:
        return list(representation)

    def init_random(self, problem: Problem) -> None:
        if not hasattr(problem, "dimension") or problem.dimension is None:
            raise ValueError("Can not randomly initialize solution without problem dimension.")

        representation = list(range(problem.dimension))
        shuffle(representation)
        self.representation = representation

    def init_from(self, representation: list[int], problem: Problem) -> None:
        if not isinstance(representation, list):
            raise TypeError("Parameter 'representation' must have type 'list'.")
        if sorted(representation) != list(range(problem.dimension)):
            raise ValueError(
                "Parameter 'representation' must be a permutation of range(problem.dimension)."
            )
        self.representation = list(representation)

    def tour_length(self, representation: list[int], problem: TravelingSalespersonProblem) -> float:
        n = len(representation)
        total = 0.0
        for k in range(n):
            city_from = representation[k]
            city_to = representation[(k + 1) % n]
            total += problem.distance(city_from, city_to)
        return total

    def calculate_quality_directly(
        self,
        representation: list[int],
        problem: TravelingSalespersonProblem
    ) -> QualityOfSolution:
        if not isinstance(representation, list):
            raise TypeError("Parameter 'representation' must have type 'list'.")
        if not isinstance(problem, TravelingSalespersonProblem):
            raise TypeError("Parameter 'problem' must have type 'TravelingSalespersonProblem'.")
        if len(representation) != problem.dimension:
            raise ValueError("Representation length must match problem dimension.")

        length = self.tour_length(representation, problem)

        return QualityOfSolution(
            fitness_value=-length,
            fitness_values=None,
            objective_value=length,
            objective_values=None,
            is_feasible=True
        )

    def native_representation(self, representation_str: str) -> list[int]:
        if not isinstance(representation_str, str):
            raise TypeError("Parameter 'representation_str' must be 'str'.")
        stripped = representation_str.strip().lstrip("[").rstrip("]").strip()
        if stripped == "":
            return []
        return [int(part.strip()) for part in stripped.split(",")]

    def representation_distance_directly(
        self,
        solution_code_1: list[int],
        solution_code_2: list[int]
    ) -> int:
        if not isinstance(solution_code_1, list):
            raise TypeError("Parameter 'solution_code_1' should be 'list'.")
        if not isinstance(solution_code_2, list):
            raise TypeError("Parameter 'solution_code_2' should be 'list'.")
        if len(solution_code_1) != len(solution_code_2):
            raise ValueError("Representations should have the same length.")

        return sum(1 for a, b in zip(solution_code_1, solution_code_2) if a != b)

    def string_rep(
        self,
        delimiter: str = "\n",
        indentation: int = 0,
        indentation_symbol: str = "   ",
        group_start: str = "{",
        group_end: str = "}"
    ) -> str:
        s = group_start
        s += super().string_rep(
            delimiter=delimiter,
            indentation=indentation,
            indentation_symbol=indentation_symbol,
            group_start="",
            group_end=""
        )
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
