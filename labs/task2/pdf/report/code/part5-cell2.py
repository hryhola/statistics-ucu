from statsmodels.stats.diagnostic import lilliefors

N = 80
REPLICATIONS = 1000
DEGREES_OF_FREEDOM = np.arange(2, 61)
# ALPHA = 0.05 follows the preceding testing sections; record this convention.
# Full assignment: 59 × 1000 = 59,000 normality tests.
