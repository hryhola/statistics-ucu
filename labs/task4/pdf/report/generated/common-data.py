# Вище: імпорти, налаштування та підготовка змінних.
df = pd.read_csv(DATA_PATH, sep="\t", keep_default_na=False, na_values=[""])
df.columns = df.columns.str.replace(" ", "").str.replace("/", "")
for column in df.select_dtypes(exclude="number").columns:
    df[column] = df[column].str.strip()
df["MSSubClass"] = df["MSSubClass"].astype(str)
X = df.drop(columns=["SalePrice", "Order", "PID", "GarageYrBlt"])
y = df["SalePrice"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED
)
numeric_columns = X.select_dtypes(include="number").columns.tolist()
categorical_columns = X.select_dtypes(exclude="number").columns.tolist()
# Далі: таблиці, графіки й перевірки; фактичні виводи наведено нижче.
