import random
from functools import partial

import numpy as np
from leap_ec import ops, Representation, context, Individual
from leap_ec.algorithm import generational_ea
from leap_ec.decoder import IdentityDecoder
from leap_ec.ops import UniformCrossover
from leap_ec.real_rep.ops import mutate_gaussian

from problem_2.probes import BestFitnessLoggerProbe
from problem_2.problem import TransportationProblem
from problem_2.outputs import process_result


def stop_fn(_population: list[Individual], generations: int) -> bool:
    current_generation = context['leap']['generation']
    best_generation = context.get('track', {}).get('best_entry', {}).get('generation', 0)

    threshold = min(5000, round(generations / 4))
    should_stop = current_generation - best_generation >= threshold
    if should_stop:
        print("Stopping at generation", current_generation, "because the solution has not improved in at least",
              threshold, "generations.")

    return should_stop


def optimise_with_ga() -> None:
    supply = np.array([2000, 3100, 100])
    demand = np.array([500, 900, 1800, 200, 700])
    cost_matrix = np.array([
        [20, 40, 50, 20, 10],
        [30, 10, 30, 20, 30],
        [10, 12, 16, 32, 14]
    ])

    num_warehouses = len(supply)
    num_stores = len(demand)
    genome_size = num_warehouses * num_stores
    representation = Representation(
        initialize=lambda: np.random.randint(0, np.max(supply), size=genome_size),
        decoder=IdentityDecoder(),
    )
    pop_size = 100
    elite_retention_count = round(pop_size / 2)
    generations = 20000

    generational_ea(
        max_generations=generations,
        pop_size=pop_size,
        problem=TransportationProblem(supply, demand, cost_matrix),
        representation=representation,
        pipeline=[
            ops.tournament_selection(k=3),
            ops.clone(),
            UniformCrossover(0.3),
            lambda pop: mutate_gaussian(
                pop, std=50, expected_num_mutations=random.randint(0, genome_size),
                bounds=(0, np.max(supply))
            ),
            ops.evaluate,
            ops.pool(size=pop_size),
            BestFitnessLoggerProbe(generations, elite_retention_count),
        ],
        k_elites=elite_retention_count,
        stop=partial(stop_fn, generations=generations)
    )

    process_result(supply, demand)


if __name__ == '__main__':
    optimise_with_ga()
