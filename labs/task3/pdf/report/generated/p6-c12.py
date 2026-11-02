# curve_fit оцінює коваріацію через лінеаризацію: pcov = s^2 (J^T J)^(-1),
# де J - похідні моделі за a і b в точці оцінки, s^2 = RSS / (n - 2).
t = x - YEAR_0
J = np.column_stack([np.exp(b_hat * t), a_hat * t * np.exp(b_hat * t)])
s2 = np.sum((y - exp_pred) ** 2) / (n - 2)
se = np.sqrt(np.diag(pcov))
z = stats.norm.ppf(1 - ALPHA / 2)
# Нормальність залишків NLS перевіряємо тим самим тестом Jarque-Bera.
residuals = y - exp_pred
jb = stats.jarque_bera(residuals)
# Далі: assert pcov = s²(JᵀJ)⁻¹, таблиця оцінок, розкид залишків за періодами, графік.
