# Вище: імпорти, налаштування та підготовка змінних.
def fit_logit(columns):
    # Усі порівняння використовують ті самі рядки й звичайний ММП без штрафу.
    result = sm.Logit(y_train, Z_train[["const"] + columns]).fit(
        method="newton", maxiter=200, tol=1e-9, disp=False)
    if not result.mle_retvals["converged"] or not np.isfinite(result.aic):
        raise RuntimeError("Кандидатна модель не збіглася; AIC не порівнюємо.")
    return result
selected = list(X.columns)
model = fit_logit(selected)
selection_rows = [{"Крок": 0, "Вилучено": "Початкова модель", "Ознак": len(selected), "AIC": model.aic}]
fits_checked = 1
while selected:
    candidates = []
    for column in selected:
        remaining = [name for name in selected if name != column]
        candidate = fit_logit(remaining)
        fits_checked += 1
        candidates.append((candidate.aic, column, candidate))
    best_aic, removed, candidate = min(candidates, key=lambda item: item[0])
    # Поріг відокремлює покращення від похибки округлення.
    if best_aic >= model.aic - 1e-8:
        break
    selected.remove(removed)
    model = candidate
    selection_rows.append({"Крок": len(selection_rows), "Вилучено": removed,
                           "Ознак": len(selected), "AIC": model.aic})
# Повертаємо нахили та константу до початкових одиниць.
beta_raw = model.params[selected] / scales[selected]
intercept_raw = model.params["const"] - (beta_raw * means[selected]).sum()
se_raw = model.bse[selected] / scales[selected]
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
