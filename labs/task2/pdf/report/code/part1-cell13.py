mean_of_mean = SHAPE * SCALE
variance_of_mean = SHAPE * SCALE**2 / SMALL_N
mean_comparison = pd.DataFrame({
    "quantity": ["E(mean)", "Var(mean)", "E(sample variance)"],
    "theoretical": [mean_of_mean, variance_of_mean, TRUE_VARIANCE],
    "simulation": [small_means.mean(), small_means.var(ddof=1), small_variances.mean()],
})
display(mean_comparison.round(6))
mean_comparison.to_csv(RESULTS_DIR / "part1_comparison.csv", index=False)
