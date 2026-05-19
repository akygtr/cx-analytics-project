\# Customer Experience Analytics for a Fashion E-commerce Brand



End to end CX analytics project for a mid-sized online fashion retailer dealing with rising returns and falling repeat purchases. Covers data sourcing, cleaning, manual labeling, journey mapping, voice-of-customer analysis, segmentation, and churn prediction.



\## The Problem

Return rates are climbing and repeat purchases are dropping. The goal is to figure out where customers are bailing, what's frustrating them, and what to fix first.



\## Stack

Python, pandas, scikit-learn, spaCy, Hugging Face Transformers, BERTopic, XGBoost, Streamlit.



\## Status

Day 1 of 12. Project setup and initial data exploration.



\## Structure

\- data/ raw, processed, and labeled datasets

\- notebooks/ one notebook per project phase

\- src/ reusable python modules

\- dashboard/ streamlit app

\- reports/ business report and case study

\- models/ saved model artifacts



\## Setup



&#x20;   python -m venv venv

&#x20;   venv\\Scripts\\activate

&#x20;   pip install -r requirements.txt

&#x20;   python -m spacy download en\_core\_web\_sm

&#x20;   python -m nltk.downloader stopwords punkt punkt\_tab wordnet

