# Task 1 — Descriptive statistics and probability

The authoritative assignment is [task1-description.pdf](task1-description.pdf).
This directory covers all three problems in that PDF; notebooks are scaffolds,
not completed solutions.

1. `task1-problem1-ceosal1.ipynb`: CEO salaries, descriptive statistics,
   correlations, age groups, and contingency tables.
2. `task1-problem2-simulation.ipynb`: contaminated normal samples and
   controlled correlations.
3. `task1-problem3-probability.ipynb`: conditional probability, binomial and
   continuous distributions, portfolio returns, and Tesla data.

Store input snapshots in `data/` and exported plots in `figures/`.
Paths work when launched from the repository root or this directory.
Problem 1 downloads ceosal1 on first execution and caches it locally.
Its age column is synthetic, reproducibly generated with seed 42;
it must not be interpreted as observed CEO ages.

## Assignment details to preserve

- Problem 2 jumps from Part 1 to Part 3 in the source; notebook labels follow it.
- The contamination sequence starting at 10 in steps of 20 ends at 190,
  although the PDF says “to 200”; document your endpoint convention.
  The separate plots explicitly request m = 20, 100, 200.
- Problem 1 Part 2 uses age < 50 and age > 50. State how exact age 50 is handled.
- Problem 3 Part 3 gives variance 0.02, not standard deviation 0.02.
- For Tesla, record the retrieval date, explicit two-year date range,
  price adjustment choice, and handling of incomplete weeks. Cache the data.

Before submission, restart each kernel, run all cells, save outputs, and
replace every TODO with code or interpretation.
