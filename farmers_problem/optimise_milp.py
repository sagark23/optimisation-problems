from pulp import *

def solve_extended_farming_problem():
    # Crop data
    crops = ["potato", "carrot", "lettuce", "tomato"]

    profit = {
        "potato": 1.4, "carrot": 1.6, "lettuce": 1.5, "tomato": 1.9
    }
    setup_cost = {
        "potato": 400, "carrot": 800, "lettuce": 600, "tomato": 700
    }
    fertilizer_use = {
        "potato": 1, "carrot": 1, "lettuce": 0.5, "tomato": 1.2
    }
    labour_use = {
        "potato": 0.5, "carrot": 0.8, "lettuce": 1.2, "tomato": 1.5
    }
    land_use = {
        "potato": 1.0, "carrot": 1.2, "lettuce": 0.8, "tomato": 1.5
    }
    equipment_required = {
        "potato": 0, "carrot": 0, "lettuce": 1, "tomato": 1
    }
    max_plant = {
        "potato": 3000, "carrot": 4000, "lettuce": 2000, "tomato": 1500
    }

    # New resource limits
    fertilizer_available = 6000
    labour_available = 5000
    land_available = 5500
    equipment_available = 2

    # Penalty for exceeding labour (soft constraint)
    labour_penalty_per_unit = 2.0  # penalty per unit of extra labour

    # Variables
    crop_amount = LpVariable.dicts("crop_amount", crops, 0)
    plant_crop = LpVariable.dicts("plant_crop", crops, cat=LpBinary)
    labour_overuse = LpVariable("labour_overuse", 0)

    # Problem
    prob = LpProblem("Extended_Farming_Knapsack_Labour_Soft_Constraint", LpMaximize)

    # Objective (with labour penalty)
    prob += (
        lpSum([
            profit[crop] * crop_amount[crop] - setup_cost[crop] * plant_crop[crop]
            for crop in crops
        ]) - labour_penalty_per_unit * labour_overuse
    ), "Total_Net_Profit_With_Labour_Penalty"

    # Constraints
    prob += lpSum([fertilizer_use[crop] * crop_amount[crop] for crop in crops]) <= fertilizer_available, "Fertilizer_Limit"
    prob += lpSum([labour_use[crop] * crop_amount[crop] for crop in crops]) <= labour_available + labour_overuse, "Labour_Limit_Soft"
    prob += lpSum([land_use[crop] * crop_amount[crop] for crop in crops]) <= land_available, "Land_Limit"
    prob += lpSum([equipment_required[crop] * plant_crop[crop] for crop in crops]) <= equipment_available, "Equipment_Limit"

    for crop in crops:
        prob += crop_amount[crop] <= max_plant[crop] * plant_crop[crop], f"Link_{crop}"

    # Solve
    prob.solve()

    # Results
    print("\n📊 Extended MILP Results (Labour Soft Constraint):")
    print(f"Status: {LpStatus[prob.status]}")
    print(f"Net Profit (with labour penalty): £{value(prob.objective):.2f}")
    print(f"Labour overuse: {value(labour_overuse):.2f} units (penalty applied if > 0)")
    for crop in crops:
        if value(plant_crop[crop]) > 0.5:
            print(f"- Plant {value(crop_amount[crop]):.2f} kg of {crop} ✅")
        else:
            print(f"- Do not plant {crop} ❌")

if __name__ == "__main__":
    solve_extended_farming_problem()


