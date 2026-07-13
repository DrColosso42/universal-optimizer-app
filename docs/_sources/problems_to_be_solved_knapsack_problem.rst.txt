Knapsack Problem
================

.. _Problem_Knapsack_Problem:

0/1 Knapsack problem consists of selecting a subset of items so that:

- total weight does not exceed the knapsack capacity
- total value is maximized

In this project, the problem is represented by the
:class:`~opt.single_objective.comb.knapsack_problem.knapsack_problem.KnapsackProblem`
class, while a solution with binary ``BitArray`` representation is implemented in
:class:`~opt.single_objective.comb.knapsack_problem.knapsack_problem_bit_array_solution.KnapsackProblemBitArraySolution`.

Implemented contributions
-------------------------

1. Representation of the problem in class
   :class:`~opt.single_objective.comb.knapsack_problem.knapsack_problem.KnapsackProblem`
   and solution with ``BitArray`` representation in class
   :class:`~opt.single_objective.comb.knapsack_problem.knapsack_problem_bit_array_solution.KnapsackProblemBitArraySolution`.

2. Genetic Algorithm method with binary ``BitArray`` solution representation.

3. Variable Neighborhood Search method with binary ``BitArray`` solution representation.

4. Entry point for all implemented methods in file
   :file:`/opt/single_objective/comb/knapsack_problem/solver.py`,
   where all parameters that govern method execution are accessible through
   command-line arguments.

Input format
------------

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

Examples of use
---------------

Examples are available in the root project directory:

- ``opt_so_comb_knapsack_ga_bitarray_exec.py``
- ``opt_so_comb_knapsack_vns_bitarray_exec.py``

Command-line solver
-------------------

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
