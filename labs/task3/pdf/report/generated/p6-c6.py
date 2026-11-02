from scipy.optimize import curve_fit
# За умовою беремо перші 500 рядків файлу.
df_500 = df.iloc[:500].copy()
x = df_500["YearBuilt"].to_numpy(dtype=float)
y = df_500["SalePrice"].to_numpy(dtype=float)
n = len(y)
# МНК через формулу statsmodels; fittedvalues - прогнози на тих самих 500 продажах.
linear_model = smf.ols("SalePrice ~ YearBuilt", data=df_500).fit()
linear_pred = linear_model.fittedvalues.to_numpy()
years = np.linspace(x.min(), x.max(), 300)
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(x, y, s=10, alpha=0.4, label="Продажі (перші 500)")
ax.plot(years, linear_model.params["Intercept"] + linear_model.params["YearBuilt"] * years,
        color="red", label="Лінійна регресія")
plt.show()
# Далі: describe(), роки продажу, таблиці оцінок і залишків, оформлення графіка.
