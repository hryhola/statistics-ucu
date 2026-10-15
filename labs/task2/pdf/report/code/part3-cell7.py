ios = df.loc[df["Platform"] == "iOS", "Revenue"].dropna()
android = df.loc[df["Platform"] == "Android", "Revenue"].dropna()
n_ios, n_android = len(ios), len(android)
mean_ios, mean_android = ios.mean(), android.mean()
var_ios, var_android = ios.var(ddof=1), android.var(ddof=1)
v_ios, v_android = var_ios / n_ios, var_android / n_android
welch_se = np.sqrt(v_ios + v_android)
t_welch = (mean_ios - mean_android) / welch_se
welch_df = (v_ios + v_android)**2 / (v_ios**2 / (n_ios - 1) + v_android**2 / (n_android - 1))
welch_critical = stats.t.ppf(1 - ALPHA / 2, welch_df)
welch_test = stats.ttest_ind(ios, android, equal_var=False, alternative="two-sided")
assert np.isclose(t_welch, welch_test.statistic)
welch_results = pd.DataFrame({"n_ios": [n_ios], "n_android": [n_android],
    "mean_ios": [mean_ios], "mean_android": [mean_android],
    "var_ios": [var_ios], "var_android": [var_android],
    "t": [t_welch], "df": [welch_df], "critical": [welch_critical],
    "p": [welch_test.pvalue], "reject": [welch_test.pvalue < ALPHA]})
display(welch_results.T)
welch_results.to_csv(RESULTS_DIR / "part3_welch.csv", index=False)
