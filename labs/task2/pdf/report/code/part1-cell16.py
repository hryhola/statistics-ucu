x_grid = np.linspace(min(0, small_means.min()), small_means.max(), 500)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(small_means, bins=30, density=True, edgecolor="white", alpha=0.7,
        label="Середні Gamma(2, 5), n = 4")
ax.plot(x_grid, stats.norm.pdf(x_grid, loc=mean_of_mean, scale=np.sqrt(variance_of_mean)),
        color="darkred", linewidth=2, label="Нормальна щільність N(10, 12.5)")
ax.set(xlabel="Вибіркове середнє (умовні одиниці)", ylabel="Щільність (1 / ум. од.)",
       title="Нормальне наближення для середнього, n = 4")
ax.legend()
fig.tight_layout()
fig.savefig(FIGURES_DIR / "part1_normal_approximation.pdf")
plt.show()
