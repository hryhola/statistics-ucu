power_rows = []
for degrees in DEGREES_OF_FREEDOM:
    samples = rng.standard_t(df=degrees, size=(REPLICATIONS, N))
    rejections = 0
    for sample in samples:
        _, p_value = lilliefors(sample, dist="norm", pvalmethod="table")
        rejections += int(p_value < ALPHA)
    power_rows.append({"df": degrees, "rejections": rejections,
                       "power": rejections / REPLICATIONS})
power_results = pd.DataFrame(power_rows)
power_results["mc_se"] = np.sqrt(power_results["power"] * (1 - power_results["power"]) / REPLICATIONS)
power_results["beta_estimate"] = 1 - power_results["power"]
display(power_results)
power_results.to_csv(RESULTS_DIR / "part5_power.csv", index=False)
print(f"Виконано тестів: {len(DEGREES_OF_FREEDOM) * REPLICATIONS}")

fig, ax = plt.subplots(figsize=(9, 4.8))
ax.plot(power_results["df"], power_results["power"], "o-", markersize=3,
        label="Оцінена потужність")
ax.axhline(ALPHA, color="black", linestyle="--", label="Рівень значущості α = 0.05")
ax.set(xlabel="Число ступенів свободи df", ylabel="Частка відхилень нормальності",
       title="Потужність критерію Лілієфорса: n = 80, M = 1000", ylim=(0, 1))
ax.legend()
fig.tight_layout()
fig.savefig(FIGURES_DIR / "part5_power.pdf")
plt.show()
