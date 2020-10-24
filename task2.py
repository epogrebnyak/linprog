"""
Task definition:
    https://github.com/epogrebnyak/linprog#task-2

Extra notation:
    
    processing_a + sales_a = requirement_a
                   sales_b = requirement_b
where                   
  processing_* - intermediate consumption
  sales_* - final client demand
  requirement_* - total demand for product

"""
import warnings
from typing import List, Dict

import pulp
from numpy import array, ndarray

# Mute <Spaces are not permitted in the name> warning
warnings.simplefilter("ignore")

# Given:
max_output_a = 15
max_output_b = 5

purchases_a = array([0, 0, 0, 15, 4, 0, 1])
purchases_b = array([1, 0, 0, 7, 4, 0, 1])

# EP: if we order B, we need requirement_b_to_a times more product A
# EP: maybe rename this without 'requirement', as the word is also used
requirement_b_to_a = 2

# Helper functions:


def peek(x: Dict[int, pulp.pulp.LpVariable]) -> ndarray:
    """Get values from pulp.LpVariable dictionary."""
    return array([v.value() for v in x.values()])


def values(xs: List[pulp.pulp.LpAffineExpression]) -> ndarray:
    return array([x.value() for x in xs])


def accumulate(var, i) -> pulp.pulp.LpAffineExpression:
    return pulp.lpSum([var[k] for k in range(i + 1)])


# Solution:

total_days = len(purchases_a)
assert len(purchases_a) == len(purchases_b)
days = [i for i in range(total_days)]
model = pulp.LpProblem("Planning Problem", pulp.LpMinimize)

# Declare variables
xa = pulp.LpVariable.dicts(
    "Production Product A", days, lowBound=0, upBound=max_output_a
)
xb = pulp.LpVariable.dicts(
    "Production Product B", days, lowBound=0, upBound=max_output_b
)

requirement_b = purchases_b
requirement_a = array([xb[d] for d in days]) * requirement_b_to_a + purchases_a

# Closed sum (zero inventory at start or end)
# AG: we can live without this constraint if we min function
# model += pulp.lpSum(xa) == pulp.lpSum(requirement_a.values())
# model += pulp.lpSum(xb) == pulp.lpSum(requirement_b)

# Constraint: positive inventory
inv_a = dict()
inv_b = dict()
for d in days:
    inv_b[d] = accumulate(xb, d) - accumulate(requirement_b, d)
    model += inv_b[d] >= 0, f"Pos.inv.B at day {d}"
    inv_a[d] = accumulate(xa, d) - accumulate(requirement_a, d)
    model += inv_a[d] >= 0, f"Pos.inv.A at day {d}"

# Target: min inventory
# AG: added requirement_b_to_a term as we need to scale the penalty for b by the proportion of a
model += pulp.lpSum(inv_a.values()) + pulp.lpSum(inv_b.values()) * (
    requirement_b_to_a + 1
)

feasibility = model.solve()
print("Status:", pulp.LpStatus[feasibility])
if feasibility == 1:
    import pandas as pd

    df = pd.DataFrame(
        dict(
            sales_b=purchases_b,
            production_b=peek(xb),
            inventory_b=peek(inv_b),
            processing_a=values(requirement_a) - purchases_a,
            sales_a=purchases_a,
            requirement_a=values(requirement_a),
            production_a=peek(xa),
            inventory_a=peek(inv_a),
        )
    ).applymap(lambda x: int(x))
    print(df.T)
