# Вище: імпорти, налаштування та підготовка змінних.
fpr, tpr, thresholds = roc_curve(y_valid, valid_probabilities, drop_intermediate=False)
auc_value = roc_auc_score(y_valid, valid_probabilities)
youden = tpr - fpr
finite = np.flatnonzero(np.isfinite(thresholds))
# При однаковому максимумі беремо найбільший поріг: roc_curve повертає їх за спаданням.
best = finite[np.argmax(youden[finite])]
optimal_threshold = thresholds[best]
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
