# Вище: імпорти, налаштування та підготовка змінних.
# Прогноз перед обчисленням: Ridge зменшить умовні дисперсії коефіцієнтів,
# але його помилка на нових даних не обов'язково буде меншою за МНК.
print("Прогноз: менші умовні дисперсії Ridge; перевага за перевірочною MSE не гарантована.")
ridge_alphas = np.logspace(-2, 5, 40)
ridge_search = GridSearchCV(
    Pipeline([("prepare", clone(preprocessor)), ("model", Ridge(solver="svd"))]),
    {"model__alpha": ridge_alphas}, cv=cv,
    scoring="neg_mean_squared_error", n_jobs=1,
)
ridge_search.fit(X_train, y_train)
ridge_model = ridge_search.best_estimator_.named_steps["model"]
ridge_alpha = ridge_search.best_params_["model__alpha"]
ols_model = LinearRegression().fit(Z_train, y_train)
# Усі три моделі використовують ту саму матрицю й ті самі рядки.
metrics = []
for name, model in [("OLS", ols_model), ("Lasso", lasso_model), ("Ridge", ridge_model)]:
    metrics.append({
        "Модель": name,
        "alpha": {"OLS": 0, "Lasso": lasso_alpha, "Ridge": ridge_alpha}[name],
        "Навчальна MSE, дол.^2": mean_squared_error(y_train, model.predict(Z_train)),
        "Перевірочна MSE, дол.^2": mean_squared_error(y_test, model.predict(Z_test)),
        "Норма коефіцієнтів": np.linalg.norm(model.coef_),
    })
# За точної колінеарності МНК повертає розв'язок найменшої норми.
# Псевдообернена матриця дозволяє порівняти саме цей розв'язок із Ridge.
Z_centered = Z_train - Z_train.mean(axis=0)
rank = ols_model.rank_
sigma2 = np.sum((y_train - ols_model.predict(Z_train)) ** 2) / (len(y_train) - rank - 1)
Z_pinv = np.linalg.pinv(Z_centered, rcond=max(Z_centered.shape) * np.finfo(float).eps)
A_ridge = np.linalg.solve(
    Z_centered.T @ Z_centered + ridge_alpha * np.eye(Z_train.shape[1]),
    Z_centered.T,
)
var_ols = sigma2 * np.sum(Z_pinv ** 2, axis=1)
var_ridge = sigma2 * np.sum(A_ridge ** 2, axis=1)
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
