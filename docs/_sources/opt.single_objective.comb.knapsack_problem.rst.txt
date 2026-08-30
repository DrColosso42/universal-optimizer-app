Knapsack Problem
================

.. _module_knapsack_problem:

Problem description
-------------------

The 0/1 Knapsack problem consists of selecting a subset of items so that:

- total weight does not exceed knapsack capacity
- total value is maximized

In this application, the problem is represented by the
:class:`opt.single_objective.comb.knapsack_problem.knapsack_problem.KnapsackProblem`
class, while candidate solutions are represented with bit arrays through the
:class:`opt.single_objective.comb.knapsack_problem.knapsack_problem_bit_array_solution.KnapsackProblemBitArraySolution`
class.

Input file format
-----------------

Problem instances are read from a text file.

Expected format:

- first line: capacity
- each following line: ``weight value``

Example:

.. code-block:: text

   15
   2 10
   3 5
   5 15
   7 7
   1 6
   4 18

Implemented approaches
----------------------

The following approaches are currently supported for solving the problem:

- Genetic Algorithm (GA)
- Variable Neighborhood Search (VNS)

Examples of use
---------------

Examples are available in the project root directory:

- ``opt_so_comb_knapsack_ga_bitarray_exec.py``
- ``opt_so_comb_knapsack_vns_bitarray_exec.py``

Solver
------

The main command-line entry point is:

``opt/single_objective/comb/knapsack_problem/solver.py``

Example usage with Genetic Algorithm:

.. code-block:: bash

   poetry run python -m opt.single_objective.comb.knapsack_problem.solver \
      --input-file opt/single_objective/comb/knapsack_problem/data/knapsack_01.txt \
      --method ga

Example usage with Variable Neighborhood Search:

.. code-block:: bash

   poetry run python -m opt.single_objective.comb.knapsack_problem.solver \
      --input-file opt/single_objective/comb/knapsack_problem/data/knapsack_01.txt \
      --method vns \
      --evaluations-max 15000 \
      --k-min 1 \
      --k-max 3

Modules
-------

Problem module
^^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.knapsack_problem.knapsack_problem
   :members:
   :undoc-members:
   :show-inheritance:

Solution module
^^^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.knapsack_problem.knapsack_problem_bit_array_solution
   :members:
   :undoc-members:
   :show-inheritance:

Solver module
^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.knapsack_problem.solver
   :members:
   :undoc-members:
   :show-inheritance:
