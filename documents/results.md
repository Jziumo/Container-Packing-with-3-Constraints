# Results Analysis

[Return to the Homepage](https://github.com/Jziumo/linear_programming_term_project)

We have tried several methods to deal with 2 datasets, 

- Impracticable (Time Limit Exceeded)
  - build a mixed integer programming problem and use solver (provided by google or-tools)
- Worse Results
  - randomly fill until a container is full
- Unstable (easily stuck)
  - use the solver to handle small batches data (unstable)
  - use the solver to repack the orders in the containers with the lowest utilization rate
- Practicable
  - Greedy method using data sorted in different ways
  - Simulated Annealing based on a greedy initial solution

The number of containers runned by different methods are shown in the following table. 

|Method|Part (a)|Part (b)|
|------|--------|--------|
|Randomly Fill<br>(avg of $10^4$ tempts)|408.68|588.83|
|Greedy Method|296|431|
|Simulated Annealing|[293](./results_display/result_a_SM_293.txt)|[428](./results_display/result_b_SM_428.txt)|

You can click on the anchors on some number to see detailed solutions.

(You may need to use GBK encoding to view the solution files)

[Return to the Homepage](https://github.com/Jziumo/linear_programming_term_project)
