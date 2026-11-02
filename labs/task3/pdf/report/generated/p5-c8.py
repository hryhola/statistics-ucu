scatter_columns = ["LotFrontage", "LotArea", "YearBuilt", "BsmtFinSF1", "BsmtUnfSF"]
units = {"LotFrontage": "фути", "LotArea": "кв. фути", "YearBuilt": "рік",
         "BsmtFinSF1": "кв. фути", "BsmtUnfSF": "кв. фути"}
# П’ять діаграм розсіювання; пропуски (LotFrontage) прибираємо попарно.
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
for ax, column in zip(axes.flat, scatter_columns):
    pairs = df[[column, "SalePrice"]].dropna()
    ax.scatter(pairs[column], pairs["SalePrice"], s=8, alpha=0.3)
    ax.set(title=f"SalePrice та {column} (n={len(pairs)})",
           xlabel=f"{column}, {units[column]}", ylabel="SalePrice, дол. США")
axes.flat[-1].axis("off")
plt.show()
# Далі: збереження рисунка; describe(), нулі, кореляції, групи років (виводи нижче).
