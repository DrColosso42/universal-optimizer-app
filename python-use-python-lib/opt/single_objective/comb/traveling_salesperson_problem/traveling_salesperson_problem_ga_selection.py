"""
..  _py_traveling_salesperson_problem_ga_selection:

The :mod:`~opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_selection`
contains class
:class:`~opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_selection.TravelingSalespersonProblemGaSelectionTournament`,
that represents the selection operator of the `GA` algorithm, where solution of
the Traveling Salesperson Problem has permutation representation.
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

from random import randint
from typing import Optional

from uo.solution.solution import Solution
from uo.algorithm.metaheuristic.genetic_algorithm.ga_optimizer import GaOptimizer
from uo.algorithm.metaheuristic.genetic_algorithm.ga_selection import GaSelection


class TravelingSalespersonProblemGaSelectionTournament(GaSelection):
    """
    Tournament selection for the GA algorithm, where solution of the
    Traveling Salesperson Problem has permutation representation.

    The tournament of the specified number of randomly chosen individuals is
    held for each selection slot, where the individual with the best fitness
    value wins the tournament.
    """

    def __init__(self, tournament_size: int = 3) -> None:
        """
        Create new `TravelingSalespersonProblemGaSelectionTournament` instance.

        :param int tournament_size: number of individuals that participate in
            each tournament
        """
        if not isinstance(tournament_size, int):
            raise TypeError("Parameter 'tournament_size' must be 'int'.")
        if tournament_size < 2:
            raise ValueError("Parameter 'tournament_size' must be at least 2.")
        self.__tournament_size: int = tournament_size

    def copy(self) -> "TravelingSalespersonProblemGaSelectionTournament":
        """
        Copy the `TravelingSalespersonProblemGaSelectionTournament` instance.

        :return: new `TravelingSalespersonProblemGaSelectionTournament` instance
            with the same properties
        :rtype: TravelingSalespersonProblemGaSelectionTournament
        """
        return TravelingSalespersonProblemGaSelectionTournament(self.tournament_size)

    @property
    def tournament_size(self) -> int:
        """
        Property getter for tournament size.

        :return: number of individuals that participate in each tournament
        :rtype: int
        """
        return self.__tournament_size

    @staticmethod
    def __wins(candidate: Solution, incumbent: Solution) -> bool:
        """
        Checks if the candidate individual wins the comparison with the
        incumbent individual, with respect to fitness value.
        """
        if incumbent.fitness_value is None:
            return True
        if candidate.fitness_value is None:
            return False
        return candidate.fitness_value > incumbent.fitness_value

    def selection(self, optimizer: GaOptimizer) -> None:
        """
        GA tournament selection.

        :return:
        :rtype: None
        """
        pop: Optional[list[Solution]] = optimizer.current_population
        if pop is None:
            raise AttributeError("Population should exist!")
        n: int = len(pop)
        if n <= 0:
            raise AttributeError("Population should contain at least one individual")
        n_e: Optional[int] = optimizer.elite_count
        if n_e is None:
            l_lim: int = 0
        else:
            l_lim: int = n_e
        temp: list[Solution] = []
        for _ in range(l_lim, n):
            winner: Solution = pop[randint(0, n - 1)]
            for _ in range(self.__tournament_size - 1):
                candidate: Solution = pop[randint(0, n - 1)]
                if self.__wins(candidate, winner):
                    winner = candidate
            temp.append(winner)
        for i in range(l_lim, n):
            pop[i] = temp[i - l_lim]

    def string_rep(self, delimiter: str, indentation: int = 0, indentation_symbol: str = '',
            group_start: str = '{', group_end: str = '}') -> str:
        """
        String representation of the ga selection instance.

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
        :return: string representation of ga selection instance
        :rtype: str
        """
        return 'TravelingSalespersonProblemGaSelectionTournament'

    def __str__(self) -> str:
        """
        String representation of the ga selection instance.

        :return: string representation of the ga selection instance
        :rtype: str
        """
        return self.string_rep('|')

    def __repr__(self) -> str:
        """
        Representation of the ga selection instance.

        :return: string representation of the ga selection instance
        :rtype: str
        """
        return self.string_rep('\n')

    def __format__(self, spec: str) -> str:
        """
        Formatted the ga selection instance.

        :param str spec: format specification
        :return: formatted ga selection instance
        :rtype: str
        """
        return self.string_rep('|')
