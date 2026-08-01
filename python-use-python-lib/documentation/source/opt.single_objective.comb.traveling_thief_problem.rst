Traveling Thief Problem
========================

.. _module_traveling_thief_problem:

Problem description
--------------------

The Traveling Thief Problem (TTP) combines two NP-hard problems: a
Traveling Salesperson tour and a 0/1 Knapsack packing. Items picked up
along the tour make the thief heavier, which slows travel down and
increases the time-dependent renting cost.

In this application, the problem is represented by the
:class:`opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem.TravelingThiefProblem`
class, while candidate solutions combine a permutation-encoded tour with a
``BitArray``-encoded packing through the
:class:`opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem_solution.TravelingThiefProblemSolution`
class.

Input file format
------------------

Problem instances are read from a ``.ttp`` text file (TSPLIB-style).

Expected format:

.. code-block:: text

   DIMENSION: <n>
   NUMBER OF ITEMS: <m>
   CAPACITY OF KNAPSACK: <capacity>
   MIN SPEED: <v_min>
   MAX SPEED: <v_max>
   RENTING RATIO: <renting_rate>
   EDGE_WEIGHT_TYPE: <EUC_2D|CEIL_2D>
   NODE_COORD_SECTION
   <id> <x> <y>
   ITEMS SECTION
   <id> <profit> <weight> <city>

Implemented approaches
-----------------------

The following approaches are currently supported for solving the problem:

- Ant Colony Optimization (MMAS), fixed evaporation control (baseline)
- Ant Colony Optimization (MMAS), adaptive evaporation control

Examples of use
----------------

Examples are available in the project root directory:

- ``opt_so_comb_ttp_aco_exec.py``

Solver
------

The main command-line entry point is:

``opt/single_objective/comb/traveling_thief_problem/solver.py``

Example usage with the fixed evaporation strategy:

.. code-block:: bash

   poetry run python -m opt.single_objective.comb.traveling_thief_problem.solver \
      --input-file opt/single_objective/comb/traveling_thief_problem/data/tiny_n7_m6.ttp \
      --method fixed \
      --iterations-max 200

Example usage with the adaptive evaporation strategy:

.. code-block:: bash

   poetry run python -m opt.single_objective.comb.traveling_thief_problem.solver \
      --input-file opt/single_objective/comb/traveling_thief_problem/data/tiny_n7_m6.ttp \
      --method adaptive \
      --iterations-max 200 \
      --rho-scale 2.0

Modules
-------

Problem module
^^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem
   :members:
   :undoc-members:
   :show-inheritance:

Solution module
^^^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem_solution
   :members:
   :undoc-members:
   :show-inheritance:

ACO construction support module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem_aco_construction_support
   :members:
   :undoc-members:
   :show-inheritance:

Solver module
^^^^^^^^^^^^^

.. automodule:: opt.single_objective.comb.traveling_thief_problem.solver
   :members:
   :undoc-members:
   :show-inheritance:
