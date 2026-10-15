small_samples = rng.gamma(shape=SHAPE, scale=SCALE, size=(REPLICATIONS, SMALL_N))
small_means = small_samples.mean(axis=1)
small_variances = small_samples.var(axis=1, ddof=1)
repeated_moments = pd.DataFrame({"mean": small_means, "variance": small_variances})
repeated_moments.to_csv(RESULTS_DIR / "part1_repeated_moments.csv", index=False)
display(repeated_moments.agg(["mean", "var"]).round(6))

fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
axes[0].hist(small_means, bins=30, edgecolor="white")
axes[0].set(xlabel="Вибіркове середнє (умовні одиниці)", ylabel="Кількість вибірок",
            title="1000 середніх, n = 4")
axes[1].hist(small_variances, bins=30, edgecolor="white", color="darkorange")
axes[1].set(xlabel="Вибіркова дисперсія (ум. од.²)", ylabel="Кількість вибірок",
            title="1000 дисперсій, n = 4")
fig.tight_layout()
fig.savefig(FIGURES_DIR / "part1_histograms.pdf")
plt.show()
