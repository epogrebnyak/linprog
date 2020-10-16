### Task description

Given:

- 1 product
- production planning for 7 days
- production quantaties are `x[t], t = 0...6`
- max production capacity C, `0 <= x[t] <= C`, let `C = 5`
- product is perishable, it can be stored for s days, let `s = 3`
- we are given a purchases schedule on each day, let `purchases = [0, 0, 2, 8, 1, 0, 1]`

Find `x[t]` (can be non-unique)

### Solution

| Day                |   0 |   1 |   2 |   3 |   4 |   5 |   6 |
|:-------------------|----:|----:|----:|----:|----:|----:|----:|
| Purchases (given)  |     |     |   2 |   8 |   1 |     |   1 |
| Production (found) |     |     |   5 |   5 |   1 |     |   1 |
| Inventory    |     |     |   3 |     |     |     |     |

Solution code [here](simple_demo.py).

### Comments

Ideas:

- we introduce min phycial inventories as target function to make solution unique
- may also use min time-weights `7*x0 + 6*x1 + ... + 1*x6` as target function 
- there are several ways to formulate constraint for limited shelf-life ("условие непротухания")
- can explcitly model FIFO warehouse (by earmarking daily production), as a check

Hidden assumptions made:

- closed sum - everything produced must be consumed
- no limit on storage capacity
- assume end of day clearance (eg all purchases made at end of day)
- probuction

May add next:

- picking form orders that are over capacity
- 2+ products, different margins (price-unit cost)
- other realistic features

![](lp.png)

### Reference

See <https://coin-or.github.io/pulp/> for PuLP package documentation.
