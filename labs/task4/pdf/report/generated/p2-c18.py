# Вище: імпорти, налаштування та підготовка змінних.
# Прогноз: збільшення штрафу зменшить дерево; за дуже великого лишиться один листок.
print("Прогноз: зі зростанням ccp_alpha кількість листків не збільшується.")
pruning_path = tree.cost_complexity_pruning_path(Z_train, y_train)
pruning_rows = []
for alpha in pruning_path.ccp_alphas:
    model = clone(tree).set_params(ccp_alpha=float(alpha)).fit(Z_train, y_train)
    pruning_rows.append({
        "ccp_alpha": alpha, "Листків": model.get_n_leaves(), "Глибина": model.get_depth(),
        "Навчальна MSE, дол.^2": mean_squared_error(y_train, model.predict(Z_train)),
        "Валідаційна MSE, дол.^2": mean_squared_error(y_valid, model.predict(Z_valid)),
    })
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
