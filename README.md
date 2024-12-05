# Container Packing Problem

This is a term project in the Linear Programming course at USC. Our work is to solve a container packing problem. A more detailed description can be found [here](./documents/description.md).

The problem is also known as [bin packing problem](https://en.wikipedia.org/wiki/Bin_packing_problem). The main challenge here is that each container has **3 constraints (weight, volume, pallets)** instead of a single constraint. We mainly use a **simulated annealing** method to approximate the optimal solution based on a greedy initial solution.

This project was completed by **Zijin Qin (Jin)** and **Zhou Zhang**.

## Catalog

[Problem Description](./documents/description.md)

[Results](./documents/results.md)


## How can I Run These Scripts?

Clone the project to the local directory.
```
git clone https://github.com/Jziumo/linear_programming_term_project.git
```

Activate the virtual environment in the root directory.

```
.\venv\Scripts\Activate.ps1
```

On the left side of the command line you should see `(venv)` instead of `(base)`.


Install the libraries listed in `requirements.txt` by running the following command:

```
py -m pip install -r requirements.txt
```

