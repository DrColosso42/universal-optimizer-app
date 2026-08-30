"""Definition of the bounded, two-dimensional Branin minimization problem."""

from __future__ import annotations

from math import pi

import numpy as np

from uo.problem.problem import Problem


class BraninMinProblem(Problem):
    """Standard Branin-Hoo benchmark problem."""

    KNOWN_MINIMUM = 0.39788735772973816

    def __init__(self) -> None:
        super().__init__("BraninMinProblem", True, False)
        self._bounds = np.asarray([(-5.0, 10.0), (0.0, 15.0)], dtype=np.float64)
        self._known_minimizers = np.asarray(
            [(-pi, 12.275), (pi, 2.275), (3.0 * pi, 2.475)],
            dtype=np.float64,
        )

    @property
    def dimension(self) -> int:
        """Return the number of decision variables."""
        return 2

    @property
    def bounds(self) -> np.ndarray:
        """Return a copy of the lower and upper bounds."""
        return self._bounds.copy()

    @property
    def known_minimizers(self) -> np.ndarray:
        """Return copies of the three known global minimizers."""
        return self._known_minimizers.copy()

    @property
    def known_minimum(self) -> float:
        """Return the objective value at every global minimizer."""
        return self.KNOWN_MINIMUM

    def copy(self) -> BraninMinProblem:
        """Return an independent problem instance."""
        return BraninMinProblem()

    def string_rep(
        self,
        delimiter: str,
        indentation: int = 0,
        indentation_symbol: str = "",
        group_start: str = "{",
        group_end: str = "}",
    ) -> str:
        """Return a string representation of the problem."""
        result = super().string_rep(
            delimiter, indentation, indentation_symbol, group_start, ""
        )
        result += delimiter + "dimension=2"
        result += delimiter + "bounds=" + str(self._bounds.tolist())
        result += delimiter + group_end
        return result

    def __str__(self) -> str:
        return self.string_rep("|")

    def __repr__(self) -> str:
        return self.string_rep("\n")

    def __format__(self, spec: str) -> str:
        return self.string_rep("|")
