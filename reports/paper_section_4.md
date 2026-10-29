## 4. Experimental Results & Discussion

### 4.1 Formal Definitions of Metrics

All timing measurements are reported in milliseconds (ms). For each
experimental condition, we collect $n = 100$ measured runs after
discarding $n_{\text{warmup}} = 10$ warm-up runs. Let $x_1, \dots, x_n$
denote the execution times of the measured runs.

**Median execution time.** The median is the 50th percentile of the
measured execution times:

$$
\operatorname{median}(x) =
\begin{cases}
x_{(\frac{n+1}{2})}, & n \text{ odd}, \\[4pt]
\dfrac{x_{(n/2)} + x_{(n/2+1)}}{2}, & n \text{ even},
\end{cases}
$$

where $x_{(1)} \le x_{(2)} \le \dots \le x_{(n)}$ is the ordered sample.

**Percentile $p_k$.** The $k$-th percentile ($k \in \{25, 75, 95, 99\}$)
is defined as

$$
p_k = x_{(\lceil k \cdot n / 100 \rceil)}.
$$

**Bootstrap 95% confidence interval for the median.** We draw
$B = 5000$ bootstrap resamples with replacement from $\{x_1, \dots, x_n\}$
using a fixed random seed ($\text{seed} = 42$) to ensure reproducibility.
For each resample $b \in \{1, \dots, B\}$ we compute the bootstrap median
$\hat{\theta}^{*}_{b}$. The 95% confidence interval is

$$
\mathrm{CI}_{95\%} = \left[ \hat{\theta}^{*}_{(0.025)},\ \hat{\theta}^{*}_{(0.975)} \right],
$$

where $\hat{\theta}^{*}_{(q)}$ denotes the $q$-th quantile of the
bootstrap distribution $\{\hat{\theta}^{*}_{1}, \dots, \hat{\theta}^{*}_{B}\}$.

**Speedup ratio.** The speedup of the proposed method over the baseline
is defined as the ratio of their median execution times:

$$
\mathcal{S} = \frac{\operatorname{median}(x^{\text{baseline}})}{\operatorname{median}(x^{\text{proposed}})}.
$$

A value $\mathcal{S} > 1$ indicates that the proposed method is faster
than the baseline; e.g., $\mathcal{S} = 4.26$ means the proposed method
is 4.26 times faster.

### 4.2 Notation Table

| Symbol | Description | Type |
|---|---|---|
| $n$ | Number of measured runs per condition | scalar (integer) |
| $n_{\text{warmup}}$ | Number of discarded warm-up runs | scalar (integer) |
| $x_i$ | Execution time of the $i$-th measured run (ms) | scalar |
| $x_{(i)}$ | $i$-th order statistic of the sample | scalar |
| $k$ | Percentile level ($k \in \{25, 75, 95, 99\}$) | scalar |
| $p_k$ | $k$-th percentile of execution time (ms) | scalar |
| $B$ | Number of bootstrap resamples | scalar (integer) |
| $\hat{\theta}^{*}_{b}$ | Bootstrap median from resample $b$ (ms) | scalar |
| $\hat{\theta}^{*}_{(q)}$ | $q$-th quantile of the bootstrap distribution | scalar |
| $\mathrm{CI}_{95\%}$ | Bootstrap 95% confidence interval for the median | interval |
| $\mathcal{S}$ | Speedup ratio (baseline / proposed) | scalar (dimensionless) |
