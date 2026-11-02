level_model = selected_model
log_model = sm.OLS(np.log(y), X_selected).fit()
n_obs = len(y)
# Двостороннє порівняння через штучні регресори (тест Девідсона–Маккіннона).
# Прогнози альтернативної моделі переводимо в шкалу залежної змінної.
assert (level_model.fittedvalues > 0).all()  # без цього log(прогнозу) не визначений
aux_level = sm.OLS(y, X_selected.assign(alternative=np.exp(log_model.fittedvalues) / 1000)).fit()
aux_log = sm.OLS(np.log(y), X_selected.assign(alternative=np.log(level_model.fittedvalues))).fit()
comparison_rows = []
for name, auxiliary in [("SalePrice ~ X", aux_level), ("log(SalePrice) ~ X", aux_log)]:
    robust = auxiliary.get_robustcov_results(cov_type="HC1", use_t=True)
    position = auxiliary.model.exog_names.index("alternative")
    comparison_rows.append({"Нульова специфікація": name,
                            "t звичайний": auxiliary.tvalues["alternative"],
                            "p звичайне": auxiliary.pvalues["alternative"],
                            "t HC1": robust.tvalues[position], "p HC1": robust.pvalues[position]})
# AIC/BIC лог-моделі переводимо до щільності самої ціни через якобіан 1/y.
jacobian = np.log(y).sum()
# Далі: збирання таблиць тесту та AIC/BIC з поправкою (виводи нижче).
