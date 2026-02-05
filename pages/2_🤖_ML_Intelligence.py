import streamlit as st
import pandas as pd

from core.data_loader import load_local_reports, get_ttp_and_country_columns
from core.geo_utils import get_nordic_baltic_countries
from core.risk_scoring import calculate_iso_risk_score, calculate_nist_risk_score
from core.ml_models import (
    ml_generate_executive_summary,
    ml_threat_actor_profiling,
    ml_automated_threat_prioritization,
    ml_nordic_geographic_risk_forecast,
    ml_nlp_intelligence_extraction,
    ml_resource_allocation_optimizer,
    ml_recommend_courses
)

st.set_page_config(page_title="ML Intelligence", page_icon="🤖", layout="wide")

items = load_local_reports()
ttp_columns, country_columns = get_ttp_and_country_columns(items)

st.markdown('<h2 class="glow-text">ADVANCED ML INTELLIGENCE CENTER</h2>', unsafe_allow_html=True)

# Select report
report_dates = sorted(items['report_date'].dt.date.unique(), reverse=True)
selected_date = st.selectbox("Select Intelligence Report Period", report_dates, index=0)
selected_report = items[items['report_date'].dt.date == selected_date]

# Country filter
all_countries = []
if country_columns:
    all_countries = pd.Series(pd.concat([items[col] for col in country_columns], ignore_index=True))
    all_countries = sorted(all_countries.dropna().unique().tolist())

nordic_baltic = get_nordic_baltic_countries()
default_countries = [c for c in nordic_baltic if c in all_countries]

selected_countries = st.multiselect("Geographic Filter", options=all_countries, default=default_countries)

# TTP metrics
if ttp_columns:
    all_ttps = pd.Series(pd.concat([selected_report[col] for col in ttp_columns], ignore_index=True))
    all_ttps_flat = []
    unique_techniques = set()
    for val in all_ttps:
        if isinstance(val, (list, tuple, set)):
            vals = [str(x) for x in val if x not in [None, "None"]]
            all_ttps_flat.extend(vals)
            unique_techniques.update(vals)
        elif pd.notna(val) and str(val) != "None":
            all_ttps_flat.append(str(val))
            unique_techniques.add(str(val))
    unique_ttps_count = len(unique_techniques)
    total_ttp_count = len(all_ttps_flat)
else:
    unique_ttps_count = 0
    total_ttp_count = 0
    unique_techniques = set()

country_count = len([c for c in all_countries if c in selected_countries]) if selected_countries else len(all_countries)
sources_count = selected_report['source'].nunique() if 'source' in selected_report.columns else 0
regional_focus = bool(selected_countries and any(c in nordic_baltic for c in selected_countries))

iso_score = calculate_iso_risk_score(total_ttp_count, country_count, sources_count, regional_focus)
nist_score = calculate_nist_risk_score(total_ttp_count, country_count, unique_techniques, regional_focus)

# Executive summary
st.markdown("""
<div style="margin-top: 20px; margin-bottom: 30px; padding: 20px; background: linear-gradient(145deg, #1a1a1a, #2a2a2a); border: 2px solid #00aaff; border-radius: 15px;">
    <h3 class="glow-text">ML-POWERED SUMMARY</h3>
</div>
""", unsafe_allow_html=True)

with st.spinner("Running machine learning analysis..."):
    summary, threat_color = ml_generate_executive_summary(
        selected_report, ttp_columns, country_columns, iso_score, nist_score
    )

st.markdown(f"""
<div style="padding: 25px; background: linear-gradient(145deg, #2a2a2a, #1a1a1a); border-left: 4px solid {threat_color}; border-radius: 10px; margin-top: 20px;">
    <h4 style="color: {threat_color}; margin-top: 0;">THREAT LEVEL: {summary['threat_level']}
    <span style="font-size: 12px; color: #00aaff; margin-left: 10px;">ML Confidence: {summary['ml_confidence']*100:.0f}%</span></h4>
</div>
""", unsafe_allow_html=True)

# Insights
if summary['key_insights']:
    st.subheader("Key Intelligence Insights")
    for insight in summary['key_insights']:
        st.write(f"• {insight}")

if summary['attack_patterns']:
    st.subheader("ML-Detected Attack Patterns")
    for pattern in summary['attack_patterns']:
        st.write(f"• {pattern}")

if summary
