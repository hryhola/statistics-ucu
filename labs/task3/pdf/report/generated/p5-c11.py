# Проста регресія з константою; summary() дає оцінки, SE, t, p та R².
simple_model = sm.OLS(df["SalePrice"], sm.add_constant(df[["LotArea"]])).fit()
print(simple_model.summary())
beta_1 = simple_model.params["LotArea"]
se_1 = simple_model.bse["LotArea"]
t_1 = (beta_1 - 0) / se_1
p_1 = 2 * stats.t.sf(abs(t_1), df=simple_model.df_resid)
assert np.isclose(t_1, simple_model.tvalues["LotArea"])
assert np.isclose(p_1, simple_model.pvalues["LotArea"])
display(pd.Series({"n": simple_model.nobs, "beta_1": beta_1, "SE(beta_1)": se_1, "t": t_1,
                   "df = n - 2": simple_model.df_resid, "p": p_1,
                   "t_0.975,df": stats.t.ppf(1 - ALPHA / 2, simple_model.df_resid),
                   "R²": simple_model.rsquared, "Скоригований R²": simple_model.rsquared_adj,
                   "Стандартна похибка регресії, дол.": np.sqrt(simple_model.mse_resid)}).to_frame("Значення"))
