import numpy as np
import pandas as pd

product_names = ["A (H)", "B (H10)", "C (TA-HSA-10)", "D (TA-240)"]
max_capacity = [4.32, 3.6, 2.16, 3.3]
# assumption: we treat below as warehouse storage days, not total product life days 
max_days_storage = [14, 14, 7, 7]
# constant cost per t, usd/t
unit_cost = np.array([293.6, 340.3, 430.1, 815.1])
# usual price, but may vary across , usd/t, given for reference 
expected_price = np.array([400, 500, 1100, 900])
margin = expected_price - unit_cost

df = pd.DataFrame(dict(max_capacity=max_capacity,
                       unit_cost = unit_cost,
                       max_days_storage=max_days_storage,
                       expected_price=expected_price
                       ), 
                  index=product_names,
                  )
df['margin'] = ((df.expected_price - df.unit_cost) / df.expected_price).round(2)


"""Our production graph:
    
  Al(OH)3 --> H --> H10 --> TA-HSA-10
  Al(OH)3 --> TA-240

In simplified notation:
    
  raw -> A -> B -> C
  raw -> D
  
Orders are taken for A, B, C, D, they can be sold separately.

"""

# TODO: content requirements and production lead times:

# - Сколько нужно тонн продукта сырья для производства 1 тонны H?
# - Сколько нужно тонн продукта H для производства 1 тонны H10?
# - Сколько нужно тонн продукта H10 для производства 1 тонны TA-HSA-10?
# - Сколько нужно тонн продукта сырья для производства 1 тонны TA-240?

# TODO: we will need a sample order schedule and terms of delievery (eg days)
