"""Real-vector solution for the Branin minimization problem."""

from __future__ import annotations

from math import cos, pi
from typing import Optional

import numpy as np

from uo.solution.quality_of_solution import QualityOfSolution
from uo.solution.solution import Solution

from opt.single_objective.glob.branin_min_problem.branin_min_problem import BraninMinProblem


class BraninMinProblemRealSolution(Solution[np.ndarray, np.ndarray]):
    """Branin solution represented by ``[x1, x2]`` real coordinates."""

    def __init__(self, random_seed: Optional[int] = None) -> None:
        super().__init__(
            random_seed=random_seed,
            fitness_value=None,
            fitness_values=None,
            objective_value=None,
            objective_values=None,
            is_feasible=False,
        )

    def copy(self) -> BraninMinProblemRealSolution:
        """Return an independent copy of the solution."""
        result = BraninMinProblemRealSolution(self.random_seed)
        result.copy_from(self)
        return result

    def copy_from(self, original: Solution) -> None:
        """Copy all solution state from another solution."""
        super().copy_from(original)

    def argument(self, representation: np.ndarray) -> np.ndarray:
        """Return a copy of the represented Branin coordinates."""
        return self._validated_representation(representation).copy()

    def init_random(self, problem: BraninMinProblem) -> None:
        """Initialize a reproducible uniformly sampled point."""
        bounds = self._problem_bounds(problem)
        rng = np.random.default_rng(self.random_seed)
        self.representation = rng.uniform(bounds[:, 0], bounds[:, 1])

    def init_from(self, representation: np.ndarray, problem: BraninMinProblem) -> None:
        """Initialize from a finite, in-bounds two-dimensional vector."""
        point = self._validated_representation(representation)
        bounds = self._problem_bounds(problem)
        if np.any(point < bounds[:, 0]) or np.any(point > bounds[:, 1]):
            raise ValueError("representation must be inside the Branin bounds.")
        self.representation = point.copy()

    def calculate_quality_directly(
        self, representation: np.ndarray, problem: BraninMinProblem
    ) -> QualityOfSolution:
        """Calculate the Branin objective and corresponding maximized fitness."""
        point = self._validated_representation(representation)
        self._problem_bounds(problem)
        x1, x2 = point
        coefficient = 5.1 / (4.0 * pi**2)
        linear_coefficient = 5.0 / pi
        cosine_coefficient = 1.0 - 1.0 / (8.0 * pi)
        objective = (
            (x2 - coefficient * x1**2 + linear_coefficient * x1 - 6.0) ** 2
            + 10.0 * cosine_coefficient * cos(x1)
            + 10.0
        )
        objective = float(objective)
        return QualityOfSolution(
            objective_value=objective,
            objective_values=None,
            fitness_value=-objective,
            fitness_values=None,
            is_feasible=True,
        )

    def native_representation(self, representation_str: str) -> np.ndarray:
        """Parse coordinates such as ``[-3.14, 12.275]``."""
        if not isinstance(representation_str, str):
            raise TypeError("representation_str must be str.")
        normalized = representation_str.strip().strip("[]").replace(",", " ")
        point = np.fromstring(normalized, sep=" ", dtype=np.float64)
        return self._validated_representation(point).copy()

    def representation_distance_directly(
        self, representation_1: np.ndarray, representation_2: np.ndarray
    ) -> float:
        """Return Euclidean distance between two Branin vectors."""
        first = self._validated_representation(representation_1)
        second = self._validated_representation(representation_2)
        return float(np.linalg.norm(first - second))

    @staticmethod
    def _validated_representation(representation: np.ndarray) -> np.ndarray:
        try:
            point = np.asarray(representation, dtype=np.float64)
        except (TypeError, ValueError) as error:
            raise TypeError("representation must contain real numbers.") from error
        if point.shape != (2,):
            raise ValueError("representation must have shape (2,).")
        if not np.all(np.isfinite(point)):
            raise ValueError("representation must contain only finite values.")
        return point

    @staticmethod
    def _problem_bounds(problem: BraninMinProblem) -> np.ndarray:
        if not isinstance(problem, BraninMinProblem):
            raise TypeError("problem must be BraninMinProblem.")
        return problem.bounds

    def __str__(self) -> str:
        return self.string_rep("|")

    def __repr__(self) -> str:
        return self.string_rep("\n")

    def __format__(self, spec: str) -> str:
        return self.string_rep("|")
