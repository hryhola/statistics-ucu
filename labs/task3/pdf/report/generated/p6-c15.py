import warnings
# 1) Збіжність: та сама крива, але без зсуву року.
def exponential_raw(year, a, b):
    return a * np.exp(b * year)
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    raw_default, raw_default_cov = curve_fit(exponential_raw, x, y)  # p0 = [1, 1] за замовчуванням
    with np.errstate(over="ignore"):
        raw_default_mse = mse(exponential_raw(x, *raw_default))
# Та сама крива без зсуву року, але з p0, перерахованим із центрованої моделі.
raw_params, raw_cov = curve_fit(exponential_raw, x, y, p0=[p0[0] * np.exp(-p0[1] * YEAR_0), p0[1]])
raw_se = np.sqrt(np.diag(raw_cov))
# 2) Усі пояснювальні змінні перших 500 рядків: кількість параметрів проти n.
features = df_500.drop(columns=["Order", "PID", "SalePrice"])
categorical = ["MSSubClass"] + list(features.select_dtypes(exclude="number").columns)
X_all = pd.get_dummies(features, columns=categorical, drop_first=True, dtype=float)
complete = X_all.notna().all(axis=1)
X_complete = X_all[complete]
# Далі: друк попереджень, таблиці порівняння параметризацій і розмірів матриці.
