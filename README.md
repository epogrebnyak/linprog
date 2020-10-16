### Task description

- 1 product
- planning for 7 days of production
- production quantaties `x[t], t = 0...6`
- max production capacity C, `0 <= x[t] <= C`, let `C = 5`
- product can be stored for s days, let `s = 3`
- we are given a purchases schedule, let purchases = [0, 0, 2, 8, 1, 0, 1]
- cumulative sum of purchases is required stock of product for day t
- find x[t] (can be non-unique)

[Solution code](simple_demo.py).

![](lp.png)

See <https://coin-or.github.io/pulp/> for package documentation.

