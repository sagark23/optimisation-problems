# Farmers Problem

This problem involves optimizing crop planting decisions to maximize profit while considering resource constraints.

## Problem Description

A farmer has the following resources:
- 3 tons of potato seeds
- 4 tons of carrot seeds
- 5 tons of fertilizer

The fertilizer must be used in a 1:1 ratio with seeds (1 kg of seeds requires 1 kg of fertilizer).

Profit margins:
- Potato seeds: $1.2/kg
- Carrot seeds: $1.7/kg

## Objective

Maximize the total profit by determining the optimal amount of potato and carrot seeds to plant, while respecting the resource constraints.

## Mathematical Formulation

### Decision Variables
- x₁: Amount of potato seeds to plant (in tons)
- x₂: Amount of carrot seeds to plant (in tons)

### Objective Function
Maximize: 1200x₁ + 1700x₂

### Constraints
1. Potato seeds available: x₁ ≤ 3
2. Carrot seeds available: x₂ ≤ 4
3. Fertilizer constraint: x₁ + x₂ ≤ 5
4. Non-negativity: x₁, x₂ ≥ 0

## Solution

The solution is implemented using PuLP, a linear programming library for Python. The implementation includes:
- Model definition using dataclasses
- Constraint formulation
- Solution using the CBC solver
- Detailed output analysis 