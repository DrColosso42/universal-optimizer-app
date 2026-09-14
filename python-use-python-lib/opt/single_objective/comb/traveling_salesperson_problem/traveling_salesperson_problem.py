"""
..  _py_traveling_salesperson_problem:
"""

import sys
from pathlib import Path

directory = Path(__file__).resolve()
sys.path.append(str(directory.parent))
sys.path.append(str(directory.parent.parent))
sys.path.append(str(directory.parent.parent.parent))
sys.path.append(str(directory.parent.parent.parent.parent))
root_dir = directory.parent.parent.parent.parent.parent
sys.path.append(str(root_dir))

from uo.problem.problem import Problem
from uo.utils.logger import logger


class TravelingSalespersonProblem(Problem):
    """
    Class representing the Traveling Salesperson Problem (TSP).

    The problem is defined by a square matrix of distances between every pair of cities.
    A solution is a permutation (visiting order) of all cities, and the tour is closed --
    after visiting the last city, the salesperson returns to the first one. The goal is to
    minimize the total length of the tour.
    """

    def __init__(self, distance_matrix: list[list[float]]) -> None:
        """
        Create new `TravelingSalespersonProblem` instance.

        :param list[list[float]] distance_matrix: square matrix, where `distance_matrix[i][j]`
        is the distance between city `i` and city `j`
        """
        if not isinstance(distance_matrix, list):
            raise TypeError("Parameter 'distance_matrix' for TravelingSalespersonProblem should be 'list'.")
        if len(distance_matrix) < 2:
            raise ValueError("Parameter 'distance_matrix' must describe at least two cities.")
        dimension = len(distance_matrix)
        for row in distance_matrix:
            if not isinstance(row, list):
                raise TypeError("Each row of 'distance_matrix' should be 'list'.")
            if len(row) != dimension:
                raise ValueError("Parameter 'distance_matrix' must be a square matrix.")
            if any((not isinstance(d, (int, float)) or d < 0) for d in row):
                raise ValueError("All distances must be non-negative numbers.")

        super().__init__(
            name="TravelingSalespersonProblem",
            is_minimization=True,
            is_multi_objective=False
        )

        self.__distance_matrix = distance_matrix
        self.__dimension = dimension

    def copy(self) -> "TravelingSalespersonProblem":
        """
        Copy the target problem.
        """
        return TravelingSalespersonProblem(
            distance_matrix=[row.copy() for row in self.__distance_matrix]
        )

    @classmethod
    def from_distance_matrix(cls, distance_matrix: list[list[float]]) -> "TravelingSalespersonProblem":
        """
        Additional constructor when the distance matrix is specified directly.
        """
        return cls(distance_matrix)

    @classmethod
    def __load_from_file__(cls, input_file_path: str) -> list[list[float]]:
        """
        Static function that reads problem data from specified file.

        Expected file format: `n` lines, each with `n` whitespace-separated numbers,
        describing a square distance matrix.

        Example (3 cities):
            0 10 15
            10 0 20
            15 20 0

        :param str input_file_path: path to the input file
        :return: distance matrix
        :rtype: list[list[float]]
        """
        logger.debug("Load parameters: input file path=" + str(input_file_path))

        with open(input_file_path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]

        if len(lines) == 0:
            raise ValueError("Input file must contain at least one line describing the distance matrix.")

        distance_matrix: list[list[float]] = []
        for line in lines:
            parts = line.split()
            row = [float(p) for p in parts]
            distance_matrix.append(row)

        return distance_matrix

    @classmethod
    def from_input_file(cls, input_file_path: str) -> "TravelingSalespersonProblem":
        """
        Additional constructor. Create new `TravelingSalespersonProblem` instance
        when input file with the distance matrix is specified.

        :param str input_file_path: path to the input file
        :return: class instance
        :rtype: TravelingSalespersonProblem
        """
        distance_matrix = cls.__load_from_file__(input_file_path)
        return cls(distance_matrix=distance_matrix)

    @property
    def distance_matrix(self) -> list[list[float]]:
        """
        Property getter for the distance matrix.
        """
        return self.__distance_matrix

    @property
    def dimension(self) -> int:
        """
        Property getter for problem dimension (number of cities).
        """
        return self.__dimension

    def distance(self, city_1: int, city_2: int) -> float:
        """
        Distance between two cities.

        :param int city_1: index of the first city
        :param int city_2: index of the second city
        :return: distance between the two cities
        :rtype: float
        """
        return self.__distance_matrix[city_1][city_2]

    def string_rep(
        self,
        delimiter: str,
        indentation: int = 0,
        indentation_symbol: str = "",
        group_start: str = "{",
        group_end: str = "}"
    ) -> str:
        """
        String representation of the `TravelingSalespersonProblem` instance.
        """
        s = delimiter
        for _ in range(0, indentation):
            s += indentation_symbol
        s += group_start
        s += super().string_rep(delimiter, indentation, indentation_symbol, "", "")
        s += delimiter
        s += "dimension=" + str(self.__dimension)
        s += delimiter
        s += "distance_matrix=" + str(self.__distance_matrix)
        s += group_end
        return s

    def __str__(self) -> str:
        return self.string_rep("|", 0, "", "{", "}")

    def __repr__(self) -> str:
        return self.string_rep("\n", 0, "   ", "{", "}")

    def __format__(self, spec: str = "") -> str:
        return self.string_rep("|")
