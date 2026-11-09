# Вище: імпорти, налаштування та підготовка змінних.
# Прогноз до досліду: усереднення зменшить коливання прогнозів; криві можуть мати нерівності.
print("Прогноз: зі збільшенням ансамблю валідаційна MSE стабілізуватиметься; монотонність не гарантована.")
ensemble_sizes = [1, 5, 10, 25, 50, 100, FINAL_TREES]
ensembles = {
    "Bagging": BaggingRegressor(
        estimator=DecisionTreeRegressor(random_state=SEED),
        bootstrap=True, max_samples=1.0, max_features=1.0,
        warm_start=True, random_state=SEED, n_jobs=1),
    "Random Forest": RandomForestRegressor(
        bootstrap=True, max_features=1/3, warm_start=True,
        random_state=SEED, n_jobs=1),
}
curve_rows = []
for name, model in ensembles.items():
    for size in ensemble_sizes:
        # Нові дерева додаються до того самого ансамблю; старі залишаються.
        model.set_params(n_estimators=size).fit(Z_train, y_train)
        curve_rows.append({"Модель": name, "Дерев": size,
                           "Навчальна MSE, дол.^2": mean_squared_error(y_train, model.predict(Z_train)),
                           "Валідаційна MSE, дол.^2": mean_squared_error(y_valid, model.predict(Z_valid))})
curves = pd.DataFrame(curve_rows)
# Описовий критерій плато: не більш ніж на 1% вище MSE при 200 деревах.
plateau_rows = []
for name, group in curves.groupby("Модель", sort=False):
    mse = group["Валідаційна MSE, дол.^2"].to_numpy()
    acceptable = np.array([np.all(mse[i:] <= 1.01 * mse[-1]) for i in range(len(mse))])
    plateau_rows.append({"Модель": name, "Початок плато на сітці": group["Дерев"].to_numpy()[acceptable][0],
                         "MSE при 200 деревах, дол.^2": mse[-1]})
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
