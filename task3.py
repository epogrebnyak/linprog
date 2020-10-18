"""Task description:

- 1 product
- planning for 7 days of production
- production quantaties x[t], t = 0...6
- max production capacity C, 0 <= x[t] <= C, let C = 5
- product can be stored for s days, let s = 3
- we are given a purchases schedule purchases[t], let purchases = [0, 0, 2, 8, 1, 0, 1]
- cumulative sum of purchases is required stock of product for day t
- find x[t] (can be non-unique)

Demonstrate solver behavior under following parameters and expected results:

- all orders are under max capacity per day, no need to make stocks ps = [1, 2, 5, 2, 1, 5, 3]
- production schedule is unique, eg when ps = [0, 0, 15, 0, 0, 0, 0] and xs = [5,5,5,0, 0, 0, 0]
- production schedule not unique (as above)
- production schedule not feasisble eg ps = [0, 0, 0, 20, 0, 0, 0]
"""

import time
import warnings
from contextlib import contextmanager
from dataclasses import dataclass

import pandas as pd
import pulp
from numpy import cumsum, array

warnings.simplefilter("ignore")  # shut <Spaces are not permitted in the name.>

@dataclass
class Order:
    day: int # zero-based
    quantity: float    

# Given:

max_output = 5
orders = [Order(0, 1), 
          Order(1, 3), 
          Order(1, 2), 
          Order(1, 0.5), 
          Order(2, 0), 
          Order(3, 5)]

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
        [order.quantity * accept[i] for i, order in enumerate(orders) if d == order.day]
    )

# Inventory is positive
def accumulate(var, i):
    return pulp.lpSum([var[k] for k in range(i + 1)])

for d in days:
    inventory[d] = accumulate(x, d) - accumulate(purchases, d)
    model += accumulate(x, d) - accumulate(purchases, d) >=0

# Closed sum
model += pulp.lpSum(x) == pulp.lpSum(purchases)

# Target
model += pulp.lpSum([purchases[d] for d in days]) - \
         0.5 * pulp.lpSum([inventory[d] for d in days])
    


feasibility = model.solve()
print("Status:", pulp.LpStatus[feasibility])

def peek(x):
    """
    Lookup into dict of pulp.LpVariable.
    """
    return [v.value() for v in x.values()]

print(peek(x))
