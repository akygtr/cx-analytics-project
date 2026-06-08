# Day 8 Summary — CX Analytics Project

**Date:** June 5, 2026
**Status:** Complete
**Phase:** plan's Day 9–10 churn model, reframed to repeat-purchase prediction (no churn label exists in Olist).

## What Got Done

### Target and the leakage rule
- Binary target: did a customer ever place a 2nd order. 96,096 customers, **3.12% positive (2,997)**.
- **Features built from the first order only.** Earliest order pulled as one intact row via `idxmin` on purchase timestamp, not `.groupby().first()` (which would mix columns across orders and leak the 2nd purchase). `segment` and all-order aggregates excluded for the same reason. First-order `review_score` kept (it precedes the repeat decision).
- Features: delivery_time_days, days_vs_estimate, is_late, total_payment, item_count, total_freight, distinct_products, review_score, payment_count, main_payment_type, customer_state.
- Nulls (delivery ~3% undelivered, review ~1%) handled by median/constant imputation inside a ColumnTransformer, fit on train only.

### Models (80/20 stratified split, 599 test positives)
| Model | ROC-AUC | PR-AUC | base rate | pos recall | pos precision |
|---|---|---|---|---|---|
| Logistic Regression (balanced) | 0.582 | 0.042 | 0.031 | 0.571 | 0.039 |
| XGBoost (scale_pos_weight 31) | 0.589 | 0.043 | 0.031 | 0.481 | 0.041 |

### The result: repeat is not predictable from first-order experience
- **AUC ~0.59 is noise-adjacent** (0.50 = random). PR-AUC 0.043 vs 0.031 base rate is ~1.4x lift, marginal.
- Confusion matrix confirms it can't target: XGBoost flags 288 true repeaters but with 6,801 false positives (4% precision). A ranked at-risk list off this would be ~96% wrong.
- **Feature importance is flat and scattered** (top 0.045, most 0.026–0.045, half the list individual state dummies). No first-order signal meaningfully moves repeat.

### Why this is a finding, not a failure
- The 3% repeat rate is **structural**, not an experience problem a model can target away. Delivery, review, basket size: none predict return.
- The leakage-free design is exactly why the low AUC is trustworthy. Aggregating across orders would have produced a fake-high AUC. Low here is the correct outcome.
- `review_score` ranked #2 but with tiny importance (0.039), so it didn't dominate, confirming no leakage. Kept it; dropping it changes nothing.

### Files Saved
- `models/repeat_model.pkl` (XGBoost, best by ROC-AUC, saved for the dashboard propensity view)
- `data/processed/customers_repeat_scored.parquet` — 96,096 customers + repeat + repeat_proba

## Tech Decisions Made
- First-order-only features as the anti-leakage backbone. The single most important design call in the modeling phase.
- class_weight='balanced' (LR) and scale_pos_weight≈31 (XGBoost) for the 3% class.
- Judged on ROC-AUC, PR-AUC, and positive-class precision/recall. Accuracy ignored (97% by predicting "never").
- Saved the model for completeness, but flagged it as non-actionable for per-customer scoring.

## Honest Metrics (do not inflate in resume/report)
- **Kill the "XGBoost churn AUC 0.87" resume bullet.** Real result: repeat-purchase model, ROC-AUC 0.59.
- Honest bullet: "Built a leakage-free repeat-purchase model (XGBoost, ROC-AUC 0.59); found first-order experience weakly predicts repeat, evidence that low retention is structural, redirecting recommendations from individual targeting to systemic delivery fixes."
- Do not present a churn risk list in the dashboard. The base rate and AUC don't support per-customer targeting.

## How this fits the project narrative
- Delivery is the lever that **works**: Day 6 showed late delivery costs 1.94 stars and 62% of late orders score 1–2★.
- Retention is **structural**: it does not respond to first-order experience in any modelable way.
- Combined recommendation: fix delivery broadly (systemic), do not spend on individual retention scoring (unsupported by the data).

## What's Next: Day 9 (Dashboard)
- Streamlit dashboard, all inputs now exist in `data/processed/`:
  - Executive summary (delivery satisfaction, retention reality, top friction points)
  - Fulfillment funnel + delivery satisfaction (`order_funnel.parquet`, master)
  - VoC: themes, KMeans complaint topics, rule-based emotion (`negative_topics.csv`, `reviews_with_emotion.parquet`)
  - Segments + descriptive CLV (`customer_segments.parquet`, `segment_clv.csv`)
  - Repeat propensity: show the distribution and the "experience doesn't predict repeat" finding, not a risk list
- Honest-labeling carries into every tile: KMeans not BERTopic, keyword not DistilBERT emotion, AUC 0.59 not 0.87.

Reference: `CX_Analytics_Project_Plan.md` Day 11 (dashboard).
