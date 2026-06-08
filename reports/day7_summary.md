# Day 7 Summary — CX Analytics Project

**Date:** June 5, 2026
**Status:** Complete
**Phase:** plan's Day 9–10 (segmentation + CLV), reframed for the 3.1% repeat reality, plus the Day 6 emotion deferral.

## What Got Done

### Customer-level feature table
- Aggregated master to one row per real person via `customer_unique_id`: 96,096 customers.
- Features: frequency, monetary (sum of total_payment), recency_days, avg_delivery_days, late_rate, avg_review.
- Reference date for recency: 2018-10-18 (max purchase + 1 day).

### RFM, with the Frequency collapse documented
- R and M scored cleanly into quintiles.
- **F is degenerate:** 93,099 of 96,096 customers have exactly one order. qcut on F fails (all bin edges = 1.0). Dropped F from segmentation, on the record, not silently.
- Kept an R x M grid as the defensible RFM. Repeat cohort (2,997 customers, 3.12%) tracked separately, too small to segment on.

### K-means segmentation (k=4)
- Features: log_monetary, recency_days, avg_delivery_days, late_rate. Standardized. F excluded (no variance).
- **k chosen as a business call, not a silhouette call.** Silhouette favored k=2 (0.607 vs 0.299 at k=4), but k=2 only recovers late-vs-on-time, which is the delivery story we already have. Chose k=4 to surface value and recency sub-segments inside the on-time majority. Tradeoff stated explicitly so it survives interview scrutiny. The late-delivery cluster is the stable one across both k values.

**Segment profile (names corrected after catching a template-label inversion in the first pass):**
| Segment | Customers | % base | Avg spend | Avg recency (d) | Avg delivery (d) | Late rate | Avg review |
|---|---|---|---|---|---|---|---|
| Low-value, recent | 34,611 | 36.0% | 72.56 | 188 | 8.9 | 0.00 | 4.30 |
| High-value | 27,065 | 28.2% | 335.15 | 231 | 12.3 | 0.00 | 4.12 |
| Dormant | 28,097 | 29.2% | 117.22 | 473 | 10.8 | 0.00 | 4.19 |
| Late & unhappy | 6,323 | 6.6% | 179.24 | 270 | 33.5 | 0.99 | 2.27 |

### Descriptive CLV per segment
- Observed historical value only. Predictive CLV (BG/NBD, Gamma-Gamma) deliberately not attempted: no repeat base to fit it.
- **High-value: 28% of customers, ~57% of observed revenue (9.07M of 16.0M total), 7.0% repeat rate (the only segment above 3%).** Protect these.
- **Late & unhappy: 6.6% of customers, mid-value (avg 179, above the low-value segment), wrecked by delivery (2.27 review, 99% late).** This is the fixable loss, not low-value churn.
- Low-value, recent: largest by count (36%), happiest (4.30), lowest repeat (1.1%). Volume, thin value.
- Dormant: oldest purchases (473 days), fine experience, gone quiet.

### Emotion on negative reviews (10,692 docs)
- **HF transformer model did NOT run** (huggingface.co offline, same wall as Day 6 BERTopic). Keyword lexicon fallback fired.
- Counts: frustration 9,349 (87%), disappointment 673 (6%), anger 670 (6%).
- **Caveat: the 87% frustration is inflated by the default rule** (unmatched negatives default to frustration). Real measured signal is ~6% explicit anger and ~6% explicit disappointment; the rest is unspecified, delivery-driven negativity. Treat emotion as directional, do not quote a precise frustration %.

### Files Saved
In `data/processed/`:
- `customer_segments.parquet` — 96,096 customers with features + cluster + segment (feeds Day 8 model + dashboard)
- `segment_clv.csv` — segment value table (report input)
- `reviews_with_emotion.parquet` — 10,692 negative reviews + emotion tag (dashboard VoC input)

## Tech Decisions Made
- Dropped Frequency from segmentation after proving it has no spread. Documented the qcut failure rather than hiding it.
- k=4 over the silhouette-optimal k=2, justified as business granularity vs statistical purity. Stated openly.
- Descriptive CLV only. Predictive CLV off the table, said in one line, not apologized for.
- Emotion kept as rule-based keyword tagging. Labelled as such everywhere downstream.

## Honest Metrics (do not inflate in resume/report)
- **Emotion is rule-based keyword tagging, not DistilBERT.** Label it that way in the dashboard. The frustration share is partly a default artifact.
- **Segmentation silhouette at the chosen k=4 is 0.299 (moderate).** Don't claim "well-separated clusters." Claim "actionable behavioral segments," and note the late-delivery segment is the cleanest.
- Segment names were inverted in the first pass (template left unedited); caught against the profile and corrected. cluster 0 = low value, cluster 1 = high value. QA caught it before save.

## Top Segment Insights (numbers attached)
1. **High-value drives revenue, barely repeats** — 28% of customers, 57% of observed value, 7% repeat. Retention upside is concentrated here.
2. **Late & unhappy is fixable mid-value loss** — 6.6% of customers, avg spend above the low-value segment, killed by 33-day deliveries and 99% lateness. Fixing delivery directly addresses this segment.
3. **Low-value, recent is the volume floor** — 36% of customers, happiest, but thinnest value and 1.1% repeat.
4. **Dormant is a re-activation target** — 29% of customers, fine past experience, silent for ~473 days.

## What's Next: Day 8
- **Repeat-purchase prediction, not churn** (the churn label doesn't exist in Olist). Binary target: did this customer ever place a 2nd order.
- LR baseline then XGBoost. Features: delivery time, late flag, monetary, review score, segment.
- Heavy class imbalance (3% positive). Report ROC-AUC and precision/recall on the minority class, not raw accuracy. Use class_weight / scale_pos_weight.
- Feature importance to confirm whether delivery and satisfaction predict repeat. This is the resume's "churn model" reframed onto an honest target.

Reference: `CX_Analytics_Project_Plan.md` Day 9–10 sections, adjusted for the retention reality.
