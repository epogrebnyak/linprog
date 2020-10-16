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
- production schedule not feasisble eg ps = [0, 0, 20, 0, 0, 0, 0]
"""

import time
import warnings
from contextlib import contextmanager
from dataclasses import dataclass

import pandas as pd
import pulp
from numpy import cumsum

warnings.simplefilter("ignore")  # shut <Spaces are not permitted in the name.>

# Given:
max_days_storage = 3
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
# No inventory at end of period, everyhting what is produced consumed within period
model += pulp.lpSum(x) == sum(purchases)

# Constraint 2
# This is availability constraint - there is enough product produced to satisfy demand
# We effectively require non-negative inventory.
for i in days:
    model += cumprod(i) - cumbuy(i) >= 0

# Constraint 3 - "nothing perished" ("условие непротухания")
# We should not have inventory that would perish (exceed storage time and would
# not be bought). If we hold inventory greater than expected purshases, at least
# some inventory will perish.
# This formulation may change if we allow non-zero end of month stocks.
for i in days:
    try:
        model += inventory(i) <= cumbuy(i + max_days_storage) - cumbuy(i)
        # this is mathematically equivalent to:
        # cumprod(i) <= cumbuy(i+max_days_storage)
        # (earlier suggested by Dmitry)
    except IndexError:
        pass


@dataclass
class Timer:
    elapsed: float = 0


@contextmanager
def timer():
    start = time.perf_counter()
    t = Timer()
    try:
        yield t
    finally:
        t.elapsed = time.perf_counter() - start


def plot(df, df_cum):
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True)
    fig.set_size_inches(8, 3)
    df_cum.plot(ax=ax1)
    df.plot.bar(ax=ax2)
    ax1.yaxis.grid()
    ax2.yaxis.grid()
    fig.savefig("lp.png")


# Solve model
with timer() as t:
    feasibility = model.solve()


# Report
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

# Note:
# 1. The solution is not unique, but how do we know it form solver?
#    How do we extract other solutions from solver?
