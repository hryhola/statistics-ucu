# Вище: імпорти, налаштування та підготовка змінних.
significant_positive = coefficient_table[(beta_raw > 0) & (model.pvalues[selected] < SIGNIFICANCE)]
significant_negative = coefficient_table[(beta_raw < 0) & (model.pvalues[selected] < SIGNIFICANCE)]
# Перевіряємо, скільки навчальних прикладів підтримують висновок щодо басейну.
display(pd.crosstab(X_train["PoolArea"] > 0, y_train).rename_axis("Площа басейну > 0"))
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
