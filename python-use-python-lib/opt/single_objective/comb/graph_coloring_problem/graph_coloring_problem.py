"""
.. _py_graph_coloring_problem:
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


class GraphColoringProblem(Problem):
    """
    Class representing the Graph Coloring Problem.

    The problem is defined by:
    - number of vertices
    - graph edges

    A feasible solution assigns colors to vertices so that no two adjacent
    vertices have the same color. The goal is to minimize the number of used
    colors while maintaining a valid coloring.
    """

    def __init__(
        self,
        number_of_vertices: int,
        edges: list[tuple[int, int]],
    ) -> None:
        """
        Create new `GraphColoringProblem` instance.

        :param int number_of_vertices: number of graph vertices
        :param list[tuple[int, int]] edges: list of graph edges
        """
        if not isinstance(number_of_vertices, int):
            raise TypeError(
                "Parameter 'number_of_vertices' for GraphColoringProblem "
                "should be 'int'."
            )
        if not isinstance(edges, list):
            raise TypeError(
                "Parameter 'edges' for GraphColoringProblem should be 'list'."
            )
        if number_of_vertices <= 0:
            raise ValueError(
                "Parameter 'number_of_vertices' must be positive."
            )

        normalized_edges: list[tuple[int, int]] = []

        for edge in edges:
            if not isinstance(edge, tuple):
                raise ValueError(
                    "Each edge must be represented as a tuple."
                )
            if len(edge) != 2:
                raise ValueError(
                    "Each edge must contain exactly two vertices."
                )

            first_vertex, second_vertex = edge

            if (
                not isinstance(first_vertex, int)
                or not isinstance(second_vertex, int)
            ):
                raise ValueError(
                    "Edge vertices must be integers."
                )

            if first_vertex < 0 or second_vertex < 0:
                raise ValueError(
                    "Edge vertices must be non-negative integers."
                )

            if (
                first_vertex >= number_of_vertices
                or second_vertex >= number_of_vertices
            ):
                raise ValueError(
                    "Edge vertices must be smaller than "
                    "number_of_vertices."
                )

            if first_vertex == second_vertex:
                raise ValueError(
                    "Self-loops are not allowed in GraphColoringProblem."
                )

            normalized_edge = (
                min(first_vertex, second_vertex),
                max(first_vertex, second_vertex),
            )

            if normalized_edge not in normalized_edges:
                normalized_edges.append(normalized_edge)

        super().__init__(
            name="GraphColoringProblem",
            is_minimization=True,
            is_multi_objective=False,
        )

        self.__number_of_vertices = number_of_vertices
        self.__edges = normalized_edges
        self.__dimension = number_of_vertices

    def copy(self) -> "GraphColoringProblem":
        """
        Copy the target problem.
        """
        return GraphColoringProblem(
            number_of_vertices=self.number_of_vertices,
            edges=self.edges.copy(),
        )

    @classmethod
    def from_number_of_vertices_and_edges(
        cls,
        number_of_vertices: int,
        edges: list[tuple[int, int]],
    ) -> "GraphColoringProblem":
        """
        Additional constructor when number of vertices and edges are specified.
        """
        return cls(number_of_vertices, edges)

    @classmethod
    def __load_from_file__(
        cls,
        input_file_path: str,
    ) -> tuple[int, list[tuple[int, int]]]:
        """
        Static function that reads problem data from specified file.

        Expected file format:
            first line: number_of_vertices number_of_edges
            each next line: first_vertex second_vertex

        Example:
            4 4
            0 1
            1 2
            2 3
            3 0

        :param str input_file_path: path to the input file
        :return: number of vertices, edges
        :rtype: tuple[int, list[tuple[int, int]]]
        """
        logger.debug(
            "Load parameters: input file path=" + str(input_file_path)
        )

        with open(input_file_path, "r", encoding="utf-8") as file:
            lines = [
                line.strip()
                for line in file
                if line.strip()
            ]

        if len(lines) < 1:
            raise ValueError(
                "Input file must contain graph size information."
            )

        first_line_parts = lines[0].split()

        if len(first_line_parts) != 2:
            raise ValueError(
                "First line must contain exactly two integers: "
                "number_of_vertices and number_of_edges."
            )

        number_of_vertices = int(first_line_parts[0])
        number_of_edges = int(first_line_parts[1])

        if len(lines[1:]) != number_of_edges:
            raise ValueError(
                "Number of edge lines must match number_of_edges."
            )

        edges: list[tuple[int, int]] = []

        for line in lines[1:]:
            parts = line.split()

            if len(parts) != 2:
                raise ValueError(
                    "Each edge line must contain exactly two integers: "
                    "first_vertex and second_vertex."
                )

            first_vertex = int(parts[0])
            second_vertex = int(parts[1])

            edges.append((first_vertex, second_vertex))

        return number_of_vertices, edges

    @classmethod
    def from_input_file(
        cls,
        input_file_path: str,
    ) -> "GraphColoringProblem":
        """
        Additional constructor. Create new `GraphColoringProblem` instance
        when input file and input format are specified.

        :param str input_file_path: path to the input file
        :return: class instance
        :rtype: GraphColoringProblem
        """
        number_of_vertices, edges = cls.__load_from_file__(
            input_file_path
        )

        return cls(
            number_of_vertices=number_of_vertices,
            edges=edges,
        )

    @property
    def number_of_vertices(self) -> int:
        """
        Property getter for number of graph vertices.
        """
        return self.__number_of_vertices

    @property
    def edges(self) -> list[tuple[int, int]]:
        """
        Property getter for graph edges.
        """
        return self.__edges

    @property
    def dimension(self) -> int:
        """
        Property getter for problem dimension.
        """
        return self.__dimension

    def string_rep(
        self,
        delimiter: str,
        indentation: int = 0,
        indentation_symbol: str = "",
        group_start: str = "{",
        group_end: str = "}",
    ) -> str:
        """
        String representation of the `GraphColoringProblem` instance.
        """
        s = delimiter

        for _ in range(0, indentation):
            s += indentation_symbol

        s += group_start
        s += super().string_rep(
            delimiter,
            indentation,
            indentation_symbol,
            "",
            "",
        )
        s += delimiter
        s += "number_of_vertices=" + str(self.__number_of_vertices)
        s += delimiter
        s += "edges=" + str(self.__edges)
        s += delimiter
        s += "dimension=" + str(self.__dimension)
        s += group_end

        return s

    def __str__(self) -> str:
        return self.string_rep("|", 0, "", "{", "}")

    def __repr__(self) -> str:
        return self.string_rep("\n", 0, "   ", "{", "}")

    def __format__(self, spec: str = "") -> str:
        return self.string_rep("|")