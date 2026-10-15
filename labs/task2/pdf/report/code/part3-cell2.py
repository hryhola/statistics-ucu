# Source: the app_metrics.csv supplied alongside assignment_2.pdf.
# Keep the source file unchanged; no external download is required.
DATA_PATH = INPUT_DIR / "app_metrics.csv"
if not DATA_PATH.is_file():
    raise FileNotFoundError(f"Place the supplied app_metrics.csv at {DATA_PATH}")
df = pd.read_csv(DATA_PATH)
required = {"Platform", "Session_Time", "Registration_Success", "Page_Views",
            "Purchase_Amount", "Revenue", "Subscription"}
missing = required.difference(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")
for column in ("Registration_Success", "Subscription"):
    if not df[column].dropna().isin([0, 1]).all():
        raise ValueError(f"{column} must contain binary values 0 or 1")
# Review missing values before choosing a per-analysis handling policy.
display(df.head())
display(df.isna().sum().rename("missing"))

from statsmodels.stats.diagnostic import lilliefors
from statsmodels.stats.proportion import proportions_ztest
