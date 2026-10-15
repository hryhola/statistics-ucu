def negative_log_likelihood(p_array):
    p = p_array[0]
    return -np.sum(registrations * np.log(p) + (1 - registrations) * np.log1p(-p))

fit = minimize(negative_log_likelihood, x0=[0.5], bounds=P_BOUNDS, method="L-BFGS-B")
if not fit.success:
    raise RuntimeError(fit.message)
p_hat = float(fit.x[0])
sample_proportion = float(registrations.mean())
mle_results = pd.DataFrame({"p_hat": [p_hat], "sample_mean": [sample_proportion],
                            "absolute_difference": [abs(p_hat - sample_proportion)],
                            "negative_log_likelihood": [fit.fun]})
display(mle_results)
mle_results.to_csv(RESULTS_DIR / "part2_mle.csv", index=False)
