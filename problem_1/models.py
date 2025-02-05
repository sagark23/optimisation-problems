from dataclasses import dataclass

from pulp import LpVariable

RouteVariables = dict[str, dict[str, LpVariable]]


@dataclass
class Inputs:
    supply: dict[str, int]
    demand: dict[str, int]
    costs: dict[str, dict[str, int]]

    @property
    def warehouses(self):
        return list(self.supply.keys())

    @property
    def stores(self):
        return list(self.demand.keys())
