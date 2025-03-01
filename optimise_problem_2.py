import json
import random
from functools import partial
from typing import TypedDict

import numpy as np
from leap_ec import ops, Representation, context, Individual
from leap_ec.algorithm import generational_ea
from leap_ec.decoder import IdentityDecoder
from leap_ec.ops import UniformCrossover
from leap_ec.real_rep.ops import mutate_gaussian
from numpy import ndarray

from args_parser import cli_args
from problem_2.outputs import process_result
from problem_2.probes import BestFitnessLoggerProbe
from problem_2.problem import TransportationProblem


def stop_fn(_population: list[Individual], generations: int) -> bool:
    current_generation = context['leap']['generation']
    best_generation = context.get('track', {}).get('best_entry', {}).get('generation', 0)

    threshold = min(5000, round(generations / 4))
    should_stop = current_generation - best_generation >= threshold
    if should_stop:
        print("Stopping at generation", current_generation, "because the solution has not improved in at least",
              threshold, "generations.")

    return should_stop


class GAInputs(TypedDict):
    supply: ndarray
    demand: ndarray
    costs: ndarray


def clean_inputs(supply: dict[str, int], demand: dict[str, int], costs: dict[str, dict[str, int]]) -> GAInputs:
    costs_matrix: list[list[int]] = [[costs[warehouse][store] for store in demand] for warehouse in supply]
    costs = np.array(costs_matrix)
    supply = np.array(list(supply.values()))
    demand = np.array(list(demand.values()))

    return {"supply": supply, "demand": demand, "costs": costs}


def optimise_with_ga(supply: ndarray[int], demand: ndarray[int], costs: ndarray[ndarray[int]]) -> None:
    num_warehouses = len(supply)
    num_stores = len(demand)
    genome_size = num_warehouses * num_stores
    representation = Representation(
        initialize=lambda: np.random.randint(0, np.max(supply), size=genome_size),
        decoder=IdentityDecoder(),
    )
    pop_size = 100
    elite_retention_count = 2
    generations = 20000

    generational_ea(
        max_generations=generations,
        pop_size=pop_size,
        problem=TransportationProblem(supply, demand, costs),
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
    args = cli_args()

    with open(args.input_file) as f:
        optimise_with_ga(**clean_inputs(**json.load(f)))
