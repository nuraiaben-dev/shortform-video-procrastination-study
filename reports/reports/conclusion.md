## 5. Conclusion and Future Work

This work presented a research protocol, a reproducible analysis pipeline and the analysis of 14-day diary data from 200 university students on short-form video consumption, procrastination, and academic deadline adherence \cite{akniet2026shortform}. All inference uses the participant as the unit of analysis, because the procrastination score is measured once per student.

With respect to **RQ1**, students watched short-form video for 73.1 minutes per day on average (95% CI 69.5–76.7), the mean Tuckman score was 36.5 (95% CI 34.7–38.3), and 23.9% of tasks due were late or missed (95% CI 22.0–25.8).

With respect to **RQ2**, daily viewing time and procrastination were strongly positively associated (Spearman $\rho_s = 0.97$, 95% CI 0.96–0.98, one-sided $p < 0.001$), so H1 is supported. The association is unusually strong for self-reported measures, and the way X and P were measured should be discussed.

With respect to **RQ3**, viewing during study time was associated with more late tasks (IRR 1.75, 95% CI 1.26–2.42, Holm $p < 0.001$), while bedtime viewing was not clearly associated (IRR 1.17, 95% CI 0.83–1.64, Holm $p = 0.18$). Each additional 100 minutes of daily viewing was associated with an IRR of 3.66 (95% CI 2.73–4.91).

The study is observational and based on a convenience sample, and the protocol covariates (workload, study year, sleep) were not collected, so the results are associations and do not show that viewing causes procrastination. A separate synthetic-data benchmark showed that a one-pass participant-level aggregation reduced median execution time by a factor of 1.85× to 4.26× relative to the grouped-aggregation-plus-merge baseline, with a 0% error rate over 800 measured runs; this evaluates software performance only.

Three directions follow. **(i) Covariates and design.** Collect workload, study year and sleep, and recruit across courses and universities. **(ii) Causal evidence.** Test the proposed app-limit intervention in a randomised extension. **(iii) Measurement.** Validate diary reports against device logs at the day level and examine shared-method effects between X and P.
