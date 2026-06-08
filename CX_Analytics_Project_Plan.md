# Customer Experience Analytics for an E-commerce Fashion Brand

**Project Duration:** May 19 – May 31, 2026 (12 days + buffer)
**Goal:** Build an end-to-end CX analytics solution covering data sourcing, cleaning, labeling, journey mapping, VoC analysis, segmentation, predictive modeling, and dashboarding.

---

## Project Narrative

A mid-sized online fashion retailer is seeing rising return rates and declining repeat purchases. You're brought in as a CX analyst to figure out where customers are dropping off, what they're frustrated about, and how to fix it.

---

## Tech Stack

- **Languages:** Python, SQL
- **Data Manipulation:** pandas, NumPy
- **NLP:** spaCy, NLTK, Hugging Face Transformers, BERTopic
- **ML:** scikit-learn, XGBoost
- **Labeling:** Label Studio or Doccano
- **Visualization:** Streamlit, matplotlib, seaborn, plotly
- **Deployment:** Streamlit Community Cloud / Hugging Face Spaces
- **Version Control:** Git, GitHub

---

## Day-by-Day Plan

### Day 1–2 (May 19–20): Data Sourcing & Setup

- [ ] Set up GitHub repo, folder structure, virtual environment
- [ ] Download datasets:
  - Olist Brazilian E-commerce (transactions, reviews, delivery) — Kaggle
  - Amazon Fashion Reviews or Women's E-commerce Clothing Reviews — Kaggle
  - Twitter Customer Support dataset — Kaggle
- [ ] Optional: scrape 1,000–2,000 Trustpilot reviews using BeautifulSoup
- [ ] Write project narrative document (brand backstory, business problem, key questions)
- [ ] Initial data exploration, document data dictionaries

---

### Day 3–4 (May 21–22): Deep Cleaning & Preparation

- [ ] Clean transactional data: missing values, duplicates, joins, date standardization
- [ ] Clean text data: HTML, emojis, URLs, contractions, lowercase, tokenize, lemmatize
- [ ] Language detection and filtering with langdetect
- [ ] Remove spam, very short reviews, duplicates
- [ ] Translate non-English reviews if needed (deep-translator)
- [ ] Document every cleaning decision in a notebook with before/after samples
- [ ] Save clean master datasets as parquet files

---

### Day 5–6 (May 23–24): Manual Labeling & Classifier Training

- [ ] Set up Label Studio or Doccano locally
- [ ] Manually label 500 reviews across:
  - Sentiment (positive, negative, neutral)
  - Theme (sizing, delivery, quality, service, price, returns)
  - Journey stage (pre-purchase, purchase, delivery, post-purchase)
- [ ] Train sentiment classifier: logistic regression on TF-IDF, then fine-tune DistilBERT
- [ ] Train multi-class theme classifier
- [ ] Validate on held-out test set, report precision, recall, F1
- [ ] Apply both classifiers to the full review dataset

---

### Day 7–8 (May 25–26): Journey Mapping + Topic Modeling

- [ ] Build customer journey funnel using transactional + behavioral data
- [ ] Calculate drop-off rates at each stage
- [ ] Overlay sentiment and theme distribution at each journey stage
- [ ] Run BERTopic on negative reviews for granular themes
- [ ] Compare themes across customer segments
- [ ] Add emotion detection (Hugging Face emotion model) for frustration, anger, disappointment
- [ ] Identify and document top 3–5 friction points with supporting numbers

---

### Day 9–10 (May 27–28): Predictive Modeling & Segmentation

- [ ] RFM segmentation (Recency, Frequency, Monetary)
- [ ] K-means clustering as a second segmentation approach, compare both
- [ ] Calculate Customer Lifetime Value per segment
- [ ] Build churn prediction model:
  - Features: purchase history, sentiment scores, delivery delays, support interactions, return behavior
  - Start with logistic regression, then XGBoost, compare results
  - Hyperparameter tuning with GridSearchCV
  - Report accuracy, precision, recall, ROC-AUC, feature importance
- [ ] Build at-risk customer list with risk scores and recommended actions

---

### Day 11 (May 29): Dashboard Build

Build Streamlit dashboard with these views:

- [ ] Executive summary (NPS proxy, churn rate, top themes, key trends)
- [ ] Journey funnel with sentiment heatmap
- [ ] VoC deep dive (themes, word clouds, sample reviews, emotion breakdown)
- [ ] Segment view (RFM segments, CLV, behavior comparison)
- [ ] Churn risk dashboard (predicted at-risk customers with recommended actions)
- [ ] Deploy on Streamlit Community Cloud or Hugging Face Spaces

---

### Day 12 (May 30): Documentation, Report & Polish

- [ ] Write 2–3 page business report:
  - Top 5 findings with supporting data
  - Specific actions for marketing, ops, and product teams
  - Projected business impact with assumptions
- [ ] Write thorough GitHub README (overview, methodology, findings, screenshots, dashboard link)
- [ ] Create one-page case study for portfolio
- [ ] Record 3-minute Loom walkthrough of the dashboard
- [ ] Final code cleanup, add comments, requirements.txt

---

### Buffer Day (May 31): Polish + LinkedIn Post

- [ ] Fix anything that broke
- [ ] Write LinkedIn post with key insights and dashboard screenshots
- [ ] Optional: short Medium article walking through methodology
- [ ] Final review of resume bullet points

---

## Suggested Folder Structure

```
cx-analytics-project/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── labeled/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_labeling_and_classifier.ipynb
│   ├── 04_journey_mapping.ipynb
│   ├── 05_topic_modeling.ipynb
│   ├── 06_segmentation_clv.ipynb
│   └── 07_churn_prediction.ipynb
│
├── src/
│   ├── data_cleaning.py
│   ├── text_preprocessing.py
│   ├── classifiers.py
│   ├── segmentation.py
│   └── churn_model.py
│
├── dashboard/
│   └── app.py
│
├── reports/
│   ├── business_report.pdf
│   └── case_study.pdf
│
├── models/
│   ├── sentiment_classifier.pkl
│   ├── theme_classifier.pkl
│   └── churn_model.pkl
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Daily Time Commitment

- **Weekdays:** 5–6 hours
- **Weekends:** 7–8 hours
- Heavier phases (labeling Day 5–6, modeling Day 9–10) on weekends if possible

---

## Resume Bullet Draft

> Designed and built an end-to-end Customer Experience analytics platform for an e-commerce fashion brand, processing 100K+ transactions and 40K+ customer reviews across multiple data sources. Engineered text cleaning and labeling pipelines, manually annotated 500 reviews to train sentiment (DistilBERT, 89% accuracy) and theme classifiers covering 6 journey stages. Applied BERTopic for granular complaint analysis and built RFM segmentation alongside an XGBoost churn prediction model (AUC 0.87). Deployed interactive Streamlit dashboard surfacing journey drop-offs, VoC insights, and at-risk customer segments. Identified that delivery delays and product quality issues drove 58% of negative sentiment, with recommended interventions projected to reduce churn by 18%.

---

## Key Principles to Stick To

1. **Momentum over perfection.** Don't get stuck on any single phase trying to make it flawless.
2. **Document everything as you go.** Future-you (and recruiters) will thank you.
3. **Quantify findings.** Every insight should have numbers attached.
4. **Cap your time per phase.** If labeling takes longer than expected, stop at the end of Day 6 and move on.
5. **Ship something deployable.** A live dashboard link beats a static screenshot every time.

---

## Final Deliverables Checklist

- [ ] GitHub repo with clean, documented code
- [ ] Jupyter notebooks for each phase
- [ ] Deployed interactive Streamlit dashboard
- [ ] 2–3 page business report
- [ ] One-page case study for portfolio
- [ ] 3-minute Loom walkthrough video
- [ ] LinkedIn post (optional but recommended)
- [ ] Updated resume bullet points
# Day 1 Summary — CX Analytics Project

**Date:** May 19, 2026
**Status:** Complete

## What Got Done

### Environment
- Project folder: `C:\Users\akskumari\Desktop\cx-analytics-project`
- Python virtual environment created (`venv`)
- All requirements installed from `requirements.txt`: pandas, numpy, scikit-learn, spaCy (with `en_core_web_sm` 3.7.1), Hugging Face Transformers, torch, BERTopic, XGBoost, Streamlit, NLTK, plus supporting libraries
- Label Studio intentionally excluded from main env due to dependency conflict with NLTK. Will install in separate venv on Day 5.
- `pip-system-certs` installed to resolve a Python SSL cert issue that was blocking Kaggle API access

### Repo
- GitHub repo live at: https://github.com/akygtr/cx-analytics-project (public)
- Initial commit + Day 1 commit both pushed
- `.gitignore` excludes venv, raw data, models, kaggle.json, and similar

### Folder Structure

cx-analytics-project/
├── dashboard/
├── data/
│   ├── raw/          (datasets downloaded here)
│   ├── processed/
│   └── labeled/
├── models/
├── notebooks/
│   └── 01_data_exploration.ipynb  (DONE)
├── reports/
│   └── project_narrative.md       (DONE)
├── src/
│   └── download_data.py           (reusable Kaggle download script)
├── .gitignore
├── CX_Analytics_Project_Plan.md
├── README.md
└── requirements.txt

### Data Downloaded
All three datasets are in `data/raw/` (not committed to git, too large):

1. **Olist Brazilian E-commerce** (~45MB)
   - `data/raw/olist/` with 9 CSVs
   - 99,441 orders, 99,224 reviews, 99,441 customers, 112,650 order items, 32,951 products, 103,886 payments
   - 41% of reviews have written text (40,977 with comments)
   - Avg review score 4.09, bimodal: 57k 5-stars vs 11k 1-stars
   - Most review text is in Portuguese, will need filtering or translation on Day 2

2. **Women's Clothing E-commerce Reviews** (~8MB)
   - `data/raw/womens_clothing/Womens Clothing E-Commerce Reviews.csv`
   - 23,486 reviews, English
   - 845 null review texts
   - Mean review length 309 chars
   - Rating distribution skewed positive (13k of 5-stars, 842 of 1-stars)
   - Top departments: Tops (10,468), Dresses (6,319), Bottoms (3,799), Intimate (1,735), Jackets (1,032)

3. **Customer Support on Twitter** (~169MB)
   - `data/raw/twitter_support/` (only peeked at first 10k rows so far)

### Notebook Work
`notebooks/01_data_exploration.ipynb` has 8 cells:
- Imports + folder check
- Load all 6 Olist tables
- Preview orders and reviews
- Review score distribution analysis
- Load Women's Clothing CSV
- Profile Women's reviews (nulls, length, rating dist, departments)
- Peek at Twitter support data (first 10k rows)

## Project Context (for picking up later)

**Brand:** Atlas and Vine, fictional mid-sized DTC fashion retailer, ~$40M revenue
**Business problem:** Returns up 22%→31%, repeat purchase down 38%→27%, support tickets up 45% QoQ
**Goal:** Identify drop-off points, root-cause customer frustration, recommend interventions
**Deliverables:** Streamlit dashboard, business report, case study, Loom walkthrough, LinkedIn post

## Tech Decisions Made
- Using browser-based GitHub auth (Git Credential Manager) instead of personal access tokens
- Kaggle CLI 1.6.14 (legacy API key required, not the newer token format)
- SSL fix via `pip-system-certs` (uses Windows cert store)
- spaCy model: `en_core_web_sm` 3.7.1 (installed via direct wheel URL, not `spacy download`)

## What's Next: Day 2 (May 20)

Deep cleaning + preparation:
- Join Olist tables (orders + reviews + customers + payments + items) into one master dataframe
- Standardize dates, handle missing values, compute derived columns (delivery time, days late)
- Clean Women's Clothing text: strip HTML/URLs/emojis, lowercase, tokenize, lemmatize
- Language detection on Olist reviews (langdetect)
- Filter or translate Portuguese reviews
- Remove spam and very short reviews
- Save clean master datasets as parquet files in `data/processed/`
- Document every cleaning decision with before/after samples

Reference: `CX_Analytics_Project_Plan.md` Day 3–4 section (project plan dates are slightly behind actual progress, ahead of schedule by one day)

# Day 2 Summary — CX Analytics Project

**Date:** May 20, 2026
**Status:** Complete

## What Got Done

### Transactional Cleaning (Olist)
- Loaded 6 Olist tables: orders (99,441), order_items (112,650), reviews (99,224), customers (99,441), payments (103,886), products (32,951)
- Standardized all date columns to datetime
- Built derived delivery features on orders:
  - `delivery_time_days` (purchase to customer delivery)
  - `days_vs_estimate` (negative = early, positive = late)
  - `is_late` (boolean flag)
- Key delivery findings: avg delivery 12.1 days, 6.8% late rate, when late they're 10.6 days late on average
- Aggregated payments per order (multi-row → single row): payment_count, total_payment, payment_types, main_payment_type
- Aggregated order items per order: item_count, total_price, total_freight, distinct_products
- Caught and fixed a duplicate-review bug: 243 orders had multiple review rows, inflating master from 99,441 to 99,684. Deduped by keeping most recent review per order_id.
- Final master shape: 99,441 rows × 31 columns. One-to-one with orders confirmed.

### Text Cleaning (Women's Clothing)
- Loaded 23,486 reviews, 22,641 after dropping nulls
- Did pattern-based noise analysis instead of generic cleaning. Key findings:
  - Dataset is pre-cleaned: zero HTML, URLs, emojis, all-caps
  - 38.8% have numbers (sizes, heights, weights — KEPT as signal)
  - 33.7% have special chars (apostrophes, quotes — KEPT)
  - 11.6% have repeated chars (mostly ellipses and !!! emphasis — KEPT)
  - 0.6% have doubled apostrophes (inch notation: 5'2'' — normalized to 5'2')
  - 0.1% have non-ASCII (mangled accents — normalized via unicodedata)
  - Reviews capped at 500 chars by publisher
  - Only 34 reviews under 5 words — flagged as `is_short` not dropped
- Built two cleaning functions:
  - `clean_text` (light): for DistilBERT, BERTopic, dashboard display
  - `preprocess_text` (aggressive): lowercase, no punct/numbers, stopwords removed, lemmatized — for TF-IDF and topic modeling
- Applied both to all 22,641 reviews
- Average tokens after aggressive preprocessing: 27.8 (down from ~60 raw words)

### Language Detection (Olist)
- Ran `langdetect` (with deterministic seed) on 40,577 Olist reviews with text
- Distribution: 84% Portuguese, 8% unknown (too-short), 159 English, rest misdetected short Portuguese
- **Strategic decision:** Only 159 English Olist reviews — not enough for NLP. All sentiment/theme/topic work goes on Women's Clothing. Olist used for transactional analysis only.

### Files Saved
In `data/processed/`:
- `olist_master.parquet` (20.7 MB) — joined Olist master with delivery/payment features
- `womens_clean.parquet` (10.5 MB) — Women's Clothing reviews with both cleaning columns
- `olist_reviews_with_lang.parquet` (4.8 MB) — language-tagged Olist reviews

## Tech Decisions Made
- Two-track cleaning strategy: preserve text for transformer models, aggressively clean for bag-of-words
- Kept numbers and punctuation in light cleaning (sizes are signal for fashion reviews)
- Deduped reviews on `order_id` by keeping most recent
- Skipped translation of Portuguese reviews (159 English is too few; pivot to Women's Clothing for all NLP)
- Used parquet over CSV for fast loading and preserved dtypes

## What's Next: Day 3 (May 21)

Manual labeling setup + start labeling:
- Install Doccano in separate venv (avoid Label Studio dep conflicts)
- Set up labeling project with three schemas:
  - Sentiment: positive / negative / neutral
  - Theme: sizing / delivery / quality / service / price / returns
  - Journey stage: pre-purchase / purchase / delivery / post-purchase
- Sample 500 reviews from Women's Clothing for labeling
- Begin labeling (target: 200 done by end of Day 3, 500 by end of Day 4)

Reference: `CX_Analytics_Project_Plan.md` Day 5–6 section

# Day 3 Summary — CX Analytics Project

**Date:** May 21, 2026
**Status:** Complete

## What Got Done

### Strategic Pivot (context for the record)
- Evaluated adding Women's Clothing (Kaggle) as NLP layer alongside Olist transactions
- Identified the core problem: two unrelated datasets with no shared keys. Olist (Brazil, Portuguese) and Women's Clothing (US, English) had zero customer overlap — every cross-analysis would have been fiction
- Decision: drop Women's Clothing from the active pipeline. Olist becomes the single spine for both transactions and text. `womens_clean.parquet` retained on disk but not used going forward
- This means every finding in the project — sentiment, themes, churn, segments — refers to the same real customer population. The "11,997 / 11,997" join count at the end of today confirmed that

### Translation (PT → EN)
- Loaded `olist_reviews_with_lang.parquet` (40,577 reviews, 84% Portuguese)
- Built stratified sample of 12,000: took ALL 1–2 star reviews first (negative signal), filled rest from 3–5 star
- Translated using `deep-translator` (GoogleTranslator backend), batched at 0.4s sleep per call
- Checkpointed every 200 rows to `olist_translation_checkpoint.parquet` — survived any crash/disconnect without losing progress
- Total fails: ~15 out of 12,000 (0.12%) — two types:
  - SSL/connection drops: random network noise, retried once, moved on
  - "No translation found": short/fragmented reviews (`"Encomenda errada"`) or ones with heavy typos. These are the weakest signal reviews anyway
- Translation quality spot-checked on 5 samples: meaning and sentiment preserved accurately across all five. Machine translation occasionally stiff but classifier-ready

### Text Cleaning
- Relocated both cleaning functions from `02_data_cleaning.ipynb` into `src/text_preprocessing.py` as importable module
- Fixed a scoping bug: `stop_words` and `lemmatizer` were notebook-level variables in Day 2, not inside the function. Moved to module level in the `.py` file so they initialize once on import
- Applied both functions to all translated reviews:
  - `clean_text` (light): unicode normalization, apostrophe fix, whitespace collapse — for DistilBERT, BERTopic, dashboard display
  - `preprocess_text` (aggressive): lowercase, strip punct/numbers, remove stopwords, lemmatize — for TF-IDF and topic modeling

### Linkage Verification
- Saved `olist_reviews_translated.parquet` keyed on `order_id`
- Inner join to `olist_master.parquet`: **11,997 / 11,997** — every translated review joins to a real order, customer, payment, and delivery record
- This is the fix that makes the project coherent: the same 11,997 customers power both the text analysis and the transactional modeling

### Files Saved
In `data/processed/`:
- `olist_reviews_translated.parquet` (2.8 MB) — 11,997 translated + cleaned reviews, keyed on `order_id`
- `olist_translation_checkpoint.parquet` — deleted after promoting to final (served its purpose)

In `src/`:
- `text_preprocessing.py` — `clean_text` and `preprocess_text` as importable functions, used by notebook 03 and all subsequent notebooks

## Tech Decisions Made
- Stratified sampling: oversample negatives (1–2 star) not random sample — complaint signal is what the project is built on
- Checkpoint every 200 rows not at the end — makes a 2-hour translation run resumable after any failure
- `BATCH_SLEEP = 0.4s` — enough to avoid rate-limiting without making the run painfully slow
- Translate 12K not all 40K — free API rate-limits; 12K is more than enough for classifier training + topic modeling
- Module-level `stop_words` / `lemmatizer` in `text_preprocessing.py` — initialize once, not on every function call

## Notebook
`notebooks/03_translation_and_cleaning.ipynb` — 20 cells covering path setup, column verification, stratified sampling, translation loop, spot-check, cleaning, before/after samples, save + join verification

## What's Next: Day 4 (May 22)

Manual labeling setup + annotation:
- Sample 500 reviews from `olist_reviews_translated.parquet` for labeling, stratified by score
- Set up Doccano in a separate venv (avoid dep conflicts with main env)
- Define three label schemas:
  - Sentiment: positive / negative / neutral
  - Theme: delivery / quality / service / price / returns / other
  - Journey stage: pre-purchase / purchase / delivery / post-purchase
- Export sample to JSONL, import into Doccano
- Target: 250 labeled by end of Day 4, 500 by end of Day 5
- Note: theme labels will skew delivery/logistics-heavy given the Olist review content — that's real signal, don't force balance

Reference: `CX_Analytics_Project_Plan.md` Day 5–6 section (project is running one day ahead of original plan)

---

# Day 4 Plan — CX Analytics Project

**Date:** May 22, 2026
**Phase:** Manual Labeling Setup + Annotation

---

## Goal for the Day

Get 250–500 reviews labeled across three schemas (sentiment, theme, journey stage) so Day 5 has training data to build classifiers on. Quality of labels determines classifier quality — this is not the day to rush.

---

## Task List

### Setup (do this first, before labeling anything)

- [ ] Create a separate venv for Doccano to avoid dep conflicts with main env:
  ```
  python -m venv venv-doccano
  venv-doccano\Scripts\activate
  pip install doccano
  ```
- [ ] Launch Doccano and create admin account:
  ```
  doccano init
  doccano createuser --username admin --password admin
  doccano webserver --port 8000
  ```
- [ ] Open `http://localhost:8000` in browser

### Sample 500 reviews for labeling

- [ ] Load `olist_reviews_translated.parquet`
- [ ] Stratified sample: take proportionally from each star rating so all sentiment classes are represented
- [ ] Export to JSONL (Doccano's import format):
  ```python
  import pandas as pd, json
  df = pd.read_parquet("data/processed/olist_reviews_translated.parquet")
  sample = df.groupby("review_score", group_keys=False).apply(
      lambda x: x.sample(min(len(x), 100), random_state=42)
  ).head(500)
  with open("data/labeled/labeling_sample.jsonl", "w") as f:
      for _, r in sample.iterrows():
          f.write(json.dumps({
              "text": r["review_clean"],
              "meta": {"order_id": r["order_id"], "score": int(r["review_score"])}
          }) + "\n")
  ```
- [ ] Import JSONL into Doccano project

### Define label schemas in Doccano

Three separate label sets (create one Doccano project per schema, or use a single project with prefixed labels):

**Sentiment**
- `positive`
- `negative`
- `neutral`

**Theme** (pick the single most dominant theme per review)
- `delivery` — late, missing, wrong item shipped
- `quality` — product condition, material, durability
- `service` — support responsiveness, communication, resolution
- `price` — value for money, overpriced, discounts
- `returns` — refund difficulty, return policy, exchange
- `other` — doesn't fit above cleanly

**Journey Stage** (where is the customer in their experience?)
- `pre-purchase` — browsing, search, product info
- `purchase` — checkout, payment, order confirmation
- `delivery` — shipping, tracking, arrival
- `post-purchase` — after receipt, satisfaction, re-order intent

### Labeling

- [ ] Label 500 reviews across all three schemas
- [ ] Hard rule: if a review genuinely fits two themes, pick the one the customer is most frustrated about
- [ ] Hard rule: neutral sentiment = factual, no clear positive or negative emotion (rare in Olist)
- [ ] Hard rule: be consistent. If "produto atrasou" (product was late) = delivery + negative in review 1, it must be the same in review 100
- [ ] Spot-check your own labels every 50 reviews — label drift is real and kills classifier quality
- [ ] Target: 250 minimum today, 500 by end of Day 5

### Export labeled data

- [ ] Export from Doccano as JSONL
- [ ] Save to `data/labeled/labeled_500.jsonl`
- [ ] Parse into a DataFrame, verify label distribution (no class should be under 30 samples)

---

## Label Distribution Target (rough guide)

| Sentiment | Target count |
|-----------|-------------|
| negative  | ~250        |
| positive  | ~175        |
| neutral   | ~75         |

| Theme    | Target count |
|----------|-------------|
| delivery | ~180        |
| quality  | ~100        |
| service  | ~80         |
| returns  | ~60         |
| price    | ~50         |
| other    | ~30         |

These are guides not hard targets. If your actual data skews different, that's fine — it's real signal. Don't manufacture balance by mislabeling.

---

## Honest Time Estimate

- Setup (venv + Doccano + sample export): 45–60 min
- 500 labels × 3 schemas: 3–4 hours minimum at a sustainable pace (~2 min per review for all three labels)
- If you hit 250 today and finish the rest on Day 5 morning, that is fine — classifier training can start on the afternoon of Day 5

---

## Files Expected at End of Day 4

- `data/labeled/labeling_sample.jsonl` — 500 raw reviews exported for labeling
- `data/labeled/labeled_500.jsonl` — same 500 with labels attached (from Doccano export)
- `notebooks/04_labeling_prep.ipynb` — sampling + export + label distribution check

---

## Watch Out For

- **Label drift:** your definition of "neutral" at review 10 vs review 400 will drift if you don't check. Every 50 reviews, re-read your first 10 labels and recalibrate.
- **Theme skew:** Olist reviews are delivery-heavy. "Delivery" will dominate your theme distribution. That's real, don't fight it by forcing other themes onto reviews that are clearly delivery complaints.
- **Short reviews are hard to label:** `"Ótimo"` translated to `"Great"` — that's positive, probably post-purchase, theme is other. Don't overthink one-word reviews; label them quickly and move on.
- **Doccano vs main env:** always activate `venv-doccano` before running `doccano webserver`. Never install doccano into your main venv.

Reference: `CX_Analytics_Project_Plan.md` Day 5–6 section
