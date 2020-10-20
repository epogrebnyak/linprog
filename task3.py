import warnings
from dataclasses import dataclass

import pulp
from numpy import cumsum, array

warnings.simplefilter("ignore")  # shut <Spaces are not permitted in the name.>

from util import peek


@dataclass
class Order:
    day: int  # zero-based
    quantity: float
    price: float = 1  # (to be relaxed)


# Given:

max_output = 5
orders = [
    Order(0, 1),
    Order(1, 3),
    Order(1, 2),
    Order(1, 0.5),
    Order(2, 0),
    Order(3, 5),
]

total_days = 1 + max([order.day for order in orders])
days = [i for i in range(total_days)]

model = pulp.LpProblem("Planning Problem", pulp.LpMaximize)
x = pulp.LpVariable.dicts("Production", days, lowBound=0, upBound=max_output)
inventory = pulp.LpVariable.dicts("Inventory", days)
purchases = pulp.LpVariable.dicts("Purchases", days, lowBound=0)
accept = pulp.LpVariable.dicts("AcceptOrder", range(len(orders)), cat="Binary")

# Purchases are accepted orders
for d in days:
    purchases[d] = pulp.lpSum(
        [order.quantity * accept[j] for j, order in enumerate(orders) if d == order.day]
    )

# Constraint: Inventory is positive
def accumulate(var, i):
    return pulp.lpSum([var[k] for k in range(i + 1)])


for d in days:
    inventory[d] = accumulate(x, d) - accumulate(purchases, d)
    model += (
        accumulate(x, d) - accumulate(purchases, d) >= 0,
        f"Pos.inventory at day {d}",
    )

# Closed sum (zero inventory at start or end)
model += pulp.lpSum(x) == pulp.lpSum(purchases), "Closed sum"

# Target: max profit with penalty for inventory
# Note: penalty coef will matter, try 0.1 instead of 100
cost_of_holding_inventory = 100
model += pulp.lpSum(
    [purchases[d] for d in days]
) - cost_of_holding_inventory * pulp.lpSum([inventory[d] for d in days])


feasibility = model.solve()
print("Status:", pulp.LpStatus[feasibility])


print("production:", peek(x))
print("total:", sum(peek(x)))
print("purchases:", peek(purchases))
print("total:", sum(peek(purchases)))
for accepted, order in zip(peek(accept), orders):
    print(order, "accepted" if accepted else "rejected")
print("Objective value:", model.objective.value())
