subscription = df["Subscription"].dropna()
n_subscription = len(subscription)
count_subscription = int(subscription.sum())
p0 = 0.10
subscription_share = count_subscription / n_subscription
z_subscription = (subscription_share - p0) / np.sqrt(p0 * (1 - p0) / n_subscription)
z_builtin, p_subscription = proportions_ztest(count_subscription, n_subscription,
    value=p0, alternative="larger", prop_var=p0)
assert np.isclose(z_subscription, z_builtin)
subscription_critical = stats.norm.ppf(1 - ALPHA)
subscription_results = pd.DataFrame({"n": [n_subscription], "successes": [count_subscription],
    "share": [subscription_share], "expected_successes_null": [n_subscription * p0],
    "expected_failures_null": [n_subscription * (1 - p0)], "z": [z_subscription],
    "critical": [subscription_critical], "p": [p_subscription], "reject": [p_subscription < ALPHA]})
display(subscription_results.T)
subscription_results.to_csv(RESULTS_DIR / "part3_subscription.csv", index=False)
