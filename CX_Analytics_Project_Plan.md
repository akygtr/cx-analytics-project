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
