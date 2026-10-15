z_critical = stats.norm.ppf(1 - ALPHA / 2)
t_critical = stats.t.ppf(1 - ALPHA / 2, df=SAMPLE_SIZES - 1)
known_margin = z_critical * np.sqrt(TRUE_VARIANCE / SAMPLE_SIZES)
estimated_margin = t_critical * np.sqrt(moments["variance"] / SAMPLE_SIZES)
intervals = moments[["n", "mean"]].copy()
intervals["known_lower"] = moments["mean"] - known_margin
intervals["known_upper"] = moments["mean"] + known_margin
intervals["estimated_lower"] = moments["mean"] - estimated_margin
intervals["estimated_upper"] = moments["mean"] + estimated_margin
display(intervals.round(6))
intervals.to_csv(RESULTS_DIR / "part1_intervals.csv", index=False)

fig, ax = plt.subplots(figsize=(8, 4.8))
ax.errorbar(SAMPLE_SIZES, moments["mean"], yerr=estimated_margin,
            fmt="o-", capsize=6, alpha=0.75, label="Оцінене s: t-інтервал")
ax.errorbar(SAMPLE_SIZES, moments["mean"], yerr=known_margin,
            fmt="s", capsize=3, color="darkorange", label="Відоме σ: z-інтервал")
ax.axhline(TRUE_MEAN, color="black", linestyle="--", label=r"$\mu=10$")
ax.set(xscale="log", xlabel="Обсяг вибірки n (логарифмічна шкала)",
       ylabel="Середній час (умовні одиниці)", title="Наближені 95% довірчі інтервали")
ax.legend()
fig.tight_layout()
fig.savefig(FIGURES_DIR / "part1_intervals.pdf")
plt.show()
