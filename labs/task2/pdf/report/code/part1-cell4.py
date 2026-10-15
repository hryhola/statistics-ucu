samples = [rng.gamma(shape=SHAPE, scale=SCALE, size=int(n)) for n in SAMPLE_SIZES]
moments = pd.DataFrame({
    "n": SAMPLE_SIZES,
    "mean": [x.mean() for x in samples],
    "variance": [x.var(ddof=1) for x in samples],
})
display(moments.round(6))
moments.to_csv(RESULTS_DIR / "part1_moments.csv", index=False)

fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(moments["n"], moments["mean"], "o-", label="Вибіркове середнє")
ax.axhline(TRUE_MEAN, color="black", linestyle="--", label=r"$\mu=10$")
ax.set(xscale="log", xlabel="Обсяг вибірки n (логарифмічна шкала)",
       ylabel="Середній час (умовні одиниці)", title="Закон великих чисел: середні Gamma(2, 5)")
ax.legend()
fig.tight_layout()
fig.savefig(FIGURES_DIR / "part1_lln.pdf")
plt.show()
