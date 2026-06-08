# Day 6 Summary — CX Analytics Project

**Date:** June 5, 2026
**Status:** Complete
**Phase:** plan's Day 7–8 (journey mapping + topic modeling), run compressed into one day.

## What Got Done

### Honest scoping decision (for the record)
- Olist has no pre-purchase behavior (no sessions, browsing, cart, checkout). A marketing acquisition funnel would be fabricated, same flaw class as the dropped cross-dataset linkage.
- Built the **fulfillment funnel** instead (order placed → payment approved → handed to carrier → delivered), reconstructed from timestamp presence, not relabelled status counts. Drop-off is real.
- journey_stage classifier stays shelved (degenerate labels from Day 5). Replaced with a rule-based theme→stage proxy, labelled as a heuristic, not a model.

### Fulfillment funnel (full population, 99,441 orders)
| Stage | Count | % of top | dropped from prev |
|---|---|---|---|
| Order placed | 99,441 | 100.0% | — |
| Payment approved | 99,281 | 99.84% | 160 |
| Handed to carrier | 97,658 | 98.21% | 1,623 |
| Delivered to customer | 96,476 | 97.02% | 1,182 |

- 2,965 orders (2.98%) never reached the customer.
- Biggest single leak is **approved → carrier** (1,623 orders), sitting in canceled / unavailable / processing / invoiced.
- Minor data quirk: 8 orders have status `delivered` but no delivery date. Known Olist inconsistency, not a code bug. Left as-is.

### Delivery satisfaction (population, from master review scores)
- On time / early: avg review 4.21, 11.3% score 1–2★ (91,820 orders)
- Late: avg review 2.27, 62.4% score 1–2★ (6,347 orders)
- **Late delivery costs 1.94 stars on average.** This is the cleanest, hardest finding in the project.
- Score degrades with delivery time: 0–7d = 4.41, 8–14d = 4.29, 15–21d = 4.10, **22d+ = 3.01.** The cliff is past ~3 weeks.

### Retention (population, via customer_unique_id)
- 96,096 unique customers, **3.12% repeat (2,997), 96.88% one-time (93,099).**
- This is the structural problem, bigger than delivery. It also kills RFM's Frequency dimension and any predictive CLV/churn model (carried into Day 7–8 planning).

### Theme + sentiment overlay (complaint corpus, 11,997 scored reviews)
- Theme: delivery 7,510 (63%), quality 2,957 (25%), other 608, service 540, returns 382.
- Sentiment: negative 9,853, positive 1,477, neutral 667.
- Theme shifts with delivery outcome: delivery is 57% of complaints on time, **82% when late.** Quality drops from 30% to 6% when late (delivery drowns everything else out).
- stage_proxy: delivery 7,510, post-purchase 3,947, support 540.

### Topic modeling (negative reviews, 10,589 docs)
- **BERTopic did NOT run.** HF couldn't reach huggingface.co and `all-MiniLM-L6-v2` wasn't cached. The TF-IDF + KMeans fallback fired automatically (8 clusters).
- Clusters are coherent and collapse to a clear story:
  - "didn't / haven't received product" (3 clusters, ~6,800 docs) — overwhelming dominant complaint
  - "arrived defective / broken" (856)
  - "poor quality, won't recommend" (552)
  - "post office pickup / collection" friction (357)
- Apostrophe-stripped tokens (`don`, `didn`, `hasn`) are `preprocess_text` artifacts, not data quality issues.

### Files Saved
In `data/processed/`:
- `order_funnel.parquet` — funnel table (dashboard input)
- `reviews_scored_with_delivery.parquet` — scored reviews joined to master delivery cols
- `negative_topics.csv` — KMeans topic clusters (dashboard VoC input)

## Tech Decisions Made
- Fulfillment funnel, not acquisition funnel. Stated explicitly so it survives recruiter scrutiny.
- Population stats (funnel, satisfaction, retention) from master (~99K); theme/topic stats from the scored set (11,997, 86% 1–2★ by design). Never mixed.
- KMeans topic fallback kept rather than fighting the HF SSL/offline issue. Momentum over perfection.
- theme→stage proxy is rule-based and labelled as such.

## Honest Metrics (do not inflate in resume/report)
- **Topic modeling is TF-IDF + KMeans, not BERTopic.** Either fix BERTopic (manual offline model download) or change the resume bullet to "TF-IDF + KMeans complaint clustering." Do not claim BERTopic on a run that fell back.
- Resume draft says "delivery and quality drove 58% of negative sentiment." Real measured figure: delivery 63% + quality 25% of complaint **themes** (~87% combined) in the reviewed set. That's theme share on an oversampled corpus, not "% of negative sentiment" and not population. Replace 58% with the real number and the caveat.
- "Late delivery costs 1.94 stars" and "62% of late orders score 1–2★" are clean and population-level. Lead with these.

## Top Friction Points (numbers attached)
1. **Late delivery** — 6.6% of orders, but avg review crashes from 4.21 to 2.27 when late (1.94-star gap), 62% score 1–2★.
2. **Non-delivery** — 63% of all complaints are delivery-themed, dominated by "never received it." Rises to 82% of complaints among late orders.
3. **Delivery-time cliff** — satisfaction holds to ~21 days then drops to 3.01★ at 22d+.
4. **Retention collapse** — 3.1% repeat rate. The headline business problem for Atlas & Vine.
5. **Fulfillment leak** — 3% of orders never reach the customer, biggest loss at carrier handoff.

## What's Next: Day 7
- Emotion detection on negatives (HF emotion model, with offline fallback) — finishes the VoC layer.
- RFM done with eyes open (show F collapses at 3.1% repeat), then K-means segmentation on features with real variance (monetary, recency, delivery time, late flag, review score).
- Descriptive CLV per segment. Predictive CLV is off the table (no repeat base to fit BG/NBD).
- Day 8 reframe: repeat-purchase prediction, not churn (the churn label doesn't exist in Olist).

Reference: `CX_Analytics_Project_Plan.md` Day 9–10 sections, adjusted for the retention reality.
