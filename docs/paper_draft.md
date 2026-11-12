1. Internal Validity

Constraint: The results were obtained in a single session on a single computer using synthetic data (a repeated sample of 10 rows, artificially expanded to 10,000).
What this means: The results may have been influenced by background operating system processes (e.g., Windows updates or antivirus activity) during the measurement. We did not test how the code would behave on other machines.
2. Construct Validity

Constraint: Only execution time was measured. No comparison of memory usage was conducted. Additionally, the p99 estimate is approximate because there were only 100 measurements per group.
What this means: We proved that Proposed is faster, but we do not know whether it requires 10 times more memory (which could crash a computer when processing large files).
3. External Validity

Constraint: The equivalence of results (i.e., Baseline and Proposed producing identical numbers) was proven only for the tested sample sizes (up to 10,000 rows).
What this means: This does not guarantee that the methods will not diverge on real data with millions of rows, missing values, or "dirty" entries. Furthermore, as the data size increased, the number of participants also increased, and we did not separate these two effects.
5. Discussion

The results suggest that the proposed single-pass aggregation method provides a substantial performance advantage over the baseline multi-step approach. Within the tested envelope (10 to 10,000 rows), the proposed method achieved a median speedup of up to 4.26×. This improvement is likely attributable to the elimination of multiple expensive merge operations, which scale poorly with increasing data volume and group count. Notably, the output equivalence check confirmed that this optimization does not compromise calculation accuracy. The findings align with the expectation that in-memory, single-pass groupby operations are more efficient for participant-level diary aggregation.

6. Limitations & Threats to Validity

While the results are promising, several limitations must be acknowledged to contextualize the findings:

Internal Validity: The benchmark was conducted in a single session on a single machine using repeated synthetic sample data. Background OS activity and dependence between successive timings may have influenced the estimates. The bootstrap confidence intervals describe within-session uncertainty but do not capture cross-machine variation.
External Validity: Output equivalence was established only for the tested workloads (up to 10,000 rows). This does not prove correctness for every possible input. Furthermore, increasing the input size simultaneously increased the number of participant groups; these effects were not evaluated separately.
Construct Validity: The evaluation focused exclusively on execution time. No memory-usage comparison was conducted. Additionally, with 100 measurements per group, the p99 estimates are approximate.
7. Conclusion

This study evaluated two distinct implementations for participant-level diary data aggregation within the context of a short-form video and procrastination research protocol. The primary objective was to optimize the computational pipeline to handle large-scale synthetic datasets efficiently without compromising data integrity.

The proposed single-pass aggregation method demonstrated a significant performance improvement over the baseline multi-step approach. Within the tested workloads (up to 10,000 rows), the proposed method achieved a maximum median speedup of approximately 4.26×. Crucially, output equivalence checks confirmed that the optimized method produced identical results to the baseline across all tested input sizes.

These findings directly support the technical readiness of the proposed pipeline for future empirical data collection. While the study successfully addresses the computational efficiency required for the research project, it is important to note that these results concern software performance only. They provide no empirical evidence regarding the behavioral hypotheses (RQ1–RQ3) concerning short-form video consumption, student procrastination, or academic deadline adherence.

8. Future Work

To build upon these findings, future work will focus on three main directions:

Memory Profiling: Conduct a comprehensive comparison of memory usage (RAM) alongside execution time to ensure the pipeline remains scalable on lower-end hardware.
Cross-Platform Benchmarking: Evaluate the performance of the proposed method across different operating systems (Windows, macOS, Linux) and hardware configurations to validate generalizability.
Real-World Data Integration: Deploy the optimized pipeline on actual participant diary data (once collected) to test its robustness against real-world data irregularities, such as missing entries or outliers.
