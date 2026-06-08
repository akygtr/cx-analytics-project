# Day 5 Summary — CX Analytics Project

**Date:** June 2, 2026
**Status:** Complete
**Note:** Running behind the original May calendar, but the phase sequence is intact. This is the "Day 5–6: Classifier Training" phase from the plan.

## What Got Done

### Label QA (before any training)
- Loaded `labeled_500.parquet`. Labels were already flattened into clean columns: order_id, review_score, review_clean, sentiment, theme, journey_stage.
- Caught 1 duplicate order_id (`ec082d3...`) with contradictory labels. Kept the correct row (negative/post-purchase), dropped the wrong one (positive/pre-purchase).
- Caught 5 reviews mislabeled `positive` that were clearly negative complaints (defective items, 15-day delays, missing items). Relabeled all 5 to `negative`.
- Audited the full set with a sentiment x review_score crosstab. Pattern was healthy (1-2 star = negative, 4-5 star = positive). No systematic labeling bug. The 5 errors were honest slips, not a tool problem.
- Collapsed theme `price` (only 5 samples) into `other`. Too few to learn or measure.
- Shelved the journey_stage classifier. The labels were degenerate: zero `purchase` samples and only 9 `pre-purchase`. Can't train 4 classes when one is empty. Will derive journey stage from theme/transactional signals later if the dashboard needs it.
- Saved cleaned labels to `data/labeled/labeled_clean.parquet` (499 rows) so the QA work survives a kernel restart.

### Classifiers
- 80/20 stratified train/test split, separate split per schema, random_state=42.
- Both models: TF-IDF (max_features=5000, ngram 1-2) + LogisticRegression(class_weight='balanced'), wrapped in an sklearn Pipeline.

**Sentiment (3-class), held-out test:**
- Accuracy 0.84
- positive F1 0.91, negative F1 0.87 (both strong, these are the ones that matter)
- neutral F1 0.42 (weak, expected: small and inherently fuzzy class)

**Theme (5-class), held-out test:**
- Accuracy 0.65
- delivery F1 0.76, quality F1 0.61 (the two dominant classes, ~80% of data, work)
- service / returns / other weak. Data-limited, not model-limited. `returns` had only 2 test samples, its metric is noise.

### Applied to full dataset
- Refit both pipelines on all 499 labeled rows (measured on holdout first, then trained on everything for production).
- Scored all 11,997 translated reviews. Added `sentiment_pred`, `theme_pred`.
- Sanity crosstab on full data confirmed predictions track review_score correctly.

### Files Saved
- `data/labeled/labeled_clean.parquet` (499 cleaned labels)
- `models/sentiment_classifier.pkl`, `models/theme_classifier.pkl` (full pipelines, vectorizer included)
- `data/processed/olist_reviews_scored.parquet` (11,997 reviews + predictions, keyed on order_id)
- `notebooks/05_classifier_training.ipynb`

## Tech Decisions Made
- Baseline-first: logistic regression before any transformer. DistilBERT deferred as an optional upgrade, not a blocker to the pipeline.
- sklearn Pipeline bundles vectorizer + model: prevents TF-IDF fitting on test data, and keeps the vectorizer attached when the model is pickled.
- `class_weight='balanced'` on both, to stop the big classes (delivery, negative) from swamping the small ones.
- Refit on the full labeled set after holdout evaluation, standard measure-then-deploy practice.
- joblib for model persistence.

## Honest Metrics (do not inflate in resume/report)
- Sentiment: 84% accuracy (LR baseline). The resume draft claims "DistilBERT 89%." Either build DistilBERT and report its real number, or change the bullet to match the 84% LR result. Measure first, write the number second.
- Theme: report delivery F1 0.76 and quality F1 0.61, and state plainly that minority themes are directional given limited labels.

## Critical Framing Rule (carry into report and dashboard)
- The 11,997 scored reviews are deliberately negative-heavy because of Day 3 oversampling (took all 1-2 star first). 86% of the set is 1-2 star.
- Valid use: "what are customers complaining about" (themes, friction points, language).
- Invalid use: "what fraction of customers are unhappy." That stat must come from the full review_score distribution (~99K in olist_master), not from model sentiment on this oversampled set. Reweight if you need population sentiment rates.

## Parked / Future Work
- DistilBERT fine-tune on sentiment (optional, chase the 89% honestly).
- journey_stage: derive from theme/transactional if the dashboard needs the journey view.
- If theme accuracy needs lifting: targeted labeling of rare themes (service, returns) via keyword-surfaced candidates, not random sampling. Random adds more delivery, not more service.

## Housekeeping
- Rename `02_data_cleaning.ipynb.ipynb` to `02_data_cleaning.ipynb` (double extension).

## What's Next
Per plan, Day 7–8 (journey mapping + topic modeling) and Day 9–10 (segmentation, CLV, churn). Concretely next:
- Join `olist_reviews_scored.parquet` to `olist_master.parquet` on order_id for combined text + transactional analysis.
- Customer journey funnel and drop-off rates from transactional data.
- BERTopic on negative reviews for granular complaint themes.
- RFM segmentation, CLV, cohort analysis.
- Churn model (LR then XGBoost), with delivery delays, sentiment scores, return behavior as features.

Reference: `CX_Analytics_Project_Plan.md` Day 7–10 sections.