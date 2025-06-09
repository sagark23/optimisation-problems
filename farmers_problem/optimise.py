from pulp import LpProblem, LpMaximize, LpVariable, LpStatus, value

from .cbc import coin_cmd_solver
from .models import Inputs, CropVariables


def create_variables() -> CropVariables:
    return CropVariables(
        potato=LpVariable("potato_seeds", 0, None),
        carrot=LpVariable("carrot_seeds", 0, None)
    )


def create_problem(inputs: Inputs, variables: CropVariables) -> LpProblem:
    prob = LpProblem("Farmers_Optimization", LpMaximize)

    # Objective Function
    prob += (
        inputs.potato_profit_per_kg * variables.potato +
        inputs.carrot_profit_per_kg * variables.carrot,
        "Total_Profit"
    )

    # Constraints
    # 1. Available potato seeds
    prob += variables.potato <= inputs.potato_seeds_available, "Potato_Seeds_Limit"

    # 2. Available carrot seeds
    prob += variables.carrot <= inputs.carrot_seeds_available, "Carrot_Seeds_Limit"

    # 3. Fertilizer constraint (1:1 ratio)
    prob += (
        variables.potato + variables.carrot <= inputs.fertilizer_available,
        "Fertilizer_Limit"
    )

    return prob


def solve_problem(inputs: Inputs) -> dict:
    variables = create_variables()
    prob = create_problem(inputs, variables)

    # Solve using CBC solver
    prob.solve(coin_cmd_solver())

    # Prepare results
    results = {
        "status": LpStatus[prob.status],
        "potato_seeds": value(variables.potato),
        "carrot_seeds": value(variables.carrot),
        "total_profit": value(prob.objective),
        "fertilizer_used": value(variables.potato) + value(variables.carrot),
        "remaining_potato": inputs.potato_seeds_available - value(variables.potato),
        "remaining_carrot": inputs.carrot_seeds_available - value(variables.carrot),
        "remaining_fertilizer": inputs.fertilizer_available - (value(variables.potato) + value(variables.carrot))
    }

    return results


def print_results(results: dict) -> None:
    print("\nOptimization Results:")
    print(f"Status: {results['status']}")
    print("\nOptimal Planting Plan:")
    print(f"Potato seeds to plant: {results['potato_seeds']:.2f} tons")
    print(f"Carrot seeds to plant: {results['carrot_seeds']:.2f} tons")
    print(f"Maximum profit: ${results['total_profit']:.2f}")

    print("\nResource Usage:")
    print(f"Total fertilizer used: {results['fertilizer_used']:.2f} tons")
    print(f"Remaining potato seeds: {results['remaining_potato']:.2f} tons")
    print(f"Remaining carrot seeds: {results['remaining_carrot']:.2f} tons")
    print(f"Remaining fertilizer: {results['remaining_fertilizer']:.2f} tons")


def main():
    inputs = Inputs(
        potato_seeds_available=3000,
        carrot_seeds_available=4000,
        fertilizer_available=5000,
        potato_profit_per_kg=1.2,
        carrot_profit_per_kg=1.7
    )

    results = solve_problem(inputs)

    print_results(results)

