# Project Narrative

## The Brand
"Atlas and Vine" is a mid-sized direct-to-consumer fashion retailer, around 5 years old. Sells womenswear and accessories online across the US and a few European markets. Annual revenue around $40M.

## The Business Problem
Over the last three quarters:
- Return rate climbed from 22% to 31%
- Repeat purchase rate dropped from 38% to 27%
- Customer support tickets up 45% quarter over quarter

Leadership wants to know where customers are dropping off, what they are frustrated about, and what to fix first.

## Data Sources
1. **Olist Brazilian E-commerce** — transactional backbone. 99k orders, 99k reviews (41% with text), order items, payments, products, customers. Stands in for our internal order management data.
2. **Women's Clothing E-commerce Reviews** — 23k English fashion reviews with ratings, departments, and recommended flags. Stands in for our product reviews.
3. **Customer Support on Twitter** — large dataset of customer support conversations. Stands in for our social and inbound support channels.

## Key Questions
1. At which journey stages do customers churn or complain most?
2. What themes dominate negative feedback? (Sizing? Delivery? Quality? Service?)
3. Which customer segments are most at risk?
4. What is the projected impact of fixing the top issues?

## Initial Observations from Day 1
- Olist reviews skew positive overall (avg 4.09) but show a clear bimodal pattern with ~11k one-star reviews. The negative tail is where the actionable insight lives.
- Women's Clothing reviews are also positive-skewed (avg around 4.2), with Tops and Dresses making up the largest categories.
- Roughly 41k Portuguese review comments will need either translation or filtering. The 23k English reviews are usable as is.

## Success Criteria
- Identify top 3 to 5 friction points with quantified impact
- An at-risk customer list with churn risk scores
- Interactive Streamlit dashboard for ongoing monitoring
- Actionable recommendations broken out by business team