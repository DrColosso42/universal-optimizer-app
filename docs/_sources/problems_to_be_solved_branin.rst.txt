.. _Problem_Branin_Min:

Branin Minimization Problem
===========================

The Branin-Hoo function is a bounded, continuous, two-dimensional minimization
benchmark. It is multimodal and has three global minimizers with the same
objective value, which makes it a useful demonstration problem for Bayesian
optimization.

The search domain is ``x1 in [-5, 10]`` and ``x2 in [0, 15]``. The known minimum
objective is approximately ``0.397887`` at ``(-pi, 12.275)``, ``(pi, 2.275)``,
and ``(3*pi, 2.475)``.

Universal Optimizer compares solutions by maximizing fitness, so
:class:`opt.single_objective.glob.branin_min_problem.branin_min_problem_real_solution.BraninMinProblemRealSolution`
reports the Branin function as ``objective_value`` and its negative as
``fitness_value``.

Bayesian optimization example
-----------------------------

Run the deterministic example from ``python-use-python-lib``:

.. code-block:: console

   python opt_so_glob_min_branin_bo_real_exec.py

The example uses six random initial points, a total budget of 40 evaluations,
and random seed 17. It prints the best vector, objective, fitness, distance to
the nearest known minimizer, and evaluation statistics.
