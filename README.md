# Scheduling and production planning problems

> The optimal solution for a model is not necessarily the optimal solution for the real problem.
`["Supplement B"]`

This is a set of demo problems to try [PuLP](https://coin-or.github.io/pulp), python librabry for linear programming. There are three tasks, followed by [project notes](#Notes) and [several references](#References):

- [Task 1 - Production schedule for one perishable product](#task1)
- [Task 2 - Sequential production](#task2)
- [Task 3 - Select orders when demand over capacity](#task3)

The problems are kept quite simple and toy size (7 days of planning, 1-2 goods). They reveal 
the logic of formulation of storage time limit, sequential production and order selection for 
a generic industrial (eg chemical or mechanical) production. 

Why this excercise can be useful? Differentiate model vs real world, detect what we capture in the model and what not with respect to real production,
see if enforcing model rules can be feasible in practice, what judgement and intuition may suggest vs the model, what are data requirements, model extensions, 
business changes may be (eg pricing, contract structure), what is "lean" materially, etc.

<a name="task1"></a>

## Task 1 - Production schedule for one perishable product 

#### Problem description

Setting:

- 1 product
- production planning for 7 days
- production quantaties are `x[t], t = 0...6`
- max production capacity C, `0 <= x[t] <= C`, let `C = 5`
- product is perishable, it can be stored for s days, let `s = 3`
- we are given a purchases schedule on each day, let `purchases = [0, 0, 2, 8, 1, 0, 1]`

Introduce target funсtion and find production volumes `x[t]`. Explore situation where result is not unique.

#### Solution formulation 

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

- we looked at several ways to formulate constraints for limited shelf-life / max storage duration  ("условие непротухания")


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

- 2 products
- good A is precursor to good B
- there are client orders for both A and B
- to produce 1 ton of B one needs 1.2 tons of A
- goods A and B are storable, there is no shelf life constraint
- the prices and unit costs of production are given
- there are capacity constraints for A and B

Introduce target function and find optimal production of product A and B (`xa`, `xb`)

<a name="task3"></a>

## Task 3 - Select orders when demand over capacity

Pick most profitable orders from a list of orders when demand is over production capacity:

- prices for same products may vary by order
- we need to limit time span for orders

## Notes

Remaining questions about the PuLP solver and example extentions:

1. The solution may be not unique, but how do we know it from solver?
   How do we extract other solutions from solver?
2. How to know which constraint was binding?
3. Are dual prices meaningful for this type of problem?
4. Is any sensitivity analysis possible?
5. Can we do multiple criteria optimisation (eg weights in target func)?
6. How to list second-best, third-best solution?
7. What would 'soft constraints' enable us to do?

What can go wrong when combining three tasks:

- more constraints overlap
- will need more days of planning (>7)
- may need to relax more constraints (eg zero outgoing inventory)
- exhaustive list of assumptions

Other modelling needs:

1. May need extra way to shift production right - prefer later production for any order
2. Explcitly model FIFO warehouse (by earmarking daily production):
  - as a direct check no expired products are shipped
  - calculate average age of products when sold, in days

## References

Software:

- [PuLP package documentation](https://coin-or.github.io/pulp)
- [Pyomo](https://www.pyomo.org)

Papers (review, etc):

- [Mixed Integer Linear Programming in Process Scheduling: Modeling, Algorithms, and Applications](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjL0N-kxL7sAhUnmYsKHWoxBm0QFjAAegQIAhAC&url=http%3A%2F%2Fcheresearch.engin.umich.edu%2Flin%2Fpublications%2FMixed%2520Integer%2520Linear%2520Programming%2520in%2520Process%2520Scheduling.pdf&usg=AOvVaw1o03XZyPw9rgAH3YG7bJOz)
- [Multiproduct, multistage machine requirements planning models](https://core.ac.uk/download/pdf/81151558.pdf)

Other:

- ["Supplement B"](http://www.uky.edu/~dsianita/300/online/LP.pdf) from [lecture notes](http://www.uky.edu/~dsianita/300/300lecture.html)
