# Вище: імпорти, налаштування та підготовка змінних.
# Окреме дерево з одним поділом демонструє роботу з порядковою ознакою.
quality_tree = DecisionTreeRegressor(max_depth=1, random_state=SEED)
quality_tree.fit(X_train[["OverallQual"]], y_train)
quality_values = np.sort(X_train["OverallQual"].unique())
print("Спостережені рівні:", quality_values)
print("Кандидати між сусідніми рівнями:", (quality_values[:-1] + quality_values[1:]) / 2)
print("Обраний поріг OverallQual:", quality_tree.tree_.threshold[0])
print("Середні ціни в лівому та правому листках:", quality_tree.tree_.value[1:, 0, 0])
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
