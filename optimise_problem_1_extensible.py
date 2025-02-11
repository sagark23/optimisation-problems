import json
from itertools import combinations

from pulp import LpInteger, LpMinimize, LpProblem, LpVariable, lpSum

from args_parser import cli_args
from problem_1.cbc import coin_cmd_solver
from problem_1.models import RouteVariables, Inputs
from problem_1.outputs import print_box, print_solution, create_gif


def solve_supply_chain(inputs: Inputs) -> tuple[LpProblem, RouteVariables]:
    problem = LpProblem('supply_chain_problem', LpMinimize)
    routes = [(w, s) for w in inputs.warehouses for s in inputs.stores]
    variables = LpVariable.dicts('route', (inputs.warehouses, inputs.stores), 0, None, LpInteger)

    transportation_cost = lpSum([variables[w][s] * inputs.costs[w][s] for (w, s) in routes])
    problem += (transportation_cost, 'total_cost')

    for w in inputs.warehouses:
        problem += (lpSum([variables[w][s] for s in inputs.stores]) <= inputs.supply[w], f'products_from_warehouse_{w}')

    for s in inputs.stores:
        problem += (lpSum([variables[w][s] for w in inputs.warehouses]) >= inputs.demand[s], f'products_to_store_{s}')

    print_box('Problem')
    print(problem)
    print_box('Run solver')
    problem.solve(coin_cmd_solver())

    return problem, variables


def solve_for(inputs: Inputs, visualise: bool) -> None:
    problem, route_variables = solve_supply_chain(inputs)
    print_solution(problem)

    if visualise:
        print()
        print_box("Create gif")

        for warehouse in inputs.warehouses:
            for store_1, store_2 in combinations(inputs.stores, 2):
                create_gif(
                    inputs.supply[warehouse], inputs.demand[store_1], inputs.demand[store_2],
                    warehouse, store_1, store_2
                )


if __name__ == '__main__':
    args = cli_args()

    with open(args.input_file) as f:
        solve_for(inputs=Inputs(**json.load(f)), visualise=args.visualise)
