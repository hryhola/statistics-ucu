registrations = df["Registration_Success"].dropna().to_numpy()
registration_d, registration_p = lilliefors(registrations, dist="norm", pvalmethod="table")
normality = pd.DataFrame({"n": [len(registrations)], "successes": [registrations.sum()],
                          "D": [registration_d], "p_returned": [registration_p],
                          "reject": [registration_p < ALPHA]})
display(normality)
normality.to_csv(RESULTS_DIR / "part2_normality.csv", index=False)
