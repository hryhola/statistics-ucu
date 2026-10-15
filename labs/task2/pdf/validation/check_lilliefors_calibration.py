"""Independent review diagnostic; does not modify the required experiment.

Run from the repository root:
    .venv/bin/python labs/task2/pdf/validation/check_lilliefors_calibration.py
"""

import inspect
import json
from pathlib import Path

import numpy as np
import scipy
import statsmodels
from scipy import stats
from statsmodels.stats._lilliefors import get_lilliefors_table
from statsmodels.stats.diagnostic import lilliefors


def independent_statistic(samples):
    """Compute the two-sided fitted-normal KS statistic for each row."""
    n = samples.shape[1]
    standardized = (samples - samples.mean(axis=1, keepdims=True)) / samples.std(
        axis=1, ddof=1, keepdims=True
    )
    fitted_cdf = stats.norm.cdf(np.sort(standardized, axis=1))
    d_plus = np.max(np.arange(1, n + 1) / n - fitted_cdf, axis=1)
    d_minus = np.max(fitted_cdf - np.arange(n) / n, axis=1)
    return np.maximum(d_plus, d_minus)


SEED = 20261014
N = 80
REPLICATIONS = 200000
BATCH_SIZE = 10000
ALPHA = 0.05

table = get_lilliefors_table("norm")
critical = float(table.crit(ALPHA, N))
critical_50 = float(table.crit(ALPHA, 50))
critical_100 = float(table.crit(ALPHA, 100))
interpolated = critical_50 + (N - 50) / (100 - 50) * (critical_100 - critical_50)
np.testing.assert_allclose(critical, interpolated)

rng = np.random.default_rng(SEED)
statistics = []
for start in range(0, REPLICATIONS, BATCH_SIZE):
    samples = rng.normal(size=(BATCH_SIZE, N))
    batch_statistics = independent_statistic(samples)
    if start == 0:
        library = np.array([lilliefors(x, pvalmethod="table") for x in samples[:100]])
        np.testing.assert_allclose(batch_statistics[:100], library[:, 0], atol=1e-15)
        np.testing.assert_array_equal(batch_statistics[:100] > critical, library[:, 1] < ALPHA)
    statistics.append(batch_statistics)

statistics = np.concatenate(statistics)
rejections = int(np.sum(statistics > critical))
rate = rejections / REPLICATIONS
interval = stats.binomtest(rejections, REPLICATIONS).proportion_ci(0.95, method="exact")
result = {
    "purpose": "Independent verification of calibration; required assignment results are unchanged",
    "versions": {"numpy": np.__version__, "scipy": scipy.__version__, "statsmodels": statsmodels.__version__},
    "installed_source_files": {
        "lilliefors": inspect.getsourcefile(lilliefors),
        "table_critical_value_interpolation": inspect.getsourcefile(type(table)._critvals),
    },
    "method": "N(0,1) samples; independent fitted-normal KS statistic with ddof=1; reject above the installed table's alpha=0.05 critical value",
    "seed": SEED,
    "n": N,
    "replications": REPLICATIONS,
    "batch_size": BATCH_SIZE,
    "nominal_alpha": ALPHA,
    "critical_n50": critical_50,
    "critical_n80": critical,
    "critical_n100": critical_100,
    "linear_interpolation_verified": True,
    "library_statistic_and_decision_checks": 100,
    "rejections": rejections,
    "estimated_actual_size": rate,
    "mc_standard_error": float(np.sqrt(rate * (1 - rate) / REPLICATIONS)),
    "exact_binomial_95_percent_interval": [float(interval.low), float(interval.high)],
    "empirical_D_95th_percentile": float(np.quantile(statistics, 0.95)),
}

destination = Path(__file__).with_name("lilliefors_calibration.json")
destination.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
