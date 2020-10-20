import warnings
from dataclasses import dataclass

import pulp
from numpy import array

warnings.simplefilter("ignore")  # shut <Spaces are not permitted in the name.>

from util import peek


@dataclass
class Order:
    day: int  # zero-based
    quantity: float
    price: float = 1  # (to be relaxed)


# Given:

max_output_a = 15
max_output_b = 100  # unconstrained

purchases_a = array([0, 0, 0, 15, 4, 0, 1.0])
purchases_b = array([0, 0, 0, 7, 4, 0, 1.0])
requirement_b_to_a = 2

total_days = len(purchases_a)
assert len(purchases_a) == len(purchases_b)
days = [i for i in range(total_days)]

model = pulp.LpProblem("Planning Problem", pulp.LpMinimize)
xa = pulp.LpVariable.dicts(
    "Production Product A", days, lowBound=0, upBound=max_output_a
)
xb = pulp.LpVariable.dicts(
    "Production Product B", days, lowBound=0, upBound=max_output_b
)
inv_a = pulp.LpVariable.dicts("Inventory Product A", days)
inv_b = pulp.LpVariable.dicts("Inventory Product B", days)
requirement_b = pulp.LpVariable.dicts("Total Demand for Product B", days)

# Constraint: Inventory is positive
def accumulate(var, i):
    return pulp.lpSum([var[k] for k in range(i + 1)])


for d in days:
    inv_a[d] = accumulate(xa, d) - accumulate(purchases_a, d)
    model += inv_a[d] >= 0, f"Pos.inv. A at day {d}"

# Closed sum (zero inventory at start or end)
model += pulp.lpSum(xa) == pulp.lpSum(purchases_a), "Closed sum for A"

# Target: min inventory
model += pulp.lpSum(inv_a)

# Requirement to produce d (intermediate + final demand):
for d in days:
    requirement_b[d] = requirement_b_to_a * xa[d] + purchases_b[d]

for d in days:
    inv_b[d] = accumulate(xb, d) - accumulate(requirement_b, d)
    model += inv_b[d] >= 0, f"Pos.inv. D at day {d}"

# Target: min inventory
model += pulp.lpSum(inv_a) + pulp.lpSum(inv_b)


# The solusion below will just silly stack production
# at days where the demand is.
feasibility = model.solve()
print("Status:", pulp.LpStatus[feasibility])
print("production A:", peek(xa))
print("total:", sum(peek(xa)))
print("purchases A: ", purchases_a)
print("total:", sum(purchases_a))
print("production B: ", peek(xb))
print("total:", sum(peek(xb)))
print("purchases B: ", purchases_b)
print("intermediate demand for B: ", array(peek(requirement_b)) - purchases_b)
print("requirement B:", peek(requirement_b))
print("total:", sum(peek(requirement_b)))

print("Objective value:", model.objective.value())
