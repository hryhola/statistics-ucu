# Вище: assert, що TotalBsmtSF і GrLivArea є сумами інших площ.
# Зберігаємо повні блоки кожної початкової змінної, навіть якщо індикатори збігаються.
# BldgType перед MSSubClass: спільний індикатор Duplex належить контрольній змінній.
category_order = ["BldgType"] + [c for c in categorical if c != "BldgType"]
groups = {column: [column] for column in numeric}
blocks = [analysis[numeric].astype(float)]
for column in category_order:
    dummies = pd.get_dummies(analysis[column], prefix=column, dtype=float)
    dummies = dummies.drop(columns=f"{column}_{analysis[column].mode()[0]}")
    groups[column] = list(dummies.columns)
    blocks.append(dummies)
X_encoded = pd.concat(blocks, axis=1)
def design_matrix(active):
    """Матриця активних змінних: прибираємо копії лише в цій моделі."""
    columns = [c for group in active for c in groups[group]]
    X = X_encoded[columns]
    return sm.add_constant(X.loc[:, ~X.T.duplicated()], has_constant="add")
X_full = design_matrix(list(groups))
y = analysis["SalePrice"].astype(float)
full_model = sm.OLS(y, X_full).fit()
# Коефіцієнти MSSubClass, які справді оцінюються (без копії індикатора дуплексу).
dummy_names = [name for name in X_full.columns if name.startswith("MSSubClass_")]
q, k = len(dummy_names), X_full.shape[1]
positions = X_full.columns.get_indexer(dummy_names)
# Матриця обмежень: один рядок на кожен коефіцієнт MSSubClass; вектор r = 0.
R = np.zeros((q, k))
R[np.arange(q), positions] = 1
r = np.zeros(q)
# f_test() перевіряє H0: R beta = r у повній моделі.
f_result = full_model.f_test((R, r))
# Далі: assert рангу, модель без MSSubClass, ручний F і assert збігу з f_test().
