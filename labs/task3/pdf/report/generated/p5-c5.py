# Вище: print типу MSSubClass (вивід нижче).
numeric_class = smf.ols("SalePrice ~ MSSubClass", data=df).fit()          # як int64
formula_class = smf.ols("SalePrice ~ C(MSSubClass)", data=df).fit()       # C(...) у формулі
df_category = df.assign(MSSubClass=pd.Categorical(df["MSSubClass"]))
category_class = smf.ols("SalePrice ~ MSSubClass", data=df_category).fit()  # pd.Categorical
# Далі: assert рівності прогнозів, збирання таблиць (виводи нижче), графік.
