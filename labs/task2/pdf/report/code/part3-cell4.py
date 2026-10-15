session = df["Session_Time"].dropna()
n_session = len(session)
session_mean, session_sd = session.mean(), session.std(ddof=1)
t_session = (session_mean - 15) / (session_sd / np.sqrt(n_session))
session_df = n_session - 1
session_critical = stats.t.ppf(1 - ALPHA, session_df)
session_test = stats.ttest_1samp(session, popmean=15, alternative="greater")
assert np.isclose(t_session, session_test.statistic)
session_results = pd.DataFrame({"n": [n_session], "mean": [session_mean], "sd": [session_sd],
    "t": [t_session], "df": [session_df], "critical": [session_critical],
    "p": [session_test.pvalue], "reject": [session_test.pvalue < ALPHA]})
display(session_results)
session_results.to_csv(RESULTS_DIR / "part3_session.csv", index=False)
