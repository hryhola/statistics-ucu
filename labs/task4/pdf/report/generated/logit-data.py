# Вище: імпорти, налаштування та підготовка змінних.
y = (df["SalePrice"] > 130000).astype(int).rename("Above130000")
excluded = ["SalePrice", "Order", "PID", "MSSubClass", "GarageYrBlt", "GrLivArea", "TotalBsmtSF"]
X = df.select_dtypes(include="number").drop(columns=excluded)
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=SEED)
imputer = SimpleImputer(strategy="median")
raw_train = pd.DataFrame(imputer.fit_transform(X_train), index=X_train.index, columns=X.columns)
raw_valid = pd.DataFrame(imputer.transform(X_valid), index=X_valid.index, columns=X.columns)
scaler = StandardScaler()
Z_train = pd.DataFrame(scaler.fit_transform(raw_train), index=X_train.index, columns=X.columns)
Z_valid = pd.DataFrame(scaler.transform(raw_valid), index=X_valid.index, columns=X.columns)
Z_train = sm.add_constant(Z_train)
Z_valid = sm.add_constant(Z_valid)
means = pd.Series(scaler.mean_, index=X.columns)
scales = pd.Series(scaler.scale_, index=X.columns)
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
