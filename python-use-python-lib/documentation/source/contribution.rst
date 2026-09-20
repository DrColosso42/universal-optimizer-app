How to Contribute
=================


This system is developed in `Python <https://www.python.org>`_ programming language, using `poetry <https://python-poetry.org>`_ as project and package manager, `unittest <https://docs.python.org/3/library/unitest.html>`_  library for unit testing and `Sphinx <https://www.sphinx-doc.org/en/master>`_ system for documentation generation. Same tool set should be use for contribution to the project.

Contribution is encouraged in following three domains:

a. Building application for solving optimization problems. Requirements:

    1. Program code for specific problem should to be put into the respective directory.

        - Each of the problems should have its own directory, with name equals to problem name. 
        
        - Code for multi-objective optimization should be placed under :file:`/opt/multi_objective/` directory, while code for single-objective optimization should be placed under :file:`/opt/single_objective/` directory.

        - Code for single-objective combinatorial optimization should be placed under :file:`opt/single_objective/comb/` directory, for single-objective constraint optimization within the :file:`/opt/single_objective/constraint/` directory, and code for single-objective global optimization in :file:`/opt/single_objective/global/` directory.
        

    2. Implemented applications should have examples of use for every approach contained within application. 
    
        - Those examples should be placed in root :file:`/` directory, and file name for example should be :file:`<problem>_<algorithm>_<representation>_exec.py`.


    3. For each problem under consideration, the problem class for specific problem should have method that read textual file and create instance of that specific problem.

    4. For each problem under consideration, there should be one file (named :file:`solver.py`, within the respective problem directory). That file will be entry point for all the methods aimed at solving the specific problem. All parameters that governs methods execution should be accessible to user through command-line parameters. Command-line parameters should have sufficient and adequate help system.


    5. Type hints and documentation.

        - All programming objects (classes, functions, variables, parameters, optional parameters etc.) should be `type-hinted <https://www.infoworld.com/article/3630372/get-started-with-python-type-hints.html>`_
        
        - All programming objects (classes, functions, etc.) should be properly documented using the system `Sphinx`, reStructuredText and doc comments within the code.

        - Problem that is solved should have separate documentation web page, where that problem is described and documented. At least, there should be the link from problem web page toward the web page that explains method that is used and vice versa.  


    6. Unit testing coverage.
    
        - Implemented programming code should be fully covered with unit tests, and `unittest` framework is used. 
        
        - Test should be placed into separate sub-directory under :file:`/opt/tests/` directory. Directory structure within :file:`/opt/tests/` directory should mirror directory structure of the :file:`/opt/` directory.  

        - All developed code should be covered with unit test, and test coverage rate should be not less than 80%. 

b. Designing and executing comparison experiments, using previously builded applications. Requirements: 

    1. Experiments should use only previously developed applications, not Python programming constructs. Comparison experiments should be invoked by batch/command file.

    2. Comparison experiments should be placed under :file:`/comparison/` directory.

c. Visualizing experimentally obtained data (either data about comparison, either data about algorithm execution). Requirements:

    1. Developed solution for the problems under consideration should be visualized. Visualizations should be invoked by batch/command file.

    2. Visualization efforts should be placed under :file:`/visualization/` directory.

Contributors
============

Contribution domains
--------------------

a. Contribution in solving **combinatorial** optimization problems:

    a.1. Ones Count Max Problem :ref:`Problem_Ones_Count_Max`:

        1. Representation of the problem (in class :class:`~opt.single_objective.comb.ones_count_max.OnesCountMaxProblem`) and solution (`BitArray`-based in class :class:`~opt.single_objective.comb.ones_count_max.OnesCountMaxProblemBitArraySolution` and `int`-based in class :class:`~opt.single_objective.comb.ones_count_max.OnesCountMaxProblemIntSolution`) - [VladimirFilipovic]_
        
        2. Integer Linear Programming method (using `linopy` library) - [VladimirFilipovic]_  

        3. Total Enumeration method, with solution that has binary `BitArray` representation - [VladimirFilipovic]_  

        4. Variable Neighborhood Search method, with solution that has binary `BitArray` representation - [VladimirFilipovic]_  

        5. Variable Neighborhood Search method, with solution that has binary `int` representation - [VladimirFilipovic]_  

        6. Genetic Algorithm method, with solution that has binary `BitArray` representation - [VladimirFilipovic]_  

        7. Entry point of the all methods for solving this problem, in file :file:`/opt/single_objective/comb/ones_count_max_problem/solver.py`. All parameters that governs method execution are accessible to user through command-line.  - [VladimirFilipovic]_  

    a.2. Minimum Multi Cut Problem :ref:`Problem_Minimum_Multi_Cut`:

        8. Representation of the problem (in class :class:`~opt.single_objective.comb.minimum_multi_cut_problem.MinMultiCutProblem`, that uses `ng.Graph` class for class representation) and solution with `BitArray`-based representation (in class :class:`~opt.single_objective.comb.minimum_multi_cut_problem.MinMultiCutProblemBitArraySolution`) - [MarkoRadosavljevic]_
        
        9. Variable Neighborhood Search method, with solution that has binary `BitArray` representation - [MarkoRadosavljevic]_  

        10. Genetic Algorithm method, with solution that has binary `BitArray` representation - [MarkoRadosavljevic]_  

    a.3. Set Covering Problem :ref:`Problem_Set_Covering`:

        11. Representation of the problem (in class :class:`~opt.single_objective.comb.set_covering_problem.set_covering_problem.MinSetCoverProblem`and solution with `BitArray`-based representation (in class :class:`~~opt.single_objective.comb.set_covering_problem.set_covering_problem_bit_array_solution.MinSetCoverProblemBitArraySolution`) - [AndjelaDamnjanovic]_
        
        12. Electromagnetism-like Metaheuristic method, with solution that has binary `BitArray` representation - [AndjelaDamnjanovic]_  

        13. ILP model, with `linopy` library and `Gurobi` solver - [AndjelaDamnjanovic]_ 

    a.4. Drug Discovery Problem :ref:`Problem_Drug_Discovery`:

        14. Representation of the problem (in class :class:`~opt.single_objective.comb.drug_discovering_problem.drug_discovering_problem.DrugDiscoveryProblem`) and solution with SMILES string-based representation (in class :class:`~~opt.single_objective.comb.drug_discovery_problem.individual.Individual`) - [LazarSavic]_

        15. Genetic Algorithm method, with fitness evaluation based solely on the QED (Quantitative Estimate of Drug-likeness) coefficient - [LazarSavic]_

        16. Entry point for the entire GUI solving this problem, in file :file:`opt_so_comb_drug_discovery_ga_exec.py`. All parameters that govern method execution are accessible to user through the graphical interface. - [LazarSavic]_


    a.9. :ref:`Job Shop Scheduling Problem <Problem_Job_Shop_Scheduling>`:

        1. Problem class, with reading of an instance from a textual file in the format of the OR-Library, and with a lower bound of the makespan derived from the longest job and the busiest machine - [NenadPesic]_

        2. Solution class with permutation with repetition representation, the encoding of Bierwirth, together with the decoder that turns an encoding into a semi-active schedule - [NenadPesic]_

        3. Simulated Annealing method, with solution that has permutation representation - [NenadPesic]_

        4. Variable Neighborhood Search method, with solution that has permutation representation, in both the first improvement and the best improvement variant - [NenadPesic]_

        5. Generational Genetic Algorithm method, with tournament selection and precedence preservative crossover, with solution that has permutation representation - [NenadPesic]_

        6. Entry point of the all methods for solving this problem, in file :file:`/opt/single_objective/comb/job_shop_scheduling_problem/solver.py`. All parameters that governs method execution are accessible to user through command-line - [NenadPesic]_

        7. Nine instances of the problem, taken from the OR-Library, together with one instance small enough for exhaustive search, which is used to test the decoder - [NenadPesic]_

b. Contribution in solving **global** optimization problems:


    b.1. Max Function One Variable Problem:

        1. Variable Neighborhood Search method, with solution that has binary `BitArray` representation - [VladimirFilipovic]_  

        2. Variable Neighborhood Search method, with solution that has binary `int` representation - [VladimirFilipovic]_  

        3. Entry point of the all methods for solving this problem, in file :file:`/opt/single_objective/glob/max_function_one_variable_problem/solver.py`. All parameters that governs method execution are accessible to user through command-line.  - [VladimirFilipovic]_  

Contributor List
----------------

.. [VladimirFilipovic] Vladimir Filipović, `<https://github.com/vladofilipovic>`_ e-mail: vladofilipovic@hotmail.com

.. [MarkoRadosavljevic] Marko Radosavljević, `<https://github.com/Markic01>`_ e-mail: mi20079@alas.matf.bg.ac.rs

.. [AndjelaDamnjanovic] Anđela Damjanović, `<https://github.com/AndjelaDamnjanovic>`_ e-mail: mi19059@alas.matf.bg.ac.rs

.. [LazarSavic] Lazar Savić, `<https://github.com/killica>`_ e-mail: mi21004@alas.matf.bg.ac.rs

.. [MarkoLazarevic] Marko Lazarević, `<https://github.com/marko-lazarevic>`_ e-mail: mi21098@alas.matf.bg.ac.rs

.. [StojanKostic] Stojan Kostić, `<https://github.com/Stojan-Kole>`_ e-mail: mi21131@alas.matf.bg.ac.rs

.. [NenadPesic] Nenad Pešić, `<https://github.com/DrColosso42>`_ e-mail: mi22062@alas.matf.bg.ac.rs
