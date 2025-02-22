import numpy as np
from leap_ec import context


def process_result(supply: np.ndarray, demand: np.ndarray) -> None:
    best_entry = context['track']['best_entry']
    generation = best_entry['generation']
    fittest = best_entry['best_individual']
    transport_plan = fittest.decode().reshape((len(supply), len(demand)))

    print(f"Optimal Transportation Plan reached in {generation}:\n", transport_plan)
    print("Total Cost:", fittest.fitness)
    print("Supply Violations:", np.sum(transport_plan, axis=1) - supply)
    print("Demand Violations:", demand - np.sum(transport_plan, axis=0))
