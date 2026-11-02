YEAR_0 = 1970  # опорний рік: a - прогноз ціни будинку, збудованого в 1970 р.
def exponential(year, a, b):
    """SalePrice = a * exp(b * (YearBuilt - 1970))."""
    return a * np.exp(b * (year - YEAR_0))
# Початкові значення: якщо log(SalePrice) = log(a) + b * (YearBuilt - 1970),
# то їх дає звичайна лінійна регресія логарифма ціни.
log_fit = sm.OLS(np.log(y), sm.add_constant(x - YEAR_0)).fit()
p0 = [np.exp(log_fit.params[0]), log_fit.params[1]]
params, pcov = curve_fit(exponential, x, y, p0=p0)
a_hat, b_hat = params
exp_pred = exponential(x, a_hat, b_hat)
# R² і MSE рахуємо однаково для обох моделей на тих самих y.
def r_squared(prediction):
    return 1 - np.sum((y - prediction) ** 2) / np.sum((y - y.mean()) ** 2)
def mse(prediction):
    return np.mean((y - prediction) ** 2)
# Далі: assert R² лінійної моделі, таблиці порівняння, контрольні роки, графік.
