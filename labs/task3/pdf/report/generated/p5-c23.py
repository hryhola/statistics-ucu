def backward_bic(y, groups):
    """Зворотний відбір початкових змінних за BIC."""
    active = list(groups)
    model = sm.OLS(y, design_matrix(active)).fit()
    history = [{"Крок": 0, "Вилучено": "-", "k": int(model.df_model + 1), "BIC": model.bic}]
    while active:
        best_group, best_model = None, None
        # Пробуємо вилучити кожну змінну окремо; запам’ятовуємо кандидата з найменшим BIC.
        for group in active:
            remaining = [g for g in active if g != group]
            candidate = sm.OLS(y, design_matrix(remaining)).fit()
            if best_model is None or candidate.bic < best_model.bic:
                best_group, best_model = group, candidate
        # Зупиняємося, коли жодне вилучення не зменшує BIC.
        if best_model.bic >= model.bic:
            break
        active.remove(best_group)
        model = best_model
        history.append({"Крок": len(history), "Вилучено": best_group,
                        "k": int(model.df_model + 1), "BIC": model.bic})
    return model, active, pd.DataFrame(history)
# Починаємо з усіх початкових змінних; категорію вилучаємо цілим блоком індикаторів.
selected_model, selected_terms, history = backward_bic(y, groups)
X_selected = design_matrix(selected_terms)
# Далі: assert рангу і локального оптимуму BIC; друк історії та списку змінних.
