revenue = df["Revenue"].dropna()
revenue_d, revenue_p = lilliefors(revenue, dist="norm", pvalmethod="table")
revenue_results = pd.DataFrame({"n": [len(revenue)], "D": [revenue_d],
    "p_returned": [revenue_p], "reject": [revenue_p < ALPHA]})
display(revenue_results)
revenue_results.to_csv(RESULTS_DIR / "part3_revenue_normality.csv", index=False)
