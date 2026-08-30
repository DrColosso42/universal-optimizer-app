Traveling Thief Problem
========================

.. _Problem_Traveling_Thief_Problem:

The Traveling Thief Problem (TTP) combines two NP-hard problems:

- **Tour** - visit all cities exactly once (Traveling Salesperson Problem)
- **Packing** - select items from cities to carry home (0/1 Knapsack Problem)

Items picked up along the tour make the thief heavier, which slows travel
down and increases the time-dependent renting cost. Solving the tour and
the packing separately gives suboptimal solutions.

Objective (maximization):

.. code-block:: text

   f(tour, packing) = profit - renting_rate * total_time
   speed(w) = v_max - (w / W) * (v_max - v_min)

In this project, the problem is represented by the
:class:`~opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem.TravelingThiefProblem`
class, while a solution combining a tour and a packing is implemented in
:class:`~opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem_solution.TravelingThiefProblemSolution`.

Implemented contributions
--------------------------

1. Representation of the problem in class
   :class:`~opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem.TravelingThiefProblem`
   and solution combining a permutation-encoded tour with a ``BitArray``-encoded
   packing in class
   :class:`~opt.single_objective.comb.traveling_thief_problem.traveling_thief_problem_solution.TravelingThiefProblemSolution`.

2. Ant Colony Optimization (MMAS variant) method, with two evaporation
   control strategies: a fixed (deterministic) baseline and an adaptive
   strategy that reacts to the search's stagnation counter.

3. Entry point for all implemented methods in file
   :file:`/opt/single_objective/comb/traveling_thief_problem/solver.py`,
   where all parameters that govern method execution are accessible through
   command-line arguments.

Input format
------------

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

Examples of use
----------------

Examples are available in the project root directory:

- ``opt_so_comb_ttp_aco_exec.py``

Command-line solver
--------------------

Example usage with the fixed (baseline) evaporation strategy:

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
