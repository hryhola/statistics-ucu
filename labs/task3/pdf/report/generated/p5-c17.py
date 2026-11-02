# Та сама матриця X_full, але відгук - log(SalePrice).
full_log_model = sm.OLS(np.log(y), X_full).fit()
first_dummy = dummy_names[0]
terms = ["LotArea", first_dummy, "BedroomAbvGr"]
gamma = full_log_model.params[terms]
# Далі: збирання таблиць коефіцієнтів і років побудови класів 20 і 30 (виводи нижче).
