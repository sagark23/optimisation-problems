from pulp import LpInteger, LpMinimize, LpProblem, LpVariable

from problem_1.cbc import coin_cmd_solver
from problem_1.outputs import print_box, print_solution


def solve_supply_chain(cost_to_s1: int, cost_to_s2: int, available_supply: int, s1_demand: int,
                       s2_demand: int) -> LpProblem:
    problem = LpProblem('supply_chain_problem', LpMinimize)
    to_s1 = LpVariable('W(a)_to_S(1)', 0, None, LpInteger)
    to_s2 = LpVariable('W(a)_to_S(2)', 0, None, LpInteger)

    problem += (cost_to_s1 * to_s1 + cost_to_s2 * to_s2, 'total_cost')

    problem += (to_s1 + to_s2 <= available_supply, f'products_from_warehouse_W(a)')

    problem += (to_s1 >= s1_demand, f'products_to_store_S(1)')
    problem += (to_s2 >= s2_demand, f'products_to_store_S(2)')

    print_box('Problem')
    print(problem)
    print_box('Run solver')
    problem.solve(coin_cmd_solver())

    return problem


if __name__ == '__main__':
    print_solution(
        solve_supply_chain(cost_to_s1=20, cost_to_s2=40, available_supply=1000, s1_demand=300, s2_demand=500)
    )
