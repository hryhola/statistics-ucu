# Вище: імпорти, налаштування та підготовка змінних.
matrix_optimal, metrics_optimal = threshold_metrics(optimal_threshold)
comparison = pd.DataFrame([metrics_default, metrics_optimal], index=["Стандартний", "За Юденом"])
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
