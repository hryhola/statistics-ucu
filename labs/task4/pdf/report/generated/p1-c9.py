# Вище: імпорти, налаштування та підготовка змінних.
# Кожне перетворення навчається лише на переданій навчальній частині.
numeric_pipe = Pipeline([
    ("impute", SimpleImputer(strategy="median")),
    ("scale", StandardScaler()),
])
categorical_pipe = Pipeline([
    ("impute", SimpleImputer(strategy="constant", fill_value="Missing")),
    ("encode", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False)),
])
preprocessor = ColumnTransformer([
    ("num", numeric_pipe, numeric_columns),
    ("cat", categorical_pipe, categorical_columns),
], verbose_feature_names_out=False)
prepared = clone(preprocessor).fit(X_train)
Z_train = prepared.transform(X_train)
Z_test = prepared.transform(X_test)
feature_names = prepared.get_feature_names_out()
scaler = prepared.named_transformers_["num"].named_steps["scale"]
encoder = prepared.named_transformers_["cat"].named_steps["encode"]
fireplace_index = categorical_columns.index("FireplaceQu")
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
