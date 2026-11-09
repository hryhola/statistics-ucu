# Вище: імпорти, налаштування та підготовка змінних.
lasso_alphas = np.logspace(1, 4, 35)
# LassoCV виконує п'ять блоків на вже підготовленій матриці.
lasso_cv = LassoCV(alphas=lasso_alphas, cv=cv, max_iter=50000, tol=1e-6)
lasso_cv.fit(Z_train, y_train)
# Перевіряємо вибір штрафу без спільного масштабування між блоками.
lasso_search = GridSearchCV(
    Pipeline([("prepare", clone(preprocessor)),
              ("model", Lasso(max_iter=50000, tol=1e-6))]),
    {"model__alpha": lasso_alphas}, cv=cv,
    scoring="neg_mean_squared_error", n_jobs=1,
)
lasso_search.fit(X_train, y_train)
lasso_model = lasso_search.best_estimator_.named_steps["model"]
lasso_alpha = lasso_search.best_params_["model__alpha"]
# Центрування потрібне, бо lasso_path не оцінює вільний член.
path_alphas, coefficients, gaps = lasso_path(
    Z_train - Z_train.mean(axis=0), y_train.to_numpy() - y_train.mean(),
    alphas=np.logspace(1, 5, 60), max_iter=50000, tol=1e-6,
)
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
