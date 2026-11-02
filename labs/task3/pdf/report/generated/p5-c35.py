X_full_cv = X_full.drop(columns="const")        # LinearRegression сама додає константу
X_selected_cv = X_selected.drop(columns="const")
splitters = {"LeaveOneOut": LeaveOneOut(),
             "KFold (5 блоків)": KFold(n_splits=5, shuffle=True, random_state=SEED)}
models = {"Повна": (X_full_cv, full_model), "Після відбору": (X_selected_cv, selected_model)}
cv_rows, cv_errors = [], {}
# cross_val_predict навчає модель без тестового блоку і прогнозує саме його.
for scheme, splitter in splitters.items():
    for name, (X_cv, fitted_model) in models.items():
        prediction = cross_val_predict(LinearRegression(), X_cv, y, cv=splitter, n_jobs=-1)
        cv_errors[(scheme, name)] = y - prediction
        mse = np.mean((y - prediction) ** 2)
        cv_rows.append({"Схема": scheme, "Модель": name, "Параметрів": X_cv.shape[1] + 1,
                        "MSE навчальне, дол.²": fitted_model.ssr / n_obs,
                        "MSE крос-валідації, дол.²": mse, "RMSE, дол.": np.sqrt(mse)})
cv_results = pd.DataFrame(cv_rows)
# Далі: assert збігу LinearRegression і OLS, найбільші помилки LOO, графік.
