# Вище: імпорти, налаштування та підготовка змінних.
# П'ять будинків із валідаційної частини, що не брали участі у відборі моделі.
sample_index = raw_valid.sample(n=5, random_state=SEED).index
sample_design = Z_valid.loc[sample_index, ["const"] + selected]
sample_probabilities = model.predict(sample_design)
sample_results = df.loc[sample_index, ["Order", "SalePrice"]].copy()
sample_results["Фактичний клас"] = y_valid.loc[sample_index]
sample_results["P(Y=1)"] = sample_probabilities
sample_results["Клас за порогом 0.5"] = (sample_probabilities >= 0.5).astype(int)
first_index = sample_index[0]
first_values = raw_valid.loc[first_index, selected]
terms = pd.DataFrame({"Значення ознаки": first_values, "Коефіцієнт": beta_raw,
                      "Добуток": first_values * beta_raw})
z_first = intercept_raw + terms["Добуток"].sum()
print("Ймовірність за формулою:", expit(z_first))
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
