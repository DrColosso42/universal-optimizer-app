"""
..  _py_traveling_thief_problem:
"""

import sys
from pathlib import Path
from dataclasses import dataclass
from math import ceil, sqrt

directory = Path(__file__).resolve()
sys.path.append(str(directory.parent))
sys.path.append(str(directory.parent.parent))
sys.path.append(str(directory.parent.parent.parent))
sys.path.append(str(directory.parent.parent.parent.parent))
root_dir = directory.parent.parent.parent.parent.parent
sys.path.append(str(root_dir))

from uo.problem.problem import Problem
from uo.utils.logger import logger


@dataclass
class TtpItem:
    """
    Single item placed at a city: index, city, profit and weight.
    """
    index: int
    city: int
    profit: float
    weight: float


class TravelingThiefProblem(Problem):
    """
    Instance of the Traveling Thief Problem (TTP): cities, items placed
    at cities, knapsack capacity, speed range, and renting rate.

    Objective (maximization): profit of collected items minus
    renting_rate * total travel time.
    """

    def __init__(
        self,
        cities: list[tuple[float, float]],
        items: list[TtpItem],
        capacity: float,
        v_min: float,
        v_max: float,
        renting_rate: float,
        edge_weight_type: str = "EUC_2D"
    ) -> None:
        """
        Create new `TravelingThiefProblem` instance.

        :param list[tuple[float, float]] cities: city coordinates
        :param list[TtpItem] items: items placed at cities
        :param float capacity: knapsack capacity
        :param float v_min: thief speed when knapsack is full
        :param float v_max: thief speed when knapsack is empty
        :param float renting_rate: renting cost per unit of time
        :param str edge_weight_type: distance rounding, 'EUC_2D' or 'CEIL_2D'
        """
        if not isinstance(cities, list) or len(cities) == 0:
            raise ValueError("Parameter 'cities' must be a non-empty list.")
        if not isinstance(items, list):
            raise TypeError("Parameter 'items' must be 'list'.")
        if capacity <= 0:
            raise ValueError("Parameter 'capacity' must be positive.")
        if v_min <= 0 or v_max <= 0 or v_min > v_max:
            raise ValueError("Speeds must satisfy 0 < v_min <= v_max.")

        super().__init__(
            name="TravelingThiefProblem",
            is_minimization=False,
            is_multi_objective=False,
        )

        self.__cities = cities
        self.__items = items
        self.__capacity = capacity
        self.__v_min = v_min
        self.__v_max = v_max
        self.__renting_rate = renting_rate
        self.__n = len(cities)
        self.__m = len(items)

        self.__items_by_city: dict[int, list[TtpItem]] = {i: [] for i in range(self.__n)}
        for item in items:
            self.__items_by_city[item.city].append(item)

        self.__distances = self.__compute_distances(cities, edge_weight_type)

    @staticmethod
    def __compute_distances(
        cities: list[tuple[float, float]], edge_weight_type: str
    ) -> list[list[float]]:
        """
        Compute the pairwise distance matrix between cities.
        """
        n = len(cities)
        distances = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                dx = cities[i][0] - cities[j][0]
                dy = cities[i][1] - cities[j][1]
                d = sqrt(dx * dx + dy * dy)
                # CEIL_2D is a TSPLIB convention some .ttp instances use
                if edge_weight_type == "CEIL_2D":
                    d = ceil(d)
                distances[i][j] = d
        return distances

    def copy(self) -> "TravelingThiefProblem":
        """
        Copy the target problem.
        """
        return TravelingThiefProblem(
            cities=self.__cities.copy(),
            items=self.__items.copy(),
            capacity=self.__capacity,
            v_min=self.__v_min,
            v_max=self.__v_max,
            renting_rate=self.__renting_rate,
        )

    @classmethod
    def __load_from_file__(
        cls, input_file_path: str
    ) -> tuple[list[tuple[float, float]], list[TtpItem], float, float, float, float, str]:
        """
        Expected file format (TSPLIB-style):

            DIMENSION: <n>
            NUMBER OF ITEMS: <m>
            CAPACITY OF KNAPSACK: <capacity>
            MIN SPEED: <v_min>
            MAX SPEED: <v_max>
            RENTING RATIO: <renting_rate>
            EDGE_WEIGHT_TYPE: <EUC_2D|CEIL_2D>
            NODE_COORD_SECTION
            <id> <x> <y>                     (n rows)
            ITEMS SECTION
            <id> <profit> <weight> <city>    (m rows, 1-indexed)

        :param str input_file_path: path to the input file
        :return: cities, items, capacity, v_min, v_max, renting_rate, edge_weight_type
        :rtype: tuple[list[tuple[float, float]], list[TtpItem], float, float, float, float, str]
        """
        logger.debug("Load TTP instance: input file path=" + str(input_file_path))

        with open(input_file_path, "r", encoding="utf-8") as f:
            n = m = None
            capacity = v_min = v_max = renting_rate = None
            edge_weight_type = "EUC_2D"

            for line in f:
                if line.startswith("DIMENSION"):
                    n = int(line.split(":")[1].strip())
                elif line.startswith("NUMBER OF ITEMS"):
                    m = int(line.split(":")[1].strip())
                elif line.startswith("CAPACITY OF KNAPSACK"):
                    capacity = float(line.split(":")[1].strip())
                elif line.startswith("MIN SPEED"):
                    v_min = float(line.split(":")[1].strip())
                elif line.startswith("MAX SPEED"):
                    v_max = float(line.split(":")[1].strip())
                elif line.startswith("RENTING RATIO"):
                    renting_rate = float(line.split(":")[1].strip())
                elif line.startswith("EDGE_WEIGHT_TYPE"):
                    edge_weight_type = line.split(":")[1].strip()
                elif line.startswith("NODE_COORD_SECTION"):
                    break

            if n is None or m is None or capacity is None:
                raise ValueError("Input file missing required header fields.")

            cities: list[tuple[float, float]] = []
            for _ in range(n):
                _, x, y = f.readline().strip().split()
                cities.append((float(x), float(y)))

            f.readline()  # "ITEMS SECTION"

            items: list[TtpItem] = []
            for _ in range(m):
                item_id, profit, weight, city = f.readline().strip().split()
                items.append(
                    TtpItem(
                        index=int(item_id) - 1,
                        city=int(city) - 1,
                        profit=float(profit),
                        weight=float(weight),
                    )
                )

        return cities, items, capacity, v_min, v_max, renting_rate, edge_weight_type

    @classmethod
    def from_input_file(cls, input_file_path: str) -> "TravelingThiefProblem":
        """
        Additional constructor. Create new `TravelingThiefProblem` instance
        when input file and input format are specified.

        :param str input_file_path: path to the input file
        :return: class instance
        :rtype: TravelingThiefProblem
        """
        cities, items, capacity, v_min, v_max, renting_rate, edge_weight_type = (
            cls.__load_from_file__(input_file_path)
        )
        return cls(
            cities=cities,
            items=items,
            capacity=capacity,
            v_min=v_min,
            v_max=v_max,
            renting_rate=renting_rate,
            edge_weight_type=edge_weight_type,
        )

    @property
    def n(self) -> int:
        """
        Property getter for number of cities.
        """
        return self.__n

    @property
    def m(self) -> int:
        """
        Property getter for number of items.
        """
        return self.__m

    @property
    def cities(self) -> list[tuple[float, float]]:
        """
        Property getter for city coordinates.
        """
        return self.__cities

    @property
    def items(self) -> list[TtpItem]:
        """
        Property getter for items.
        """
        return self.__items

    @property
    def items_by_city(self) -> dict[int, list[TtpItem]]:
        """
        Property getter for items grouped by city.
        """
        return self.__items_by_city

    @property
    def capacity(self) -> float:
        """
        Property getter for knapsack capacity.
        """
        return self.__capacity

    @property
    def v_min(self) -> float:
        """
        Property getter for thief speed when knapsack is full.
        """
        return self.__v_min

    @property
    def v_max(self) -> float:
        """
        Property getter for thief speed when knapsack is empty.
        """
        return self.__v_max

    @property
    def renting_rate(self) -> float:
        """
        Property getter for renting cost per unit of time.
        """
        return self.__renting_rate

    @property
    def distances(self) -> list[list[float]]:
        """
        Property getter for the distance matrix between cities.
        """
        return self.__distances

    def string_rep(
        self, delimiter: str, indentation: int = 0, indentation_symbol: str = "",
        group_start: str = "{", group_end: str = "}"
    ) -> str:
        """
        String representation of the `TravelingThiefProblem` instance.
        """
        s = delimiter
        for _ in range(indentation):
            s += indentation_symbol
        s += group_start
        s += super().string_rep(delimiter, indentation, indentation_symbol, "", "")
        s += delimiter
        s += f"n={self.__n}" + delimiter
        s += f"m={self.__m}" + delimiter
        s += f"capacity={self.__capacity}" + delimiter
        s += f"v_min={self.__v_min}, v_max={self.__v_max}" + delimiter
        s += f"renting_rate={self.__renting_rate}"
        s += group_end
        return s

    def __str__(self) -> str:
        return self.string_rep("|", 0, "", "{", "}")

    def __repr__(self) -> str:
        return self.string_rep("\n", 0, "   ", "{", "}")

    def __format__(self, spec: str = "") -> str:
        return self.string_rep("|")
