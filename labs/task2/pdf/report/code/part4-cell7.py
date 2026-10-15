null_samples = rng.normal(loc=NULL_MEAN, scale=TRUE_SD, size=(REPLICATIONS, N))
t_statistics = (null_samples.mean(axis=1) - NULL_MEAN) / (null_samples.std(axis=1, ddof=1) / np.sqrt(N))
rejection_indicators = (np.abs(t_statistics) > critical).astype(int)
empirical_alpha = rejection_indicators.mean()
mc_se = np.sqrt(ALPHA * (1 - ALPHA) / REPLICATIONS)
size_results = pd.DataFrame({"M": [REPLICATIONS], "rejections": [rejection_indicators.sum()],
    "empirical_alpha": [empirical_alpha], "nominal_alpha": [ALPHA],
    "mc_se_under_null": [mc_se], "difference_in_se": [(empirical_alpha - ALPHA) / mc_se]})
display(size_results.T)
size_results.to_csv(RESULTS_DIR / "part4_size.csv", index=False)
pd.DataFrame({"t": t_statistics, "reject": rejection_indicators}).to_csv(
    RESULTS_DIR / "part4_replications.csv", index=False)
