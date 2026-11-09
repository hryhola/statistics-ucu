# Вище: імпорти, налаштування та підготовка змінних.
# Відтворюємо фінальні Lasso та OLS частини (1), не читаючи її стан ядра.
lasso_search = GridSearchCV(
    Pipeline([("prepare", clone(preprocessor)), ("model", Lasso(max_iter=50000, tol=1e-6))]),
    {"model__alpha": np.logspace(1, 4, 35)},
    cv=KFold(n_splits=5, shuffle=True, random_state=SEED),
    scoring="neg_mean_squared_error", n_jobs=1,
).fit(X_train, y_train)
lasso_model = lasso_search.best_estimator_.named_steps["model"]
ols_model = LinearRegression().fit(Z_train, y_train)
importance = pd.DataFrame({"Lasso, коеф.": lasso_model.coef_, "OLS, коеф.": ols_model.coef_,
                           "CART MDI": tree.feature_importances_},
                          index=pd.Index(feature_names, name="Ознака"))
tree_top10 = importance.sort_values("CART MDI", ascending=False, kind="stable").head(10)
# Перевіряємо MDI через зважені зменшення неоднорідності всіх поділів.
manual_mdi = np.zeros(Z_train.shape[1])
for node, feature in enumerate(t.feature):
    if feature >= 0:
        l, r = t.children_left[node], t.children_right[node]
        manual_mdi[feature] += (t.weighted_n_node_samples[node] * t.impurity[node]
                               - t.weighted_n_node_samples[l] * t.impurity[l]
                               - t.weighted_n_node_samples[r] * t.impurity[r])
manual_mdi /= manual_mdi.sum()
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
