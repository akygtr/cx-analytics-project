"""
Atlas & Vine: Customer Experience Analytics Dashboard
Run locally:  streamlit run dashboard/app.py
Reads everything from data/processed/ (built across Days 2-8).
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

st.set_page_config(
    page_title="Atlas & Vine: CX Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).resolve().parent.parent
PROC = ROOT / "data" / "processed"

# Atlas & Vine palette
PRIMARY  = "#2C4A3E"   # vine
ACCENT   = "#C97B5A"   # terracotta
DANGER   = "#A8442A"   # deep terracotta
OK       = "#6B8E7F"   # sage
MUTED    = "#8B6F47"   # warm brown
CREAM    = "#F5F0E8"
BONE     = "#EAE3D2"
CHARCOAL = "#1A1A1A"
LINE     = "#D4CCB8"


# ----------------------------- THEME -----------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}
.stApp {{ background-color: {CREAM}; }}

h1, h2, h3, h4 {{
    font-family: 'Playfair Display', serif !important;
    color: {PRIMARY};
    letter-spacing: -0.5px;
}}
h1 {{ font-size: 2.6rem !important; font-weight: 700 !important; }}
h2 {{ font-size: 1.7rem !important; }}
h3 {{ font-size: 1.25rem !important; }}

[data-testid="stMetric"] {{
    background: #FFFFFF;
    border: 1px solid {LINE};
    border-radius: 4px;
    padding: 16px 18px;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}}
[data-testid="stMetricLabel"] {{
    font-size: 0.7rem !important;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #6B6B6B !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'Playfair Display', serif !important;
    color: {PRIMARY} !important;
    font-size: 1.7rem !important;
}}

.stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid {LINE}; }}
.stTabs [data-baseweb="tab"] {{
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.76rem;
    padding: 12px 18px;
    color: #555;
}}
.stTabs [aria-selected="true"] {{
    color: {PRIMARY} !important;
    border-bottom: 2px solid {ACCENT} !important;
}}

hr {{ border-color: {LINE}; }}

[data-testid="stSidebar"] {{ background-color: {BONE}; border-right: 1px solid {LINE}; }}
[data-testid="stSidebar"] h3 {{ font-family: 'Playfair Display', serif !important; color: {PRIMARY}; }}

.filter-badge {{
    display: inline-block;
    background: {ACCENT};
    color: white;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.68rem;
    letter-spacing: 1px;
    text-transform: uppercase;
    font-weight: 600;
}}
</style>
""", unsafe_allow_html=True)

# Plotly theme
pio.templates["atlas"] = go.layout.Template(
    layout=dict(
        font=dict(family="Inter, sans-serif", color=CHARCOAL, size=12),
        title=dict(font=dict(family="Playfair Display, serif", size=18, color=PRIMARY)),
        colorway=[PRIMARY, ACCENT, OK, MUTED, "#A4B5A0", "#7A9080"],
        paper_bgcolor=CREAM,
        plot_bgcolor=CREAM,
        xaxis=dict(gridcolor=LINE, linecolor=LINE, zerolinecolor=LINE),
        yaxis=dict(gridcolor=LINE, linecolor=LINE, zerolinecolor=LINE),
        margin=dict(l=10, r=10, t=40, b=10),
    )
)
pio.templates.default = "atlas"
px.defaults.template = "atlas"


# ----------------------------- LOADERS -----------------------------
@st.cache_data
def load_parquet(name):
    p = PROC / name
    return pd.read_parquet(p) if p.exists() else None

@st.cache_data
def load_csv(name, **kw):
    p = PROC / name
    return pd.read_csv(p, **kw) if p.exists() else None


master = load_parquet("olist_master.parquet")
if master is None:
    st.error(f"olist_master.parquet not found in {PROC}. Run the pipeline first.")
    st.stop()
master["order_purchase_timestamp"] = pd.to_datetime(master["order_purchase_timestamp"])

rev_deliv     = load_parquet("reviews_scored_with_delivery.parquet")
topics        = load_csv("negative_topics.csv")
segments      = load_parquet("customer_segments.parquet")
clv           = load_csv("segment_clv.csv", index_col=0)
emotion       = load_parquet("reviews_with_emotion.parquet")
repeat_scored = load_parquet("customers_repeat_scored.parquet")
scored        = load_parquet("olist_reviews_scored.parquet")


# ----------------------------- SIDEBAR FILTERS -----------------------------
with st.sidebar:
    st.markdown("### Filters")
    st.caption("Apply across all tabs.")

    min_d = master["order_purchase_timestamp"].min().date()
    max_d = master["order_purchase_timestamp"].max().date()
    date_range = st.date_input(
        "Order date range",
        value=(min_d, max_d),
        min_value=min_d, max_value=max_d,
    )

    top_states = master["customer_state"].value_counts().head(15).index.tolist()
    sel_states = st.multiselect(
        "Customer state",
        options=top_states,
        default=[],
        placeholder="All states",
    )

    delivery_filter = st.radio(
        "Delivery outcome",
        ["All", "On time / early", "Late"],
        horizontal=False,
    )

    score_range = st.slider("Review score", 1, 5, (1, 5))

    if segments is not None and "segment" in segments.columns:
        seg_options = sorted(segments["segment"].dropna().unique().tolist())
        sel_segs = st.multiselect(
            "Customer segment",
            options=seg_options,
            default=[],
            placeholder="All segments",
        )
    else:
        sel_segs = []

    st.divider()
    if st.button("Reset filters", use_container_width=True):
        st.rerun()


# Normalize date_range to a 2-tuple for the cached filter
if isinstance(date_range, tuple) and len(date_range) == 2:
    dr_arg = date_range
else:
    dr_arg = (min_d, max_d)


# ----------------------------- FILTER HELPER -----------------------------
@st.cache_data(show_spinner=False)
def filter_master(df, dr, states, delivery, scores, segs, _seg_df):
    out = df
    d = out["order_purchase_timestamp"].dt.date
    out = out[(d >= dr[0]) & (d <= dr[1])]

    if states:
        out = out[out["customer_state"].isin(states)]

    if delivery == "Late":
        out = out[out["is_late"] == True]
    elif delivery == "On time / early":
        out = out[out["is_late"] == False]

    if scores != (1, 5):
        out = out[out["review_score"].between(scores[0], scores[1])]

    if segs and _seg_df is not None:
        keep = set(_seg_df[_seg_df["segment"].isin(segs)]["customer_unique_id"])
        out = out[out["customer_unique_id"].isin(keep)]

    return out


master_f = filter_master(
    master, dr_arg, tuple(sel_states), delivery_filter,
    score_range, tuple(sel_segs), segments,
)

order_ids_f    = set(master_f["order_id"])
customer_ids_f = set(master_f["customer_unique_id"])

rev_deliv_f      = rev_deliv[rev_deliv["order_id"].isin(order_ids_f)] if rev_deliv is not None else None
scored_f         = scored[scored["order_id"].isin(order_ids_f)] if scored is not None else None
segments_f       = segments[segments["customer_unique_id"].isin(customer_ids_f)] if segments is not None else None
repeat_scored_f  = repeat_scored[repeat_scored["customer_unique_id"].isin(customer_ids_f)] if repeat_scored is not None else None
if emotion is not None and "order_id" in emotion.columns:
    emotion_f = emotion[emotion["order_id"].isin(order_ids_f)]
else:
    emotion_f = emotion

filters_active = (
    bool(sel_states) or bool(sel_segs)
    or delivery_filter != "All"
    or score_range != (1, 5)
    or dr_arg != (min_d, max_d)
)


# ----------------------------- HEADER -----------------------------
st.markdown(f"""
<div style="border-bottom: 1px solid {LINE}; padding-bottom: 16px; margin-bottom: 22px;">
    <p style="font-size: 0.7rem; letter-spacing: 3px; text-transform: uppercase; color: #6B6B6B; margin: 0;">Atlas &amp; Vine</p>
    <h1 style="margin: 4px 0 0 0;">Customer Experience Report</h1>
    <p style="color: #6B6B6B; margin-top: 6px; font-size: 0.95rem;">
        Fulfillment, voice of customer, and retention diagnostics. Olist Brazilian e-commerce, ~99K orders.
        All metrics labeled by method and population.
    </p>
</div>
""", unsafe_allow_html=True)

if filters_active:
    pct = len(master_f) / len(master) * 100 if len(master) else 0
    st.markdown(
        f"<p><span class='filter-badge'>Filtered view</span> &nbsp; "
        f"Showing <b>{len(master_f):,}</b> of {len(master):,} orders ({pct:.1f}%).</p>",
        unsafe_allow_html=True,
    )
else:
    st.caption(f"Full population: {len(master):,} orders.")

if len(master_f) == 0:
    st.error("No orders match the current filters. Loosen them on the sidebar.")
    st.stop()
elif len(master_f) < 500:
    st.warning(f"Only {len(master_f)} orders in view. Percentages below are noisy at this sample size.")


# ----------------------------- KPIs -----------------------------
order_counts = master_f.groupby("customer_unique_id")["order_id"].nunique()
repeat_rate = (order_counts > 1).mean() * 100 if len(order_counts) else 0
avg_review  = master_f["review_score"].mean()
pct_low     = (master_f["review_score"] <= 2).mean() * 100
late_rate   = master_f["is_late"].mean() * 100

tabs = st.tabs([
    "Executive Summary",
    "Fulfillment & Delivery",
    "Voice of Customer",
    "Segments & CLV",
    "Repeat Propensity",
])


# ===================== TAB 1: EXECUTIVE SUMMARY =====================
with tabs[0]:
    c = st.columns(6)
    c[0].metric("Orders", f"{len(master_f):,}")
    c[1].metric("Unique customers", f"{order_counts.size:,}")
    c[2].metric("Avg review", f"{avg_review:.2f}" if pd.notna(avg_review) else "—")
    c[3].metric("1-2 star share", f"{pct_low:.1f}%")
    c[4].metric("Late delivery rate", f"{late_rate:.1f}%")
    c[5].metric("Repeat rate", f"{repeat_rate:.1f}%")

    st.markdown("---")
    st.subheader("The headline finding")
    st.success(
        "Late delivery costs **1.94 stars** on average (4.21 on time vs 2.27 when late). "
        "62% of late orders score 1-2 stars vs 11% on time. This is the cleanest, "
        "population-level lever in the dataset."
    )
    if filters_active:
        st.caption("The headline figure above is from the full population. KPIs above the line move with filters.")

    st.subheader("Top friction points")
    st.markdown(
        "1. **Late delivery** — 6.6% of orders, but review crashes 4.21 to 2.27 when late.\n"
        "2. **Non-delivery** — 63% of complaints are delivery-themed, rising to 82% among late orders.\n"
        "3. **Delivery-time cliff** — satisfaction holds to ~21 days, then drops to 3.01 stars at 22d+.\n"
        "4. **Retention collapse** — 3.1% repeat rate. The structural problem, not a modelable one.\n"
        "5. **Fulfillment leak** — 3% of orders never reach the customer, biggest loss at carrier handoff."
    )


# ===================== TAB 2: FULFILLMENT & DELIVERY =====================
with tabs[1]:
    st.subheader("Fulfillment funnel")
    st.caption(
        "Reconstructed live from order timestamps in the current view. "
        "Fulfillment funnel, NOT a marketing acquisition funnel."
    )

    stages = {}
    stages["Order placed"] = len(master_f)
    if "order_approved_at" in master_f.columns:
        stages["Payment approved"] = master_f["order_approved_at"].notna().sum()
    if "order_delivered_carrier_date" in master_f.columns:
        stages["Handed to carrier"] = master_f["order_delivered_carrier_date"].notna().sum()
    if "order_delivered_customer_date" in master_f.columns:
        stages["Delivered"] = master_f["order_delivered_customer_date"].notna().sum()

    funnel_live = pd.DataFrame(stages.items(), columns=["stage", "count"])
    fig = go.Figure(go.Funnel(
        y=funnel_live["stage"], x=funnel_live["count"],
        textinfo="value+percent initial",
        marker={"color": PRIMARY},
    ))
    fig.update_layout(height=340)
    st.plotly_chart(fig, use_container_width=True)

    if len(funnel_live) > 1:
        lost = funnel_live["count"].iloc[0] - funnel_live["count"].iloc[-1]
        drop_pct = (1 - funnel_live["count"].iloc[-1] / funnel_live["count"].iloc[0]) * 100
        st.caption(f"{lost:,} orders ({drop_pct:.2f}%) never reached the customer in this view.")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Satisfaction by delivery outcome")
        dlv = master_f.dropna(subset=["review_score", "is_late"])
        if len(dlv) and dlv["is_late"].nunique() == 2:
            g = dlv.groupby("is_late")["review_score"].mean().reset_index()
            g["outcome"] = g["is_late"].map({False: "On time / early", True: "Late"})
            fig = px.bar(
                g, x="outcome", y="review_score", text_auto=".2f",
                color="outcome",
                color_discrete_map={"On time / early": OK, "Late": DANGER},
            )
            fig.update_layout(showlegend=False, height=320, yaxis_title="Avg review")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need both on-time and late orders in view. Set Delivery filter to 'All'.")

    with col2:
        st.subheader("The delivery-time cliff")
        dlv2 = master_f.dropna(subset=["review_score", "delivery_time_days"]).copy()
        if len(dlv2):
            dlv2["bucket"] = pd.cut(
                dlv2["delivery_time_days"],
                bins=[-1, 7, 14, 21, 1000],
                labels=["0-7d", "8-14d", "15-21d", "22d+"],
            )
            gb = dlv2.groupby("bucket", observed=True)["review_score"].mean().reset_index()
            fig = px.line(gb, x="bucket", y="review_score", markers=True)
            fig.update_traces(line_color=PRIMARY, marker=dict(size=10, color=ACCENT))
            fig.update_layout(height=320, yaxis_title="Avg review")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Not enough rows after filtering.")

    st.markdown("---")
    st.subheader("Satisfaction over time")
    ts = master_f.dropna(subset=["review_score"]).copy()
    if len(ts) > 200:
        ts["month"] = ts["order_purchase_timestamp"].dt.to_period("M").dt.to_timestamp()
        monthly = ts.groupby("month").agg(
            avg_review=("review_score", "mean"),
            orders=("order_id", "count"),
        ).reset_index()
        monthly = monthly[monthly["orders"] >= 50]
        if len(monthly):
            fig = px.line(monthly, x="month", y="avg_review", markers=True)
            fig.update_traces(line_color=PRIMARY, marker=dict(size=6, color=ACCENT))
            fig.update_layout(height=300, yaxis_title="Avg review (months with 50+ orders)")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.caption("Time series suppressed: need at least 200 reviewed orders in view.")


# ===================== TAB 3: VOICE OF CUSTOMER =====================
with tabs[2]:
    st.caption(
        "Scored complaint corpus (~12K reviews, 86% 1-2 star BY DESIGN from Day 3 oversampling). "
        "Describes WHAT customers complain about, never HOW MANY are unhappy."
    )

    if rev_deliv_f is not None and len(rev_deliv_f) > 0:
        st.markdown(
            f"<p><span class='filter-badge'>VoC corpus</span> &nbsp; "
            f"<b>{len(rev_deliv_f):,}</b> reviews in current view.</p>",
            unsafe_allow_html=True,
        )

        with st.expander("Filter this tab by sentiment or theme"):
            tcol1, tcol2 = st.columns(2)
            with tcol1:
                sent_pick = st.multiselect(
                    "Sentiment",
                    ["positive", "negative", "neutral"],
                    default=[],
                    placeholder="All sentiments",
                    key="voc_sent",
                )
            with tcol2:
                theme_opts = sorted(rev_deliv_f["theme_pred"].dropna().unique().tolist())
                theme_pick = st.multiselect(
                    "Theme",
                    theme_opts,
                    default=[],
                    placeholder="All themes",
                    key="voc_theme",
                )

        rev_view = rev_deliv_f.copy()
        if sent_pick and "sentiment_pred" in rev_view.columns:
            rev_view = rev_view[rev_view["sentiment_pred"].isin(sent_pick)]
        if theme_pick:
            rev_view = rev_view[rev_view["theme_pred"].isin(theme_pick)]

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Complaint themes")
            tc = rev_view["theme_pred"].value_counts().reset_index()
            tc.columns = ["theme", "count"]
            if len(tc):
                fig = px.bar(tc, x="count", y="theme", orientation="h",
                             color_discrete_sequence=[PRIMARY])
                fig.update_layout(height=300, yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No reviews match.")

        with col2:
            st.subheader("Theme shift when delivery is late")
            if "is_late" in rev_view.columns and rev_view["is_late"].nunique() == 2:
                ct = pd.crosstab(rev_view["theme_pred"], rev_view["is_late"], normalize="columns") * 100
                ct = ct.rename(columns={False: "On time", True: "Late"}).round(1).reset_index()
                ctm = ct.melt(id_vars="theme_pred", var_name="outcome", value_name="pct")
                fig = px.bar(ctm, x="theme_pred", y="pct", color="outcome", barmode="group",
                             color_discrete_map={"On time": OK, "Late": DANGER})
                fig.update_layout(height=300, xaxis_title="", yaxis_title="% of complaints")
                st.plotly_chart(fig, use_container_width=True)
                st.caption("Delivery jumps from 57% to 82% of complaints when the order is late (full corpus baseline).")
            else:
                st.info("Need both on-time and late orders in view. Set Delivery filter to 'All'.")

        st.markdown("---")
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Complaint topics")
            st.caption(
                "Method: TF-IDF + KMeans (BERTopic fell back, HF was offline). "
                "Based on the full negative corpus, not the filtered view."
            )
            if topics is not None:
                st.dataframe(topics, use_container_width=True, height=320)
            else:
                st.warning("negative_topics.csv not found.")
        with col4:
            st.subheader("Emotion breakdown")
            st.caption(
                "Method: rule-based keyword tagging (HF emotion model offline). "
                "Frustration share inflated by default rule, treat as directional."
            )
            if emotion_f is not None and "emotion" in emotion_f.columns and len(emotion_f):
                ec = emotion_f["emotion"].value_counts().reset_index()
                ec.columns = ["emotion", "count"]
                fig = px.pie(ec, names="emotion", values="count", hole=0.45,
                             color_discrete_sequence=[PRIMARY, ACCENT, OK, MUTED])
                fig.update_layout(height=320)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No emotion data in current view.")

        st.markdown("---")
        st.subheader("Sample reviews")
        src = scored_f if scored_f is not None and len(scored_f) else rev_view
        if src is not None and len(src):
            text_col = "review_en" if "review_en" in src.columns else "review_clean"
            sample_themes = sorted(src["theme_pred"].dropna().unique())
            if sample_themes:
                theme_pick2 = st.selectbox("Filter samples by theme", sample_themes, key="sample_theme")
                sample = src[src["theme_pred"] == theme_pick2]
                show_cols = [c for c in [text_col, "sentiment_pred", "review_score"] if c in sample.columns]
                st.dataframe(sample[show_cols].head(15), use_container_width=True, height=300)
    else:
        st.warning("No reviews match current filters.")


# ===================== TAB 4: SEGMENTS & CLV =====================
with tabs[3]:
    if segments_f is not None and len(segments_f):
        st.subheader("Customer segments (K-means, k=4)")
        st.caption(
            "Frequency dropped (no variance at 3% repeat). Silhouette favored k=2; "
            "k=4 chosen for business granularity. The late-delivery segment is the cleanest cluster."
        )
        if filters_active:
            st.markdown(
                f"<p><span class='filter-badge'>Filtered</span> &nbsp; "
                f"<b>{len(segments_f):,}</b> of {len(segments):,} customers in view.</p>",
                unsafe_allow_html=True,
            )

        col1, col2 = st.columns([1, 1])
        with col1:
            sc = segments_f["segment"].value_counts().reset_index()
            sc.columns = ["segment", "customers"]
            fig = px.bar(sc, x="customers", y="segment", orientation="h",
                         color_discrete_sequence=[PRIMARY])
            fig.update_layout(height=300, yaxis={"categoryorder": "total ascending"})
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            prof_cols = {}
            if "monetary" in segments_f.columns:
                prof_cols["avg_spend"] = ("monetary", "mean")
            if "avg_review" in segments_f.columns:
                prof_cols["avg_review"] = ("avg_review", "mean")
            if "late_rate" in segments_f.columns:
                prof_cols["late_rate"] = ("late_rate", "mean")
            prof = segments_f.groupby("segment").agg(**prof_cols).round(2)
            st.dataframe(prof, use_container_width=True, height=300)

        st.markdown("---")
        st.subheader("Descriptive CLV per segment")
        st.caption("Observed historical value. Predictive CLV not attempted (no repeat base to fit BG/NBD).")

        if "monetary" in segments_f.columns and "frequency" in segments_f.columns:
            live_clv = segments_f.groupby("segment").agg(
                customers=("customer_unique_id", "nunique"),
                total_value=("monetary", "sum"),
                avg_value=("monetary", "mean"),
                repeat_rate_pct=("frequency", lambda x: (x > 1).mean() * 100),
            ).round(2)
            total = live_clv["total_value"].sum()
            if total > 0:
                live_clv["pct_of_revenue"] = (live_clv["total_value"] / total * 100).round(1)
            st.dataframe(live_clv, use_container_width=True)
        elif clv is not None:
            st.caption("Live recompute unavailable, showing pre-aggregated table.")
            st.dataframe(clv, use_container_width=True)

        st.success(
            "High-value: 28% of customers, ~57% of observed revenue, the only segment above 3% repeat. "
            "Late & unhappy: mid-value customers wrecked by delivery, the fixable loss."
        )
    else:
        st.warning("No segments in current view (or customer_segments.parquet missing).")


# ===================== TAB 5: REPEAT PROPENSITY =====================
with tabs[4]:
    st.subheader("Repeat-purchase propensity")
    st.caption(
        "Reframed from churn (no churn label exists in Olist). Leakage-free model on first-order "
        "features only. XGBoost ROC-AUC 0.59 (population level)."
    )
    st.warning(
        "This is deliberately NOT a ranked at-risk list. At a 3% base rate with AUC 0.59, "
        "per-customer targeting would be ~96% wrong. The finding is that first-order experience "
        "does not predict repeat, so the lever is systemic (fix delivery), not individual scoring."
    )

    if repeat_scored_f is not None and "repeat_proba" in repeat_scored_f.columns and len(repeat_scored_f):
        c = st.columns(3)
        c[0].metric("Customers in view", f"{len(repeat_scored_f):,}")
        if "repeat" in repeat_scored_f.columns:
            actual = repeat_scored_f["repeat"].mean() * 100
            c[1].metric("Actual repeat rate", f"{actual:.2f}%")
        c[2].metric("Mean predicted probability", f"{repeat_scored_f['repeat_proba'].mean():.3f}")

        fig = px.histogram(repeat_scored_f, x="repeat_proba", nbins=50,
                            color_discrete_sequence=[PRIMARY])
        fig.update_layout(height=340, xaxis_title="Predicted repeat probability", yaxis_title="Customers")
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            "Distribution barely separates repeaters from non-repeaters, which is the point: "
            "retention is structural, not an experience problem a model can target away."
        )
    else:
        st.warning("customers_repeat_scored.parquet not found or no customers in view.")

    st.markdown("---")
    st.subheader("So what should Atlas & Vine do")
    st.markdown(
        "- **Fix delivery broadly.** It is the one proven lever (1.94-star swing, population-level).\n"
        "- **Do not buy individual retention scoring.** The data does not support per-customer targeting.\n"
        "- **Protect the High-value segment** (28% of customers, 57% of revenue, the only real repeat base)."
    )
