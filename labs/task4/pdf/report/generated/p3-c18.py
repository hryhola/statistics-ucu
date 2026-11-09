# Вище: імпорти, налаштування та підготовка змінних.
valid_probabilities = model.predict(Z_valid[["const"] + selected])
def threshold_metrics(threshold):
    predicted = (valid_probabilities >= threshold).astype(int)
    matrix = confusion_matrix(y_valid, predicted, labels=[0, 1])
    tn, fp, fn, tp = matrix.ravel()
    metrics = {"Поріг": threshold, "TN": tn, "FP": fp, "FN": fn, "TP": tp,
               "Чутливість": tp / (tp + fn), "Специфічність": tn / (tn + fp),
               "Accuracy": (tp + tn) / matrix.sum(), "Прогнозів класу 1": predicted.sum()}
    return matrix, metrics
matrix_default, metrics_default = threshold_metrics(0.5)
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
