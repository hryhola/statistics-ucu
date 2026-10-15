sample = rng.normal(loc=NULL_MEAN, scale=TRUE_SD, size=N)
sample_mean, sample_sd = sample.mean(), sample.std(ddof=1)
t_statistic = (sample_mean - NULL_MEAN) / (sample_sd / np.sqrt(N))
critical = stats.t.ppf(1 - ALPHA / 2, df=N - 1)
p_value = 2 * stats.t.sf(abs(t_statistic), df=N - 1)
single_result = pd.DataFrame({"n": [N], "mean": [sample_mean], "sd": [sample_sd],
    "t": [t_statistic], "df": [N - 1], "critical": [critical], "p": [p_value],
    "reject": [abs(t_statistic) > critical]})
display(single_result)
single_result.to_csv(RESULTS_DIR / "part4_single.csv", index=False)
