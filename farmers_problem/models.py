from dataclasses import dataclass
from pulp import LpVariable


@dataclass
class CropVariables:
    potato: LpVariable
    carrot: LpVariable


@dataclass
class Inputs:
    potato_seeds_available: float  # in tons
    carrot_seeds_available: float  # in tons
    fertilizer_available: float    # in tons
    potato_profit_per_kg: float   # in dollars
    carrot_profit_per_kg: float   # in dollars

    @property
    def crops(self):
        return ["potato", "carrot"]
