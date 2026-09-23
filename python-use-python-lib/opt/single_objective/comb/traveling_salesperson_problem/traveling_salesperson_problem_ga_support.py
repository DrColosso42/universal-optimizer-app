"""
..  _py_traveling_salesperson_problem_ga_support:

The :mod:`~opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_support`
contains classes
:class:`~opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_support.TravelingSalespersonProblemGaCrossoverSupportErx`
and
:class:`~opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_support.TravelingSalespersonProblemGaMutationSupportInversion`,
that represent supporting parts of the `GA` algorithm, where solution of the
Traveling Salesperson Problem has permutation representation.
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

from random import randrange, random
from typing import Optional

from uo.problem.problem import Problem
from uo.solution.solution import Solution
from uo.algorithm.metaheuristic.population_based_metaheuristic import (
    PopulationBasedMetaheuristic,
)
from uo.algorithm.metaheuristic.genetic_algorithm.ga_crossover_support import (
    GaCrossoverSupport,
)
from uo.algorithm.metaheuristic.genetic_algorithm.ga_mutation_support import (
    GaMutationSupport,
)


def _matrix_is_symmetric(distances: list[list[int]]) -> bool:
    """
    Checks if the distance matrix is symmetric.
    """
    dimension: int = len(distances)
    return all(
        distances[i][j] == distances[j][i]
        for i in range(dimension)
        for j in range(dimension)
    )


def _two_opt_sweep(distances: list[list[int]], representation: list[int],
        symmetric: bool) -> bool:
    """
    Single first-improvement sweep of the 2-opt local search over the cyclic
    tour, improving the representation in place. Moves are evaluated by delta
    calculation (O(1) per move for symmetric matrices), so the sweep does not
    consume evaluations from the optimization budget.

    :param list[list[int]] distances: distance matrix of the problem
    :param list[int] representation: tour that is improved in place
    :param bool symmetric: if the distance matrix is symmetric
    :return: if the representation has been changed
    :rtype: bool
    """
    dimension: int = len(representation)
    changed: bool = False
    for i in range(dimension - 1):
        for j in range(i + 2, dimension):
            if i == 0 and j == dimension - 1:
                continue
            a: int = representation[i]
            b: int = representation[i + 1]
            c: int = representation[j]
            e: int = representation[(j + 1) % dimension]
            delta: int = (distances[a][c] + distances[b][e]
                    - distances[a][b] - distances[c][e])
            if not symmetric:
                for k in range(i + 1, j):
                    delta += (distances[representation[k + 1]][representation[k]]
                            - distances[representation[k]][representation[k + 1]])
            if delta < 0:
                representation[i + 1:j + 1] = reversed(representation[i + 1:j + 1])
                changed = True
    return changed


class TravelingSalespersonProblemGaMutationSupportInversion(GaMutationSupport[list[int], str]):
    """
    GA mutation support for the TSP based on inversion: with the mutation
    probability per gene, a random segment of the tour is reversed (a 2-opt
    style move). The operator preserves permutation validity.
    """

    def __init__(self, mutation_probability: float, apply_two_opt: bool = False) -> None:
        """
        Create new `TravelingSalespersonProblemGaMutationSupportInversion` instance.

        :param float mutation_probability: probability of the mutation
        :param bool apply_two_opt: if a 2-opt sweep is applied to the mutated
            individual (memetic GA)
        """
        self.__mutation_probability: float = mutation_probability
        self.__apply_two_opt: bool = apply_two_opt
        self.__symmetric: Optional[bool] = None

    def copy(self) -> "TravelingSalespersonProblemGaMutationSupportInversion":
        """
        Copy the `TravelingSalespersonProblemGaMutationSupportInversion` instance.
        """
        return TravelingSalespersonProblemGaMutationSupportInversion(
                self.mutation_probability, self.__apply_two_opt)

    @property
    def mutation_probability(self) -> float:
        """
        Property getter for mutation probability.
        """
        return self.__mutation_probability

    def mutation(self, problem: Problem, solution: Solution,
            optimizer: PopulationBasedMetaheuristic) -> None:
        """
        GA individual mutation determined as an inversion (reversal) of a
        random segment of the tour, which preserves permutation validity.

        :param `Problem` problem: problem that is solved
        :param `Solution` solution: individual that is mutated
        :param `PopulationBasedMetaheuristic` optimizer: metaheuristic optimizer
            that is executed
        :return: None
        """
        if solution.representation is None:
            return
        dimension:int = len(solution.representation)
        changed:bool = False
        for i in range(dimension):
            if random() < self.__mutation_probability:
                j:int = randrange(dimension)
                lo:int = min(i, j)
                hi:int = max(i, j)
                if hi > lo:
                    solution.representation[lo:hi + 1] = \
                        reversed(solution.representation[lo:hi + 1])
                    changed = True
        if self.__apply_two_opt:
            if self.__symmetric is None:
                self.__symmetric = _matrix_is_symmetric(problem.distances)
            changed |= _two_opt_sweep(problem.distances, solution.representation,
                    self.__symmetric)
        if not changed:
            return
        optimizer.write_output_values_if_needed("before_evaluation", "b_e")
        optimizer.evaluation += 1
        solution.evaluate(problem)
        optimizer.write_output_values_if_needed("after_evaluation", "a_e")

    def string_rep(self, delimiter: str, indentation: int = 0, indentation_symbol: str = '',
            group_start: str = '{', group_end: str = '}') -> str:
        """
        String representation of the ga support instance.
        """
        return 'TravelingSalespersonProblemGaMutationSupportInversion'

    def __str__(self) -> str:
        return self.string_rep('|')

    def __repr__(self) -> str:
        return self.string_rep('\n')

    def __format__(self, spec: str) -> str:
        return self.string_rep('|')


class TravelingSalespersonProblemGaCrossoverSupportErx(GaCrossoverSupport[list[int], str]):
    """
    GA edge recombination crossover (ERX) support for the TSP: each child is
    built by inheriting as many edges from the parents as possible, which
    makes it well suited for the TSP objective.
    """

    def __init__(self, crossover_probability: float) -> None:
        """
        Create new `TravelingSalespersonProblemGaCrossoverSupportErx` instance.

        :param float crossover_probability: probability of the crossover
        """
        self.__crossover_probability: float = crossover_probability

    def copy(self) -> "TravelingSalespersonProblemGaCrossoverSupportErx":
        """
        Copy the `TravelingSalespersonProblemGaCrossoverSupportErx` instance.
        """
        return TravelingSalespersonProblemGaCrossoverSupportErx(self.crossover_probability)

    @property
    def crossover_probability(self) -> float:
        """
        Property getter for crossover probability.
        """
        return self.__crossover_probability

    @staticmethod
    def __edge_recombination(parent_1: list[int], parent_2: list[int]) -> list[int]:
        """
        Edge recombination operator: starting from the first city of the first
        parent, the child is extended by the unvisited neighbor (from either
        parent) with the fewest unvisited neighbors, ties broken randomly.

        :param list[int] parent_1: first parent
        :param list[int] parent_2: second parent
        :return: child permutation
        :rtype: list[int]
        """
        dimension: int = len(parent_1)
        edge_table: dict[int, set[int]] = {city: set() for city in parent_1}
        for parent in (parent_1, parent_2):
            for position in range(dimension):
                city: int = parent[position]
                edge_table[city].add(parent[(position - 1) % dimension])
                edge_table[city].add(parent[(position + 1) % dimension])
        current: int = parent_1[0]
        child: list[int] = []
        remaining: set[int] = set(parent_1)
        while True:
            child.append(current)
            remaining.discard(current)
            if not remaining:
                break
            for neighbors in edge_table.values():
                neighbors.discard(current)
            options: set[int] = edge_table[current] & remaining
            if not options:
                options = remaining
            current = min(options,
                    key=lambda city: (len(edge_table[city] & remaining), random()))
        return child

    def crossover(self, problem: Problem, solution1: Solution, solution2: Solution,
            child1: Solution, child2: Solution,
            optimizer: PopulationBasedMetaheuristic) -> None:
        """
        Executes edge recombination crossover (ERX) within GA, which preserves
        permutation validity of both children.

        :param `Problem` problem: problem that is solved
        :param `Solution` solution1: first parent
        :param `Solution` solution2: second parent
        :param `Solution` child1: first child that is created
        :param `Solution` child2: second child that is created
        :param `PopulationBasedMetaheuristic` optimizer: optimizer that is executed
        :rtype: None
        """
        if solution1.representation is None or solution2.representation is None:
            child1.copy_from(solution1)
            child2.copy_from(solution2)
            return
        child1.copy_from(solution1)
        child2.copy_from(solution2)
        if random() > self.__crossover_probability:
            return
        child1.representation = self.__edge_recombination(
            solution1.representation, solution2.representation
        )
        child2.representation = self.__edge_recombination(
            solution2.representation, solution1.representation
        )
        optimizer.evaluation += 2
        child1.evaluate(problem)
        child2.evaluate(problem)

    def string_rep(self, delimiter: str, indentation: int = 0, indentation_symbol: str = '',
            group_start: str = '{', group_end: str = '}') -> str:
        """
        String representation of the ga support instance.
        """
        return 'TravelingSalespersonProblemGaCrossoverSupportErx'

    def __str__(self) -> str:
        return self.string_rep('|')

    def __repr__(self) -> str:
        return self.string_rep('\n')

    def __format__(self, spec: str) -> str:
        return self.string_rep('|')
