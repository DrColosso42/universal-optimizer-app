"""
.. _py_job_shop_scheduling_problem_permutation_solution:
"""

import sys
from pathlib import Path

directory = Path(__file__).resolve()
sys.path.append(str(directory.parent))
root_dir = directory.parent.parent.parent.parent.parent
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / "lib"))

from random import Random
from typing import Optional

from uo.problem.problem import Problem
from uo.solution.quality_of_solution import QualityOfSolution
from uo.solution.solution import Solution

from opt.single_objective.comb.job_shop_scheduling_problem.job_shop_scheduling_problem import (
    JobShopSchedulingProblem,
)


class JobShopSchedulingProblemPermutationSolution(Solution[list[int], str]):
    """
    Permutation encoded solution for the Job Shop Scheduling Problem.

    The representation is the encoding of Bierwirth, a permutation with repetition.

    The list is turned into a schedule by a decoder. 
    """

    def __init__(
        self,
        random_seed: Optional[int] = None,
        evaluation_cache_is_used: bool = False,
        evaluation_cache_max_size: int = 0,
        distance_calculation_cache_is_used: bool = False,
        distance_calculation_cache_max_size: int = 0,
    ) -> None:
        """
        Create new `JobShopSchedulingProblemPermutationSolution` instance.

        :param Optional[int] random_seed: random seed used for initialization
        """
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

        self.is_minimization = True

    @property
    def value(self) -> float:
        """
        Fitness value used by metaheuristic optimizers.

        """
        if self.fitness_value is None:
            return float("-inf")

        return self.fitness_value

    def is_better_than(
        self,
        other: "JobShopSchedulingProblemPermutationSolution",
    ) -> bool:
        """
        Compare two solutions by fitness value.

        A larger fitness value represents a better solution, that is a shorter makespan.
        """
        if not isinstance(other, JobShopSchedulingProblemPermutationSolution):
            raise TypeError(
                "Parameter 'other' must have type "
                "'JobShopSchedulingProblemPermutationSolution'."
            )

        if self.fitness_value is None:
            return False

        if other.fitness_value is None:
            return True

        return self.fitness_value > other.fitness_value

    def copy(self) -> "JobShopSchedulingProblemPermutationSolution":
        """
        Copy the target solution.
        """
        duplicate = JobShopSchedulingProblemPermutationSolution(self.random_seed)
        duplicate.copy_from(self)

        return duplicate

    def copy_from(self, original: Solution) -> None:
        """
        Copy all data from the original target solution.
        """
        super().copy_from(original)

    def argument(self, representation: list[int]) -> str:
        """
        Argument of the target solution, the order in which operations are dispatched.

        :param list[int] representation: internal representation of the solution
        :return: job indices, separated by a single space
        :rtype: str
        """
        return " ".join(str(job) for job in representation)

    def native_representation(self, representation_str: str) -> list[int]:
        """
        Obtain the native representation out of its string form.

        :param str representation_str: job indices, separated by whitespace
        :return: internal representation of the solution
        :rtype: list[int]
        """
        return [int(part) for part in representation_str.split()]

    @staticmethod
    def sorted_representation(problem: JobShopSchedulingProblem) -> list[int]:
        """
        The multiset of job indices that every representation of this problem must contain.

        :param JobShopSchedulingProblem problem: problem that is solved
        :return: index of every job, repeated as many times as that job has operations
        :rtype: list[int]
        """
        representation: list[int] = []

        for job_index, job in enumerate(problem.jobs):
            representation.extend([job_index] * len(job))

        return representation

    def init_random(self, problem: Problem) -> None:
        """
        Random initialization of the solution.

        :param Problem problem: problem that is solved
        """
        if not isinstance(problem, JobShopSchedulingProblem):
            raise TypeError(
                "Parameter 'problem' must have type 'JobShopSchedulingProblem'."
            )

        representation = self.sorted_representation(problem)
        Random(self.random_seed).shuffle(representation)

        self.representation = representation

    def init_from(self, representation: list[int], problem: Problem) -> None:
        """
        Initialization of the solution by setting its native representation.

        :param list[int] representation: internal representation of the solution
        :param Problem problem: problem that is solved
        """
        if not isinstance(representation, list):
            raise TypeError(
                "Parameter 'representation' must have type 'list'."
            )
        if not isinstance(problem, JobShopSchedulingProblem):
            raise TypeError(
                "Parameter 'problem' must have type 'JobShopSchedulingProblem'."
            )
        if sorted(representation) != self.sorted_representation(problem):
            raise ValueError(
                "Parameter 'representation' must contain the index of every job exactly as many "
                "times as that job has operations."
            )

        self.representation = list(representation)

    def schedule(
        self,
        representation: list[int],
        problem: JobShopSchedulingProblem,
    ) -> dict:
        """
        Decode the representation into a schedule.


        :param list[int] representation: internal representation of the solution
        :param JobShopSchedulingProblem problem: problem that is solved
        :return: makespan, and the start and the end of every operation, keyed by the pair of
        job index and index of the operation within that job
        :rtype: dict
        """
        if sorted(representation) != self.sorted_representation(problem):
            raise ValueError(
                "Parameter 'representation' does not encode a schedule of the supplied problem."
            )

        job_ready: list[int] = [0] * problem.number_of_jobs
        machine_ready: list[int] = [0] * problem.number_of_machines
        operation_counter: list[int] = [0] * problem.number_of_jobs
        start: dict[tuple[int, int], int] = {}
        end: dict[tuple[int, int], int] = {}

        for job_index in representation:
            operation_index = operation_counter[job_index]
            machine, duration = problem.jobs[job_index][operation_index]
            started_at = max(job_ready[job_index], machine_ready[machine])
            finished_at = started_at + duration
            job_ready[job_index] = finished_at
            machine_ready[machine] = finished_at
            start[(job_index, operation_index)] = started_at
            end[(job_index, operation_index)] = finished_at
            operation_counter[job_index] += 1

        return {
            "makespan": max(job_ready),
            "start": start,
            "end": end,
        }

    def calculate_quality_directly(
        self,
        representation: list[int],
        problem: Problem,
    ) -> QualityOfSolution:
        """
        Calculate the quality of the solution, that is the makespan of the schedule it encodes.


        :param list[int] representation: internal representation of the solution
        :param Problem problem: problem that is solved
        :return: quality of the solution
        :rtype: QualityOfSolution
        """
        if not isinstance(problem, JobShopSchedulingProblem):
            raise TypeError(
                "Parameter 'problem' must have type 'JobShopSchedulingProblem'."
            )

        makespan = self.schedule(representation, problem)["makespan"]

        return QualityOfSolution(
            objective_value=makespan,
            objective_values=None,
            fitness_value=-makespan,
            fitness_values=None,
            is_feasible=True,
        )

    def representation_distance_directly(
        self,
        representation_1: list[int],
        representation_2: list[int],
    ) -> float:
        """
        Distance between two representations, the number of positions at which they differ.

        :param list[int] representation_1: first representation
        :param list[int] representation_2: second representation
        :return: distance between the two representations
        :rtype: float
        """
        if len(representation_1) != len(representation_2):
            raise ValueError(
                "Representations must be of the same length."
            )

        return float(
            sum(1
                for first, second in zip(representation_1, representation_2)
                if first != second)
        )

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
        s += "representation=" + str(self.representation)
        s += group_end

        return s

    def __str__(self) -> str:
        return self.string_rep("|", 0, "", "{", "}")

    def __repr__(self) -> str:
        return self.string_rep("\n", 0, "   ", "{", "}")

    def __format__(self, spec: str = "") -> str:
        return self.string_rep("|")
