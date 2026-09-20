.. _Problem_Job_Shop_Scheduling:

Job Shop Scheduling Problem
============================

Problem definition
-------------------

An instance is given by a set of `n` **jobs** and `m` **machines**. Every job is an ordered list
of **operations**, and every operation is a pair holding the machine that has to process it and
the time that processing takes. Three constraints apply:

* the operations of one job are processed in the given order, and the next one cannot start before
  the previous one is finished;
* a machine processes at most one operation at a time;
* an operation cannot be interrupted once it has started.

A solution is given as a schedule, an assignment of a starting time to every operation. The objective
is the makespan, the moment at which the last operation is finished, and it is minimized.



Lower bound
------------

No schedule can be shorter than the longest job, since its operations are processed one after
another, and none can be shorter than the total load of the busiest machine, for the same reason.
The larger of the two is a lower bound of the makespan. It is attained for the instances ``la01``
and ``la05`` distributed with this problem, which proves the optimality of a solution reaching it
without any solver.

Input format
-------------

The format is the one used by the OR-Library. The first line holds the number of jobs and the
number of machines. Every following line describes one job as pairs of machine and duration::

   3 3
   0 3 1 2 2 2
   0 2 2 1 1 4
   1 4 2 3 0 1

The first job is processed on machine 0 for three units of time, then on machine 1 for two, and
finally on machine 2 for two.

Instances
----------

Nine instances are distributed with the problem, taken from Fisher and Thompson
[FisherThompson1963]_ and from Lawrence [Lawrence1984]_. Their optimal makespans are known from
the literature.

+-----------+-----------+-------------+-------------+----------+
| Instance  | Jobs      | Machines    | Lower bound | Optimum  |
+===========+===========+=============+=============+==========+
| mini3     | 3         | 3           | 10          | 11       |
+-----------+-----------+-------------+-------------+----------+
| ft06      | 6         | 6           | 47          | 55       |
+-----------+-----------+-------------+-------------+----------+
| ft10      | 10        | 10          | 655         | 930      |
+-----------+-----------+-------------+-------------+----------+
| ft20      | 20        | 5           | 1119        | 1165     |
+-----------+-----------+-------------+-------------+----------+
| la01      | 10        | 5           | 666         | 666      |
+-----------+-----------+-------------+-------------+----------+
| la02      | 10        | 5           | 635         | 655      |
+-----------+-----------+-------------+-------------+----------+
| la03      | 10        | 5           | 588         | 597      |
+-----------+-----------+-------------+-------------+----------+
| la04      | 10        | 5           | 537         | 590      |
+-----------+-----------+-------------+-------------+----------+
| la05      | 10        | 5           | 593         | 593      |
+-----------+-----------+-------------+-------------+----------+

The instance ``mini3`` is small enough for exhaustive search: it has 1680 distinct encodings, and
enumerating all of them yields the optimum 11. It is used to test the decoder.

Solution representation
------------------------

The solution is encoded as a permutation with repetition, the encoding of Bierwirth
[BierwirthJSP1995]_. It is a list
in which the index of every job appears exactly as many times as that job has operations, so
``mini3`` is encoded by an ordering of ``[0, 0, 0, 1, 1, 1, 2, 2, 2]``. The `c`-th occurrence of
job `j` stands for the `c`-th operation of that job.

The list is turned into a schedule by a decoder that walks it from left to right and starts each
operation at the earliest time at which both its job and its machine are free. Schedules produced
this way are semi-active, and an optimal schedule is always among them.


Methods
--------

Three methods are available through the solver, all of them over the same representation and the
same decoder: simulated annealing, variable neighborhood search and a generational genetic
algorithm with tournament selection and PPX crossover.

Usage
------

.. code-block:: bash

   python -m opt.single_objective.comb.job_shop_scheduling_problem.solver \
       --input-file opt/single_objective/comb/job_shop_scheduling_problem/data/ft06.txt \
       --method sa --evaluations-max 20000

Every parameter of every method is available through a command line argument; see ``--help``.

Comparison and visualization
-----------------------------

The experiment under :file:`/comparison/job_shop_scheduling_problem/` compares the three methods
over seven instances with five random seeds each, giving all of them the same budget expressed as
the number of evaluations of the objective function. The script under
:file:`/visualization/job_shop_scheduling_problem/` draws a Gantt chart of the best schedule found
for every instance, one row per machine, with the boxes coloured by job.

API reference
--------------

See :doc:`opt.single_objective.comb.job_shop_scheduling_problem`.

References
-----------

.. [FisherThompson1963] Fisher, H.; Thompson, G. L. (1963). "Probabilistic learning combinations of local job-shop scheduling rules". Industrial Scheduling, Prentice Hall: 225-251.

.. [Lawrence1984] Lawrence, S. (1984). "Resource constrained project scheduling: an experimental investigation of heuristic scheduling techniques". Graduate School of Industrial Administration, Carnegie Mellon University.

.. [BierwirthJSP1995] Bierwirth, C. (1995). "A generalized permutation approach to job shop scheduling with genetic algorithms". OR Spektrum. 17 (2-3): 87-92.

.. [Manne1960] Manne, A. S. (1960). "On the job-shop scheduling problem". Operations Research. 8 (2): 219-223.
