"""
..  _py_traveling_salesperson_problem_vns_support:

The :mod:`~opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_vns_support`
contains classes
:class:`~opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_vns_support.TravelingSalespersonProblemVnsShakingSupport`
and
:class:`~opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_vns_support.TravelingSalespersonProblemVnsLocalSearchSupport`,
that represent supporting parts of the `VNS` algorithm, where solution of the
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

from random import randrange
from typing import Optional

from uo.problem.problem import Problem
from uo.solution.solution import Solution
from uo.algorithm.metaheuristic.single_solution_metaheuristic import SingleSolutionMetaheuristic
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_shaking_support import (
    VnsShakingSupport,
)
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_ls_support import (
    VnsLocalSearchSupport,
)
from opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_support import (
    _matrix_is_symmetric,
    _two_opt_sweep,
)


class TravelingSalespersonProblemVnsShakingSupport(VnsShakingSupport[list[int], str]):
    """
    VNS shaking support for the Traveling Salesperson Problem, where solution
    has permutation representation.
    """

    def __init__(self, dimension: int) -> None:
        """
        Create new `TravelingSalespersonProblemVnsShakingSupport` instance.

        :param int dimension: number of cities of the solved problem
        """
        super().__init__(dimension=dimension)
        self.__ladder_k: Optional[int] = None
        self.__last_best_value: Optional[float] = None

    def copy(self) -> "TravelingSalespersonProblemVnsShakingSupport":
        """
        Copy the `TravelingSalespersonProblemVnsShakingSupport` instance.

        :return: new `TravelingSalespersonProblemVnsShakingSupport` instance
            with the same properties
        :rtype: TravelingSalespersonProblemVnsShakingSupport
        """
        return TravelingSalespersonProblemVnsShakingSupport(self.dimension)

    def shaking(self, k: int, problem: Problem, solution: Solution,
            optimizer: SingleSolutionMetaheuristic) -> bool:
        """
        Random VNS shaking of the permutation solution, determined as k random
        rewire moves, where a single city is relocated to a random position.

        :param int k: int parameter for VNS
        :param `Problem` problem: problem that is solved
        :param `Solution` solution: solution used for the problem that is solved
        :param `SingleSolutionMetaheuristic` optimizer: metaheuristic optimizer
            that is executed
        :return: if shaking is successful
        :rtype: bool
        """
        if optimizer.should_finish():
            return False
        if k < optimizer.k_min or k > optimizer.k_max:
            return False
        # classic VNS ladder, kept inside the support because the optimizer
        # always invokes shaking with k=k_min: after an improving cycle the
        # kick strength resets to k_min, after a failed cycle it grows, so the
        # search can escape the current basin of attraction
        best_value:Optional[float] = None
        if optimizer.best_solution is not None:
            best_value = optimizer.best_solution.objective_value
        if self.__ladder_k is None:
            self.__ladder_k = optimizer.k_min
        elif best_value is not None and self.__last_best_value is not None:
            if best_value < self.__last_best_value:
                self.__ladder_k = optimizer.k_min
            else:
                self.__ladder_k = min(self.__ladder_k + 1, optimizer.k_max)
        self.__last_best_value = best_value
        k = self.__ladder_k
        dimension:int = self.dimension
        # classic VNS: shake the incumbent (best-so-far) instead of the
        # current solution, which may have drifted after failed cycles
        source_representation:list[int] = solution.representation
        if optimizer.best_solution is not None:
            source_representation = optimizer.best_solution.representation
        representation:list[int] = solution.representation
        representation[:] = source_representation
        original_representation:list[int] = source_representation.copy()
        tries:int = 0
        limit:int = 100
        while tries < limit:
            for _ in range(0, k):
                source:int = randrange(dimension)
                city:int = representation[source]
                del representation[source]
                destination:int = randrange(dimension - 1)
                representation.insert(destination, city)
            if representation != original_representation:
                break
            tries += 1
        if tries < limit:
            if optimizer.should_finish():
                solution.representation = original_representation
                return False
            optimizer.write_output_values_if_needed("before_evaluation", "b_e")
            optimizer.evaluation += 1
            solution.evaluate(problem)
            optimizer.write_output_values_if_needed("after_evaluation", "a_e")
            return True
        else:
            solution.representation = original_representation
            return False

    def string_rep(self, delimiter: str, indentation: int = 0, indentation_symbol: str = '',
            group_start: str = '{', group_end: str = '}') -> str:
        """
        String representation of the vns support instance.

        :param delimiter: delimiter between fields
        :type delimiter: str
        :param indentation: level of indentation
        :type indentation: int, optional, default value 0
        :param indentation_symbol: indentation symbol
        :type indentation_symbol: str, optional, default value ''
        :param group_start: group start string
        :type group_start: str, optional, default value '{'
        :param group_end: group end string
        :type group_end: str, optional, default value '}'
        :return: string representation of vns support instance
        :rtype: str
        """
        return 'TravelingSalespersonProblemVnsShakingSupport'

    def __str__(self) -> str:
        """
        String representation of the vns support instance.

        :return: string representation of the vns support instance
        :rtype: str
        """
        return self.string_rep('|')

    def __repr__(self) -> str:
        """
        Representation of the vns support instance.

        :return: string representation of the vns support instance
        :rtype: str
        """
        return self.string_rep('\n')

    def __format__(self, spec: str) -> str:
        """
        Formatted the vns support instance.

        :param str spec: format specification
        :return: formatted vns support instance
        :rtype: str
        """
        return self.string_rep('|')


class TravelingSalespersonProblemVnsLocalSearchSupportDelta(
        VnsLocalSearchSupport[list[int], str]):
    """
    VNS local search support for the TSP based on the or-opt procedure with
    delta (incremental) move evaluation: candidate relocations of blocks of at
    most k consecutive cities are evaluated by O(1) delta calculation on the
    distance matrix, so a full local search call consumes only one evaluation
    from the optimization budget. The evaluation budget of the optimizer is
    therefore spent on shaking and on confirming improved solutions, not on
    rescanning the neighborhood.
    """

    def __init__(self, dimension: int) -> None:
        """
        Create new `TravelingSalespersonProblemVnsLocalSearchSupportDelta` instance.

        :param int dimension: number of cities of the solved problem
        """
        super().__init__(dimension=dimension)
        self.__symmetric: Optional[bool] = None

    def copy(self) -> "TravelingSalespersonProblemVnsLocalSearchSupportDelta":
        """
        Copy the `TravelingSalespersonProblemVnsLocalSearchSupportDelta` instance.
        """
        return TravelingSalespersonProblemVnsLocalSearchSupportDelta(self.dimension)

    def local_search(self, k: int, problem: Problem, solution: Solution,
            optimizer: SingleSolutionMetaheuristic) -> bool:
        """
        Executes the or-opt local search procedure with delta evaluation,
        where blocks of at most k consecutive cities are relocated to better
        positions, until no improving relocation exists.

        :param int k: int parameter for VNS, determining the maximal length of
            the relocated block of consecutive cities
        :param `Problem` problem: problem that is solved
        :param `Solution` solution: solution used for the problem that is solved
        :param `SingleSolutionMetaheuristic` optimizer: metaheuristic optimizer
            that is executed
        :return: result of the local search procedure
        :rtype: bool
        """
        if optimizer.should_finish():
            return False
        if k < optimizer.k_min or k > optimizer.k_max:
            return False
        dimension:int = self.dimension
        if k >= dimension:
            return False
        distances:list[list[int]] = problem.distances
        representation:list[int] = solution.representation
        if self.__symmetric is None:
            self.__symmetric = _matrix_is_symmetric(distances)
        changed:bool = False
        improved:bool = True
        while improved:
            improved = False
            if optimizer.should_finish():
                break
            # 2-opt phase: exchange crossing edges (delta evaluated, so it
            # does not consume evaluations from the optimization budget)
            while _two_opt_sweep(distances, representation, self.__symmetric):
                changed = True
                improved = True
            # or-opt phase: relocate blocks of up to k consecutive cities;
            # always scan the full block range (up to k_max) for thoroughness,
            # since the optimizer resets the ladder to k_min after improvements
            for block_size in range(1, optimizer.k_max + 1):
                for source in range(dimension - block_size + 1):
                    first:int = representation[source]
                    last:int = representation[source + block_size - 1]
                    before:int = representation[(source - 1) % dimension]
                    after:int = representation[(source + block_size) % dimension]
                    gap:int = (distances[before][first] + distances[last][after]
                            - distances[before][after])
                    if gap <= 0:
                        continue
                    for position in range(dimension):
                        if (source <= position <= source + block_size - 2
                                or position == (source - 1) % dimension
                                or position == (source + block_size - 1) % dimension):
                            continue
                        left:int = representation[position]
                        right:int = representation[(position + 1) % dimension]
                        insertion:int = (distances[left][first] + distances[last][right]
                                - distances[left][right])
                        if gap - insertion > 0:
                            block:list[int] = representation[source:source + block_size]
                            del representation[source:source + block_size]
                            target:int = representation.index(left)
                            representation[target + 1:target + 1] = block
                            changed = True
                            improved = True
                            break
                    if improved:
                        break
                if improved:
                    break
        if changed:
            optimizer.write_output_values_if_needed("before_evaluation", "b_e")
            optimizer.evaluation += 1
            solution.evaluate(problem)
            optimizer.write_output_values_if_needed("after_evaluation", "a_e")
            # report improvement only when the descended candidate is actually
            # better than the incumbent: the optimizer overwrites its
            # best_solution whenever local_search returns True, without any
            # comparison, so returning True for a candidate that is worse than
            # the incumbent would degrade the best-so-far solution
            is_better_result:Optional[bool] = solution.is_better(
                    optimizer.best_solution, problem)
            return optimizer.best_solution is None or bool(is_better_result)
        return False

    def string_rep(self, delimiter: str, indentation: int = 0, indentation_symbol: str = '',
            group_start: str = '{', group_end: str = '}') -> str:
        """
        String representation of the vns support instance.
        """
        return 'TravelingSalespersonProblemVnsLocalSearchSupportDelta'

    def __str__(self) -> str:
        return self.string_rep('|')

    def __repr__(self) -> str:
        return self.string_rep('\n')

    def __format__(self, spec: str) -> str:
        return self.string_rep('|')
