import numpy as np

product_names = ["A", "B", "C", "D"]
max_capacity = [4.32, 3.6, 2.16, 3.3]
# это максимальный срок хранения на складе до отправки покупателю
# или максимальный срок жизни всего продукта
max_days_storage = [14, 14, 7, 7]
# constant cost per t, usd/t
unit_cost = np.array([293.6, 340.3, 430.1, 815.1])
# usual price, but may vary across , usd/t
expected_price = np.array([400, 500, 1100, 900])
margin = expected_price - unit_cost
