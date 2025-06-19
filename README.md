# Optimisation problem

This codebase demonstrates different optimisation techniques, including linear programming (LP), mixed-integer linear programming (MILP), and genetic algorithms. It is used for educational purposes and accompanies a talk given at various conferences.

## One time setup 

```shell
brew install uv
```

## How to run

```shell
# Linear programming (simple and extensible)
uv run optimise_problem_1_simple.py
uv run optimise_problem_1_extensible.py --input-file problem_1/simple.json
uv run optimise_problem_1_extensible.py --input-file problem_1/complex.json

# Mixed-Integer Linear Programming (Farmers Problem)
uv run farmers_problem/optimise_milp.py

# Genetic algorithm
uv run optimise_problem_2.py
```

## Problems Included

- **Problem 1:** Simple and extensible LP models for resource allocation
- **Farmers Problem:** MILP model for crop selection with resource and binary constraints (see `farmers_problem/`)
- **Problem 2:** Genetic algorithm for optimisation

See individual problem folders for detailed descriptions and mathematical formulations.

