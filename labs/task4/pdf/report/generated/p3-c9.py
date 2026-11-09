# Вище: імпорти, налаштування та підготовка змінних.
lot_beta = beta_raw["LotArea"]
lot_ci = model.conf_int().loc["LotArea"] / scales["LotArea"]
lot_rows = []
for increase in [1, 1000]:
    odds_ratio = np.exp(increase * lot_beta)
    lot_rows.append({"Приріст площі, кв. футів": increase, "beta на 1 кв. фут": lot_beta,
                     "Відношення шансів": odds_ratio, "Зміна шансів, %": 100 * (odds_ratio - 1),
                     "Нижня межа OR, 95%": np.exp(increase * lot_ci.iloc[0]),
                     "Верхня межа OR, 95%": np.exp(increase * lot_ci.iloc[1])})
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
