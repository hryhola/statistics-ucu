expected_registrations = FUTURE_VISITORS * p_hat
first_above_mean = int(np.floor(expected_registrations)) + 1
probabilities = pd.DataFrame({
    "event": ["K = 5", "K >= 8", f"K > 20*p_hat (K >= {first_above_mean})"],
    "probability": [stats.binom.pmf(5, FUTURE_VISITORS, p_hat),
                    stats.binom.sf(7, FUTURE_VISITORS, p_hat),
                    stats.binom.sf(first_above_mean - 1, FUTURE_VISITORS, p_hat)],
})
print(f"E(K) = {expected_registrations:.8f}; first integer above E(K): {first_above_mean}")
display(probabilities)
probabilities.to_csv(RESULTS_DIR / "part2_probabilities.csv", index=False)
