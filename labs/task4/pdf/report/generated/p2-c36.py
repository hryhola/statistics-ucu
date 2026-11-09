# Вище: імпорти, налаштування та підготовка змінних.
# Прогноз: ліс із третиною ознак має навчатися швидше; перевіряємо фактичний час.
print("Прогноз: Random Forest із max_features=1/3 швидший за беггінг з усіма ознаками.")
timing_rows = []
for repeat in range(3):
    # Чергуємо порядок, щоб один метод не завжди виконувався першим.
    names = list(ensembles) if repeat % 2 == 0 else list(reversed(ensembles))
    for name in names:
        model = clone(ensembles[name]).set_params(warm_start=False, n_estimators=FINAL_TREES)
        start = time.time()
        model.fit(Z_train, y_train)
        elapsed = time.time() - start
        timing_rows.append({"Повтор": repeat + 1, "Модель": name, "Час навчання, с": elapsed})
        # Незалежне навчання з нуля відтворює ансамбль, нарощений у (і).
        assert np.allclose(model.predict(Z_valid), ensembles[name].predict(Z_valid))
timings = pd.DataFrame(timing_rows)
timing_summary = timings.groupby("Модель")["Час навчання, с"].agg(["median", "min", "max"])
forest = ensembles["Random Forest"]
importance["Random Forest MDI"] = forest.feature_importances_
# Відтворюємо MDI лісу за нормованими важливостями окремих дерев.
forest_mdi = np.mean([
    estimator.feature_importances_
    for estimator in forest.estimators_
    if estimator.tree_.node_count > 1
], axis=0)
forest_mdi /= forest_mdi.sum()
mdi_difference = np.abs(forest_mdi - forest.feature_importances_)
# Повна таблиця зберігає знак коефіцієнтів і не змішує їх одиниці з MDI.
final_importance = importance.sort_values("Random Forest MDI", ascending=False)
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
