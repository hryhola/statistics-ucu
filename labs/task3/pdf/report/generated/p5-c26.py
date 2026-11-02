influence = OLSInfluence(selected_model)
with np.errstate(invalid="ignore", divide="ignore"):  # для h = 1 формули містять 0/0
    leverage = pd.Series(influence.hat_matrix_diag, index=y.index)
    student = pd.Series(influence.resid_studentized_internal, index=y.index)
    cooks = pd.Series(influence.cooks_distance[0], index=y.index)
# h = 1: модель точно підганяє продаж, його залишок дорівнює нулю.
exact_fit = leverage > 1 - 1e-8
cooks[exact_fit] = np.nan    # h = 1: залишок 0, D = 0/0 не визначено
student[exact_fit] = np.nan
# Чутливість: оцінки без спостереження з найбільшим Cook's D.
top_cook = cooks.idxmax()
without_top = sm.OLS(y.drop(top_cook), X_selected.drop(top_cook)).fit()
# Далі: assert суми важелів, пошук рідкісних рівнів для h = 1, таблиці, графіки.
