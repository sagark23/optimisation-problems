# Optimizing Distribution Costs for a Retail Chain

## Problem Statement

A retail company operates multiple warehouses and supplies goods to a network of retail stores. The company wants to optimize its transportation plan to minimize costs while ensuring that store demands are met as effectively as possible. The objective is to determine the optimal number of units to be transported from each warehouse to each store while considering supply constraints, demand requirements.

## Objective Function

Minimize the total transportation cost while ensuring supply and demand constraints are met.

## Constraints

1. **Supply:** Each warehouse has a maximum number of units available for distribution.
2. **Demand:** Each store requires a certain minimum number of units.
3. **Transportation:** The cost of moving a unit from a warehouse to a store is predefined.

---

## Input Data

### Warehouses and Supply Capacity

| Warehouse | Supply Capacity |
|-----------|-----------------|
| W(A)      | 2000 units      |
| W(B)      | 3100 units      |
| W(C)      | 100 units       |

### Retail Stores and Demand Requirements

| Store | Minimum Demand |
|-------|----------------|
| S(1)  | 500 units      |
| S(2)  | 900 units      |
| S(3)  | 1800 units     |
| S(4)  | 200 units      |
| S(5)  | 700 units      |

### Transportation Cost Matrix (Cost per Unit Moved)

| From \ To | S(1) | S(2) | S(3) | S(4) | S(5) |
|-----------|------|------|------|------|------|
| W(1)      | 20   | 40   | 50   | 20   | 10   |
| W(2)      | 30   | 10   | 30   | 20   | 30   |
| W(3)      | 10   | 12   | 16   | 32   | 14   |

---

## Expected Outcome

The optimal transportation plan should:

1. Allocate units from warehouses to stores in a way that minimizes transportation costs.
2. Ensure supply and demand constraints are satisfied as much as possible.

