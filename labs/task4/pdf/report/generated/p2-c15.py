# Вище: імпорти, налаштування та підготовка змінних.
tree = DecisionTreeRegressor(max_leaf_nodes=11, random_state=SEED)
tree.fit(Z_train, y_train)
structure = pd.Series({
    "Листків": tree.get_n_leaves(), "Поділів": tree.tree_.node_count - tree.get_n_leaves(),
    "Глибина": tree.get_depth(),
    "Навчальна MSE, дол.^2": mean_squared_error(y_train, tree.predict(Z_train)),
    "Валідаційна MSE, дол.^2": mean_squared_error(y_valid, tree.predict(Z_valid)),
})
shown_tree = deepcopy(tree)
scaler = prepared.named_transformers_["num"].named_steps["scale"]
for node, feature in enumerate(shown_tree.tree_.feature):
    if 0 <= feature < len(numeric_columns):
        shown_tree.tree_.threshold[node] = tree.tree_.threshold[node] * scaler.scale_[feature] + scaler.mean_[feature]
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
