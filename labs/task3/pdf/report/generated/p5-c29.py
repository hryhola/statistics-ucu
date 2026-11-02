# Повний df: усі 2930 рядків і всі колонки. Ховаємо LotArea у 5 випадкових рядках.
masked_index = rng.choice(df.index.to_numpy(), size=5, replace=False)
true_lotarea = df.loc[masked_index, "LotArea"]
df_missing = df.copy()
df_missing["LotArea"] = df_missing["LotArea"].astype(float)
df_missing.loc[masked_index, "LotArea"] = np.nan
# Заповнюємо лише числові NaN. Категоріальні "NA" не чіпаємо; GarageYrBlt без гаража
# не є пропуском; MSSubClass - коди категорій; SalePrice - відгук, який пояснюємо.
impute_columns = [c for c in df.select_dtypes("number").columns
                  if c not in ["Order", "PID", "SalePrice", "MSSubClass", "GarageYrBlt"]]
# Підхід 1: медіана колонки. Підхід 2: кожну колонку з пропусками регресуємо на решту.
median_filled = df_missing.copy()
median_filled[impute_columns] = SimpleImputer(strategy="median").fit_transform(df_missing[impute_columns])
iterative_filled = df_missing.copy()
iterative_filled[impute_columns] = IterativeImputer(max_iter=25, random_state=SEED).fit_transform(df_missing[impute_columns])
# Далі: таблиці порівняння з істинними значеннями; assert, що змінено лише пропуски.
