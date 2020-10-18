# Scheduling and production planning problems

- [Task 1 - Production schedule for one perishable product](#task1)
- [Task 2 - Sequential production, product A is a precursor to product B](#task2)
- [Notes](#Notes)
- [References](#References)

<a name="task1"></a>

## Task 1 - production schedule for one perishable product 

### Problem description

Setting:

- 1 product
- production planning for 7 days
- production quantaties are `x[t], t = 0...6`
- max production capacity C, `0 <= x[t] <= C`, let `C = 5`
- product is perishable, it can be stored for s days, let `s = 3`
- we are given a purchases schedule on each day, let `purchases = [0, 0, 2, 8, 1, 0, 1]`

Find production volumes `x[t]` (result can be non-unique).

### Solution formulation 

Target function:

- without target function we just find some feasible solution within the constraints
- we introduce min phycial inventories as target function to make solution unique
- may also use min time-weights `7*x0 + 6*x1 + ... + 1*x6` as alternative target function (unconditional preference for later production)

Revealed assumptions:

1. closed sum - everything produced must be consumed, zero outgoing inventory
2. we set no limit on storage capacity - infinite warehouse
3. we assume end of day clearance, all purchases made at end of day - everything produced at day t can be sold at day t

|                       | Is contrained?    |
|-----------------------|-------------------|
| Production capacity   | Yes               |
| Max storage duration  | Yes               |
| Storage capacity      | No                |
| Outgoing inventory    | Yes, set to zero  |

Other comments:

- there are several ways to formulate constraints for limited shelf-life / max storage duration  ("условие непротухания")


### Solution

| Day                |   0 |   1 |   2 |   3 |   4 |   5 |   6 |
|:-------------------|----:|----:|----:|----:|----:|----:|----:|
| Purchases (given)  |     |     |   2 |   8 |   1 |     |   1 |
| Production (found) |     |     |   5 |   5 |   1 |     |   1 |
| Inventory          |     |     |   3 |     |     |     |     |

Solution code [here](simple_demo.py).

![](simple_demo.png)

<a name="task2"></a>

## Task 2 - Sequential production, product A is a precursor to product B

- we produce two goods 
- good A is precursor to good B, but there are orders for both A and B.
- to produce 1 ton of B one needs 1.2 tons of A. 
- goods A and B are storable, no shelf life constraint
- the prices and unit costs of production are given
- there are capacity constraintrs for A and B

Find optimal production of good A and B (`xa`, `xb`)

## Notes

May add next:

- picking most profitable orders from a list over capacity
- 2+ products, different margins (price-unit cost)
- can explcitly model FIFO warehouse (by earmarking daily production), as a check

Questions:

1. The solution may be not unique, but how do we know it from solver?
   How do we extract other solutions from solver?
2. How to know which constraint was binding?

Quote:

> The optimal solution for a model is not necessarily the optimal solution for the real problem.
`["Supplement B"]`

## References

Software:

- [PuLP package documentation](https://coin-or.github.io/pulp)

Papers (review, etc):

- [Mixed Integer Linear Programming in Process Scheduling: Modeling, Algorithms, and Applications](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjL0N-kxL7sAhUnmYsKHWoxBm0QFjAAegQIAhAC&url=http%3A%2F%2Fcheresearch.engin.umich.edu%2Flin%2Fpublications%2FMixed%2520Integer%2520Linear%2520Programming%2520in%2520Process%2520Scheduling.pdf&usg=AOvVaw1o03XZyPw9rgAH3YG7bJOz)
- [Multiproduct, multistage machine requirements planning models](https://core.ac.uk/download/pdf/81151558.pdf)

Other:

- ["Supplement B"](http://www.uky.edu/~dsianita/300/online/LP.pdf) from [lecture notes](http://www.uky.edu/~dsianita/300/300lecture.html)
