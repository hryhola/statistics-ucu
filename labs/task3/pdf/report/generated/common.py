# Вище: імпорти бібліотек, шляхи до файлів, налаштування графіків.
SEED = 42
ALPHA = 0.05
rng = np.random.default_rng(SEED)
DATA_PATH = INPUT_DIR / "AmesHousing.txt"
# Пропуск - лише порожнє поле; текст "NA" лишається значенням категорії.
df = pd.read_csv(DATA_PATH, sep="\t", keep_default_na=False, na_values=[""])
# Назви як у Kaggle та в умові: "Lot Area" -> "LotArea", "Year Remod/Add" -> "YearRemodAdd".
df.columns = df.columns.str.replace(" ", "").str.replace("/", "")
text_columns = list(df.select_dtypes(exclude="number").columns)
for column in text_columns:
    df[column] = df[column].str.strip()  # у SaleType є зайві пробіли, напр. "WD "
# MSSubClass і текстові колонки - категорії; рядок "NA" в них - окремий рівень.
categorical = ["MSSubClass"] + text_columns
# Order, PID - ідентифікатори; GarageYrBlt не існує для будинків без гаража;
# TotalBsmtSF і GrLivArea - точні суми інших площ (див. пункт 4).
excluded = ["Order", "PID", "SalePrice", "GarageYrBlt", "TotalBsmtSF", "GrLivArea"]
numeric = [column for column in df.columns if column not in categorical + excluded]
analysis = df.dropna(subset=numeric + categorical).copy()
# Далі: розмір df, кількість пропусків і структурних рівнів "NA".
