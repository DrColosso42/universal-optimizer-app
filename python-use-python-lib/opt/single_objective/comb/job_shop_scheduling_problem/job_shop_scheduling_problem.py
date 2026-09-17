"""
.. _py_job_shop_scheduling_problem:
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


class JobShopSchedulingProblem(Problem):
    """
    Class representing the Job Shop Scheduling Problem.

    The problem is defined by a list of jobs. Every job is an ordered list of operations, and every
    operation is a pair holding the machine that has to process it and the time that processing
    takes. Operations of one job have to be processed in the given order, a machine processes at
    most one operation at a time, and an operation cannot be interrupted once it has started.

    A solution is a schedule, that is an assignment of a starting time to every operation. The
    objective is the makespan, the moment at which the last operation is finished, and it is
    minimized.
    """

    def __init__(
        self,
        jobs: list[list[tuple[int, int]]],
    ) -> None:
        """
        Create new `JobShopSchedulingProblem` instance.

        :param list[list[tuple[int, int]]] jobs: for every job, the ordered list of its operations,
        where an operation is a pair holding the machine index and the processing time
        """
        if not isinstance(jobs, list):
            raise TypeError(
                "Parameter 'jobs' for JobShopSchedulingProblem should be 'list'."
            )
        if len(jobs) == 0:
            raise ValueError(
                "Parameter 'jobs' must contain at least one job."
            )

        machines: set[int] = set()

        for job in jobs:
            if not isinstance(job, list):
                raise TypeError(
                    "Each job must be represented as a 'list' of operations."
                )
            if len(job) == 0:
                raise ValueError(
                    "Each job must contain at least one operation."
                )
            for operation in job:
                if not isinstance(operation, tuple):
                    raise TypeError(
                        "Each operation must be represented as a tuple."
                    )
                if len(operation) != 2:
                    raise ValueError(
                        "Each operation must contain exactly two integers: "
                        "machine and duration."
                    )
                machine, duration = operation
                if not isinstance(machine, int) or not isinstance(duration, int):
                    raise TypeError(
                        "Machine and duration of an operation must be integers."
                    )
                if machine < 0:
                    raise ValueError(
                        "Machine of an operation must be a non-negative integer."
                    )
                if duration <= 0:
                    raise ValueError(
                        "Duration of an operation must be positive."
                    )
                machines.add(machine)

        number_of_machines: int = max(machines) + 1

        if len(machines) != number_of_machines:
            raise ValueError(
                "Machines must be indexed consecutively, starting from zero."
            )

        super().__init__(
            name="JobShopSchedulingProblem",
            is_minimization=True,
            is_multi_objective=False,
        )

        self.__jobs: list[list[tuple[int, int]]] = [list(job) for job in jobs]
        self.__number_of_jobs: int = len(jobs)
        self.__number_of_machines: int = number_of_machines
        self.__dimension: int = sum(len(job) for job in jobs)

    def copy(self) -> "JobShopSchedulingProblem":
        """
        Copy the target problem.
        """
        return JobShopSchedulingProblem(jobs=[list(job) for job in self.__jobs])

    @classmethod
    def from_jobs(
        cls,
        jobs: list[list[tuple[int, int]]],
    ) -> "JobShopSchedulingProblem":
        """
        Additional constructor when the list of jobs is specified.
        """
        return cls(jobs)

    @classmethod
    def __load_from_file__(
        cls,
        input_file_path: str,
    ) -> list[list[tuple[int, int]]]:
        """
        Static function that reads problem data from specified file.

        :param str input_file_path: path to the input file
        :return: for every job, the ordered list of its operations
        :rtype: list[list[tuple[int, int]]]
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
                "Input file must contain instance size information."
            )

        first_line_parts = lines[0].split()

        if len(first_line_parts) != 2:
            raise ValueError(
                "First line must contain exactly two integers: "
                "number_of_jobs and number_of_machines."
            )

        number_of_jobs = int(first_line_parts[0])
        number_of_machines = int(first_line_parts[1])

        if len(lines[1:]) != number_of_jobs:
            raise ValueError(
                "Number of job lines must match number_of_jobs."
            )

        jobs: list[list[tuple[int, int]]] = []

        for line in lines[1:]:
            parts = [int(part) for part in line.split()]

            if len(parts) != 2 * number_of_machines:
                raise ValueError(
                    "Each job line must contain exactly two integers per machine: "
                    "machine and duration of every operation."
                )

            jobs.append(list(zip(parts[0::2], parts[1::2])))

        return jobs

    @classmethod
    def from_input_file(
        cls,
        input_file_path: str,
    ) -> "JobShopSchedulingProblem":
        """
        Additional constructor. Create new `JobShopSchedulingProblem` instance
        when input file is specified.

        :param str input_file_path: path to the input file
        :return: class instance
        :rtype: JobShopSchedulingProblem
        """
        jobs = cls.__load_from_file__(input_file_path)

        return cls(jobs=jobs)

    @property
    def jobs(self) -> list[list[tuple[int, int]]]:
        """
        Getter for the jobs of the instance.
        """
        return self.__jobs

    @property
    def number_of_jobs(self) -> int:
        """
        Getter for number of jobs.
        """
        return self.__number_of_jobs

    @property
    def number_of_machines(self) -> int:
        """
        Gtter for number of machines.
        """
        return self.__number_of_machines

    @property
    def dimension(self) -> int:
        """
        Getter for problem dimension, that is the total number of operations.
        """
        return self.__dimension

    @property
    def lower_bound(self) -> int:
        """
        Getter for a trivial lower bound of the makespan.

        """
        longest_job: int = max(
            sum(duration for _, duration in job) for job in self.__jobs
        )
        machine_load: list[int] = [0] * self.__number_of_machines
        for job in self.__jobs:
            for machine, duration in job:
                machine_load[machine] += duration
        return max(longest_job, max(machine_load))

    def string_rep(
        self,
        delimiter: str,
        indentation: int = 0,
        indentation_symbol: str = "",
        group_start: str = "{",
        group_end: str = "}",
    ) -> str:
        """
        String representation of the `JobShopSchedulingProblem` instance.
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
        s += "number_of_jobs=" + str(self.__number_of_jobs)
        s += delimiter
        s += "number_of_machines=" + str(self.__number_of_machines)
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
