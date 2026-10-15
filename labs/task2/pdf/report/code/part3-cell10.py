paired = df[["Page_Views", "Purchase_Amount"]].dropna()
n_pairs = len(paired)
x, y = paired["Page_Views"], paired["Purchase_Amount"]
dx, dy = x - x.mean(), y - y.mean()
sum_xy, sum_xx, sum_yy = (dx * dy).sum(), (dx**2).sum(), (dy**2).sum()
r = sum_xy / np.sqrt(sum_xx * sum_yy)
t_correlation = r * np.sqrt((n_pairs - 2) / (1 - r**2))
correlation_critical = stats.t.ppf(1 - ALPHA / 2, n_pairs - 2)
correlation_test = stats.pearsonr(x, y)
assert np.isclose(r, correlation_test.statistic)
assert np.isclose(2 * stats.t.sf(abs(t_correlation), n_pairs - 2), correlation_test.pvalue)
correlation_results = pd.DataFrame({"n": [n_pairs], "sum_xy": [sum_xy],
    "sum_xx": [sum_xx], "sum_yy": [sum_yy], "r": [r], "t": [t_correlation],
    "df": [n_pairs - 2], "critical": [correlation_critical],
    "p": [correlation_test.pvalue], "reject": [correlation_test.pvalue < ALPHA]})
display(correlation_results.T)
correlation_results.to_csv(RESULTS_DIR / "part3_correlation.csv", index=False)
