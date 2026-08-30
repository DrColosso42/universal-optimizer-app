"""
.. _py_graph_coloring_problem_int_solution:
"""

import sys
from pathlib import Path

directory = Path(__file__).resolve()
sys.path.append(str(directory.parent))
root_dir = directory.parent.parent.parent.parent.parent
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / "lib"))

from random import randint
from typing import Optional

from uo.problem.problem import Problem
from uo.solution.quality_of_solution import QualityOfSolution
from uo.solution.solution import Solution

from opt.single_objective.comb.graph_coloring_problem.graph_coloring_problem import (
    GraphColoringProblem,
)


class GraphColoringProblemIntSolution(Solution[int, str]):
    """
    Integer-encoded solution for the Graph Coloring Problem.

    The whole coloring is stored as one integer. Each vertex color is encoded
    using a fixed number of bits.

    The maximum number of available colors is equal to the number of graph
    vertices. The objective is to find a valid coloring that uses as few
    colors as possible.
    """

    def __init__(
        self,
        colors_count: int,
        random_seed: Optional[int] = None,
        evaluation_cache_is_used: bool = False,
        evaluation_cache_max_size: int = 0,
        distance_calculation_cache_is_used: bool = False,
        distance_calculation_cache_max_size: int = 0,
    ) -> None:
        if not isinstance(colors_count, int):
            raise TypeError(
                "Parameter 'colors_count' must be 'int'."
            )

        if colors_count <= 0:
            raise ValueError(
                "Parameter 'colors_count' must be positive."
            )

        if not isinstance(random_seed, int) and random_seed is not None:
            raise TypeError(
                "Parameter 'random_seed' must be 'int' or 'None'."
            )

        super().__init__(
            random_seed=random_seed,
            fitness_value=None,
            fitness_values=None,
            objective_value=None,
            objective_values=None,
            is_feasible=False,
            evaluation_cache_is_used=evaluation_cache_is_used,
            evaluation_cache_max_size=evaluation_cache_max_size,
            distance_calculation_cache_is_used=(
                distance_calculation_cache_is_used
            ),
            distance_calculation_cache_max_size=(
                distance_calculation_cache_max_size
            ),
        )

        self.colors_count = colors_count
        self.bits_per_color = max(
            1,
            (colors_count - 1).bit_length(),
        )
        self.is_minimization = True

    @property
    def value(self) -> float:
        """
        Value used by metaheuristic optimizers.

        Since fitness is maximized by the optimizers, value is equal to the
        fitness value. For this minimization problem fitness is the negative
        objective value.
        """
        if self.fitness_value is None:
            return float("-inf")

        return self.fitness_value

    def is_better_than(self, other: "GraphColoringProblemIntSolution") -> bool:
        """
        Compare two solutions by fitness value.

        A larger fitness value represents a better solution.
        """
        if not isinstance(other, GraphColoringProblemIntSolution):
            raise TypeError(
                "Parameter 'other' must have type "
                "'GraphColoringProblemIntSolution'."
            )

        if self.fitness_value is None:
            return False

        if other.fitness_value is None:
            return True

        return self.fitness_value > other.fitness_value

    def copy(self) -> "GraphColoringProblemIntSolution":
        """
        Internal copy of the solution.
        """
        sol = GraphColoringProblemIntSolution(
            colors_count=self.colors_count,
            random_seed=self.random_seed,
        )
        sol.copy_from(self)

        return sol

    def copy_from(self, original) -> None:
        """
        Copy all data from the original target solution.
        """
        super().copy_from(original)

    def argument(self, representation: int) -> str:
        """
        Convert internal representation to solution code.

        Since the number of available colors is equal to the number of
        vertices, colors_count is also the number of colors that must be
        decoded for printing.
        """
        coloring = self.decode_coloring(
            representation=representation,
            number_of_vertices=self.colors_count,
        )

        return " ".join(
            str(color)
            for color in coloring
        )

    def init_random(self, problem: Problem) -> None:
        """
        Random initialization of the solution.
        """
        if not isinstance(problem, GraphColoringProblem):
            raise TypeError(
                "Parameter 'problem' must have type "
                "'GraphColoringProblem'."
            )

        if self.colors_count != problem.number_of_vertices:
            raise ValueError(
                "The number of available colors must be equal to "
                "the number of graph vertices."
            )

        representation = 0

        for vertex in range(problem.number_of_vertices):
            color = randint(0, self.colors_count - 1)

            representation |= (
                color << (vertex * self.bits_per_color)
            )

        self.representation = representation

    def init_from(
        self,
        representation: int,
        problem: Problem,
    ) -> None:
        """
        Initialization of the solution by setting its native representation.
        """
        if not isinstance(representation, int):
            raise TypeError(
                "Parameter 'representation' must have type 'int'."
            )

        if representation < 0:
            raise ValueError(
                "Parameter 'representation' must be non-negative."
            )

        if not isinstance(problem, GraphColoringProblem):
            raise TypeError(
                "Parameter 'problem' must have type "
                "'GraphColoringProblem'."
            )

        if self.colors_count != problem.number_of_vertices:
            raise ValueError(
                "The number of available colors must be equal to "
                "the number of graph vertices."
            )

        self.representation = representation

    def decode_color(
        self,
        representation: int,
        vertex: int,
    ) -> int:
        """
        Decode the color assigned to one graph vertex.
        """
        mask = (1 << self.bits_per_color) - 1

        return (
            representation
            >> (vertex * self.bits_per_color)
        ) & mask

    def decode_coloring(
        self,
        representation: int,
        number_of_vertices: int,
    ) -> list[int]:
        """
        Decode colors of all graph vertices.

        The number of vertices is passed explicitly so that vertices assigned
        color zero are not omitted from the decoded representation.
        """
        if not isinstance(representation, int):
            raise TypeError(
                "Parameter 'representation' must have type 'int'."
            )

        if not isinstance(number_of_vertices, int):
            raise TypeError(
                "Parameter 'number_of_vertices' must have type 'int'."
            )

        if number_of_vertices <= 0:
            raise ValueError(
                "Parameter 'number_of_vertices' must be positive."
            )

        colors = []

        for vertex in range(number_of_vertices):
            colors.append(
                self.decode_color(representation, vertex)
            )

        return colors

    def used_colors_count(
        self,
        representation: int,
        problem: GraphColoringProblem,
    ) -> int:
        """
        Return the number of valid colors used by the representation.
        """
        if not isinstance(representation, int):
            raise TypeError(
                "Parameter 'representation' must have type 'int'."
            )

        if not isinstance(problem, GraphColoringProblem):
            raise TypeError(
                "Parameter 'problem' must have type "
                "'GraphColoringProblem'."
            )

        colors = self.decode_coloring(
            representation=representation,
            number_of_vertices=problem.number_of_vertices,
        )

        valid_colors = {
            color
            for color in colors
            if color < self.colors_count
        }

        return len(valid_colors)

    def calculate_quality_directly(
        self,
        representation: int,
        problem: GraphColoringProblem,
    ) -> QualityOfSolution:
        """
        Calculate the quality of a graph coloring.

        Invalid encoded colors receive the largest penalty. Conflicting
        adjacent vertices receive the next largest penalty. Among valid
        conflict-free colorings, the solution using fewer colors is better.
        """
        if not isinstance(representation, int):
            raise TypeError(
                "Parameter 'representation' must have type 'int'."
            )

        if not isinstance(problem, GraphColoringProblem):
            raise TypeError(
                "Parameter 'problem' must have type "
                "'GraphColoringProblem'."
            )

        if self.colors_count != problem.number_of_vertices:
            raise ValueError(
                "The number of available colors must be equal to "
                "the number of graph vertices."
            )

        conflicts = 0
        invalid_colors = 0
        used_colors = set()

        colors = self.decode_coloring(
            representation=representation,
            number_of_vertices=problem.number_of_vertices,
        )

        for color in colors:
            if color >= self.colors_count:
                invalid_colors += 1
            else:
                used_colors.add(color)

        for first_vertex, second_vertex in problem.edges:
            if colors[first_vertex] == colors[second_vertex]:
                conflicts += 1

        objective_value = float(
            1000000 * invalid_colors
            + 1000 * conflicts
            + len(used_colors)
        )

        fitness_value = -objective_value

        feasible = (
            invalid_colors == 0
            and conflicts == 0
        )

        return QualityOfSolution(
            fitness_value=fitness_value,
            fitness_values=None,
            objective_value=objective_value,
            objective_values=None,
            is_feasible=feasible,
        )

    def native_representation(
        self,
        representation_str: str,
    ) -> int:
        """
        Native solution representation from its string representation.
        """
        if not isinstance(representation_str, str):
            raise TypeError(
                "Parameter 'representation_str' must be 'str'."
            )

        return int(representation_str)

    def representation_distance_directly(
        self,
        solution_code_1: str,
        solution_code_2: str,
    ) -> int:
        """
        Bitwise Hamming distance between two integer solution codes.
        """
        if not isinstance(solution_code_1, str):
            raise TypeError(
                "Parameter 'solution_code_1' must be 'str'."
            )

        if not isinstance(solution_code_2, str):
            raise TypeError(
                "Parameter 'solution_code_2' must be 'str'."
            )

        first = int(solution_code_1)
        second = int(solution_code_2)

        return (first ^ second).bit_count()

    def string_rep(
        self,
        delimiter: str = "\n",
        indentation: int = 0,
        indentation_symbol: str = "   ",
        group_start: str = "{",
        group_end: str = "}",
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
            group_end="",
        )
        s += delimiter + "string_representation()="
        s += (
            ""
            if self.representation is None
            else self.argument(self.representation)
        )
        s += group_end

        return s

    def __str__(self) -> str:
        return self.string_rep("|", 0, "", "{", "}")

    def __repr__(self) -> str:
        return self.string_rep("\n", 0, "   ", "{", "}")

    def __format__(self, spec: str = "") -> str:
        return self.string_rep("|")