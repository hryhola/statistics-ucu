# Вище: імпорти, налаштування та підготовка змінних.
t = tree.tree_
left, right = t.children_left[0], t.children_right[0]
N, NL, NR = t.weighted_n_node_samples[[0, left, right]]
I, IL, IR = t.impurity[[0, left, right]]
improvement = I - NL / N * IL - NR / N * IR
root_feature = feature_names[t.feature[0]]
root_threshold = shown_tree.tree_.threshold[0]
# Незалежна перевірка без використання збережених impurity дочірніх вузлів.
mask = Z_train[:, t.feature[0]] <= t.threshold[0]
root_rss = np.sum((y_train - y_train.mean()) ** 2)
children_rss = sum(np.sum((group - group.mean()) ** 2) for group in [y_train[mask], y_train[~mask]])
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
