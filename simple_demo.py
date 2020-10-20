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

from util import timer

import pandas as pd
import pulp
from numpy import cumsum

import warnings
warnings.simplefilter("ignore")  # shut the message <Spaces are not permitted in the name.>


# Given:

max_days_storage: int = 3
max_output = 5
purchases = [0, 0, 2, 8, 1, 0, 1]


# Notation and problem definition:

cum_purchases = cumsum(purchases)
total_days = len(purchases)
days = [i for i in range(total_days)]  # days index is zero-based [0, 1, 2, 3, 4, 5, 6]

model = pulp.LpProblem("Planning Problem", pulp.LpMinimize)
x = pulp.LpVariable.dicts("Production", days, lowBound=0, upBound=max_output)


def cumbuy(i: int):
    """
    Cumulative purchases / shipments by end of day i. 
    Returns a scalar value.
    """
    return cum_purchases[i]


def cumprod(i: int):
    """
    Cumulative production by end of day i. 
    Returns an expression containing x. 
    
    Example:
      cumprod(2)
      >> 1*Production_0 + 1*Production_1 + 1*Production_2 + 0
    """
    return pulp.lpSum([x[k] for k in range(i + 1)])


def inventory(i):
    return cumprod(i) - cumbuy(i)


# Target function (целевая фукнция):
# - minimise inventory
model += pulp.lpSum(inventory(i) for i in days)

# Constraint 1
# No inventory at start or end of period, everyhting what is produced consumed within period
model += pulp.lpSum(x) == sum(purchases)

# Constraint 2
# This is availability constraint - there is enough product produced to satisfy demand
# THis is equivalent to require non-negative inventory.
for i in days:
    model += cumprod(i) - cumbuy(i) >= 0

# Constraint 3 - "nothing perished" ("условие непротухания")
# We should not have inventory that would perish (exceed storage time and would
# not be bought). If we hold inventory greater than expected purshases, at least
# some inventory will perish.
# This formulation may change if we allow non-zero end of month stocks.
for i in days:
    try:
        model += inventory(i) <= cumbuy(i + max_days_storage - 1) - cumbuy(i)
        # this is mathematically equivalent to:
        # cumprod(i) <= cumbuy(i+max_days_storage-1)
        # (earlier suggested by Dmitry)
    except IndexError:
        pass


def plot(df, df_cum):
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True)
    fig.set_size_inches(8, 3)
    df_cum.plot(ax=ax1)
    df.plot.bar(ax=ax2)
    ax1.yaxis.grid()
    ax2.yaxis.grid()
    fig.savefig("simple_demo.png")


# Solve model
with timer() as t:
    feasibility = model.solve()


# Report
print("Status:", pulp.LpStatus[feasibility])
if feasibility == 1:
    print("Solution found in %.4f seconds" % t.elapsed)
    # show results
    planned_x = [v.value() for v in x.values()]
    df = pd.DataFrame(
        dict(
            production=planned_x,
            purchases=purchases,
            inventory=cumsum(planned_x) - cum_purchases,
        )
    )
    df_cum = pd.DataFrame(
        dict(cum_production=cumsum(planned_x), cum_purchases=cum_purchases)
    )
    print(df)
    plot(df, df_cum)
else:
    print("Solution not found")


def calculate(purchases, max_days_storage, max_output):
    """
    Model wrapped in a single function.
    """
    cum_purchases = cumsum(purchases)
    total_days = len(purchases)
    days = [i for i in range(total_days)]
    model = pulp.LpProblem("Planning Problem", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("Production", days, lowBound=0, upBound=max_output)
    cum_prod = cumsum([v for k, v in x.items()])
    inventory = cum_prod - cum_purchases
    # target function: min inventory
    model += pulp.lpSum(inventory[i] for i in days)
    # constriant 1: zero inventory at start and end
    model += pulp.lpSum(x) == sum(purchases), "Closed sum"
    # constriant 2: enough production to satisfy purchases
    for i in days:
        model += cum_prod[i] - cum_purchases[i] >= 0, f"Inventory at day {i} >=0"
    # constriant 3: no goods stored beyond expiry
    for i in days[: (-max_days_storage + 1)]:
        offtake = cum_purchases[i + max_days_storage - 1] - cum_purchases[i]
        model += inventory[i] <= offtake, f"Inventory at day {i} will not expire"
    return model, x


def peek(x):
    """
    Lookup into dict of pulp.LpVariable.
    """
    return [v.value() for v in x.values()]


assert days[: -max_days_storage + 1][-1] + max_days_storage - 1 == days[-1]

m, x = calculate([0, 0, 0, 20, 0, 0, 0], 3, 5)
assert m.solve() == -1

m, x = calculate([0, 0, 15, 0, 0, 0, 0], 3, 5)
m.solve()
assert peek(x) == [5, 5, 5, 0, 0, 0, 0]

m, x = calculate([0, 0, 15, 0, 0, 0, 0], 3, 5)
m.solve()
assert peek(x) == [5, 5, 5, 0, 0, 0, 0]

m, x = calculate([0, 0, 2, 8, 1, 0, 1], 3, 5)
m.solve()
assert peek(x) == [0, 0, 5, 5, 1, 0, 1]
