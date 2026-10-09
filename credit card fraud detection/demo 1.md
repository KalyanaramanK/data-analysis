# Task 1 — Business Problem Statement

Credit card fraud costs issuing banks both direct financial losses and customer trust,
yet fraud is extremely rare (0.17% of transactions in our dataset), which makes it easy
for real fraud cases to slip through standard rule-based monitoring while legitimate
customers get incorrectly flagged and frustrated. This analysis will identify which
transaction characteristics — amount ranges, time-of-day patterns, and the underlying
PCA-derived behavioral features (V1–V28) — are most strongly associated with fraudulent
transactions, so the **fraud operations / risk management team** can prioritize which
transactions get routed to real-time manual review versus automatic approval. The
decision this analysis should inform is: **where to set the fraud-risk score threshold
that triggers a manual review or transaction hold**, balancing the cost of missed fraud
against the cost of blocking or delaying legitimate customer transactions. Success means
a measurable increase in the share of fraud dollars caught per review-team hour spent,
without a corresponding spike in legitimate transactions wrongly declined.

---

# Task 2 — KPIs

| KPI Name | Formula / Calculation | Data Column(s) Needed | Target / Benchmark | Why It Matters |
|---|---|---|---|---|
| **Fraud Detection Rate (Recall)** | (Fraud transactions correctly flagged ÷ Total actual fraud transactions) × 100 | `Class`, model's predicted flag | ≥ 90% of fraud dollars caught | *Lagging.* Directly measures how much real fraud the system is actually catching; the core outcome the risk team is judged on. |
| **False Positive Rate** | (Legitimate transactions incorrectly flagged ÷ Total legitimate transactions) × 100 | `Class`, model's predicted flag | Keep below 0.5% | *Lagging.* Every false flag is a real customer's card declined or delayed — this protects customer experience and review-team workload. |
| **Fraud Loss Rate (\$)** | (Total \$ amount of confirmed fraud ÷ Total \$ transaction volume) × 100 | `Amount`, `Class` | Reduce quarter-over-quarter | *Lagging.* Ties fraud performance to actual dollars at risk, not just transaction counts — a few large fraudulent transactions matter more than many small ones. |
| **High-Risk Transaction Share by Hour** | (Transactions flagged high-risk in a given `Hour_of_Day` bucket ÷ Total transactions in that bucket) × 100 | `Time` (converted to `Hour_of_Day`), predicted risk score | Identify peak-risk windows for staffing | *Leading.* Signals when fraud attempts cluster during the day so staffing and monitoring intensity can be adjusted proactively, before losses occur. |
| **Average Transaction Amount — Flagged vs. Not Flagged** | Mean(`Amount`) where flagged = fraud vs. Mean(`Amount`) where not flagged | `Amount`, `Class` | Track the gap over time | *Leading.* A widening or shifting gap can indicate fraud tactics are changing (e.g., moving to smaller "under-the-radar" amounts), prompting a model/threshold review before losses climb. |
| **Review Queue Precision** | (Transactions sent to manual review that were confirmed fraud ÷ Total transactions sent to manual review) × 100 | `Class`, predicted flag | ≥ 20–30% (given how rare fraud is) | *Lagging.* Measures how efficiently the review team's time is spent — low precision means reviewers are wasting effort on legitimate transactions. |

**Notes on the guidance requirements:**
- Every KPI references columns that exist in `creditcard.csv` (`Amount`, `Class`, `Time`/`Hour_of_Day`) or a model output derived from them (a predicted fraud flag/score, which any fraud model built on this data would produce).
- **Leading indicators:** *High-Risk Transaction Share by Hour* and *Average Transaction Amount — Flagged vs. Not Flagged* — both help anticipate emerging fraud patterns before losses are fully realized.
- **Lagging indicators:** *Fraud Detection Rate*, *False Positive Rate*, *Fraud Loss Rate*, and *Review Queue Precision* — all report on outcomes after transactions have already occurred.
- No vanity metrics (e.g., total transaction count) are included — each KPI ties to a decision the risk team can act on.
