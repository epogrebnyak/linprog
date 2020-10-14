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

import pulp
import pandas as pd
from numpy import cumsum

max_days_storage = 3
max_output = 5
purchases = [0, 0, 2, 8, 1, 0, 1]
cum_purchases = cumsum(purchases)


model = pulp.LpProblem("Planning Problem", pulp.LpMinimize)
x = pulp.LpVariable.dicts("Production", 
                           [0,1,2,3,4,5,6],
                           lowBound = 0,
                           upBound = max_output)

def cumprod(i: int):
    return pulp.lpSum([x[k] for k in range(i+1)])


def inventory(i):
    return cumprod(i) - cum_purchases[i]

def all_periods():
    return [t for t, _ in enumerate(x)]

# Minimise inventory - target function (целевая фукнция)
model += pulp.lpSum(inventory(i) for i in all_periods())

# Constraint 1
# No inventory at end of period, everyhting what is produced consumed within period 
model += pulp.lpSum(x) == sum(purchases)

# Constraint 2
# This is availability constraint - there is enough product produced to satisfy demand
# We effectively require non-negative inventory
for i, cp in enumerate(cum_purchases):
        model += cumprod(i) >= cum_purchases[i]    

# Constraint 3 - "условие непротухания"      
# This is storage constriant - we do not produce anyhting that would not conumed after n days
# В нулевой день не больше, чем нужно кумулятивно на третий
# Если это не выполняется, то часть продукции с нудевого дня должит до четвертого , а это нельзя
for i in all_periods():   
    try:
        model += cumprod(i) <= cum_purchases[i+max_days_storage-1]
    except IndexError:
        pass

model.solve()

# show results
planned_x = [v.value() for v in x.values()]
df = pd.DataFrame(dict(production=planned_x, purchases=purchases, inventory=cumsum(planned_x)-cum_purchases))
df_cum = pd.DataFrame(dict(cum_production=cumsum(planned_x), cum_purchases=cum_purchases))
print(df)
df.plot.bar()
df_cum.plot()

# Note:
# 1. If the solution is not unique, how do we know it from solver?
#    How do we extract other solutions from solver?
