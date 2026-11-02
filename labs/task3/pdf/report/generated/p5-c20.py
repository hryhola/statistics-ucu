# conf_int() будує інтервал beta ± t_{0.975, n-k} * SE.
ci = full_model.conf_int(alpha=ALPHA).loc["LotArea"]
# H0 Jarque-Bera: асиметрія 0 та ексцес 3, як у нормального розподілу.
jb = stats.jarque_bera(full_model.resid)
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(full_model.resid, bins=60, edgecolor="white")
sm.qqplot(full_model.resid, line="s", ax=axes[1], markersize=3)
plt.show()
# Далі: ручний перерахунок інтервалу з assert, підписи осей, збереження рисунка.
