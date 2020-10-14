"""Task description:
- 1 product
- planning for 7 days
- production quantaties x[t], t = 1...7
- max production capacity C, 0 <= x[t] <= C, let C = 5
- product can be stored for s days, let s = 3
- we are given a purchases schedule ps[t], let ps = [0, 0, 2, 8, 1, 0, 1]
- cumulative sum of purchases is required stock of product for day t, r[t]
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

max_output = 5

model = pulp.LpProblem("Planning Problem", pulp.LpMinimize) # orLpMinimize - does not matter

x = pulp.LpVariable.dicts("Production", 
                           [1,2,3,4,5,6,7],
                           lowBound = 0,
                           upBound = max_output)

#purchase schedule
ps =                   [0, 0, 2, 8, 1, 0, 1]
cum_purchases = cumsum(ps)
#                      [ 0, 0  2, 10, 11, 11, 12],
#                       x1 x2 x3  x4  x5  x6  x7 

# This is availability constraint - there is enough product produced to satisfy demand
model += x[1] + x[2] + x[3]                             >= 2
model += x[1] + x[2] + x[3] + x[4]                      >= 10
model += x[1] + x[2] + x[3] + x[4] + x[5] + x[6]        >= 11
model += x[1] + x[2] + x[3] + x[4] + x[5] + x[6] + x[7] == 12

# This is storage constraint - three days of production prior to purchase
# must satisfy demand. EP: is this correct?
model += x[1] + x[2] + x[3] >= 2
model += x[2] + x[3] + x[4] >= 8
model += x[4] + x[5] + x[6] >= 1
model += x[5] + x[6] + x[7] >= 1 # Note >=1 will give different results, maybe this is solver behavior

model.solve()

# show results
planned_x = [v.value() for v in x.values()]
df = pd.DataFrame(dict(production=planned_x, purchases=ps, inventory=cumsum(planned_x)-cum_purchases))
df_cum = pd.DataFrame(dict(cum_production=cumsum(planned_x), cum_purchases=cum_purchases))
print(df)
df.plot.bar()

# 0. Are we introducing the variables and contrsaints right?
# 1. The production is shifted now to start of three-day period, may want to produce at the latest possible day.
#    Introduce cost of storage? Can we do dual maximisation (eg. profit and )
# 2. The solution is not unique, but how do we know it form solver?
#    How do we extract other solutions from solver?
# 3. x[5] + x[6] + x[7] as noted - does equality or >= make a difference?

# May do:
# - functions to generate avialbility and storage constraints
# - make a plot 1-based on x axis
