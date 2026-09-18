Traveling Salesperson Problem
=============================

.. _Problem_Traveling_Salesperson_Problem:

The Traveling Salesperson Problem (TSP) asks for the shortest cyclic tour
through a given set of cities:

- every city is visited exactly once and the tour returns to the starting city
- the total traveled distance is minimized

The TSP is NP-hard, so for larger instances it is solved heuristically.
Candidate solutions are naturally represented as permutations of city indexes.

In this project, the problem is represented by the
:class:`~opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem.TravelingSalespersonProblem`
class, while a solution with permutation representation is implemented in
:class:`~opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_solution.TravelingSalespersonProblemSolution`.

The objective value of a solution is the total length of the cyclic tour that
its permutation describes, while its fitness value is the negated tour length,
so that maximization of fitness corresponds to minimization of the tour length.

Implemented approaches
----------------------

The following approaches are currently supported for solving the problem:

- Genetic Algorithm (GA), with order (OX), partially mapped (PMX) and edge
  recombination (ERX) crossover, swap, scramble and inversion mutation,
  tournament or roulette selection, random or nearest-neighbor initialization,
  and an optional delta-evaluated 2-opt sweep over the offspring (memetic GA)
- Variable Neighborhood Search (VNS), with relocation shaking, best- and
  first-improvement or-opt local search and a delta-evaluated 2-opt + or-opt
  local search
- Tabu Search (TS) over permutations

Input file format
-----------------

Problem instances are read from a text file containing a square distance
matrix: ``n`` lines, each with ``n`` whitespace-separated numbers, where the
value in row ``i`` and column ``j`` is the distance from city ``i`` to city
``j``. Lines starting with ``#`` are treated as comments and skipped.

Example (3 cities):

.. code-block:: text

   0 10 15
   10 0 20
   15 20 0

Implemented approaches
----------------------

The following approaches are currently supported for solving the problem:

- Genetic Algorithm (GA) -- a memetic algorithm with edge recombination
  crossover (ERX), inversion mutation, a delta-evaluated 2-opt sweep over
  each offspring, tournament selection, elitism and nearest-neighbor
  initialization of the population
- Variable Neighborhood Search (VNS) -- relocation shaking with growing kick
  strength and a delta-evaluated 2-opt + or-opt local search
- Tabu Search (TS) over permutations

Examples of use
---------------

Examples are available in the project root directory:

- ``opt_so_comb_traveling_salesperson_ga_perm_exec.py``
- ``opt_so_comb_traveling_salesperson_vns_perm_exec.py``
- ``opt_so_comb_traveling_salesperson_tabu_search_permutation_exec.py``

Solver
------

The main command-line entry point is:

``opt/single_objective/comb/traveling_salesperson_problem/solver.py``

Example usage with Genetic Algorithm:

.. code-block:: bash

   poetry run python -m opt.single_objective.comb.traveling_salesperson_problem.solver \
      --input-file opt/single_objective/comb/traveling_salesperson_problem/inputs/usa-1.txt \
      --method ga

Example usage with Variable Neighborhood Search:

.. code-block:: bash

   poetry run python -m opt.single_objective.comb.traveling_salesperson_problem.solver \
      --input-file opt/single_objective/comb/traveling_salesperson_problem/inputs/usa-1.txt \
      --method vns

Example usage with Tabu Search:

.. code-block:: bash

   poetry run python -m opt.single_objective.comb.traveling_salesperson_problem.solver \
      --input-file opt/single_objective/comb/traveling_salesperson_problem/inputs/usa-1.txt \
      --method tabu \
      --evaluations-max 20000 \
      --tabu-tenure 10

Modules
-------

Problem module
^^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem
   :members:
   :undoc-members:
   :show-inheritance:

Solution module
^^^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_solution
   :members:
   :undoc-members:
   :show-inheritance:

GA support module
^^^^^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_support
   :members:
   :undoc-members:
   :show-inheritance:

GA selection module
^^^^^^^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_ga_selection
   :members:
   :undoc-members:
   :show-inheritance:

VNS support module
^^^^^^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_vns_support
   :members:
   :undoc-members:
   :show-inheritance:

Permutation solution module (tabu search)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.traveling_salesperson_problem.traveling_salesperson_problem_permutation_solution
   :members:
   :undoc-members:
   :show-inheritance:

Solver module
^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.traveling_salesperson_problem.solver
   :members:
   :undoc-members:
   :show-inheritance:
