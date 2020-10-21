"""
Task definition:
    https://github.com/epogrebnyak/linprog#task-2

"""
import warnings
from typing import List

import pulp
from numpy import array

# Mute <Spaces are not permitted in the name.> warning
warnings.simplefilter("ignore")  

# Given:

max_output_a = 15
max_output_b = 5

purchases_a = array([0, 0, 0, 15, 4, 0, 1])
purchases_b = array([1, 0, 0, 7, 4, 0, 1])

# EP: if we order B, we need requirement_b_to_a times more product A
requirement_b_to_a = 2

# Functions:    

def peek(x) -> List[float]:
    """Get values of pulp.LpVariable."""
    return [v.value() for v in x.values()]    

def accumulate(var, i):
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
inv_a = dict()
inv_b = dict()

requirement_b = purchases_b
requirement_a = dict()
for d in days:
    # AG: more of b requires more of a, not other way around
    requirement_a[d] = requirement_b_to_a * xb[d] + purchases_a[d]

# Closed sum (zero inventory at start or end)  
# AG: we can live without this constraint
# model += pulp.lpSum(xa) == pulp.lpSum(requirement_a.values())
# model += pulp.lpSum(xb) == pulp.lpSum(requirement_b)

# Constraint: positive inventory
for d in days:
    inv_b[d] = accumulate(xb, d) - accumulate(requirement_b, d)
    model += inv_b[d] >= 0, f"Pos.inv.B at day {d}"
    inv_a[d] = accumulate(xa, d) - accumulate(requirement_a, d)
    model += inv_a[d] >= 0,  f"Pos.inv.A at day {d}" #EP: somehow naming gives an error

# Target: min inventory
# AG: added requirement_b_to_a term as we need to scale the penalty for b by the proportion of a  
model += (pulp.lpSum(inv_a.values()) + pulp.lpSum(inv_b.values()) * (requirement_b_to_a + 1))

feasibility = model.solve()
print("Status:", pulp.LpStatus[feasibility])

# Consolidating the Prodcut A Production Result
xa_values = peek(xa)

# Consolidating the Prodcut B Production Result
xb_values = peek(xb)

# Consolidating the inventory values for Product A
inv_a_values = [x.value() for x in inv_a.values()]

# Consolidating the inventory values for Product B
inv_b_values =  [x.value() for x in inv_b.values()]

# EP: notation:
# processing_a + sales_a = requirement_a
import pandas as pd
df = pd.DataFrame(dict(sales_b = purchases_b,
                       production_b = peek(xb),
                       inventory_b = inv_b_values,
                       processing_a = peek(requirement_a) - purchases_a,
                       sales_a = purchases_a,
                       requirement_a = peek(requirement_a),
                       production_a = peek(xa),                       
                       inventory_a = inv_a_values)
                  ).applymap(lambda x: int(x))
print(df.T)    

# EP, maybe: should we use more of numpy.array structures, instead of dicts?
#            will allow requirement_a = requirement_b_to_a * xb + purchases_a