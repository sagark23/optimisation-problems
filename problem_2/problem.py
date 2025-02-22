import numpy as np
from leap_ec.problem import ScalarProblem
from numpy import ndarray


class TransportationProblem(ScalarProblem):
    def __init__(self, supply, demand, cost_matrix):
        super().__init__(maximize=False)
        self.supply = supply
        self.num_warehouses = len(self.supply)
        self.demand = demand
        self.num_stores = len(demand)
        self.cost_matrix = cost_matrix

    def evaluate(self, solution: ndarray, *args, **kwargs):
        transport_matrix = solution.reshape((self.num_warehouses, self.num_stores))

        supply_violation = np.maximum(0, np.sum(transport_matrix, axis=1) - self.supply).sum()
        demand_violation = np.maximum(0, self.demand - np.sum(transport_matrix, axis=0)).sum()
        penalty = 1000 * (supply_violation + demand_violation)

        return np.sum(transport_matrix * self.cost_matrix) + penalty
